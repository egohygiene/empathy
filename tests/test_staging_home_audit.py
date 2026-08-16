# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import unittest

REPOSITORY_ROOT = Path(__file__).parents[1]
MODULE_PATH = REPOSITORY_ROOT / "tools/staging_home_audit.py"
SPEC = importlib.util.spec_from_file_location("staging_home_audit", MODULE_PATH)
assert SPEC is not None
assert SPEC.loader is not None
staging_home_audit = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = staging_home_audit
SPEC.loader.exec_module(staging_home_audit)


class StagingHomeAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.rows = staging_home_audit.build_rows(REPOSITORY_ROOT)
        cls.by_path = {row.source_path: row for row in cls.rows}

    def test_every_staged_file_has_a_concrete_home(self) -> None:
        tracked_staging_paths = {
            path
            for path, _mode, _blob in staging_home_audit.tracked_entries(REPOSITORY_ROOT)
            if path.startswith(".staging/")
        }

        self.assertEqual(set(self.by_path), tracked_staging_paths)
        self.assertNotIn("manual-review", {row.canonical_owner for row in self.rows})
        self.assertNotIn("TBD", {row.canonical_home for row in self.rows})

    def test_realm_devcontainer_variants_share_one_destination(self) -> None:
        first = self.by_path[".staging/devenvironment/.devcontainer/devcontainer.json"]
        second = self.by_path[".staging/devenvironment/.devcontainer/devcontainer2.json"]

        self.assertEqual(first.canonical_owner, "realm")
        self.assertEqual(first.canonical_home, second.canonical_home)
        self.assertEqual(first.merge_group, "realm-devcontainer-config")
        self.assertEqual(second.merge_group, first.merge_group)

    def test_product_fixture_is_kept_out_of_realm(self) -> None:
        api = self.by_path[".staging/devenvironment/containers/services/api/Dockerfile.old"]

        self.assertEqual(api.canonical_owner, "holon")
        self.assertTrue(api.canonical_home.startswith("holon/templates/universal-app/"))

    def test_cross_cutting_sources_follow_capability_ownership(self) -> None:
        cases = {
            ".staging/.pre-commit-config.yaml": "egolint",
            ".staging/.github/workflows/flutter-ci-reusable.yml": "relay",
            ".staging/.github/specs/agent-system.spec.md": "aether",
            ".staging/mkdocs.yml": "mindgarden",
            ".staging/templates/paper/README.md": "beacon",
        }

        for path, expected_owner in cases.items():
            with self.subTest(path=path):
                self.assertEqual(self.by_path[path].canonical_owner, expected_owner)

    def test_community_instructions_remain_quarantined(self) -> None:
        community_rows = [row for row in self.rows if row.collection.startswith("community ")]

        self.assertGreater(len(community_rows), 1_000)
        self.assertEqual({row.canonical_owner for row in community_rows}, {"aether"})
        self.assertEqual({row.disposition for row in community_rows}, {"quarantine-and-curate"})
        self.assertTrue(
            all(row.incubation_home.startswith("aether/.staging/") for row in community_rows)
        )


if __name__ == "__main__":
    unittest.main()
