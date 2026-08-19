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

    def test_remaining_devcontainer_features_have_realm_destinations(self) -> None:
        paths = [
            ".staging/devenvironment/.devcontainer/features/devtools/devcontainer-feature.json",
            ".staging/devenvironment/.devcontainer/features/docker-proxy/devcontainer-feature.json",
        ]

        for path in paths:
            with self.subTest(path=path):
                row = self.by_path[path]
                self.assertEqual(row.canonical_owner, "realm")
                self.assertTrue(row.canonical_home.startswith("realm/devcontainer-features/"))

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

    def test_emoji_cache_is_classified_as_generated_renderflow_intake(self) -> None:
        rows = [
            row
            for row in self.rows
            if row.source_path.startswith(".staging/tools/emoji-precache/assets/emojis/")
        ]

        self.assertGreater(len(rows), 7_000)
        self.assertEqual({row.canonical_owner for row in rows}, {"renderflow"})
        self.assertEqual({row.migration_state for row in rows}, {"quarantined"})
        self.assertEqual(
            {row.provenance_state for row in rows}, {"needs-source-license-review"}
        )

    def test_ledger_records_deletion_gate_fields(self) -> None:
        row = self.by_path[".staging/misc/ROADMAP.md"]

        self.assertEqual(row.migration_state, "candidate-removal")
        self.assertEqual(row.destination_evidence, "")
        self.assertEqual(row.deletion_approved_by, "")
        self.assertIn("source removal approved separately", row.exit_criteria)

    def test_summary_json_covers_the_file_ledger(self) -> None:
        rendered = staging_home_audit.render_summary_json(self.rows)

        self.assertIn(f'"tracked_files": {len(self.rows)}', rendered)
        self.assertIn('"unclassified_files": 0', rendered)


if __name__ == "__main__":
    unittest.main()
