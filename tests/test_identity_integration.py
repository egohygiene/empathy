# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

from __future__ import annotations

import json
from pathlib import Path, PurePosixPath
import tomllib
import unittest

REPOSITORY_ROOT = Path(__file__).parents[1]
IDENTITY_ROOT = REPOSITORY_ROOT / "identity"
PROJECT_SPEC_PATH = REPOSITORY_ROOT / ".identity" / "identity.toml"


class IdentityIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.specification = tomllib.loads(PROJECT_SPEC_PATH.read_text(encoding="utf8"))

    def test_empathy_selects_versioned_profiles_and_human_approval(self) -> None:
        self.assertEqual(self.specification["schema"], "identity.project/v0")
        self.assertEqual(self.specification["project"]["id"], "empathy")
        self.assertEqual(self.specification["sources"]["approval"], "human")

        enabled = self.specification["profiles"]["enabled"]
        self.assertEqual(len(enabled), len(set(enabled)))
        self.assertEqual(
            set(enabled),
            {"core", "docs", "github", "metadata", "pwa", "social", "tokens", "web"},
        )

    def test_profiles_resolve_unique_safe_targets_and_declared_sources(self) -> None:
        declared_sources = {source["role"] for source in self.specification["sources"]["required"]}
        declared_sources.update({"identity-brief", "project-spec"})
        paths: set[str] = set()

        for profile_id in self.specification["profiles"]["enabled"]:
            profile_path = IDENTITY_ROOT / "profiles" / f"{profile_id}.json"
            profile = json.loads(profile_path.read_text(encoding="utf8"))
            self.assertEqual(profile["schema"], "identity.profile/v0")
            self.assertEqual(profile["id"], profile_id)
            self.assertRegex(profile["version"], r"^\d+\.\d+\.\d+$")
            self.assertRegex(profile["verified_at"], r"^\d{4}-\d{2}-\d{2}$")

            for target in profile["targets"]:
                path = PurePosixPath(target["path"])
                self.assertFalse(path.is_absolute())
                self.assertNotIn("..", path.parts)
                self.assertNotIn(target["path"], paths)
                paths.add(target["path"])
                self.assertIn(target["source_role"], declared_sources)
                self.assertEqual("width" in target, "height" in target)

    def test_platform_profiles_capture_foundational_constraints(self) -> None:
        github = json.loads((IDENTITY_ROOT / "profiles" / "github.json").read_text(encoding="utf8"))
        social_preview = next(
            target for target in github["targets"] if target["id"] == "repository-social-preview"
        )
        self.assertEqual((social_preview["width"], social_preview["height"]), (1280, 640))
        self.assertEqual(social_preview["maximum_bytes"], 1_000_000)

        pwa = json.loads((IDENTITY_ROOT / "profiles" / "pwa.json").read_text(encoding="utf8"))
        purposes = {target.get("purpose") for target in pwa["targets"]}
        self.assertTrue({"any", "maskable", "monochrome"}.issubset(purposes))
        raster_sizes = {
            (target.get("width"), target.get("height"))
            for target in pwa["targets"]
            if target["format"] == "png"
        }
        self.assertTrue({(192, 192), (512, 512)}.issubset(raster_sizes))

    def test_contracts_and_consumer_paths_are_present(self) -> None:
        for contract_name in (
            "candidate-manifest.schema.json",
            "handoff-manifest.schema.json",
            "profile.schema.json",
            "project.schema.json",
        ):
            contract = json.loads(
                (IDENTITY_ROOT / "contracts" / contract_name).read_text(encoding="utf8")
            )
            self.assertEqual(contract["$schema"], "https://json-schema.org/draft/2020-12/schema")

        for path_key in ("brief", "source_root"):
            path = REPOSITORY_ROOT / self.specification["paths"][path_key]
            self.assertTrue(path.exists(), path_key)
        for context_path in self.specification["context"]["files"]:
            self.assertTrue((REPOSITORY_ROOT / context_path).is_file(), context_path)

    def test_task_contract_exposes_identity_workflow(self) -> None:
        root_taskfile = (REPOSITORY_ROOT / "Taskfile.yml").read_text(encoding="utf8")
        taskfile = (REPOSITORY_ROOT / ".tasks/identity.yml").read_text(encoding="utf8")
        project_tasks = (REPOSITORY_ROOT / ".tasks/project.yml").read_text(encoding="utf8")

        self.assertIn("taskfile: ./.tasks/identity.yml", root_taskfile)
        self.assertIn("flatten: true", root_taskfile)
        for task_name in ("identity:check:", "identity:plan:", "identity:handoff:"):
            self.assertIn(task_name, taskfile)
        self.assertIn('--manifest-path "identity/Cargo.toml"', taskfile)
        self.assertIn("- identity:check", project_tasks)


if __name__ == "__main__":
    unittest.main()
