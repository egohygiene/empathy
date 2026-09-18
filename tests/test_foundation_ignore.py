# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Verify source integrity, explicit selection, and actual composed Git behavior."""

from __future__ import annotations

from contextlib import redirect_stderr, redirect_stdout
import copy
import hashlib
import io
from pathlib import Path
import sys
import tempfile
import unittest

import test_gitignore_baseline

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import foundation_ignore  # noqa: E402

import foundation  # noqa: E402


def inputs():
    return (
        foundation.load_json(ROOT / "foundation/catalog.json"),
        foundation.load_json(ROOT / "foundation/empathy.manifest.json"),
    )


def scope(root=".", overlays=(), local=""):
    return {"root": root, "overlays": list(overlays), "local_additions": local}


def definition(catalog):
    return next(item for item in catalog["artifacts"] if item["id"] == "gitignore")["composition"]


class IgnoreContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.catalog, self.manifest = inputs()

    def test_checked_in_plan_is_current_and_byte_repeatable(self) -> None:
        first, errors = foundation.plan_gitignore(self.catalog, self.manifest, ROOT)
        self.assertEqual([], errors)
        second, errors = foundation.plan_gitignore(
            dict(reversed(list(self.catalog.items()))), self.manifest, ROOT
        )
        self.assertEqual([], errors)
        self.assertEqual(foundation.render_resolved(first), foundation.render_resolved(second))
        self.assertEqual(
            (ROOT / "foundation/contracts/empathy.gitignore-plan.json").read_text(encoding="utf-8"),
            foundation.render_resolved(first),
        )
        self.assertEqual("plan-only", first["status"])
        self.assertEqual(
            ["overlay", "local", "baseline"],
            [layer["kind"] for layer in first["files"][0]["layers"]],
        )
        for file in first["files"]:
            self.assertEqual(
                hashlib.sha256(file["content"].encode()).hexdigest(), file["content_sha256"]
            )
            for layer in file["layers"]:
                if "path" in layer:
                    self.assertEqual(
                        hashlib.sha256((ROOT / layer["path"]).read_bytes()).hexdigest(),
                        layer["sha256"],
                    )
                    self.assertEqual("egohygiene/empathy", layer["owner"])

    def test_scopes_are_sorted_but_local_text_is_preserved(self) -> None:
        local = "# Keep the reviewed build note.\n!/target/\n/target/*\n!/target/README.md\n\n# Repetition is intentional.\n/target/*\n!/target/README.md\n"
        self.manifest["gitignore"]["scopes"] = [scope("apps/rust", ("rust-build",), local), scope()]
        first, errors = foundation.plan_gitignore(self.catalog, self.manifest, ROOT)
        self.assertEqual([], errors)
        self.manifest["gitignore"]["scopes"].reverse()
        second, errors = foundation.plan_gitignore(self.catalog, self.manifest, ROOT)
        self.assertEqual([], errors)
        self.assertEqual(first, second)
        self.assertEqual(
            [".gitignore", "apps/rust/.gitignore"], [file["path"] for file in first["files"]]
        )
        self.assertIn(local, first["files"][1]["content"])
        self.assertEqual(foundation_ignore.digest(local), first["files"][1]["layers"][1]["sha256"])
        self.assertEqual("egohygiene/empathy", first["files"][1]["layers"][1]["owner"])

    def test_omitted_selection_remains_valid_but_cannot_silently_plan(self) -> None:
        del self.manifest["gitignore"]
        resolved, errors = foundation.resolve_manifest(self.catalog, self.manifest)
        self.assertEqual([], errors)
        self.assertNotIn("gitignore", resolved)
        plan, errors = foundation.plan_gitignore(self.catalog, self.manifest, ROOT)
        self.assertIsNone(plan)
        self.assertIn("manifest must select gitignore scopes before planning", errors)

    def test_overlay_requires_profile_and_explicit_scope_selection(self) -> None:
        self.manifest["selected_profiles"].remove("language-rust")
        plan, errors = foundation.plan_gitignore(self.catalog, self.manifest, ROOT)
        self.assertIsNone(plan)
        self.assertTrue(any("requires selected profile language-rust" in error for error in errors))
        self.manifest["gitignore"]["scopes"] = [scope()]
        plan, errors = foundation.plan_gitignore(self.catalog, self.manifest, ROOT)
        self.assertEqual([], errors)
        self.assertEqual(
            ["local", "baseline"], [layer["kind"] for layer in plan["files"][0]["layers"]]
        )

    def test_invalid_scope_configuration_fails_closed(self) -> None:
        invalid = [
            None,
            {},
            {"scopes": []},
            {"scopes": [None]},
            {"scopes": [scope("nested")]},
            {"scopes": [scope(), scope()]},
            {"scopes": [scope(), scope("Apps"), scope("apps")]},
            {"scopes": [scope(overlays=("missing",))]},
            {"scopes": [scope(overlays=("rust-build", "rust-build"))]},
        ]
        invalid.extend(
            {"scopes": [scope(), scope(root)]}
            for root in (
                "../escape",
                "/absolute",
                "./nested",
                "a//b",
                "a/../b",
                "a/",
                "a\\b",
                ".git",
                "a/.GiT",
                "a/*",
                "a\nb",
                "a/.gitignore",
                " leading",
            )
        )
        invalid.extend(
            {"scopes": [scope(local=local)]}
            for local in ("/cache/", "bad\r\n", "bad\0\n", None, [])
        )
        invalid.extend(
            {"scopes": [{**scope(), "overlays": value}]} for value in (None, "rust-build", [{}])
        )
        for selection in invalid:
            with self.subTest(selection=selection):
                self.manifest["gitignore"] = selection
                plan, errors = foundation.plan_gitignore(self.catalog, self.manifest, ROOT)
                self.assertIsNone(plan)
                self.assertTrue(errors)

    def test_invalid_source_metadata_fails_closed(self) -> None:
        invalid = [None, {}, {**definition(self.catalog), "unknown": True}]
        for field, value in (
            ("id", []),
            ("path", "../escape"),
            ("path", "."),
            ("sha256", "not-a-digest"),
        ):
            candidate = copy.deepcopy(definition(self.catalog))
            candidate["baseline"][field] = value
            invalid.append(candidate)
        duplicate = copy.deepcopy(definition(self.catalog))
        duplicate["overlays"].append(duplicate["overlays"][0])
        invalid.append(duplicate)
        for candidate in invalid:
            with self.subTest(candidate=candidate):
                catalog = copy.deepcopy(self.catalog)
                next(item for item in catalog["artifacts"] if item["id"] == "gitignore")[
                    "composition"
                ] = candidate
                plan, errors = foundation.plan_gitignore(catalog, self.manifest, ROOT)
                self.assertIsNone(plan)
                self.assertTrue(errors)

    def test_missing_changed_unscoped_and_duplicate_sources_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            sources = definition(self.catalog)
            baseline = sources["baseline"]
            path = root / baseline["path"]
            path.parent.mkdir(parents=True)
            path.write_bytes((ROOT / baseline["path"]).read_bytes())
            rust = sources["overlays"][0]
            for contents, expected in (
                (None, "cannot read"),
                ("/changed/\n", "digest mismatch"),
                ("target/\n", "must be anchored"),
                ("/target/\n/target/\n", "unique active rules"),
                ("/target/\r\n", "LF-terminated"),
            ):
                with self.subTest(contents=contents):
                    if contents is not None:
                        (root / rust["path"]).write_bytes(contents.encode())
                        if expected != "digest mismatch":
                            rust["sha256"] = foundation_ignore.digest(contents)
                    plan, errors = foundation.plan_gitignore(self.catalog, self.manifest, root)
                    self.assertIsNone(plan)
                    self.assertTrue(any(expected in error for error in errors), errors)

    def test_source_symlink_cannot_escape_supplied_source_root(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "foundation").symlink_to(ROOT / "foundation", target_is_directory=True)
            plan, errors = foundation.plan_gitignore(self.catalog, self.manifest, root)
            self.assertIsNone(plan)
            self.assertTrue(all("escapes source root" in error for error in errors))

    def test_preserve_metadata_does_not_drop_baseline_or_claim_materialization(self) -> None:
        self.manifest["overrides"].append({"artifact": "gitignore", "mode": "preserve"})
        self.manifest["repository"] = "egohygiene/fixture"
        before = (ROOT / ".gitignore").read_bytes()
        plan, errors = foundation.plan_gitignore(self.catalog, self.manifest, ROOT)
        self.assertEqual([], errors)
        file = plan["files"][0]
        self.assertEqual("preserve", file["override"])
        self.assertEqual("repository-owned", file["ownership"])
        self.assertEqual("egohygiene/fixture", file["layers"][1]["owner"])
        self.assertEqual("baseline", file["layers"][-1]["kind"])
        self.assertEqual(before, (ROOT / ".gitignore").read_bytes())

    def test_cli_checks_staleness_and_never_writes_consumer_ignore_files(self) -> None:
        with (
            tempfile.TemporaryDirectory() as temporary,
            redirect_stdout(io.StringIO()),
            redirect_stderr(io.StringIO()),
        ):
            output = Path(temporary) / "plan.json"
            arguments = [
                "--manifest",
                str(ROOT / "foundation/empathy.manifest.json"),
                "--source-root",
                str(ROOT),
                "--output",
                str(output),
            ]
            prefix = ["--catalog", str(ROOT / "foundation/catalog.json")]
            self.assertEqual(0, foundation.main([*prefix, "plan-gitignore", *arguments]))
            self.assertEqual(0, foundation.main([*prefix, "check-gitignore-plan", *arguments]))
            output.write_text("{}\n", encoding="utf-8")
            self.assertEqual(1, foundation.main([*prefix, "check-gitignore-plan", *arguments]))
            self.assertEqual("{}\n", output.read_text(encoding="utf-8"))
            ignore = Path(temporary) / ".gitignore"
            ignore.write_text("original\n", encoding="utf-8")
            self.assertEqual(
                2, foundation.main([*prefix, "plan-gitignore", *arguments[:-1], str(ignore)])
            )
            self.assertEqual("original\n", ignore.read_text(encoding="utf-8"))


class ComposedIgnoreBehaviorTests(test_gitignore_baseline.GitignoreFixture):
    def install(self, scopes):
        catalog, manifest = inputs()
        manifest["gitignore"]["scopes"] = scopes
        plan, errors = foundation.plan_gitignore(catalog, manifest, ROOT)
        self.assertEqual([], errors)
        for file in plan["files"]:
            self.write(file["path"], file["content"])

    def test_nested_rust_scope_leaves_unrelated_target_sources_visible(self) -> None:
        self.install([scope(), scope("apps/rust", ("rust-build",))])
        self.assert_paths(
            ("apps/rust/target/debug/example", "apps/rust/.env", "other/.env"), ignored=True
        )
        self.assert_paths(
            (
                "target/source.rs",
                "apps/other/target/source.rs",
                "apps/rust/fixtures/target/source.rs",
                "apps/rust/Cargo.lock",
                "apps/rust/src/lib.rs",
            ),
            ignored=False,
        )

    def test_root_rust_overlay_is_anchored_to_the_workspace(self) -> None:
        self.install([scope(overlays=("rust-build",))])
        self.assert_paths(("target/debug/example",), ignored=True)
        self.assert_paths(("tests/fixtures/target/source.rs", "Cargo.lock"), ignored=False)

    def test_profile_selection_alone_does_not_install_any_overlay(self) -> None:
        self.install([scope()])
        self.assert_paths(("target/source.rs", "apps/rust/target/source.rs"), ignored=False)

    def test_local_exception_reopens_parent_and_keeps_adjacent_output_ignored(self) -> None:
        self.install(
            [
                scope(),
                scope(
                    "apps/rust",
                    ("rust-build",),
                    "# Owner: fixture maintainer; reason: reviewed build note.\n!/target/\n/target/*\n!/target/README.md\n",
                ),
            ]
        )
        self.assert_paths(
            ("apps/rust/target/debug/example", "apps/rust/target/other.md"), ignored=True
        )
        self.assert_paths(("apps/rust/target/README.md", "other/target/source.rs"), ignored=False)

    def test_baseline_wins_over_local_negations_in_every_declared_scope(self) -> None:
        local = "!.env\n!.env.*\n!/.secrets/\n!/.secrets/**\n!/node_modules/\n!/node_modules/**\n"
        self.install([scope(local=local), scope("apps/rust", ("rust-build",), local)])
        for prefix in ("", "apps/rust/"):
            self.assert_paths(
                tuple(
                    prefix + path
                    for path in (
                        ".env",
                        ".env.production",
                        ".env.example.local",
                        ".secrets/example.key",
                        "node_modules/dep/index.js",
                    )
                ),
                ignored=True,
            )
            self.assert_paths(
                tuple(
                    prefix + path
                    for path in (
                        ".env.example",
                        ".env.production.template",
                        ".vscode/settings.json",
                        "fixtures/public.key",
                    )
                ),
                ignored=False,
            )

    def test_unmanaged_nested_ignore_can_still_override_ancestor_baseline(self) -> None:
        self.install([scope()])
        self.write("unmanaged/.gitignore", "!.env\n")
        self.assert_paths(("unmanaged/.env",), ignored=False)
        self.assert_paths(("other/.env",), ignored=True)


if __name__ == "__main__":
    unittest.main()
