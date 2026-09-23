# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Consumer paths and trust fixtures against the exact reviewed Relay owner code.

Set RELAY_CHECKOUT to a clean checkout at the workflow's immutable pin. No Relay
implementation is vendored here; local runs without that checkout skip these
owner-integration fixtures, and the publication policy workflow supplies it.
"""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
RELAY_REVISION = "9a6315978766c336566b9fa7139b800fa8789ba5"
CONSUMER_REVISION = "a" * 40
ROLLBACK_REVISION = "254185272ab27b6858b8b0393af6549c205c9a8d"
SOURCE_EPOCH = 1_800_000_000
REPOSITORY = "egohygiene/empathy"
OWNER_PATHS = (
    "actions/repository-intelligence/scripts/create_repository_intelligence_build_manifest.py",
    "actions/repository-intelligence-deployment-provenance/scripts/repository_intelligence_deployment_provenance.py",
)


def checked_relay_root(root: Path) -> Path:
    """Reject mutable, wrong-revision or edited owner code before importing it."""
    revision = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True, text=True, check=True
    ).stdout.strip()
    if revision != RELAY_REVISION:
        raise ValueError("The owner fixtures require the reviewed immutable Relay revision.")
    subprocess.run(
        ["git", "-C", str(root), "diff", "--exit-code", "HEAD", "--", *OWNER_PATHS],
        capture_output=True,
        check=True,
    )
    return root


def load_module(name: str, path: Path):
    specification = importlib.util.spec_from_file_location(name, path)
    assert specification is not None and specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


class OwnerCheckoutTrustTests(unittest.TestCase):
    def test_wrong_owner_revision_is_rejected_before_loading_any_code(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for arguments in (
                ["init", "-q"],
                [
                    "-c",
                    "user.name=Fixture",
                    "-c",
                    "user.email=fixture@example.invalid",
                    "commit",
                    "--allow-empty",
                    "-qm",
                    "Unreviewed owner fixture",
                ],
            ):
                subprocess.run(
                    ["git", "-C", str(root), *arguments], check=True, capture_output=True
                )
            with self.assertRaisesRegex(ValueError, "reviewed immutable"):
                checked_relay_root(root)


@unittest.skipUnless(
    os.environ.get("RELAY_CHECKOUT"), "Set RELAY_CHECKOUT to the reviewed Relay checkout."
)
class EmpathyProvenanceOwnerIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        owner = checked_relay_root(Path(os.environ["RELAY_CHECKOUT"]))
        cls.manifest_owner = load_module("empathy_manifest_owner_fixture", owner / OWNER_PATHS[0])
        cls.provenance_owner = load_module(
            "empathy_provenance_owner_fixture", owner / OWNER_PATHS[1]
        )
        cls.consumer = load_module(
            "empathy_publication_fixture",
            REPOSITORY_ROOT / "tools/repository_intelligence_publication.py",
        )

    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.workspace = Path(temporary.name)
        self.site = self.workspace / ".cache/mindgarden/site"
        self.evidence = self.workspace / ".cache/mindgarden/publication"
        for route in self.consumer.GARDEN_ROUTES:
            path = self.site / (route + "index.html" if not route or route.endswith("/") else route)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("Reviewed public Quartz fixture: " + route, encoding="utf-8")
        static = self.site / "static/contentIndex.json"
        static.parent.mkdir()
        static.write_text('{"public":true}\n', encoding="utf-8")
        (self.site / ".nojekyll").touch()
        self.baseline = self.evidence / "consumer-route-baseline.json"
        self.verification = self.evidence / "composition-verification.json"
        self.receipt = self.evidence / "deployment-receipt.json"
        self.invoke("capture-baseline")
        self.consumer.canonicalize_baseline(self.baseline)
        self.intelligence = self.site / "intelligence"
        for route in self.consumer.INTELLIGENCE_ROUTES:
            path = self.site / route / "index.html"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("Public Repository Intelligence fixture: " + route, encoding="utf-8")
        (self.intelligence / "site.css").write_text("body { color: black; }\n", encoding="utf-8")
        self.manifest_path = self.intelligence / "build-manifest.json"
        manifest = self.manifest_owner.build_manifest(
            output_root=self.intelligence,
            repository=REPOSITORY,
            consumer_revision=CONSUMER_REVISION,
            generator_revision=RELAY_REVISION,
            generator_version="1.6.0",
            source_epoch=SOURCE_EPOCH,
        )
        self.manifest_owner.write_json(self.manifest_path, manifest)

    def arguments(self, operation: str, **overrides: str) -> list[str]:
        values = {
            "operation": operation,
            "workspace": str(self.workspace),
            "site-directory": ".cache/mindgarden/site",
            "intelligence-directory": ".cache/mindgarden/site/intelligence",
            "baseline-path": ".cache/mindgarden/publication/consumer-route-baseline.json",
            "verification-path": ".cache/mindgarden/publication/composition-verification.json",
            "receipt-path": ".cache/mindgarden/publication/deployment-receipt.json",
            "consumer-repository": REPOSITORY,
            "consumer-revision": CONSUMER_REVISION,
            "relay-revision": RELAY_REVISION,
            "verified-epoch": str(SOURCE_EPOCH + 60),
            "maximum-source-age-seconds": "120",
            "required-routes": json.dumps(
                ["/", "/projects/", *["/" + route for route in self.consumer.INTELLIGENCE_ROUTES]]
            ),
            "aliases": "[]",
            "workflow-run-id": "42",
            "workflow-run-attempt": "2",
            "deployment-environment": "github-pages",
            "deployment-url": self.consumer.SITE_URL,
            "deployment-conclusion": "success",
            "recorded-at": "2027-01-15T08:01:00Z",
            "rollback-revision": ROLLBACK_REVISION,
            "rollback-site-digest": "sha256:" + "4" * 64,
            "rollback-url": self.consumer.SITE_URL,
        }
        values.update(overrides)
        return [part for key, value in values.items() for part in ("--" + key, value)]

    def invoke(self, operation: str, **overrides: str) -> int:
        with contextlib.redirect_stdout(io.StringIO()):
            return self.provenance_owner.main(self.arguments(operation, **overrides))

    def rewrite_manifest(self, field: str, value: object) -> None:
        manifest = json.loads(self.manifest_path.read_bytes())
        manifest[field] = value
        self.manifest_owner.write_json(self.manifest_path, manifest)

    def test_real_owner_verifies_consumer_paths_and_separate_receipt(self) -> None:
        before = self.consumer.site_inventory(self.site)
        self.assertEqual(self.invoke("verify-composition"), 0)
        self.assertEqual(self.invoke("record-receipt"), 0)
        self.assertEqual(self.invoke("verify-receipt"), 0)
        self.assertEqual(self.consumer.site_inventory(self.site), before)
        receipt = json.loads(self.receipt.read_bytes())
        verification = json.loads(self.verification.read_bytes())
        self.assertEqual(
            receipt["consumer"], {"repository": REPOSITORY, "revision": CONSUMER_REVISION}
        )
        self.assertEqual(receipt["build_manifest"], verification["build_manifest"])
        self.assertEqual(receipt["workflow"], {"run_id": 42, "run_attempt": 2})
        self.assertEqual(receipt["deployment"]["environment"], "github-pages")
        self.assertEqual(receipt["composition"]["preserved_consumer_files"]["file_count"], 7)
        self.assertEqual(receipt["rollback"]["consumer_revision"], ROLLBACK_REVISION)
        self.assertNotIn(str(self.workspace), self.receipt.read_text(encoding="utf-8"))

    def test_repeated_owner_manifest_is_identical_before_and_after_receipt(self) -> None:
        first = self.manifest_path.read_bytes()
        self.invoke("record-receipt")
        generated = self.manifest_owner.build_manifest(
            output_root=self.intelligence,
            repository=REPOSITORY,
            consumer_revision=CONSUMER_REVISION,
            generator_revision=RELAY_REVISION,
            generator_version="1.6.0",
            source_epoch=SOURCE_EPOCH,
        )
        self.manifest_owner.write_json(self.manifest_path, generated)
        self.assertEqual(self.manifest_path.read_bytes(), first)
        self.assertEqual(self.invoke("verify-receipt"), 0)

    def test_consumer_and_relay_revision_drift_fail(self) -> None:
        for argument in ("consumer-revision", "relay-revision"):
            with (
                self.subTest(argument=argument),
                self.assertRaisesRegex(SystemExit, "revision drift"),
            ):
                self.invoke("verify-composition", **{argument: "f" * 40})

    def test_payload_tamper_fails(self) -> None:
        (self.intelligence / "site.css").write_text("unreviewed", encoding="utf-8")
        with self.assertRaisesRegex(SystemExit, "bundle digest mismatch"):
            self.invoke("verify-composition")

    def test_removed_generated_route_fails(self) -> None:
        (self.intelligence / "health/index.html").unlink()
        with self.assertRaisesRegex(SystemExit, "bundle digest mismatch"):
            self.invoke("verify-composition")

    def test_missing_required_consumer_route_fails(self) -> None:
        with self.assertRaisesRegex(SystemExit, "missing required routes"):
            self.invoke("verify-composition", **{"required-routes": '["/garden-missing/"]'})

    def test_quartz_html_and_nonroute_asset_cannot_be_clobbered(self) -> None:
        for relative in ("dashboard.html", "static/contentIndex.json"):
            path = self.site / relative
            before = path.read_bytes()
            path.write_text("PRIVATE unreviewed replacement", encoding="utf-8")
            with (
                self.subTest(path=relative),
                self.assertRaisesRegex(SystemExit, "clobbered") as failure,
            ):
                self.invoke("verify-composition")
            self.assertNotIn("PRIVATE", str(failure.exception))
            path.write_bytes(before)

    def test_freshness_rejects_stale_and_future_source_epochs(self) -> None:
        for verified in (SOURCE_EPOCH - 1, SOURCE_EPOCH + 121):
            with self.subTest(epoch=verified), self.assertRaisesRegex(SystemExit, "stale"):
                self.invoke("verify-composition", **{"verified-epoch": str(verified)})

    def test_incompatible_manifest_contract_fails(self) -> None:
        self.rewrite_manifest("schema_version", 2)
        with self.assertRaisesRegex(SystemExit, "unsupported build manifest version"):
            self.invoke("verify-composition")

    def test_ambiguous_manifest_json_fails(self) -> None:
        source = self.manifest_path.read_bytes()
        self.manifest_path.write_bytes(
            source.replace(b'"schema_version": 1', b'"schema_version": 1, "schema_version": 1')
        )
        with self.assertRaisesRegex(SystemExit, "duplicate members"):
            self.invoke("verify-composition")

    def test_receipt_cannot_be_written_inside_site(self) -> None:
        with self.assertRaisesRegex(SystemExit, "outside"):
            self.invoke("record-receipt", **{"receipt-path": ".cache/mindgarden/site/receipt.json"})
        self.assertFalse((self.site / "receipt.json").exists())

    def test_incomplete_receipt_cannot_verify(self) -> None:
        self.invoke("record-receipt")
        receipt = json.loads(self.receipt.read_bytes())
        receipt.pop("rollback")
        self.provenance_owner.write_json(self.receipt, receipt)
        with self.assertRaisesRegex(SystemExit, "incomplete or inconsistent"):
            self.invoke("verify-receipt")

    def test_failed_deployment_is_recorded_without_turning_green(self) -> None:
        self.assertEqual(self.invoke("record-receipt", **{"deployment-conclusion": "failure"}), 0)
        receipt = json.loads(self.receipt.read_bytes())
        self.assertEqual(receipt["deployment"]["conclusion"], "failure")
        with self.assertRaisesRegex(SystemExit, "incomplete or inconsistent"):
            self.invoke("verify-receipt")
        self.assertEqual(self.invoke("verify-receipt", **{"deployment-conclusion": "failure"}), 0)

    def test_secret_bearing_url_fails_without_echoing_secret(self) -> None:
        for url in (
            "https://user:SECRET@egohygiene.github.io/empathy/",
            "https://egohygiene.github.io/empathy/?token=SECRET",
            "http://127.0.0.1/SECRET",
        ):
            with self.subTest(url=url), self.assertRaises(SystemExit) as failure:
                self.invoke("record-receipt", **{"deployment-url": url})
            self.assertNotIn("SECRET", str(failure.exception))
            self.assertNotIn(str(self.workspace), str(failure.exception))


if __name__ == "__main__":
    unittest.main()
