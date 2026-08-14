# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Tests for the deterministic static repository intelligence dashboard."""

from __future__ import annotations

from datetime import UTC, datetime
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
ACTION_ROOT = REPOSITORY_ROOT / ".github/actions/generate-repository-intelligence-dashboard"
FIXTURE_ROOT = REPOSITORY_ROOT / "tests/fixtures/repository-intelligence-dashboard"
MODULE_PATH = ACTION_ROOT / "generate_repository_intelligence_dashboard.py"
SPEC = importlib.util.spec_from_file_location(
    "generate_repository_intelligence_dashboard", MODULE_PATH
)
assert SPEC is not None
assert SPEC.loader is not None
dashboard_builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(dashboard_builder)

AS_OF = datetime(2026, 8, 14, 12, tzinfo=UTC)
REPOSITORY = "egohygiene/empathy"


def git(repository: Path, *arguments: str, environment: dict[str, str] | None = None) -> str:
    """Run one deterministic Git command in a fixture repository."""

    result = subprocess.run(
        ["git", "-C", str(repository), *arguments],
        check=True,
        capture_output=True,
        text=True,
        env=environment,
    )
    return result.stdout.strip()


def initialize_repository(root: Path) -> str:
    """Create a minimal full-history repository for vitality collection."""

    git(root, "init", "--quiet")
    git(root, "config", "--local", "user.name", "Dashboard Fixture")
    git(root, "config", "--local", "user.email", "fixture@example.test")
    workflow = root / ".github/workflows/example.yml"
    action = root / ".github/actions/example/action.yml"
    test_module = root / "tests/test_example.py"
    for path, content in (
        (workflow, "name: Example\n"),
        (action, "name: Example\nruns:\n  using: composite\n  steps: []\n"),
        (test_module, '"""Fixture test module."""\n'),
        (root / "README.md", "# Fixture repository\n"),
    ):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    git(root, "add", "--all")
    environment = os.environ.copy()
    environment.update(
        {
            "GIT_AUTHOR_DATE": "2026-08-14T10:00:00Z",
            "GIT_COMMITTER_DATE": "2026-08-14T10:00:00Z",
        }
    )
    git(root, "commit", "--quiet", "--message", "fixture: initialize", environment=environment)
    return git(root, "rev-parse", "HEAD")


class RepositoryIntelligenceDashboardTests(unittest.TestCase):
    """Keep aggregation, public projection, and rendering truthful."""

    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.repository_root = Path(self.temporary_directory.name) / "repository"
        self.repository_root.mkdir()
        self.source_commit = initialize_repository(self.repository_root)

    def build(self, reports_root: Path) -> dict[str, object]:
        """Build one dashboard against the fixture checkout."""

        return dashboard_builder.build_dashboard(
            repository_root=self.repository_root,
            reports_root=reports_root,
            repository=REPOSITORY,
            default_branch="main",
            source_commit=self.source_commit,
            as_of=AS_OF,
        )

    def copy_reports(self) -> Path:
        """Copy the complete producer fixture set into the temporary checkout."""

        reports_root = self.repository_root / ".reports"
        shutil.copytree(FIXTURE_ROOT, reports_root)
        return reports_root

    def test_complete_reports_preserve_independent_states(self) -> None:
        dashboard = self.build(self.copy_reports())

        self.assertEqual(dashboard["states"]["execution"]["success"], 2)
        self.assertEqual(dashboard["states"]["execution"]["failure"], 1)
        self.assertEqual(dashboard["states"]["findings"]["attention"], 2)
        self.assertEqual(dashboard["states"]["findings"]["clear"], 1)
        self.assertEqual(dashboard["states"]["freshness"]["fresh"], 2)
        self.assertEqual(dashboard["states"]["freshness"]["stale"], 1)
        self.assertEqual(dashboard["producers"]["scorecard"]["metrics"]["aggregate_score"], 4.1)

    def test_missing_reports_are_unavailable_and_unknown(self) -> None:
        dashboard = self.build(self.repository_root / ".reports")

        self.assertEqual(dashboard["states"]["availability"]["unavailable"], 3)
        self.assertEqual(dashboard["states"]["execution"]["unknown"], 3)
        self.assertEqual(dashboard["states"]["findings"]["unknown"], 3)
        self.assertEqual(dashboard["states"]["freshness"]["unknown"], 3)

    def test_malformed_report_is_invalid_instead_of_green(self) -> None:
        reports_root = self.repository_root / ".reports"
        malformed = reports_root / "scorecard/summary.json"
        malformed.parent.mkdir(parents=True)
        malformed.write_text("{not-json}\n", encoding="utf-8")

        dashboard = self.build(reports_root)

        scorecard = dashboard["producers"]["scorecard"]
        self.assertEqual(scorecard["availability"], "invalid")
        self.assertEqual(scorecard["execution"]["state"], "failure")
        self.assertEqual(scorecard["findings"]["state"], "unknown")

    def test_stale_boundary_is_inclusive(self) -> None:
        reports_root = self.copy_reports()
        osv_path = reports_root / "osv/summary.json"
        osv = json.loads(osv_path.read_text(encoding="utf-8"))
        osv["generated_at"] = "2026-08-06T12:00:00Z"
        osv["freshness"]["expires_at"] = "2026-08-14T12:00:00Z"
        osv_path.write_text(json.dumps(osv), encoding="utf-8")

        dashboard = self.build(reports_root)

        self.assertEqual(dashboard["producers"]["osv"]["freshness"]["state"], "stale")

    def test_renderer_escapes_text_and_rejects_unsafe_links(self) -> None:
        reports_root = self.copy_reports()
        osv_path = reports_root / "osv/summary.json"
        osv = json.loads(osv_path.read_text(encoding="utf-8"))
        osv["execution"]["message"] = "<script>alert('no')</script>"
        osv["links"]["detail"] = "javascript:alert(1)"
        osv["links"]["workflow"] = "//example.invalid/phish"
        osv_path.write_text(json.dumps(osv), encoding="utf-8")

        dashboard = self.build(reports_root)
        rendered = dashboard_builder.render_html(dashboard)

        self.assertNotIn("<script>", rendered)
        self.assertNotIn("javascript:", rendered)
        self.assertNotIn("example.invalid", rendered)
        self.assertIn("&lt;script&gt;", rendered)

    def test_bundle_is_deterministic_and_contains_no_contributor_identities(self) -> None:
        reports_root = self.copy_reports()
        first = self.build(reports_root)
        second = self.build(reports_root)
        output_root = self.repository_root / "site/intelligence"

        dashboard_builder.write_dashboard_bundle(
            output_root, first, ACTION_ROOT / "dashboard.css"
        )
        first_json = (output_root / "summary.json").read_text(encoding="utf-8")
        first_html = (output_root / "index.html").read_text(encoding="utf-8")
        dashboard_builder.write_dashboard_bundle(
            output_root, second, ACTION_ROOT / "dashboard.css"
        )

        self.assertEqual(
            first_json, (output_root / "summary.json").read_text(encoding="utf-8")
        )
        self.assertEqual(
            first_html, (output_root / "index.html").read_text(encoding="utf-8")
        )
        self.assertNotIn("fixture@example.test", first_json)
        self.assertEqual(first["vitality"]["metrics"]["contributors_90_days"], 1)
        self.assertTrue((output_root / "styles.css").is_file())

    def test_vitality_uses_the_represented_commit_not_untracked_files(self) -> None:
        untracked_workflow = self.repository_root / ".github/workflows/untracked.yml"
        untracked_action = self.repository_root / ".github/actions/untracked/action.yml"
        untracked_test = self.repository_root / "tests/test_untracked.py"
        for path in (untracked_workflow, untracked_action, untracked_test):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("# not represented by the source commit\n", encoding="utf-8")

        dashboard = self.build(self.repository_root / ".reports")
        metrics = dashboard["vitality"]["metrics"]

        self.assertEqual(metrics["workflows"], 1)
        self.assertEqual(metrics["composite_actions"], 1)
        self.assertEqual(metrics["python_tests"], 1)

    def test_checked_in_schema_declares_public_contract(self) -> None:
        schema = json.loads(
            (ACTION_ROOT / "repository-intelligence-dashboard.schema.json").read_text(
                encoding="utf-8"
            )
        )

        self.assertEqual(
            schema["properties"]["schema"]["const"], dashboard_builder.DASHBOARD_SCHEMA
        )
        self.assertIn("producers", schema["required"])
        self.assertIn("vitality", schema["required"])

    def test_artifact_workflow_generates_and_uploads_the_dashboard(self) -> None:
        workflow = (REPOSITORY_ROOT / ".github/workflows/repository-intelligence.yml").read_text(
            encoding="utf-8"
        )

        self.assertIn("dashboard-output-root", workflow)
        self.assertIn("generate-repository-intelligence-dashboard", workflow)
        self.assertIn("${{ inputs.dashboard-output-root }}", workflow)


if __name__ == "__main__":
    unittest.main()
