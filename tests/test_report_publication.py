# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Policy tests for trusted report generation and publication."""

from __future__ import annotations

from pathlib import Path
import unittest

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


class ReportPublicationPolicyTests(unittest.TestCase):
    """Keep pull requests read-only and report snapshots stable."""

    def workflow(self, name: str) -> str:
        """Read one canonical workflow."""

        return (REPOSITORY_ROOT / ".github/workflows" / name).read_text(encoding="utf-8")

    def test_commitlint_uses_the_locked_local_node_toolchain(self) -> None:
        workflow = self.workflow("commitlint.yml")
        self.assertNotIn("wagoid/commitlint-github-action", workflow)
        self.assertIn("actions/setup-node@249970729cb0ef3589644e2896645e5dc5ba9c38", workflow)
        self.assertIn("pnpm@11.21.0", workflow)
        self.assertIn("--frozen-lockfile", workflow)
        self.assertIn('--from "${BASE_SHA}"', workflow)
        self.assertIn('--to "${HEAD_SHA}"', workflow)

    def test_report_workflows_exclude_pull_requests_from_publish_jobs(self) -> None:
        for workflow_name in (
            "lint-architecture.yml",
            "megalinter.yml",
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
                self.assertIn("./.github/actions/publish-report-snapshot", workflow)

    def test_report_only_commits_do_not_retrigger_scanners(self) -> None:
        self.assertIn('- ".reports/**"', self.workflow("megalinter.yml"))
        self.assertIn('- ".reports/**"', self.workflow("osv-scan.yml"))
        architecture_workflow = self.workflow("lint-architecture.yml")
        self.assertNotIn('".reports/egolint/**"', architecture_workflow)

    def test_osv_uses_stable_latest_snapshots(self) -> None:
        workflow = self.workflow("osv-scan.yml")
        self.assertNotIn("HISTORY_ROOT", workflow)
        self.assertNotIn("history_root", workflow)
        self.assertNotIn("commit-reports", workflow)
        self.assertIn("Git history and per-run artifacts preserve history", workflow)

    def test_publisher_enforces_report_only_default_branch_writes(self) -> None:
        action = (REPOSITORY_ROOT / ".github/actions/publish-report-snapshot/action.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("pull_request | pull_request_target", action)
        self.assertIn('GITHUB_REF_NAME}" != "${INPUT_DEFAULT_BRANCH', action)
        self.assertIn(".reports/*", action)
        self.assertIn("Timestamped history directories are forbidden", action)
        self.assertIn("git add --force --all", action)
        self.assertIn("git pull --rebase", action)


if __name__ == "__main__":
    unittest.main()
