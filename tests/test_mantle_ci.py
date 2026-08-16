# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

from __future__ import annotations

import json
from pathlib import Path
import unittest

REPOSITORY_ROOT = Path(__file__).parents[1]


class MantleIntegrationTests(unittest.TestCase):
    def test_root_taskfile_delegates_to_mantle(self) -> None:
        taskfile = (REPOSITORY_ROOT / "Taskfile.yml").read_text(encoding="utf-8")
        project_tasks = (REPOSITORY_ROOT / ".tasks/project.yml").read_text(encoding="utf-8")
        self.assertIn("mantle:", taskfile)
        self.assertIn("taskfile: ./mantle/Taskfile.yml", taskfile)
        self.assertIn("- mantle:check", project_tasks)

        mantle_taskfile = (REPOSITORY_ROOT / "mantle/Taskfile.yml").read_text(encoding="utf-8")
        for task_name in (
            "status:",
            "test:",
            "lint:",
            "install:smoke:",
            "docs:",
            "check:",
            "ci:",
        ):
            with self.subTest(task=task_name):
                self.assertIn(f"  {task_name}", mantle_taskfile)

        self.assertIn("./tests/run.sh --strict", mantle_taskfile)
        self.assertIn("/bin/bash ./tests/smoke/install.sh", mantle_taskfile)

    def test_vscode_exposes_the_mantle_task_contract(self) -> None:
        tasks = json.loads((REPOSITORY_ROOT / ".vscode/tasks.json").read_text(encoding="utf-8"))[
            "tasks"
        ]
        task_arguments = {
            tuple(task.get("args", [])) for task in tasks if task.get("command") == "task"
        }

        for task_name in (
            "mantle:status",
            "mantle:test",
            "mantle:lint",
            "mantle:install:smoke",
            "mantle:docs",
            "mantle:check",
            "mantle:ci",
        ):
            with self.subTest(task=task_name):
                self.assertIn((task_name,), task_arguments)

    def test_workflow_runs_strict_validation_and_real_install_smoke(self) -> None:
        workflow = (REPOSITORY_ROOT / ".github/workflows/mantle.yml").read_text(encoding="utf-8")

        for expected in (
            "ubuntu-24.04",
            "macos-15",
            "./tests/run.sh --strict",
            "/bin/bash ./tests/smoke/install.sh",
            'FASTFETCH_VERSION: "2.67.0"',
            "tests/validate_fastfetch.py",
            "fastfetch-linux-amd64.tar.gz",
            "f14538f30286f83affe129c8fb874d2b13c669365fa2e71533986d188c6c5af1",
            "--config config/fastfetch/fastfetch.jsonc",
            "permissions:\n  contents: read",
            "persist-credentials: false",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, workflow)

        self.assertNotIn("pull_request_target:", workflow)

    def test_install_smoke_is_hermetic_and_avoids_shell_hooks(self) -> None:
        smoke_test = (REPOSITORY_ROOT / "mantle/tests/smoke/install.sh").read_text(encoding="utf-8")

        for expected in (
            "env -i",
            "--no-shell-hook",
            "mantle-install-smoke.",
            '"${MANTLE_SMOKE_PREFIX}/bin/mantle" doctor',
            "--status",
            "--uninstall",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, smoke_test)


if __name__ == "__main__":
    unittest.main()
