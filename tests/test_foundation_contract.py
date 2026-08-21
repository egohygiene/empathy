# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import foundation  # noqa: E402

SOURCE_REVISION = "a" * 40


class FoundationContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog = foundation.load_json(ROOT / "foundation" / "catalog.json")
        cls.manifest = foundation.load_json(
            ROOT / "foundation" / "empathy.manifest.json"
        )

    def test_catalog_and_golden_manifest_are_valid(self) -> None:
        self.assertEqual([], foundation.validate_catalog(self.catalog))
        resolved, errors = foundation.resolve_manifest(self.catalog, self.manifest)
        self.assertEqual([], errors)
        self.assertIsNotNone(resolved)
        assert resolved is not None
        self.assertEqual("egohygiene/empathy", resolved["repository"])
        self.assertIn("universal", resolved["profiles"])
        self.assertIn("documentation", resolved["profiles"])

    def test_all_required_categories_and_presence_states_are_inventory_visible(self) -> None:
        self.assertEqual(
            foundation.REQUIRED_CATEGORIES, set(self.catalog["categories"])
        )
        self.assertEqual(
            {"optional", "profile", "required"},
            {artifact["presence"] for artifact in self.catalog["artifacts"]},
        )
        self.assertEqual(
            {"generated", "repository-owned", "required"},
            {artifact["ownership"] for artifact in self.catalog["artifacts"]},
        )

    def test_resolution_is_byte_idempotent(self) -> None:
        first, first_errors = foundation.resolve_manifest(self.catalog, self.manifest)
        second, second_errors = foundation.resolve_manifest(
            copy.deepcopy(self.catalog), copy.deepcopy(self.manifest)
        )
        self.assertEqual([], first_errors)
        self.assertEqual([], second_errors)
        assert first is not None
        assert second is not None
        self.assertEqual(first, second)
        self.assertEqual(
            foundation.render_resolved(first), foundation.render_resolved(second)
        )

    def test_safe_override_preserves_repository_ownership(self) -> None:
        resolved, errors = foundation.resolve_manifest(self.catalog, self.manifest)
        self.assertEqual([], errors)
        assert resolved is not None
        artifacts = {artifact["id"]: artifact for artifact in resolved["artifacts"]}
        self.assertEqual(
            "repository-owned", artifacts["issue-template-config"]["effective_ownership"]
        )
        self.assertEqual("preserve", artifacts["issue-template-config"]["override"])
        self.assertEqual(
            "required", artifacts["issue-template-config"]["ownership"]
        )

    def test_generated_artifact_override_fails_closed(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        manifest["overrides"] = [
            {"artifact": "ecosystem-context", "mode": "preserve"}
        ]
        resolved, errors = foundation.resolve_manifest(self.catalog, manifest)
        self.assertIsNone(resolved)
        self.assertIn(
            "generated artifact cannot be preserved by override: ecosystem-context",
            errors,
        )

    def test_unknown_and_conflicting_profiles_fail_closed(self) -> None:
        unknown = copy.deepcopy(self.manifest)
        unknown["selected_profiles"] = ["unknown"]
        _, unknown_errors = foundation.resolve_manifest(self.catalog, unknown)
        self.assertIn("manifest references unknown profiles: unknown", unknown_errors)

        conflict = copy.deepcopy(self.manifest)
        conflict["selected_profiles"].append("publication")
        _, conflict_errors = foundation.resolve_manifest(self.catalog, conflict)
        self.assertTrue(
            any("conflicts with" in error for error in conflict_errors),
            conflict_errors,
        )

    def test_optional_artifacts_are_inventoried_but_not_enforced(self) -> None:
        resolved, errors = foundation.resolve_manifest(self.catalog, self.manifest)
        self.assertEqual([], errors)
        assert resolved is not None
        selected = {artifact["id"] for artifact in resolved["artifacts"]}
        self.assertNotIn("contributing", selected)
        self.assertIn("contributing", resolved["optional_artifacts"])
        self.assertIn("security-policy", resolved["optional_artifacts"])

    def test_golden_workspace_satisfies_selected_foundation(self) -> None:
        resolved, errors = foundation.resolve_manifest(self.catalog, self.manifest)
        self.assertEqual([], errors)
        assert resolved is not None
        self.assertEqual([], foundation.validate_workspace(ROOT, resolved))

    def test_inventory_and_egolint_contract_are_deterministic(self) -> None:
        inventory = foundation.render_inventory(self.catalog)
        self.assertEqual(inventory, foundation.render_inventory(copy.deepcopy(self.catalog)))
        self.assertIn("community-health", inventory)
        self.assertIn("Generated outputs", inventory)

        resolved, errors = foundation.resolve_manifest(self.catalog, self.manifest)
        self.assertEqual([], errors)
        assert resolved is not None
        contract = foundation.render_egolint_contract(resolved, SOURCE_REVISION)
        self.assertIn('id = "empathy-universal-foundation"', contract)
        self.assertIn("provisional = false", contract)
        self.assertIn('revision-kind = "git-commit"', contract)
        self.assertIn('ownership = "generated"', contract)

    def test_invalid_catalog_paths_and_generated_markers_are_rejected(self) -> None:
        invalid_path = copy.deepcopy(self.catalog)
        invalid_path["artifacts"][0]["path"] = "../README.md"
        self.assertTrue(
            any("path must be normalized" in error for error in foundation.validate_catalog(invalid_path))
        )

        missing_marker = copy.deepcopy(self.catalog)
        generated = next(
            artifact
            for artifact in missing_marker["artifacts"]
            if artifact["ownership"] == "generated"
        )
        generated["markers"] = []
        self.assertTrue(
            any(
                "generated artifact must declare deterministic markers" in error
                for error in foundation.validate_catalog(missing_marker)
            )
        )

    def test_authoring_schemas_are_valid_json(self) -> None:
        for name in (
            "repository-foundation-catalog.v1.schema.json",
            "repository-foundation-manifest.v1.schema.json",
        ):
            schema = json.loads((ROOT / "schemas" / name).read_text(encoding="utf-8"))
            self.assertEqual(
                "https://json-schema.org/draft/2020-12/schema", schema["$schema"]
            )

    def test_checked_in_inventory_and_contract_are_current(self) -> None:
        contract_path = (
            ROOT / "foundation" / "contracts" / "empathy.repository-contract.toml"
        )
        contract = tomllib.loads(contract_path.read_text(encoding="utf-8"))
        source_revision = contract["source"]["revision"]
        resolved, errors = foundation.resolve_manifest(self.catalog, self.manifest)
        self.assertEqual([], errors)
        assert resolved is not None
        self.assertEqual(
            foundation.render_inventory(self.catalog),
            (ROOT / "docs" / "foundation" / "INVENTORY.md").read_text(
                encoding="utf-8"
            ),
        )
        self.assertEqual(
            foundation.render_egolint_contract(resolved, source_revision),
            contract_path.read_text(encoding="utf-8"),
        )
        self.assertFalse(contract["provisional"])
        self.assertTrue((ROOT / contract["source"]["path"]).is_file())


if __name__ == "__main__":
    unittest.main()
