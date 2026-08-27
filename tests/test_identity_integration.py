# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Evidence for Empathy's immutable, calm Identity v1 consumer."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import unittest

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
IDENTITY_ROOT = REPOSITORY_ROOT / "identity"
LOCK_PATH = REPOSITORY_ROOT / ".config/identity/consumer-lock.json"
PROJECT_PATH = REPOSITORY_ROOT / ".identity/identity.json"
ORGANIZATION_DEFAULT_SHA256 = "6098e60eaab67887c597327e55da646685443eeddc1e27188beab4a1311e36aa"


class IdentityIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.lock = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
        self.project = json.loads(PROJECT_PATH.read_text(encoding="utf-8"))

    def test_immutable_identity_contract_preserves_extraction_lineage(self) -> None:
        self.assertEqual(self.lock["schema"], "identity.consumer-lock/v1")
        self.assertEqual(self.lock["consumer"], "egohygiene/empathy")
        self.assertEqual(self.lock["repository"], "egohygiene/identity")
        self.assertEqual(self.lock["revision_kind"], "git-commit")
        self.assertRegex(self.lock["revision"], r"^[0-9a-f]{40}$")
        self.assertRegex(self.lock["source_extraction_revision"], r"^[0-9a-f]{40}$")
        self.assertIn('path = identity', (REPOSITORY_ROOT / ".gitmodules").read_text())

    def test_v0_fixture_is_explicitly_promoted_to_v1_with_a_rollback_anchor(self) -> None:
        self.assertTrue((REPOSITORY_ROOT / ".identity/identity.toml").is_file())
        self.assertEqual(self.project["schema"], "identity.project/v1")
        self.assertEqual(self.project["project"]["id"], "empathy")
        self.assertEqual(self.project["compatibility"]["migrationFrom"], ["identity.project/v0"])
        self.assertTrue((REPOSITORY_ROOT / "docs/integrations/IDENTITY_V1.md").is_file())

    def test_only_reviewed_product_differences_override_shared_defaults(self) -> None:
        layers = self.project["layers"]
        self.assertEqual([layer["kind"] for layer in layers], ["organization-defaults", "product-override"])
        self.assertEqual(layers[0]["sha256"], ORGANIZATION_DEFAULT_SHA256)
        self.assertEqual(
            hashlib.sha256(
                (REPOSITORY_ROOT / layers[0]["tokens"]).read_bytes()
            ).hexdigest(),
            ORGANIZATION_DEFAULT_SHA256,
        )
        overrides = json.loads(
            (REPOSITORY_ROOT / layers[1]["tokens"]).read_text(encoding="utf-8")
        )
        primary = overrides["color"]["brand"]["primary"]
        self.assertEqual(primary["$value"]["components"], [0.431, 0.369, 0.745])
        self.assertEqual(
            primary["$extensions"]["org.egohygiene.identity"]["override"]["approval"],
            "approve-empathy-primary",
        )
        self.assertEqual(overrides["color"]["action"]["primary"]["$value"], "{color.brand.primary}")

    def test_full_profile_selection_is_versioned(self) -> None:
        profiles = json.loads(
            (REPOSITORY_ROOT / ".identity/targets/profiles.json").read_text(encoding="utf-8")
        )
        self.assertEqual(profiles["schema"], "identity.targets/v1")
        self.assertEqual(
            [profile["id"] for profile in profiles["enabled"]],
            ["core", "web", "pwa", "github", "docs", "social", "tokens", "metadata", "archive"],
        )
        self.assertEqual(profiles["inapplicable"], [])
        self.assertTrue(all(profile["version"] == "1.0.0" for profile in profiles["enabled"]))

    @unittest.skipUnless(
        (REPOSITORY_ROOT / "assets/identity/packages/tokens/tokens.css").is_file(),
        "Identity package has not been generated",
    )
    def test_generated_package_snapshot_preserves_the_reviewed_calm_violet(self) -> None:
        css = (
            REPOSITORY_ROOT / "assets/identity/packages/tokens/tokens.css"
        ).read_text(encoding="utf-8")
        self.assertIn("--identity-color-brand-primary: #6e5ebe;", css)

    @unittest.skipUnless((IDENTITY_ROOT / "Cargo.toml").is_file(), "Identity submodule is not initialized")
    def test_pinned_v1_validator_and_compiler_detect_no_generated_state_drift(self) -> None:
        subprocess.run(
            ["python3", str(IDENTITY_ROOT / "scripts/validate_identity.py"), "--repository-root", str(REPOSITORY_ROOT)],
            check=True,
        )
        subprocess.run(
            ["cargo", "run", "--quiet", "--manifest-path", str(IDENTITY_ROOT / "Cargo.toml"), "--", "v1-verify", "--repository-root", str(REPOSITORY_ROOT)],
            check=True,
        )


if __name__ == "__main__":
    unittest.main()
