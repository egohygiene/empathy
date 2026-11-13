# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Policy tests for trusted report generation and publication."""

from __future__ import annotations

import json
from pathlib import Path
import re
import subprocess  # nosec B404 # Fixed local commands in an owned disposable Git fixture.
from tempfile import TemporaryDirectory
import textwrap
import unittest

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


class ReportPublicationPolicyTests(unittest.TestCase):
    """Keep pull requests read-only and report snapshots stable."""

    def workflow(self, name: str) -> str:
        """Read one canonical workflow."""

        return (REPOSITORY_ROOT / ".github/workflows" / name).read_text(encoding="utf-8")

    def test_commitlint_uses_the_locked_local_node_toolchain(self) -> None:
        workflow = self.workflow("commitlint.yml")
        package = json.loads((REPOSITORY_ROOT / "egolint/package.json").read_text(encoding="utf-8"))
        self.assertNotIn("wagoid/commitlint-github-action", workflow)
        setup_references = re.findall(r"(?m)^\s+uses: (actions/setup-node@\S+)\s*$", workflow)
        self.assertEqual(len(setup_references), 1)
        self.assertRegex(setup_references[0], r"^actions/setup-node@[0-9a-f]{40}$")
        self.assertIn(f'node-version: "{package["engines"]["node"].removeprefix(">=")}"', workflow)
        self.assertIn(f"corepack prepare {package['packageManager']} --activate", workflow)
        self.assertIn("cd egolint", workflow)
        self.assertIn("sh scripts/pnpm.sh install", workflow)
        self.assertIn("--frozen-lockfile", workflow)
        self.assertIn("--ignore-scripts", workflow)
        self.assertIn("sh scripts/pnpm.sh exec commitlint", workflow)
        self.assertIn("--config .config/lint/commits/commitlint.emoji.config.cjs", workflow)
        self.assertIn('BASE_SHA: "${{ github.event.pull_request.base.sha }}"', workflow)
        self.assertIn('HEAD_SHA: "${{ github.event.pull_request.head.sha }}"', workflow)
        self.assertIn('--from "${BASE_SHA}"', workflow)
        self.assertIn('--to "${HEAD_SHA}"', workflow)

    def test_report_workflows_exclude_pull_requests_from_publish_jobs(self) -> None:
        for workflow_name in (
            "lint-architecture.yml",
            "megalinter.yml",
            "ossf-scorecard.yml",
            "osv-scan.yml",
        ):
            with self.subTest(workflow=workflow_name):
                workflow = self.workflow(workflow_name)
                self.assertIn("github.event_name != 'pull_request'", workflow)
                self.assertIn(
                    "github.ref_name == github.event.repository.default_branch",
                    workflow,
                )
                self.assertEqual(workflow.count("contents: write"), 1)
                top_level = workflow.split("\njobs:\n", maxsplit=1)[0]
                self.assertTrue(
                    "permissions: {}" in top_level or "permissions:\n  contents: read" in top_level
                )
                self.assertIn("contents: write", workflow)
                self.assertIn(
                    "egohygiene/relay/actions/publish-report-snapshot@",
                    workflow,
                )

    def test_report_only_commits_do_not_retrigger_scanners(self) -> None:
        self.assertIn('- ".reports/**"', self.workflow("megalinter.yml"))
        self.assertIn('- ".reports/**"', self.workflow("ossf-scorecard.yml"))
        self.assertIn('- ".reports/**"', self.workflow("osv-scan.yml"))
        architecture_workflow = self.workflow("lint-architecture.yml")
        self.assertNotIn('".reports/egolint/**"', architecture_workflow)

    def test_osv_uses_stable_latest_snapshots(self) -> None:
        workflow = self.workflow("osv-scan.yml")
        self.assertNotIn("HISTORY_ROOT", workflow)
        self.assertNotIn("history_root", workflow)
        self.assertNotIn("commit-reports", workflow)
        self.assertIn("Git history and per-run artifacts preserve history", workflow)

    def test_scorecard_normalization_runs_outside_the_attested_job(self) -> None:
        workflow = self.workflow("ossf-scorecard.yml")
        scorecard_job, summary_job = workflow.split("\n  publish-summary:\n", maxsplit=1)
        self.assertNotIn("normalize-repository-report", scorecard_job)
        self.assertIn("normalize-repository-report", summary_job)
        self.assertIn("publish-report-snapshot", summary_job)
        self.assertIn(".repo.commit == $commit", summary_job)

    def test_scorecard_cleanup_executes_without_removing_other_producers(self) -> None:
        """Run the real cleanup step against tracked and already-absent summaries."""

        workflow = self.workflow("ossf-scorecard.yml")
        cleanup = workflow.split("      - name: Clear the previous Scorecard summary\n", 1)[1]
        script = textwrap.dedent(cleanup.split("run: |\n", 1)[1].split("\n      - name:", 1)[0])
        with TemporaryDirectory() as directory:
            root = Path(directory)
            scorecard = root / ".reports/scorecard/summary.json"
            osv = root / ".reports/osv/summary.json"
            for path in (scorecard, osv):
                path.parent.mkdir(parents=True)
                path.write_text("preserved source fixture\n", encoding="utf-8")
            subprocess.run(  # nosec B603, B607
                ["git", "init", "--quiet", "--initial-branch=main"],  # noqa: S607
                cwd=root,
                check=True,
                capture_output=True,
            )
            subprocess.run(  # nosec B603, B607
                ["git", "add", ".reports"],  # noqa: S607
                cwd=root,
                check=True,
                capture_output=True,
            )
            for _attempt in range(2):
                subprocess.run(  # noqa: S603 # nosec B603, B607
                    ["bash", "-euo", "pipefail", "-c", script],  # noqa: S607
                    cwd=root,
                    check=True,
                    capture_output=True,
                )
                self.assertTrue(scorecard.parent.is_dir())
                self.assertFalse(scorecard.exists())
                self.assertEqual(osv.read_text(encoding="utf-8"), "preserved source fixture\n")
            tracked = subprocess.run(  # nosec B603, B607 # Fixed local Git arguments, no shell.
                ["git", "ls-files"],  # noqa: S607
                cwd=root,
                check=True,
                capture_output=True,
                text=True,
            ).stdout.splitlines()
            self.assertEqual(tracked, [".reports/osv/summary.json"])

    def test_existing_producers_emit_normalized_summaries(self) -> None:
        for workflow_name in ("megalinter.yml", "osv-scan.yml", "ossf-scorecard.yml"):
            with self.subTest(workflow=workflow_name):
                self.assertIn(
                    "egohygiene/relay/actions/normalize-repository-report@",
                    self.workflow(workflow_name),
                )


if __name__ == "__main__":
    unittest.main()
