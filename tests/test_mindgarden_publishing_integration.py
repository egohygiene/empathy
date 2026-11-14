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
            5,
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
                    "projects/egohygiene-web-namespace.md",
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
            self.assertIn("https://egohygiene.github.io/empathy/intelligence/", rendered)

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
        self.assertIn(
            "github.ref == format('refs/heads/{0}', github.event.repository.default_branch)",
            workflow,
        )
        self.assertIn("environment:\n      name: github-pages", workflow)

    def test_pages_workflow_composes_and_refreshes_repository_intelligence(self) -> None:
        workflow = (REPOSITORY_ROOT / ".github/workflows/mindgarden-pages.yml").read_text(
            encoding="utf8"
        )

        self.assertIn(
            "egohygiene/relay/actions/repository-intelligence@",
            workflow,
        )
        self.assertIn(
            'work-directory: ".cache/mindgarden/repository-intelligence"',
            workflow,
        )
        self.assertIn(
            'reports-directory: ".reports"',
            workflow,
        )
        self.assertIn('output-directory: ".cache/mindgarden/site/intelligence"', workflow)
        self.assertIn('path: ".cache/mindgarden/site"', workflow)
        # Every source/report change participates in the complete PR/main build.
        # Do not reintroduce a path filter that can omit represented inputs.
        triggers = workflow.split("permissions:", maxsplit=1)[0]
        self.assertIn("  pull_request:\n", triggers)
        self.assertIn("  push:\n    branches:\n      - main\n", triggers)
        self.assertNotIn("    paths:", triggers)
        self.assertIn("event != 'pull_request'", workflow)
        self.assertIn("head_branch == github.event.repository.default_branch", workflow)
        self.assertNotIn("workflow_run.conclusion", workflow)
        for producer_workflow in (
            "MegaLinter",
            "OpenSSF Scorecard",
            "🔍 OSV Vulnerability Scan",
        ):
            self.assertIn(producer_workflow, workflow)
        self.assertLess(
            workflow.index("Build the pinned Quartz site"),
            workflow.index("Generate repository intelligence dashboard"),
        )
        self.assertLess(
            workflow.index("Generate repository intelligence dashboard"),
            workflow.index("Upload GitHub Pages artifact"),
        )

    def test_pages_current_uses_external_owner_and_preserves_rollback_compatibility(self) -> None:
        workflow = (REPOSITORY_ROOT / ".github/workflows/mindgarden-pages.yml").read_text()
        garden = workflow.split("- name: Verify deterministic public boundary", 1)[1].split(
            "- name: Build the pinned Quartz site", 1
        )[0]
        quartz = workflow.split("- name: Build the pinned Quartz site", 1)[1].split(
            "- name: Retain standalone garden owner", 1
        )[0]
        for selected in (garden, quartz):
            self.assertIn('GARDEN_MODE: "${{ matrix.mode }}"', selected)
            self.assertIn('if [[ "${GARDEN_MODE}" == "current" ]]; then', selected)
            self.assertIn("else\n", selected)
            self.assertIn("set -euo pipefail", selected)
        self.assertIn("--requirement requirements/mindgarden-standalone.txt", garden)
        self.assertIn("from mindgarden_consumer import engine", garden)
        self.assertIn("engine(Path.cwd())", garden)
        self.assertIn("-I -m mindgarden publish verify", garden.split("else\n", 1)[0])
        self.assertIn("python3 mindgarden/scripts/publish_garden.py", garden.split("else\n", 1)[1])
        self.assertIn("-I -m mindgarden site", quartz.split("else\n", 1)[0])
        self.assertIn("python3 mindgarden/scripts/quartz_site.py", quartz.split("else\n", 1)[1])
        receipt = workflow.split("- name: Retain standalone garden owner", 1)[1].split(
            "- name: Capture consumer routes", 1
        )[0]
        self.assertIn("if: matrix.mode == 'current'", receipt)
        self.assertIn(".cache/mindgarden/publication/mindgarden-owner.json", receipt)
        self.assertIn('"projection_sha256"', receipt)

    def test_task_and_documentation_surface_the_publish_contract(self) -> None:
        root_taskfile = (REPOSITORY_ROOT / "Taskfile.yml").read_text(encoding="utf8")
        taskfile = (REPOSITORY_ROOT / ".tasks/mindgarden.yml").read_text(encoding="utf8")
        self.assertIn("taskfile: ./.tasks/mindgarden.yml", root_taskfile)
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
        self.assertIn("https://egohygiene.github.io/empathy/intelligence/", profile_readme)


if __name__ == "__main__":
    unittest.main()
