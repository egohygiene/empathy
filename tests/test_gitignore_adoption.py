# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Prove the golden root migration against real Git and the complete old audit."""

from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess  # nosec B404
import sys
from typing import TYPE_CHECKING
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

if TYPE_CHECKING:
    # Mypy cannot infer the runtime sys.path entry above; name the source modules.
    from tests import test_gitignore_baseline
    from tools import foundation
else:
    import foundation
    import test_gitignore_baseline


class GitignoreAdoptionTests(test_gitignore_baseline.GitignoreFixture):
    def setUp(self) -> None:
        super().setUp()
        self.migration = json.loads(
            (ROOT / "tests/fixtures/gitignore/empathy-migration.json").read_text(encoding="utf-8")
        )
        self.write(".gitignore", (ROOT / ".gitignore").read_text(encoding="utf-8"))
        # Preserve the real nested precedence; a root-only fixture would overstate adoption.
        for path in self.migration["existing_nested_ignores"]:
            self.write(path, (ROOT / path).read_text(encoding="utf-8"))

    def test_active_root_is_byte_identical_to_the_resolved_golden_plan(self) -> None:
        catalog = foundation.load_json(ROOT / "foundation/catalog.json")
        manifest = foundation.load_json(ROOT / "foundation/empathy.manifest.json")
        plan, errors = foundation.plan_gitignore(catalog, manifest, ROOT)
        self.assertEqual([], errors)
        if plan is None:
            self.fail("The golden manifest must produce a composition plan")
        self.assertEqual([".gitignore"], [file["path"] for file in plan["files"]])
        self.assertEqual((ROOT / ".gitignore").read_bytes(), plan["files"][0]["content"].encode())

    def test_every_historical_rule_has_exactly_one_migration_disposition(self) -> None:
        audit = []
        for line in (
            (ROOT / "docs/foundation/gitignore/RULE_AUDIT.md")
            .read_text(encoding="utf-8")
            .splitlines()
        ):
            if not line.startswith("|"):
                continue
            fields = [field.strip() for field in line.split("|")]
            if fields[1].isdigit():
                audit.append(fields[2].strip("`"))
        accounted = [rule for group in self.migration["groups"] for rule in group["audited_rules"]]
        self.assertEqual(176, len(audit))
        self.assertEqual(Counter(audit), Counter(accounted))
        self.assertEqual(len(accounted), len(set(accounted)))
        for group in self.migration["groups"]:
            self.assertTrue(group["decision"], group["id"])
            self.assertTrue(group["ignored"] or group["visible"], group["id"])
            for path in group["evidence"]:
                self.assertTrue((ROOT / path).is_file(), path)

    def test_all_migration_examples_have_the_reviewed_git_visibility(self) -> None:
        for group in self.migration["groups"]:
            with self.subTest(disposition=group["id"]):
                self.assert_paths(tuple(group["ignored"]), ignored=True)
                self.assert_paths(tuple(group["visible"]), ignored=False)

    def test_active_root_has_no_duplicate_rules_and_ends_with_the_baseline(self) -> None:
        contents = (ROOT / ".gitignore").read_text(encoding="utf-8")
        rules = [line for line in contents.splitlines() if line and not line.startswith("#")]
        self.assertEqual(len(rules), len(set(rules)))
        self.assertTrue(
            contents.endswith(test_gitignore_baseline.BASELINE.read_text(encoding="utf-8"))
        )

    def test_reconciled_nested_policies_preserve_environment_and_source_boundaries(self) -> None:
        self.assert_paths(
            (
                ".devcontainer/.env",
                "holon/packs/react-vite/template/.env.sample.local",
            ),
            ignored=True,
        )
        self.assert_paths(("egolint/examples/target/source.rs",), ignored=False)
        self.assert_paths(("examples/target/source.rs",), ignored=False)
        # Retiring the Mantle snapshot also retires its nested template exception.
        self.assert_paths(
            ("examples/.env.example.local", "mantle/.env.example.local"), ignored=True
        )

    def test_imported_template_uses_the_accepted_literal_suffix_policy(self) -> None:
        self.assert_paths(
            (
                "holon/packs/react-vite/template/.env.example.local",
                "holon/packs/react-vite/template/.env.template.backup",
            ),
            ignored=True,
        )
        self.assert_paths(
            (
                "holon/packs/react-vite/template/.env.production.example",
                "holon/packs/react-vite/template/.env.production.sample",
            ),
            ignored=False,
        )
        self.assert_paths(("examples/.env.production.example",), ignored=False)
        self.assert_paths(("examples/.env.template.backup",), ignored=True)

    def test_accepted_target_policy_does_not_hide_target_named_source(self) -> None:
        self.assert_paths(
            ("egolint/examples/target/source.rs", "egolint/fixtures/target/README.md"),
            ignored=False,
        )
        self.assert_paths(("examples/target/source.rs", "fixtures/target/README.md"), ignored=False)
        self.assert_paths(("egolint/target/debug/program",), ignored=True)

    def test_devcontainer_marker_is_explicit_configuration_not_a_tracked_environment_file(
        self,
    ) -> None:
        indexed = subprocess.run(  # noqa: S603  # nosec B603
            [
                self.git_executable,
                "-C",
                str(ROOT),
                "ls-files",
                "--error-unmatch",
                "--",
                ".devcontainer/.env",
            ],
            env=self.environment,
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
        self.assertEqual(indexed.returncode, 1)
        configuration = json.loads((ROOT / ".devcontainer/devcontainer.json").read_text())
        for section in ("containerEnv", "remoteEnv"):
            with self.subTest(section=section):
                self.assertIn(
                    configuration[section]["IN_DEVCONTAINER"].casefold(), {"true", "1", "yes", "on"}
                )

    def test_scoped_owner_adoptions_bind_the_actual_policy_bytes(self) -> None:
        record = json.loads(
            (ROOT / "docs/foundation/gitignore/data/nested-adoptions-20261113.json").read_text()
        )
        for adoption in record["policy_adoptions"]:
            with self.subTest(path=adoption["path"]):
                actual = hashlib.sha256((ROOT / adoption["path"]).read_bytes()).hexdigest()
                self.assertEqual(actual, adoption["after_sha256"])


if __name__ == "__main__":
    unittest.main()
