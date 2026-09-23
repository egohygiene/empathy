# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Prove Empathy's report inputs against the reviewed external Relay checkout.

Run with RELAY_CHECKOUT pointing to the exact immutable revision below. The
ordinary offline suite skips this external integration when it is unavailable;
the publication fixture job supplies the checkout explicitly.
"""

from __future__ import annotations

from datetime import UTC, datetime
import importlib.util
import json
import os
from pathlib import Path
import subprocess  # nosec B404 # Fixed local Git queries; no shell input.
from tempfile import TemporaryDirectory
from typing import TYPE_CHECKING, Any, ClassVar, cast
import unittest

if TYPE_CHECKING:
    from types import ModuleType

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
RELAY_REVISION = "9a6315978766c336566b9fa7139b800fa8789ba5"
REPOSITORY = "egohygiene/empathy"
SOURCE_COMMIT = "1" * 40
AS_OF = datetime(2026, 9, 23, 12, tzinfo=UTC)


class RepositoryIntelligenceReportTests(unittest.TestCase):
    """Exercise the released renderer without copying its implementation."""

    renderer: ClassVar[ModuleType]

    @classmethod
    def setUpClass(cls) -> None:
        checkout = os.environ.get("RELAY_CHECKOUT")
        if not checkout:
            message = "Set RELAY_CHECKOUT to run the pinned Relay integration"
            raise unittest.SkipTest(message)
        relay_root = Path(checkout).resolve(strict=True)
        # Only fixed local Git operations execute; no shell or remote input is used.
        revision = subprocess.run(  # noqa: S603  # nosec B603, B607
            ["git", "-C", str(relay_root), "rev-parse", "HEAD"],  # noqa: S607
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        if revision != RELAY_REVISION:
            message = f"RELAY_CHECKOUT must be at {RELAY_REVISION}"
            raise AssertionError(message)
        module_path = (
            relay_root
            / "actions/repository-intelligence/scripts/generate_repository_intelligence_dashboard.py"
        )
        spec = importlib.util.spec_from_file_location("empathy_relay_reports", module_path)
        if spec is None or spec.loader is None:
            message = "Cannot load the reviewed Relay report renderer"
            raise AssertionError(message)
        cls.renderer = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.renderer)

    def setUp(self) -> None:
        directory = TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.reports = Path(directory.name) / ".reports"

    @staticmethod
    def report(producer: str = "osv") -> dict[str, Any]:
        """Declare consumer fixture data using the normalized report contract."""

        return {
            "schema": "egohygiene.repository-report-summary/v1",
            "schema_version": 1,
            "producer": producer,
            "repository": REPOSITORY,
            "commit": SOURCE_COMMIT,
            "generated_at": "2026-09-23T10:00:00Z",
            "freshness": {"expires_at": "2026-10-01T10:00:00Z", "stale_after_days": 8},
            "execution": {"state": "success", "message": "Validated producer output."},
            "findings": {
                "state": "blocked",
                "total": 3,
                "blocking": 2,
                "advisory": 1,
                "by_severity": {"high": 2, "low": 1},
            },
            "provenance": {
                "event": "schedule",
                "workflow": "Consumer report fixture",
                "run_id": "123",
                "run_attempt": 1,
            },
            "links": {
                "detail": f"https://github.com/{REPOSITORY}/tree/{SOURCE_COMMIT}/.reports/{producer}",
                "workflow": f"https://github.com/{REPOSITORY}/actions/runs/123",
                "security": f"https://github.com/{REPOSITORY}/security/code-scanning",
                "source": f"https://github.com/{REPOSITORY}/commit/{SOURCE_COMMIT}",
            },
            producer: {
                "scan": {
                    "vulnerabilities": 3,
                    "affected_packages": 2,
                    "severity": {"high": 2, "low": 1},
                },
                "discovery": {"ecosystem_count": 1},
                "severity_threshold": "high",
            },
        }

    def write_report(self, document: dict[str, Any], producer: str = "osv") -> Path:
        path = self.reports / producer / "summary.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(document), encoding="utf-8")
        return path

    def project(self, producer: str = "osv", *, as_of: datetime = AS_OF) -> dict[str, Any]:
        # JSON payloads cross the dynamic owner boundary and are asserted below.
        return cast(
            "dict[str, Any]",
            self.renderer.load_report(self.reports, producer, REPOSITORY, SOURCE_COMMIT, as_of),
        )

    def assert_unknown_findings(self, projection: dict[str, Any]) -> None:
        self.assertEqual(projection["findings"]["state"], "unknown")
        for count in ("total", "blocking", "advisory"):
            self.assertIsNone(projection["findings"][count])

    def test_successful_scan_keeps_blocking_findings_and_provenance_links(self) -> None:
        document = self.report()
        self.write_report(document)
        projection = self.project()
        self.assertEqual(projection["availability"], "available")
        self.assertEqual(projection["execution"]["state"], "success")
        self.assertEqual(projection["findings"], document["findings"])
        self.assertEqual(projection["freshness"]["state"], "fresh")
        self.assertEqual(projection["commit"], SOURCE_COMMIT)
        self.assertEqual(projection["links"], document["links"])
        self.assertEqual(projection["metrics"]["vulnerabilities"], 3)
        self.assertIn("Findings: blocked", self.renderer.render_producer_card("osv", projection))

    def test_failed_megalinter_execution_cannot_become_a_success_from_zero_findings(self) -> None:
        document = self.report("megalinter")
        document["execution"]["state"] = "failure"
        document["findings"] = {
            "state": "clear",
            "total": 0,
            "blocking": 0,
            "advisory": 0,
            "by_severity": {},
        }
        document["megalinter"] = {
            "profile": "holistic",
            "tools": {"active": 4, "passed": 4, "runner_failed": 1},
            "diagnostics": {"errors": 1, "warnings": 0},
        }
        self.write_report(document, "megalinter")
        projection = self.project("megalinter")
        self.assertEqual(projection["execution"]["state"], "failure")
        self.assertEqual(projection["findings"]["state"], "clear")
        self.assertEqual(projection["metrics"]["tools"]["runner_failed"], 1)
        self.assertIn(
            "Execution: failure", self.renderer.render_producer_card("megalinter", projection)
        )

    def test_absent_producers_remain_unknown(self) -> None:
        for producer in ("osv", "megalinter", "scorecard"):
            with self.subTest(producer=producer):
                projection = self.project(producer)
                self.assertEqual(projection["availability"], "unavailable")
                self.assertEqual(projection["execution"]["state"], "unknown")
                self.assertEqual(projection["freshness"]["state"], "unknown")
                self.assert_unknown_findings(projection)

    def test_successful_clear_report_is_accepted_only_with_matching_source(self) -> None:
        document = self.report()
        document["findings"] = {
            "state": "clear",
            "total": 0,
            "blocking": 0,
            "advisory": 0,
            "by_severity": {},
        }
        document["osv"]["scan"] = {"vulnerabilities": 0, "affected_packages": 0, "severity": {}}
        self.write_report(document)
        projection = self.project()
        self.assertEqual(projection["execution"]["state"], "success")
        self.assertEqual(projection["findings"]["state"], "clear")
        self.assertEqual(projection["metrics"]["vulnerabilities"], 0)
        document["commit"] = "2" * 40
        self.write_report(document)
        self.assert_unknown_findings(self.project())

    def test_stale_scorecard_api_does_not_invent_an_aggregate_score(self) -> None:
        document = self.report("scorecard")
        document["findings"] = {
            "state": "attention",
            "total": 3,
            "blocking": 0,
            "advisory": 3,
            "by_severity": {"high": 2, "low": 1},
        }
        document["scorecard"] = {
            "aggregate_score": None,
            "aggregate_source": "unavailable",
            "api_status": "stale",
            "checks_total": 3,
            "checks_needing_attention": 3,
            "weakest_checks": [],
        }
        self.write_report(document, "scorecard")
        projection = self.project("scorecard")
        self.assertIsNone(projection["metrics"]["aggregate_score"])
        self.assertEqual(projection["metrics"]["aggregate_source"], "unavailable")
        self.assertEqual(projection["metrics"]["api_status"], "stale")
        self.assertEqual(projection["findings"]["state"], "attention")

    def test_expiry_is_stale_at_the_exact_declared_boundary(self) -> None:
        self.write_report(self.report())
        for instant, expected in (
            (datetime(2026, 10, 1, 9, 59, 59, tzinfo=UTC), "fresh"),
            (datetime(2026, 10, 1, 10, tzinfo=UTC), "stale"),
            (datetime(2026, 10, 2, 10, tzinfo=UTC), "stale"),
        ):
            with self.subTest(instant=instant):
                projection = self.project(as_of=instant)
                self.assertEqual(projection["freshness"]["state"], expected)
                self.assertEqual(projection["findings"]["state"], "blocked")

    def test_incompatible_or_misattributed_reports_never_look_clear(self) -> None:
        for field, value in (
            ("schema", "unsupported.report/v2"),
            ("schema_version", 2),
            ("producer", "scorecard"),
            ("repository", "untrusted/repository"),
            ("commit", "2" * 40),
        ):
            with self.subTest(field=field):
                document = self.report()
                document[field] = value
                self.write_report(document)
                projection = self.project()
                self.assertEqual(projection["availability"], "invalid")
                self.assertEqual(projection["execution"]["state"], "failure")
                self.assertEqual(projection["freshness"]["state"], "unknown")
                self.assert_unknown_findings(projection)

    def test_malformed_input_diagnostics_do_not_echo_raw_payload(self) -> None:
        path = self.write_report(self.report())
        path.write_text('{"private": "DO-NOT-PUBLISH",', encoding="utf-8")
        projection = self.project()
        self.assertEqual(projection["availability"], "invalid")
        self.assert_unknown_findings(projection)
        self.assertNotIn("DO-NOT-PUBLISH", json.dumps(projection))

    def test_public_projection_omits_raw_payload_and_unsafe_urls(self) -> None:
        for unsafe_url in (
            "https://artifacts.example.invalid/archive?sig=DO-NOT-PUBLISH",
            "https://github.com/untrusted/repository/actions/runs/123",
            f"https://github.com/{REPOSITORY}/actions/runs/123?token=DO-NOT-PUBLISH",
            "http://127.0.0.1/DO-NOT-PUBLISH",
            "javascript:alert('DO-NOT-PUBLISH')",
        ):
            with self.subTest(url=unsafe_url):
                document = self.report()
                document["execution"]["message"] = "DO-NOT-PUBLISH raw scanner exception"
                document["osv"]["raw_log"] = "DO-NOT-PUBLISH"
                document["provenance"]["private_context"] = "DO-NOT-PUBLISH"
                document["links"] = dict.fromkeys(document["links"], unsafe_url)
                self.write_report(document)
                projection = self.project()
                self.assertEqual(projection["links"], {})
                public_output = json.dumps(projection) + self.renderer.render_producer_card(
                    "osv", projection
                )
                self.assertNotIn("DO-NOT-PUBLISH", public_output)
                self.assertNotIn(unsafe_url, public_output)
                self.assertEqual(projection["findings"]["state"], "blocked")

    def test_duplicate_projection_is_identical_and_does_not_rewrite_snapshots(self) -> None:
        path = self.write_report(self.report())
        original = path.read_bytes()
        first = self.project()
        second = self.project()
        self.assertEqual(first, second)
        self.assertEqual(path.read_bytes(), original)

    def test_committed_reports_keep_their_original_source_commit(self) -> None:
        # Read only the local fixture revision using fixed Git arguments.
        source_commit = subprocess.run(  # noqa: S603  # nosec B603, B607
            ["git", "-C", str(REPOSITORY_ROOT), "rev-parse", "HEAD"],  # noqa: S607
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        for producer in ("osv", "megalinter", "scorecard"):
            path = REPOSITORY_ROOT / ".reports" / producer / "summary.json"
            if not path.is_file():
                continue
            with self.subTest(producer=producer):
                original = path.read_bytes()
                document = json.loads(original)
                projection = self.renderer.load_report(
                    REPOSITORY_ROOT / ".reports", producer, REPOSITORY, source_commit, AS_OF
                )
                self.assertEqual(path.read_bytes(), original)
                if document["commit"] != source_commit:
                    self.assertEqual(projection["availability"], "invalid")
                    self.assert_unknown_findings(projection)


if __name__ == "__main__":
    unittest.main()
