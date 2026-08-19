# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).parents[1]


def load_module(name: str, path: Path):
    specification = importlib.util.spec_from_file_location(name, path)
    assert specification is not None
    assert specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


audit = load_module("staging_home_audit", ROOT / "tools" / "staging_home_audit.py")
gate = load_module("staging_removal_gate", ROOT / "tools" / "staging_removal_gate.py")


class StagingRemovalGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.rows = audit.build_rows(ROOT)
        cls.row = next(row for row in cls.rows if row.source_path == ".staging/misc/ROADMAP.md")

    def test_missing_approval_blocks_removal(self) -> None:
        errors = gate.validate_removals(self.rows, {}, [self.row.source_path])
        self.assertEqual([f"missing removal approval: {self.row.source_path}"], errors)

    def test_exact_complete_approval_allows_removal(self) -> None:
        approval = {
            "source_path": self.row.source_path,
            "git_blob": self.row.git_blob,
            "destination": self.row.canonical_home,
            "destination_revision": "0123456789abcdef",
            "validation_evidence": "https://github.com/egohygiene/empathy/pull/1",
            "provenance_resolution": "active copy preserves original Git history",
            "sensitivity_resolution": "passive documentation; no sensitive content",
            "approved_by": "szmyty",
            "approved_at": "2026-08-18T00:00:00Z",
        }
        errors = gate.validate_removals(
            self.rows, {self.row.source_path: approval}, [self.row.source_path]
        )
        self.assertEqual([], errors)

    def test_blob_change_invalidates_approval(self) -> None:
        approval = {
            "source_path": self.row.source_path,
            "git_blob": "0" * 40,
            "destination": self.row.canonical_home,
            "destination_revision": "0123456789abcdef",
            "validation_evidence": "evidence",
            "provenance_resolution": "resolved",
            "sensitivity_resolution": "resolved",
            "approved_by": "szmyty",
            "approved_at": "2026-08-18T00:00:00Z",
        }
        errors = gate.validate_removals(
            self.rows, {self.row.source_path: approval}, [self.row.source_path]
        )
        self.assertIn(
            f"{self.row.source_path} approval blob does not match current source", errors
        )


if __name__ == "__main__":
    unittest.main()
