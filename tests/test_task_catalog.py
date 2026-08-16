# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import unittest

REPOSITORY_ROOT = Path(__file__).parents[1]
MODULE_PATH = REPOSITORY_ROOT / "tools/task_catalog.py"
SPEC = importlib.util.spec_from_file_location("task_catalog", MODULE_PATH)
assert SPEC is not None
assert SPEC.loader is not None
task_catalog = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = task_catalog
SPEC.loader.exec_module(task_catalog)


class TaskCatalogTests(unittest.TestCase):
    def test_escape_cell_normalizes_markdown_content(self) -> None:
        self.assertEqual(task_catalog.escape_cell("one | two\nthree"), "one \\| two three")

    def test_render_catalog_includes_task_metadata(self) -> None:
        catalog = task_catalog.render_catalog(
            [
                {
                    "name": "check",
                    "desc": "Validate everything",
                    "aliases": ["verify"],
                }
            ]
        )

        self.assertIn("1 public commands", catalog)
        self.assertIn("`task check`", catalog)
        self.assertIn("Validate everything", catalog)
        self.assertIn("`verify`", catalog)

    def test_update_catalog_preserves_authored_content(self) -> None:
        document = f"before\n{task_catalog.START_MARKER}\nold\n{task_catalog.END_MARKER}\nafter\n"
        replacement = f"{task_catalog.START_MARKER}\nnew\n{task_catalog.END_MARKER}"

        self.assertEqual(
            task_catalog.update_catalog(document, replacement),
            f"before\n{replacement}\nafter\n",
        )

    def test_update_catalog_rejects_missing_markers(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "exactly one generated region"):
            task_catalog.update_catalog("no generated region", "replacement")


if __name__ == "__main__":
    unittest.main()
