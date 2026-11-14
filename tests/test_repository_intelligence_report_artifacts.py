# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
# ruff: noqa: PT027

"""Exercise exact-source artifact admission without provider calls or secrets."""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any
import unittest
from unittest.mock import patch

import yaml

from tools import repository_intelligence_report_artifacts as intake
from tools.repository_intelligence_publication import REPORT_SCHEMA, REPOSITORY, PublicationError

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "a" * 40


class ReportArtifactTests(unittest.TestCase):
    """Keep explicit selection fail-closed and preserve literal report bytes."""

    def setUp(self) -> None:
        directory = TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.summary: dict[str, Any] = {
            "schema": REPORT_SCHEMA,
            "schema_version": 1,
            "producer": "osv",
            "repository": REPOSITORY,
            "commit": SOURCE,
            "generated_at": "2026-11-13T22:00:00Z",
            "execution": {"state": "failure"},
            "findings": {"state": "blocked"},
            "provenance": {
                "run_id": "123",
                "run_attempt": 2,
                "event": "workflow_dispatch",
                "workflow": "🔍 OSV Vulnerability Scan",
            },
        }
        self.raw = (json.dumps(self.summary, indent=2) + "\n").encode()
        self.selection: dict[str, Any] = {
            "schema": intake.SELECTION_SCHEMA,
            "reports": [
                {
                    "producer": "osv",
                    "run_id": 123,
                    "run_attempt": 2,
                    "artifact_id": 456,
                    "archive_sha256": "b" * 64,
                    "summary_sha256": hashlib.sha256(self.raw).hexdigest(),
                }
            ],
        }
        self.producer_run: dict[str, Any] = {
            "id": 123,
            "run_attempt": 2,
            "repository": {"full_name": REPOSITORY},
            "head_repository": {"full_name": REPOSITORY},
            "head_sha": SOURCE,
            "head_branch": "main",
            "path": ".github/workflows/osv-scan.yml",
            "name": "🔍 OSV Vulnerability Scan",
            "status": "completed",
            "event": "workflow_dispatch",
            "conclusion": "failure",
        }
        self.artifact: dict[str, Any] = {
            "id": 456,
            "name": "empathy-report-osv-123-2",
            "expired": False,
            "size_in_bytes": 1024,
            "digest": "sha256:" + "b" * 64,
            "workflow_run": {"id": 123, "head_sha": SOURCE},
        }

    def fetch(self, path: str) -> dict[str, Any]:
        """Return only the exact metadata endpoints exercised by admission."""
        self.assertIn(path, {"runs/123", "artifacts/456"})
        return self.producer_run if path == "runs/123" else self.artifact

    def admitted(self) -> dict[str, Any]:
        """Admit a failed but completed same-source producer without changing it."""
        return intake.admit(self.selection, SOURCE, "main", self.fetch)

    def download(self) -> Path:
        """Create the one dedicated artifact payload supplied by the provider action."""
        folder = self.root / intake.DOWNLOAD_ROOT / str(self.artifact["name"])
        folder.mkdir(parents=True)
        path = folder / "summary.json"
        path.write_bytes(self.raw)
        return path

    def test_exact_failed_run_and_literal_summary_are_preserved(self) -> None:
        receipt = self.admitted()
        self.assertEqual(receipt["reports"][0]["conclusion"], "failure")
        original = deepcopy(self.summary)
        self.download()
        with patch.object(intake, "revision", return_value=SOURCE):
            intake.stage(self.root, receipt)
        result = self.root / intake.REPORT_ROOT / "osv/summary.json"
        self.assertEqual(result.read_bytes(), self.raw)
        self.assertEqual(json.loads(result.read_bytes()), original)
        self.assertFalse((self.root / intake.REPORT_ROOT / "scorecard").exists())
        self.assertFalse((self.root / ".reports").exists())

    def test_run_boundaries_reject_mismatch_untrusted_and_incomplete_inputs(self) -> None:
        changes = [
            ("id", 789),
            ("run_attempt", 1),
            ("repository", {"full_name": "other/repo"}),
            ("head_repository", {"full_name": "other/repo"}),
            ("head_sha", "c" * 40),
            ("head_branch", "feature"),
            ("path", ".github/workflows/other.yml"),
            ("name", "Other scanner"),
            ("status", "in_progress"),
            ("event", "pull_request"),
            ("event", "pull_request_target"),
            ("conclusion", "cancelled"),
            ("conclusion", None),
        ]
        for key, value in changes:
            with self.subTest(field=key, value=value):
                original = self.producer_run[key]
                self.producer_run[key] = value
                with self.assertRaises(PublicationError):
                    self.admitted()
                self.producer_run[key] = original

    def test_artifact_identity_expiry_digest_and_source_are_required(self) -> None:
        changes = [
            ("id", 789),
            ("name", "other-artifact"),
            ("expired", True),
            ("size_in_bytes", True),
            ("size_in_bytes", intake.MAX_BYTES + 1),
            ("digest", None),
            ("digest", "sha256:" + "c" * 64),
            ("workflow_run", {"id": 789, "head_sha": SOURCE}),
            ("workflow_run", {"id": 123, "head_sha": "c" * 40}),
        ]
        for key, value in changes:
            with self.subTest(field=key, value=value):
                original = self.artifact[key]
                self.artifact[key] = value
                with self.assertRaises(PublicationError):
                    self.admitted()
                self.artifact[key] = original

    def test_selection_is_closed_unique_and_bounded(self) -> None:
        invalid: list[dict[str, Any]] = [
            {},
            {"schema": intake.SELECTION_SCHEMA, "reports": []},
            {**self.selection, "unselected": "not-admitted"},
            {**self.selection, "reports": self.selection["reports"] * 2},
        ]
        for key, value in [
            ("run_id", True),
            ("run_attempt", "2"),
            ("artifact_id", -1),
            ("archive_sha256", "B" * 64),
            ("summary_sha256", "bad"),
            ("producer", "other"),
        ]:
            candidate = deepcopy(self.selection)
            candidate["reports"][0][key] = value
            invalid.append(candidate)
        for candidate in invalid:
            with self.subTest(candidate=candidate), self.assertRaises(PublicationError):
                intake.selected(candidate)

    def test_downloaded_bytes_and_original_provenance_are_not_relabelled(self) -> None:
        path = self.download()
        receipt = self.admitted()
        for key, value in [
            ("commit", "c" * 40),
            ("repository", "other/repo"),
            ("producer", "scorecard"),
            ("generated_at", "not-a-clock"),
        ]:
            with self.subTest(field=key):
                summary = {**self.summary, key: value}
                raw = json.dumps(summary).encode()
                path.write_bytes(raw)
                changed = deepcopy(receipt)
                changed["reports"][0]["summary_sha256"] = hashlib.sha256(raw).hexdigest()
                with (
                    patch.object(intake, "revision", return_value=SOURCE),
                    self.assertRaises(PublicationError),
                ):
                    intake.stage(self.root, changed)
                self.assertFalse((self.root / intake.REPORT_ROOT).exists())
        path.write_bytes(self.raw + b" ")
        with (
            patch.object(intake, "revision", return_value=SOURCE),
            self.assertRaises(PublicationError),
        ):
            intake.stage(self.root, receipt)

    def test_extra_files_links_and_stale_destinations_are_denied(self) -> None:
        path = self.download()
        receipt = self.admitted()
        extra = path.parent / "raw-log.txt"
        extra.write_text("unselected data", encoding="utf-8")
        with (
            patch.object(intake, "revision", return_value=SOURCE),
            self.assertRaises(PublicationError),
        ):
            intake.stage(self.root, receipt)
        extra.unlink()
        path.unlink()
        outside = self.root / "outside.json"
        outside.write_bytes(self.raw)
        path.symlink_to(outside)
        with (
            patch.object(intake, "revision", return_value=SOURCE),
            self.assertRaises(PublicationError),
        ):
            intake.stage(self.root, receipt)
        path.unlink()
        path.write_bytes(self.raw)
        (self.root / intake.REPORT_ROOT).mkdir()
        with (
            patch.object(intake, "revision", return_value=SOURCE),
            self.assertRaises(PublicationError),
        ):
            intake.stage(self.root, receipt)

    def test_both_consumers_use_one_read_only_intake_and_native_report_reader(self) -> None:
        for filename in ("mindgarden-pages.yml", "repository-intelligence.yml"):
            workflow = yaml.safe_load((ROOT / ".github/workflows" / filename).read_text())
            job = workflow["jobs"]["build" if filename == "mindgarden-pages.yml" else "generate"]
            step = next(s for s in job["steps"] if s.get("id") == "report_selection")
            self.assertEqual(step["uses"], "./.github/actions/report-artifacts")
            calls = [
                s
                for s in job["steps"]
                if s.get("uses", "").startswith("egohygiene/relay/actions/repository-intelligence@")
            ]
            for call in calls:
                if call["id"] != "intelligence_rollback":
                    self.assertIn(
                        "steps.report_selection.outputs.reports-directory",
                        call["with"]["reports-directory"],
                    )
        action = yaml.safe_load((ROOT / ".github/actions/report-artifacts/action.yml").read_text())
        downloads = [
            s for s in action["runs"]["steps"] if "actions/download-artifact@" in s.get("uses", "")
        ]
        self.assertEqual(len(downloads), 3)
        self.assertTrue(all(s["with"]["digest-mismatch"] == "error" for s in downloads))

    def test_artifact_only_opt_in_preserves_default_snapshot_policy(self) -> None:
        for filename in ("megalinter.yml", "osv-scan.yml", "ossf-scorecard.yml"):
            workflow = yaml.safe_load((ROOT / ".github/workflows" / filename).read_text())
            self.assertIs(
                workflow[True]["workflow_dispatch"]["inputs"]["publish-snapshot"]["default"], True
            )
            writes = [
                j
                for j in workflow["jobs"].values()
                if j.get("permissions", {}).get("contents") == "write"
            ]
            self.assertEqual(len(writes), 1)
            self.assertIn("inputs['publish-snapshot']", writes[0]["if"])
            normalizers = [
                s
                for j in workflow["jobs"].values()
                for s in j.get("steps", [])
                if "actions/normalize-repository-report@" in s.get("uses", "")
            ]
            self.assertEqual(len(normalizers), 1)
            self.assertEqual(normalizers[0]["id"], "normalize")


if __name__ == "__main__":
    unittest.main()
