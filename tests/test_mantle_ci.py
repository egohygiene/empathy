# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Keep extracted Mantle source outside Empathy's active integration graph."""

from __future__ import annotations

import json
from pathlib import Path
import unittest

REPOSITORY_ROOT = Path(__file__).parents[1]
MANTLE_REPOSITORY = "https://github.com/egohygiene/mantle"


class MantleExtractionBoundaryTests(unittest.TestCase):
    def test_extracted_source_and_duplicate_workflow_are_absent(self) -> None:
        self.assertFalse((REPOSITORY_ROOT / "mantle").exists())
        self.assertFalse((REPOSITORY_ROOT / ".github/workflows/mantle.yml").exists())

    def test_repository_validation_does_not_import_mantle_tasks(self) -> None:
        taskfile = (REPOSITORY_ROOT / "Taskfile.yml").read_text(encoding="utf-8")
        project_tasks = (REPOSITORY_ROOT / ".tasks/project.yml").read_text(encoding="utf-8")
        self.assertNotIn("mantle:", taskfile)
        self.assertNotIn("./mantle/", taskfile)
        self.assertNotIn("mantle:", project_tasks)

    def test_editor_tasks_do_not_invoke_the_retired_namespace(self) -> None:
        tasks = json.loads((REPOSITORY_ROOT / ".vscode/tasks.json").read_text(encoding="utf-8"))[
            "tasks"
        ]
        for task in tasks:
            if task.get("command") == "task":
                with self.subTest(task=task.get("label")):
                    self.assertFalse(
                        any(
                            str(argument).startswith("mantle:") for argument in task.get("args", [])
                        )
                    )

    def test_task_documentation_identifies_the_canonical_owner(self) -> None:
        for path in ("TASKS.md", ".tasks/README.md"):
            with self.subTest(path=path):
                contents = (REPOSITORY_ROOT / path).read_text(encoding="utf-8")
                self.assertIn(MANTLE_REPOSITORY, contents)
                self.assertNotIn("`task mantle:", contents)


if __name__ == "__main__":
    unittest.main()
