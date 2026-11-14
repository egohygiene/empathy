# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
"""Exercise mailmap composition against actual Git matching and history behavior."""

from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess  # nosec B404
import sys
import tempfile
from typing import TYPE_CHECKING, Any
import unittest

GIT = shutil.which("git")
if GIT is None:
    message = "The mailmap behavior contract requires actual Git"
    raise RuntimeError(message)

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
if TYPE_CHECKING:
    from tools import foundation, foundation_mailmap as mailmap
else:
    import foundation_mailmap as mailmap

    import foundation

BASELINE = "Canonical Author <canonical@example.invalid> <alias@example.invalid>\n"
LOCAL = "# Preserve this exact consumer comment.\nLocal Author <local@example.invalid> <old@example.invalid>\n"


class FoundationMailmapTests(unittest.TestCase):
    def selection(self) -> dict[str, Any]:
        return {
            "baseline": BASELINE,
            "local_additions": LOCAL,
            "identity_evidence": ["https://example.invalid/review/1"],
        }

    def plan(self, selection: dict[str, Any] | None = None) -> dict[str, Any]:
        catalog = foundation.load_json(ROOT / "foundation/catalog.json")
        manifest = foundation.load_json(ROOT / "foundation/empathy.manifest.json")
        manifest["repository"] = "synthetic-organization/sample"
        manifest["mailmap"] = selection or self.selection()
        resolved, errors = foundation.resolve_manifest(catalog, manifest)
        self.assertEqual([], errors)
        assert resolved is not None
        plan, errors = mailmap.compose(catalog, resolved, ROOT)
        self.assertEqual([], errors)
        assert plan is not None
        return plan

    @staticmethod
    def git(root: Path, *args: str, input_text: str | None = None) -> str:
        environment = {
            **os.environ,
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_AUTHOR_NAME": "Legacy Author",
            "GIT_AUTHOR_EMAIL": "alias@example.invalid",
            "GIT_COMMITTER_NAME": "Fixture Committer",
            "GIT_COMMITTER_EMAIL": "committer@example.invalid",
        }
        assert GIT is not None
        return subprocess.check_output(  # noqa: S603 # nosec B603 # Fixed Git; only synthetic fixture args.
            [GIT, "-C", str(root), *args],
            input=input_text,
            text=True,
            env=environment,
        ).strip()

    def test_git_presentation_local_update_and_guarded_rollback_preserve_history(self) -> None:
        with tempfile.TemporaryDirectory(prefix="mailmap fixture ") as temporary:
            root = Path(temporary)
            self.git(root, "init", "--quiet")
            (root / "content.txt").write_text("immutable commit content\n", encoding="utf-8")
            self.git(root, "add", "content.txt")
            self.git(root, "-c", "core.hooksPath=/dev/null", "commit", "--quiet", "-m", "fixture")
            before = self.git(root, "rev-parse", "HEAD")
            before_tree = self.git(root, "rev-parse", "HEAD^{tree}")
            raw = self.git(root, "log", "-1", "--format=%an <%ae>")
            self.assertEqual("Legacy Author <alias@example.invalid>", raw)
            first = self.plan()["files"][0]["content"]
            target = root / ".mailmap"
            target.write_text(first, encoding="utf-8")
            self.assertEqual(
                "Canonical Author <canonical@example.invalid>",
                self.git(root, "check-mailmap", "Legacy Author <ALIAS@example.invalid>"),
            )
            self.assertEqual(
                "Canonical Author <canonical@example.invalid>",
                self.git(root, "log", "-1", "--format=%aN <%aE>"),
            )
            self.assertEqual(
                "Local Author <local@example.invalid>",
                self.git(root, "check-mailmap", "Original <old@example.invalid>"),
            )
            self.assertEqual(
                "Unmapped <unknown@example.invalid>",
                self.git(root, "check-mailmap", "Unmapped <unknown@example.invalid>"),
            )
            self.assertEqual(first, self.plan()["files"][0]["content"])
            updated = self.selection()
            updated["baseline"] = BASELINE.replace("Canonical Author", "Reviewed Name")
            second = self.plan(updated)["files"][0]["content"]
            self.assertIn(LOCAL, second)
            expected_preimage = hashlib.sha256(first.encode()).hexdigest()
            self.assertEqual(expected_preimage, hashlib.sha256(target.read_bytes()).hexdigest())
            target.write_text(second, encoding="utf-8")
            self.assertEqual(
                "Reviewed Name <canonical@example.invalid>",
                self.git(root, "log", "-1", "--format=%aN <%aE>"),
            )
            # A reviewed consumer can restore a retained preimage only if the update is untouched.
            self.assertEqual(
                hashlib.sha256(second.encode()).hexdigest(),
                hashlib.sha256(target.read_bytes()).hexdigest(),
            )
            target.write_text(first, encoding="utf-8")
            self.assertEqual(expected_preimage, hashlib.sha256(target.read_bytes()).hexdigest())
            self.assertEqual(before, self.git(root, "rev-parse", "HEAD"))
            self.assertEqual(before_tree, self.git(root, "rev-parse", "HEAD^{tree}"))
            self.assertEqual(raw, self.git(root, "log", "-1", "--format=%an <%ae>"))
            self.assertEqual("?? .mailmap", self.git(root, "status", "--short"))

    def test_all_four_git_forms_and_specific_alias_precedence(self) -> None:
        content = (
            "Name Only <name@example.invalid>\n"
            "<email@example.invalid> <email-old@example.invalid>\n"
            "Both <both@example.invalid> <both-old@example.invalid>\n"
            "Specific <specific@example.invalid> Legacy Name <shared@example.invalid>\n"
        )
        rows, errors = mailmap.mappings(content)
        self.assertEqual([], errors)
        self.assertEqual(4, len(rows))
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.git(root, "init", "--quiet")
            (root / ".mailmap").write_text(content, encoding="utf-8")
            queries = "Old <name@example.invalid>\nOld <email-old@example.invalid>\nOld <both-old@example.invalid>\nlegacy name <SHARED@example.invalid>\nOther Name <shared@example.invalid>\n"
            actual = self.git(root, "check-mailmap", "--stdin", input_text=queries).splitlines()
            self.assertEqual(
                [
                    "Name Only <name@example.invalid>",
                    "Old <email@example.invalid>",
                    "Both <both@example.invalid>",
                    "Specific <specific@example.invalid>",
                    "Other Name <shared@example.invalid>",
                ],
                actual,
            )

    def test_git_last_alias_wins_but_composition_rejects_silent_identity_override(self) -> None:
        selection = self.selection()
        selection["local_additions"] = (
            "Different <different@example.invalid> <ALIAS@example.invalid>\n"
        )
        self.assertTrue(
            any("conflicting" in error for error in mailmap.validate_selection(selection))
        )
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.git(root, "init", "--quiet")
            (root / ".mailmap").write_text(
                BASELINE + selection["local_additions"], encoding="utf-8"
            )
            self.assertEqual(
                "Different <different@example.invalid>",
                self.git(root, "check-mailmap", "Original <alias@example.invalid>"),
            )

    def test_missing_malformed_and_ambiguous_input_is_actionable(self) -> None:
        for value in [
            None,
            {},
            {**self.selection(), "baseline": ""},
            {**self.selection(), "baseline": "# No identities\n"},
            {**self.selection(), "baseline": "No explicit address\n"},
            {**self.selection(), "baseline": "Name <x@example.invalid> extra\n"},
            {**self.selection(), "baseline": "Name <x@example.invalid>\r\n"},
            {**self.selection(), "identity_evidence": []},
        ]:
            with self.subTest(value=value):
                self.assertTrue(mailmap.validate_selection(value))
        selected = self.selection()
        selected["local_additions"] = (
            "Different <different@example.invalid> Specific <alias@example.invalid>\n"
        )
        self.assertTrue(
            any("name-specific" in error for error in mailmap.validate_selection(selected))
        )

    def test_portable_template_and_second_organization_never_inherit_personal_values(self) -> None:
        plan = self.plan()
        serialized = json.dumps(plan)
        self.assertNotIn("Szmyt", serialized)
        self.assertNotIn("noreply.github.com", serialized)
        self.assertEqual("synthetic-organization/sample", plan["repository"])
        self.assertIn(LOCAL, plan["files"][0]["content"])
        self.assertEqual("plan-only", plan["status"])

    def test_cli_refuses_consumer_target_and_preserves_existing_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / ".mailmap"
            target.write_text(LOCAL, encoding="utf-8")
            self.assertEqual(
                2,
                foundation.main(
                    [
                        "--catalog",
                        str(ROOT / "foundation/catalog.json"),
                        "plan-mailmap",
                        "--manifest",
                        str(ROOT / "foundation/empathy.manifest.json"),
                        "--source-root",
                        str(ROOT),
                        "--output",
                        str(target),
                    ]
                ),
            )
            self.assertEqual(LOCAL, target.read_text(encoding="utf-8"))

    def test_golden_proposal_matches_adopted_file_and_preserves_local_text(self) -> None:
        catalog = foundation.load_json(ROOT / "foundation/catalog.json")
        manifest = foundation.load_json(ROOT / "foundation/empathy.manifest.json")
        resolved, errors = foundation.resolve_manifest(catalog, manifest)
        self.assertEqual([], errors)
        assert resolved is not None
        plan, errors = mailmap.compose(catalog, resolved, ROOT)
        self.assertEqual([], errors)
        assert plan is not None
        self.assertEqual(
            (ROOT / ".mailmap").read_text(encoding="utf-8"), plan["files"][0]["content"]
        )
        self.assertIn(manifest["mailmap"]["local_additions"], plan["files"][0]["content"])

    def test_presence_is_distinct_from_selected_identity_and_source_digest(self) -> None:
        catalog = foundation.load_json(ROOT / "foundation/catalog.json")
        manifest = foundation.load_json(ROOT / "foundation/empathy.manifest.json")
        manifest.pop("mailmap")
        resolved, errors = foundation.resolve_manifest(catalog, manifest)
        self.assertEqual([], errors)
        assert resolved is not None
        self.assertIn("mailmap", {row["id"] for row in resolved["artifacts"]})
        plan, errors = mailmap.compose(catalog, resolved, ROOT)
        self.assertIsNone(plan)
        self.assertTrue(errors)
        manifest["mailmap"] = self.selection()
        resolved, errors = foundation.resolve_manifest(catalog, manifest)
        assert resolved is not None
        damaged = copy.deepcopy(catalog)
        artifact = next(row for row in resolved["artifacts"] if row["id"] == "mailmap")
        artifact["composition"]["header"]["sha256"] = "0" * 64
        self.assertTrue(mailmap.compose(damaged, resolved, ROOT)[1])


if __name__ == "__main__":
    unittest.main()
