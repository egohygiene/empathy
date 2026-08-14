# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
# pylint: disable=wrong-import-position
# ruff: noqa: E402

from __future__ import annotations

import json
from pathlib import Path
import re
import sys
from tempfile import TemporaryDirectory
import unittest

REPOSITORY_ROOT = Path(__file__).parents[1]
MINDGARDEN_ROOT = REPOSITORY_ROOT / "mindgarden"
sys.path.insert(0, str(MINDGARDEN_ROOT))

from scripts.publish_garden import project_garden, verify_projection


class MindgardenPublishingIntegrationTests(unittest.TestCase):
    def test_repository_projection_is_public_reviewed_and_deterministic(self) -> None:
        self.assertEqual(
            verify_projection(REPOSITORY_ROOT, Path("mindgarden/profiles/quartz/profile.yaml")),
            4,
        )
        with TemporaryDirectory() as directory:
            output = Path(directory) / "projection"
            paths = project_garden(REPOSITORY_ROOT, output)
            self.assertEqual(
                [path.as_posix() for path in paths],
                [
                    "dashboard.md",
                    "index.md",
                    "projects/index.md",
                    "projects/repository-intelligence-dashboard.md",
                ],
            )
            marker = json.loads((output / ".mindgarden-projection.json").read_text(encoding="utf8"))
            self.assertEqual(marker["schema"], "mindgarden.projection/v0")
            self.assertFalse((output / "provenance").exists())
            self.assertFalse((output / "context-packs").exists())
            self.assertFalse((output / "views").exists())
            rendered = "\n".join(path.read_text(encoding="utf8") for path in output.rglob("*.md"))
            self.assertNotIn("knowledge.base", rendered)
            self.assertNotIn(".garden.local", rendered)
            self.assertNotIn("status: draft", rendered)
            self.assertNotIn("status: proposed", rendered)

    def test_pages_workflow_uses_immutable_dependencies_and_main_only_deploy(self) -> None:
        workflow = (REPOSITORY_ROOT / ".github/workflows/mindgarden-pages.yml").read_text(
            encoding="utf8"
        )
        remote_uses = re.findall(r"uses:\s+([^\s#]+)", workflow)
        self.assertTrue(remote_uses)
        for target in remote_uses:
            if target.startswith("./"):
                continue
            self.assertRegex(target.rsplit("@", maxsplit=1)[-1], r"^[0-9a-f]{40}$")
        self.assertIn("github.event_name == 'push'", workflow)
        self.assertIn("github.ref == 'refs/heads/main'", workflow)
        self.assertIn("environment:\n      name: github-pages", workflow)

    def test_task_and_documentation_surface_the_publish_contract(self) -> None:
        taskfile = (REPOSITORY_ROOT / "Taskfile.yml").read_text(encoding="utf8")
        for task_name in (
            "garden:publish:check:",
            "garden:publish:",
            "garden:site:build:",
            "garden:site:serve:",
        ):
            self.assertIn(task_name, taskfile)
        profile_readme = (REPOSITORY_ROOT / "mindgarden/profiles/quartz/README.md").read_text(
            encoding="utf8"
        )
        self.assertIn("Settings → Pages", profile_readme)
        self.assertIn("both `reviewed` and\n`public`", profile_readme)


if __name__ == "__main__":
    unittest.main()
