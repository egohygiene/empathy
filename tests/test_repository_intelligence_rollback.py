# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Consumer rollback invariants, including historical Quartz date variance."""

from __future__ import annotations

from contextlib import redirect_stderr, redirect_stdout
from dataclasses import replace
import hashlib
from io import StringIO
import json
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from tools import verify_repository_intelligence_rollback as rollback


def canonical_digest(records: list[dict]) -> str:
    """Compute fixture expectations independently of the production helper."""
    text = json.dumps(records, separators=(",", ":"), sort_keys=True) + "\n"
    return "sha256:" + hashlib.sha256(text.encode()).hexdigest()


class RepositoryIntelligenceRollbackTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.site = self.root / "site"
        (self.site / "intelligence").mkdir(parents=True)
        self.provenance = {
            "consumer": {
                "repository": rollback.REPOSITORY,
                "source_commit": rollback.SOURCE_COMMIT,
                "visibility": "public",
            },
            "generator": {
                "immutable": True,
                "name": "egohygiene/relay/actions/repository-intelligence",
                "repository": "egohygiene/relay",
                "source_commit": rollback.RELAY_COMMIT,
                "source_ref": rollback.RELAY_COMMIT,
                "version": "1.4.0",
            },
            "projection": {
                "classification": "public-safe",
                "deployment_authority": "consumer",
                "route": "/intelligence/",
            },
            "schema": "egohygiene.relay.repository-intelligence-provenance/v1",
            "schema_version": 1,
            "generated_at": "2026-09-23T08:56:50Z",
            "timestamp_source": "consumer-source-commit",
        }
        self.provenance_path = self.site / "intelligence" / "provenance.json"
        self.provenance_path.write_text(json.dumps(self.provenance), encoding="utf8")
        for relative in ("index.html", "dashboard.html", "intelligence/index.html"):
            (self.site / relative).write_text(
                "<html>Reviewed public fixture</html>", encoding="utf8"
            )
        (self.site / "index.xml").write_text(
            '<rss version="2.0"><channel><item>'
            "<link>https://egohygiene.github.io/empathy/tags/empathy</link>"
            "<pubDate>Wed, 23 Sep 2026 08:57:41 GMT</pubDate>"
            "<description>Reviewed fixture</description></item></channel></rss>",
            encoding="utf8",
        )
        (self.site / "sitemap.xml").write_text(
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url>'
            "<loc>https://egohygiene.github.io/empathy/tags/empathy</loc>"
            "<lastmod>2026-09-23T08:57:41.288Z</lastmod></url></urlset>",
            encoding="utf8",
        )
        records = self.fixture_inventory(self.site)
        self.baseline = rollback.Baseline(
            paths=canonical_digest([{"path": record["path"]} for record in records]),
            intelligence=canonical_digest(self.fixture_inventory(self.site / "intelligence")),
            stable_quartz=canonical_digest(
                [record for record in records if record["path"] in {"dashboard.html", "index.html"}]
            ),
            rss=rollback.normalized_feed_digest(self.site / "index.xml"),
            sitemap=rollback.normalized_feed_digest(self.site / "sitemap.xml"),
        )

    @staticmethod
    def fixture_inventory(root: Path) -> list[dict]:
        records = []
        for path in sorted(root.rglob("*")):
            if path.is_file():
                data = path.read_bytes()
                records.append(
                    {
                        "path": path.relative_to(root).as_posix(),
                        "bytes": len(data),
                        "sha256": "sha256:" + hashlib.sha256(data).hexdigest(),
                    }
                )
        return records

    def verify(self) -> dict:
        return rollback.verify_site(self.site, baseline=self.baseline)

    def test_verified_report_keeps_new_composition_separate_from_historical_deployment(
        self,
    ) -> None:
        report = self.verify()
        self.assertEqual(report["status"], "verified")
        self.assertEqual(
            report["known_good"]["original_composed_digest"], rollback.ORIGINAL_SITE_DIGEST
        )
        self.assertEqual(
            report["verification"]["composed_digest"],
            canonical_digest(self.fixture_inventory(self.site)),
        )
        self.assertFalse(report["verification"]["full_site_equality_claimed"])
        self.assertNotIn(str(self.root), json.dumps(report))
        self.assertNotIn("Reviewed public fixture", json.dumps(report))

    def test_only_synthetic_tag_dates_may_change(self) -> None:
        before = self.verify()["verification"]["composed_digest"]
        for name in rollback.FEEDS:
            path = self.site / name
            path.write_text(path.read_text().replace("08:57:41", "12:30:15"), encoding="utf8")
        after = self.verify()["verification"]["composed_digest"]
        self.assertNotEqual(before, after)
        path = self.site / "index.xml"
        path.write_text(
            path.read_text().replace("Reviewed fixture", "Invented fixture"), encoding="utf8"
        )
        with self.assertRaisesRegex(rollback.RollbackError, "ERB-005"):
            self.verify()

    def test_provenance_cannot_claim_new_source_or_generator(self) -> None:
        for section, key in (("consumer", "source_commit"), ("generator", "source_commit")):
            with self.subTest(section=section):
                changed = json.loads(json.dumps(self.provenance))
                changed[section][key] = "f" * 40
                self.provenance_path.write_text(json.dumps(changed), encoding="utf8")
                with self.assertRaisesRegex(rollback.RollbackError, "ERB-004"):
                    self.verify()

    def test_changed_intelligence_and_quartz_bytes_fail(self) -> None:
        for relative in ("intelligence/index.html", "dashboard.html"):
            with self.subTest(relative=relative):
                path = self.site / relative
                original = path.read_bytes()
                path.write_bytes(original + b" changed")
                with self.assertRaisesRegex(rollback.RollbackError, "ERB-008"):
                    self.verify()
                path.write_bytes(original)

    def test_missing_routes_and_unexpected_public_receipts_fail(self) -> None:
        path = self.site / "dashboard.html"
        original = path.read_bytes()
        path.unlink()
        with self.assertRaisesRegex(rollback.RollbackError, "ERB-007"):
            self.verify()
        path.write_bytes(original)
        (self.site / "deployment-receipt.json").write_text("{}", encoding="utf8")
        with self.assertRaisesRegex(rollback.RollbackError, "ERB-007"):
            self.verify()

    def test_symlinks_and_empty_sites_fail(self) -> None:
        (self.site / "leak").symlink_to(self.provenance_path)
        with self.assertRaisesRegex(rollback.RollbackError, "ERB-001"):
            self.verify()
        empty = self.root / "empty"
        empty.mkdir()
        with self.assertRaisesRegex(rollback.RollbackError, "ERB-001"):
            rollback.inventory(empty)

    def test_duplicate_keys_nonfinite_numbers_and_malformed_json_fail(self) -> None:
        for content in ('{"private-secret": 1, "private-secret": 2}', '{"value": NaN}', "{broken"):
            with self.subTest(content=content):
                self.provenance_path.write_text(content, encoding="utf8")
                with self.assertRaisesRegex(rollback.RollbackError, "ERB-003"):
                    self.verify()

    def test_xml_entities_and_invalid_runtime_dates_fail(self) -> None:
        path = self.site / "sitemap.xml"
        original = path.read_text()
        for content in (
            '<!DOCTYPE urlset [<!ENTITY secret "private-secret">]>' + original,
            original.replace("2026-09-23T08:57:41.288Z", "private-secret"),
        ):
            with self.subTest(content=content):
                path.write_text(content, encoding="utf8")
                with self.assertRaisesRegex(rollback.RollbackError, "ERB-005"):
                    self.verify()

    def test_wrong_checkout_revision_or_tree_fails(self) -> None:
        for results in (
            [subprocess.CompletedProcess([], 0, "f" * 40)],
            [
                subprocess.CompletedProcess([], 0, rollback.SOURCE_COMMIT),
                subprocess.CompletedProcess([], 0, "f" * 40),
            ],
        ):
            with patch.object(rollback.subprocess, "run", side_effect=results):
                with self.assertRaisesRegex(rollback.RollbackError, "ERB-006"):
                    rollback.verify_source(self.root)

    def test_public_output_and_diagnostics_cannot_leak_paths_or_payloads(self) -> None:
        self.provenance_path.write_text('{"private-secret":', encoding="utf8")
        for output in (self.site / "receipt.json", self.root / "report.json"):
            stderr = StringIO()
            with redirect_stderr(stderr), redirect_stdout(StringIO()):
                result = rollback.main(["--site-root", str(self.site), "--output", str(output)])
            self.assertEqual(result, 1)
            self.assertRegex(stderr.getvalue(), r"^Rollback verification failed: ERB-\d{3}\n$")
            self.assertNotIn(str(self.root), stderr.getvalue())
            self.assertNotIn("private-secret", stderr.getvalue())
            self.assertFalse(output.exists())

    def test_production_baseline_is_not_a_command_line_option(self) -> None:
        changed = replace(self.baseline, intelligence="sha256:" + "0" * 64)
        with self.assertRaisesRegex(rollback.RollbackError, "ERB-008"):
            rollback.verify_site(self.site, baseline=changed)
        self.assertEqual(rollback.RELAY_COMMIT, "b71b090406a3a9e4cd9f107e9d14a623bbecb127")
        self.assertEqual(rollback.QUARTZ_COMMIT, "075afd3f712da0088a07f5284a7b3aba37dd61b6")


if __name__ == "__main__":
    unittest.main()
