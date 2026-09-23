# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
# Keep the repository's unittest exception assertions without a pytest dependency.
# ruff: noqa: PT027

"""Exercise Empathy's publication boundary without provider credentials or network."""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
from pathlib import Path
import shutil

# Fixed Git commands initialize only temporary fixture repositories.
import subprocess  # nosec B404
import tempfile
from typing import TYPE_CHECKING
import unittest
from unittest.mock import patch
from urllib.error import URLError

if TYPE_CHECKING:
    from collections.abc import Callable

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "publication", ROOT / "tools/repository_intelligence_publication.py"
)
assert SPEC is not None
assert SPEC.loader is not None
publication = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(publication)
REVISION = "a" * 40
RELAY = "b" * 40
SENTINEL = "SECRET"


class PublicationEvidenceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)

    def write(self, path: Path, value: object) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value), encoding="utf-8")

    def normalized_report(self) -> dict[str, object]:
        return {
            "schema": publication.REPORT_SCHEMA,
            "schema_version": 1,
            "producer": "osv",
            "repository": publication.REPOSITORY,
            "commit": REVISION,
            "execution": {"state": "failure", "message": "PRIVATE-MESSAGE"},
            "links": {"detail": "https://private.invalid/?token=SECRET"},
        }

    def site(self, root: Path, *, rollback: bool = False) -> Path:
        for route in publication.GARDEN_ROUTES + publication.INTELLIGENCE_ROUTES:
            entrypoint = route + "index.html" if not route or route.endswith("/") else route
            path = root / entrypoint
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("<!doctype html><title>" + route + "</title>", encoding="utf-8")
        identity = (
            {
                "schema": "egohygiene.relay.repository-intelligence-provenance/v1",
                "consumer": {"repository": publication.REPOSITORY, "source_commit": REVISION},
                "generator": {"source_commit": RELAY},
            }
            if rollback
            else {
                "schema": publication.MANIFEST_SCHEMA,
                "consumer": {"repository": publication.REPOSITORY, "revision": REVISION},
                "generator": {"revision": RELAY},
            }
        )
        filename = "provenance.json" if rollback else "build-manifest.json"
        self.write(root / "intelligence" / filename, identity)
        return root

    def fetch_from(self, root: Path) -> Callable[[str], bytes]:
        def fetch(route: str) -> bytes:
            entrypoint = route + "index.html" if not route or route.endswith("/") else route
            return (root / entrypoint).read_bytes()

        return fetch

    def test_json_rejects_nested_duplicate_keys(self) -> None:
        for data in (b'{"state":"failure","state":"success"}', b'{"nested":{"key":1,"key":2}}'):
            with self.subTest(data=data), self.assertRaises(publication.DuplicateKeyError):
                publication.parse_json(data)

    def test_json_rejects_nonfinite_oversized_nonobject_and_invalid_inputs(self) -> None:
        for data in (b'{"x":NaN}', b"[]", b"\xff", b"{" + b" " * publication.MAX_JSON_BYTES):
            with self.subTest(prefix=data[:10]), self.assertRaises(publication.PublicationError):
                publication.parse_json(data)

    def test_canonicalization_changes_only_baseline_file_order(self) -> None:
        path = self.root / "baseline.json"
        source = {
            "schema": publication.BASELINE_SCHEMA,
            "schema_version": 1,
            "consumer": {"revision": REVISION},
            "routes": [{"route": "/"}],
            "files": [
                {"path": "a/index.html", "sha256": "one"},
                {"path": "a.html", "sha256": "two"},
            ],
        }
        self.write(path, source)
        publication.canonicalize_baseline(path)
        result = publication.parse_json(path.read_bytes())
        self.assertEqual(result["files"], list(reversed(source["files"])))
        self.assertEqual(
            {k: v for k, v in result.items() if k != "files"},
            {k: v for k, v in source.items() if k != "files"},
        )

    def test_canonicalization_rejects_unknown_schema_and_duplicate_paths(self) -> None:
        path = self.root / "baseline.json"
        for schema, files in (
            ("future/v2", [{"path": "a"}]),
            (publication.BASELINE_SCHEMA, [{"path": "a"}, {"path": "a"}]),
        ):
            self.write(path, {"schema": schema, "schema_version": 1, "files": files})
            with self.assertRaises(publication.PublicationError):
                publication.canonicalize_baseline(path)

    def test_report_missing_invalid_and_incompatible_remain_unknown(self) -> None:
        path = self.root / "summary.json"
        self.assertEqual(publication.report_evidence(path, "osv", REVISION)["state"], "missing")
        path.write_bytes(b'{"secret": invalid')
        result = publication.report_evidence(path, "osv", REVISION)
        self.assertEqual((result["state"], result["execution"]), ("invalid", "unknown"))
        self.assertEqual(result["sha256"], publication.sha256(path.read_bytes()))
        self.write(path, {"schema": "SECRET-SCHEMA"})
        result = publication.report_evidence(path, "osv", REVISION)
        self.assertEqual((result["state"], result["execution"]), ("incompatible", "unknown"))
        self.assertNotIn("SECRET", json.dumps(result))

    def test_duplicate_report_keys_fail_before_build(self) -> None:
        path = self.root / "summary.json"
        path.write_bytes(b'{"execution":{"state":"failure","state":"success"}}')
        with self.assertRaises(publication.DuplicateKeyError):
            publication.report_evidence(path, "osv", REVISION)

    def test_report_failed_execution_and_revision_mismatch_are_preserved(self) -> None:
        path = self.root / "summary.json"
        self.write(path, self.normalized_report())
        result = publication.report_evidence(path, "osv", RELAY)
        self.assertEqual(result["execution"], "failure")
        self.assertFalse(result["matches_consumer_revision"])
        self.assertEqual(result["source_revision"], REVISION)
        self.assertNotIn("PRIVATE", json.dumps(result))
        self.assertNotIn("SECRET", json.dumps(result))
        self.assertNotIn("invalid", json.dumps(result))

    def test_report_freshness_audit_normalizes_valid_instants_and_omits_arbitrary_values(
        self,
    ) -> None:
        path = self.root / "summary.json"
        report = self.normalized_report()
        report["generated_at"] = "2026-09-23T12:00:00+02:00"
        report["freshness"] = {"expires_at": "2026-09-30T10:00:00Z"}
        self.write(path, report)
        evidence = publication.report_evidence(path, "osv", REVISION)
        self.assertEqual(evidence["generated_at"], "2026-09-23T10:00:00Z")
        self.assertEqual(evidence["expires_at"], "2026-09-30T10:00:00Z")
        malformed: tuple[object, ...] = (
            "SECRET",
            "2026-02-30T10:00:00Z",
            "2026-09-23T10:00:00",
            None,
            [],
        )
        for value in malformed:
            report["generated_at"] = value
            report["freshness"] = {"expires_at": value}
            self.write(path, report)
            evidence = publication.report_evidence(path, "osv", REVISION)
            self.assertIsNone(evidence["generated_at"])
            self.assertIsNone(evidence["expires_at"])
            self.assertNotIn("SECRET", json.dumps(evidence))

    def test_adversarial_nested_metadata_types_cannot_claim_a_trusted_refresh(self) -> None:
        malformed: tuple[dict[str, object], ...] = (
            {"repository": {"full_name": []}},
            {"head_repository": None},
            {"name": {}},
            {"event": []},
            {"head_sha": []},
        )
        for change in malformed:
            with self.subTest(change=change):
                metadata = publication.workflow_metadata(self.event(**change))
                self.assertFalse(metadata["triggering_producer"]["trusted_refresh_candidate"])
        # Synthetic sentinel proves malformed metadata cannot leak into public evidence.
        metadata = publication.workflow_metadata(self.event(conclusion={SENTINEL: True}))
        self.assertEqual(metadata["triggering_producer"]["conclusion"], "unknown")
        self.assertNotIn("SECRET", json.dumps(metadata))

    def test_report_unknown_execution_is_never_green(self) -> None:
        path = self.root / "summary.json"
        report = self.normalized_report()
        report["execution"] = {"state": "SECRET"}
        self.write(path, report)
        self.assertEqual(publication.report_evidence(path, "osv", REVISION)["execution"], "unknown")

    def event(self, **overrides: object) -> dict[str, str]:
        run = {
            "id": 123,
            "run_attempt": 2,
            "name": "MegaLinter",
            "event": "push",
            "conclusion": "failure",
            "status": "completed",
            "head_branch": "main",
            "head_sha": REVISION,
            "repository": {"full_name": publication.REPOSITORY},
            "head_repository": {"full_name": publication.REPOSITORY},
            "logs_url": "https://private.invalid/SECRET",
            "actor": {"login": "PRIVATE"},
        }
        run.update(overrides)
        path = self.root / "event.json"
        self.write(path, {"workflow_run": run})
        return {
            "GITHUB_EVENT_NAME": "workflow_run",
            "GITHUB_EVENT_PATH": str(path),
            "GITHUB_RUN_ID": "456",
            "GITHUB_RUN_ATTEMPT": "1",
            # Synthetic sentinel only: no requests or authentication are performed.
            "GITHUB_TOKEN": SENTINEL,
        }

    def test_non_successful_producer_refresh_metadata_stays_useful_and_sanitized(self) -> None:
        for conclusion in ("failure", "cancelled", "timed_out", "neutral", "success"):
            result = publication.workflow_metadata(self.event(conclusion=conclusion))
            producer = result["triggering_producer"]
            self.assertTrue(producer["trusted_refresh_candidate"])
            self.assertEqual(producer["conclusion"], conclusion)
            self.assertNotIn("SECRET", json.dumps(result))
            self.assertNotIn("PRIVATE", json.dumps(result))

    def test_pr_fork_unknown_workflow_and_nondefault_producer_are_not_trusted(self) -> None:
        for change in (
            {"event": "pull_request"},
            {"event": "pull_request_target"},
            {"head_repository": {"full_name": "attacker/empathy"}},
            {"head_branch": "feature"},
            {"name": "SECRET"},
            {"status": "queued"},
            {"head_sha": "SECRET"},
            {"id": True},
        ):
            with self.subTest(change=change):
                result = publication.workflow_metadata(self.event(**change))
                self.assertFalse(result["triggering_producer"]["trusted_refresh_candidate"])
                self.assertNotIn("SECRET", json.dumps(result))

    def test_workflow_metadata_rejects_duplicate_event_keys(self) -> None:
        environment = self.event()
        Path(environment["GITHUB_EVENT_PATH"]).write_bytes(b'{"workflow_run":{},"workflow_run":{}}')
        with self.assertRaises(publication.DuplicateKeyError):
            publication.workflow_metadata(environment)

    def test_input_evidence_binds_exact_git_tree_and_quartz_bytes(self) -> None:
        profile = self.root / "mindgarden/profiles/quartz/profile.yaml"
        profile.parent.mkdir(parents=True)
        profile.write_text("quartz_commit: " + RELAY + "\n", encoding="utf-8")
        configuration = profile.with_name("quartz.config.yaml")
        configuration.write_text("configuration: {}\n", encoding="utf-8")
        for arguments in (
            ["init", "-q"],
            ["add", "."],
            [
                "-c",
                "user.name=Fixture",
                "-c",
                "user.email=fixture@example.invalid",
                "commit",
                "-qm",
                "Fixture",
            ],
        ):
            # Arguments above create only the local temporary Git fixture.
            subprocess.run(  # noqa: S603  # nosec B603, B607
                ["git", "-C", str(self.root), *arguments],  # noqa: S607
                check=True,
                capture_output=True,
            )
        result = publication.collect_input_evidence(self.root, {})
        self.assertEqual(result["consumer"]["revision"], publication._git(self.root, "HEAD"))
        self.assertEqual(result["consumer"]["tree"], publication._git(self.root, "HEAD^{tree}"))
        self.assertEqual(result["quartz"]["revision"], RELAY)
        self.assertEqual(
            result["quartz"]["profile_sha256"], publication.sha256(profile.read_bytes())
        )
        self.assertEqual({report["state"] for report in result["reports"]}, {"missing"})
        self.assertNotIn(str(self.root), json.dumps(result))

    def test_foreign_repository_cannot_claim_empathy_inputs(self) -> None:
        with self.assertRaises(publication.PublicationError):
            publication.collect_input_evidence(self.root, {"GITHUB_REPOSITORY": "attacker/empathy"})

    def test_duplicate_composition_records_all_bytes_in_same_checkout_scope(self) -> None:
        left = self.site(self.root / "first")
        right = self.root / "second"
        shutil.copytree(left, right)
        result = publication.compare_sites(left, right)
        self.assertTrue(result["identical"])
        self.assertEqual(result["file_count"], 18)
        self.assertIn("same Quartz", result["scope"])
        (right / "dashboard.html").write_text("changed", encoding="utf-8")
        with self.assertRaises(publication.PublicationError):
            publication.compare_sites(left, right)

    def test_duplicate_composition_detects_extra_files_and_ambiguous_manifest(self) -> None:
        left = self.site(self.root / "first")
        right = self.root / "second"
        shutil.copytree(left, right)
        (right / "extra.txt").write_text("extra", encoding="utf-8")
        with self.assertRaises(publication.PublicationError):
            publication.compare_sites(left, right)
        (right / "extra.txt").unlink()
        for site in (left, right):
            (site / "intelligence/build-manifest.json").write_bytes(b'{"schema":1,"schema":2}')
        with self.assertRaises(publication.DuplicateKeyError):
            publication.compare_sites(left, right)

    def test_symlinks_and_run_evidence_inside_site_are_rejected(self) -> None:
        site = self.site(self.root / "site")
        (site / "linked").symlink_to(site / "index.html")
        with self.assertRaises(publication.PublicationError):
            publication.site_inventory(site)
        with self.assertRaises(publication.PublicationError):
            publication.write_json(site / "receipt.json", {"run_id": 1}, sites=(site,))
        self.assertFalse((site / "receipt.json").exists())

    def test_live_current_and_rollback_verify_every_route_and_exact_identity(self) -> None:
        for mode in ("current", "rollback"):
            site = self.site(self.root / mode, rollback=mode == "rollback")
            with patch.object(
                publication, "fetch_public", side_effect=self.fetch_from(site)
            ) as fetch:
                result = publication.verify_live(site, REVISION, RELAY, mode, attempts=1, delay=0)
            self.assertEqual(len(result["routes"]), 17)
            self.assertEqual(fetch.call_count, 19)
            self.assertEqual(result["consumer_revision"], REVISION)
            self.assertNotIn(str(self.root), json.dumps(result))

    def test_live_stale_or_mixed_deployment_fails_even_when_http_is_successful(self) -> None:
        site = self.site(self.root / "site")
        read = self.fetch_from(site)
        for changed in ("intelligence/build-manifest.json", "dashboard.html", "intelligence/now/"):

            def fetch(route: str, changed_route: str = changed) -> bytes:
                return b"{}" if route == changed_route else read(route)

            with (
                self.subTest(changed=changed),
                patch.object(publication, "fetch_public", side_effect=fetch),
                self.assertRaises(publication.PublicationError),
            ):
                publication.verify_live(site, REVISION, RELAY, "current", attempts=1)

    def test_live_retries_are_bounded_and_transient_failure_can_recover(self) -> None:
        site = self.site(self.root / "site")
        read = self.fetch_from(site)
        failures = [True]

        def fetch(route: str) -> bytes:
            if failures:
                failures.pop()
                message = "SECRET exception"
                raise URLError(message)
            return read(route)

        with (
            patch.object(publication, "fetch_public", side_effect=fetch),
            patch.object(publication.time, "sleep") as sleep,
        ):
            result = publication.verify_live(site, REVISION, RELAY, "current", attempts=2, delay=10)
        self.assertEqual(result["attempt"], 2)
        sleep.assert_called_once_with(10)
        with self.assertRaises(publication.PublicationError):
            publication.verify_live(site, REVISION, RELAY, "current", attempts=13)

    def test_live_checks_expected_revision_before_any_request(self) -> None:
        site = self.site(self.root / "site")
        with patch.object(publication, "fetch_public") as fetch:
            with self.assertRaises(publication.PublicationError):
                publication.verify_live(site, "c" * 40, RELAY, "current", attempts=1)
            fetch.assert_not_called()

    def test_public_probe_rejects_untrusted_urls_and_redirects(self) -> None:
        with patch.object(publication, "build_opener") as opener:
            for route in (
                "https://private.invalid/SECRET",
                "//127.0.0.1",
                "../private",
                "intelligence/?token=SECRET",
            ):
                with self.subTest(route=route), self.assertRaises(publication.PublicationError):
                    publication.fetch_public(route)
            opener.assert_not_called()
        self.assertIsNone(
            publication.NoRedirects().redirect_request(None, None, 302, "", {}, "http://127.0.0.1/")
        )

    def test_public_probe_requires_bounded_bytes(self) -> None:
        with patch.object(publication, "build_opener") as opener:
            response = opener.return_value.open.return_value.__enter__.return_value
            response.status = 200
            response.geturl.return_value = publication.SITE_URL
            for payload in ("PRIVATE response", b"x" * (publication.MAX_FILE_BYTES + 1)):
                response.read.return_value = payload
                with self.subTest(kind=type(payload).__name__):
                    with self.assertRaises(publication.PublicationError) as failure:
                        publication.fetch_public("")
                    self.assertNotIn("PRIVATE", str(failure.exception))
            response.read.assert_called_with(publication.MAX_FILE_BYTES + 1)

    def test_failures_are_closed_public_safe_and_thirty_day(self) -> None:
        codes = set()
        for stage in publication.FAILURES:
            result = publication.failure_report(
                # Synthetic value must never be copied to a public failure report.
                stage,
                {"GITHUB_RUN_ID": "123", "GITHUB_RUN_ATTEMPT": "2", SENTINEL: "token"},
            )
            self.assertEqual(result["retention_days"], 30)
            self.assertNotIn("token", json.dumps(result))
            codes.add(result["code"])
        self.assertEqual(len(codes), len(publication.FAILURES))

    def test_cli_never_echoes_private_paths_or_argument_values(self) -> None:
        for arguments in (
            ["failure-report", "--stage", "SECRET", "--output", "/private/SECRET"],
            ["canonicalize-baseline", "--baseline", "/private/SECRET"],
            ["verify-live", "--attempts", "SECRET"],
        ):
            output = io.StringIO()
            with contextlib.redirect_stderr(output):
                self.assertEqual(publication.main(arguments), 1)
            self.assertNotIn("SECRET", output.getvalue())
            self.assertNotIn("Traceback", output.getvalue())


if __name__ == "__main__":
    unittest.main()
