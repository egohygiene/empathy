# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

from __future__ import annotations

import configparser
import json
from pathlib import Path, PurePosixPath
import subprocess
import tomllib
import unittest

REPOSITORY_ROOT = Path(__file__).parents[1]
IDENTITY_ROOT = REPOSITORY_ROOT / "identity"
PROJECT_SPEC_PATH = REPOSITORY_ROOT / ".identity" / "identity.toml"
CONSUMER_LOCK_PATH = REPOSITORY_ROOT / ".config" / "identity" / "consumer-lock.json"
GITMODULES_PATH = REPOSITORY_ROOT / ".gitmodules"


class IdentityIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.specification = tomllib.loads(PROJECT_SPEC_PATH.read_text(encoding="utf8"))
        self.consumer_lock = json.loads(CONSUMER_LOCK_PATH.read_text(encoding="utf8"))

    def test_identity_source_is_an_immutable_submodule(self) -> None:
        self.assertEqual(self.consumer_lock["schema"], "identity.consumer-lock/v1")
        self.assertEqual(self.consumer_lock["consumer"], "egohygiene/empathy")
        self.assertEqual(self.consumer_lock["repository"], "egohygiene/identity")
        self.assertEqual(self.consumer_lock["revision_kind"], "git-commit")
        self.assertEqual(self.consumer_lock["path"], "identity")
        self.assertRegex(self.consumer_lock["revision"], r"^[0-9a-f]{40}$")
        self.assertRegex(self.consumer_lock["source_extraction_revision"], r"^[0-9a-f]{40}$")

        gitmodules = configparser.ConfigParser()
        gitmodules.read(GITMODULES_PATH, encoding="utf8")
        section = 'submodule "identity"'
        self.assertTrue(gitmodules.has_section(section))
        self.assertEqual(gitmodules[section]["path"], "identity")
        self.assertEqual(
            gitmodules[section]["url"],
            "https://github.com/egohygiene/identity.git",
        )

        tree_entry = subprocess.run(
            ["git", "ls-tree", "HEAD", "identity"],
            cwd=REPOSITORY_ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        mode, object_type, revision_and_path = tree_entry.split(maxsplit=2)
        tree_revision, tree_path = revision_and_path.split("\t", maxsplit=1)
        self.assertEqual(mode, "160000")
        self.assertEqual(object_type, "commit")
        self.assertEqual(tree_path, "identity")
        self.assertEqual(tree_revision, self.consumer_lock["revision"])

        worktree_revision = subprocess.run(
            ["git", "-C", "identity", "rev-parse", "HEAD"],
            cwd=REPOSITORY_ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        self.assertEqual(worktree_revision, self.consumer_lock["revision"])
        self.assertTrue((IDENTITY_ROOT / "Cargo.toml").is_file())

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

        self.assertTrue((REPOSITORY_ROOT / "docs" / "integrations" / "IDENTITY.md").is_file())

    def test_task_and_ci_contracts_use_the_pinned_consumer(self) -> None:
        root_taskfile = (REPOSITORY_ROOT / "Taskfile.yml").read_text(encoding="utf8")
        taskfile = (REPOSITORY_ROOT / ".tasks/identity.yml").read_text(encoding="utf8")
        project_tasks = (REPOSITORY_ROOT / ".tasks/project.yml").read_text(encoding="utf8")
        workflow = (REPOSITORY_ROOT / ".github/workflows/identity.yml").read_text(
            encoding="utf8"
        )

        self.assertIn("taskfile: ./.tasks/identity.yml", root_taskfile)
        self.assertIn("flatten: true", root_taskfile)
        for task_name in (
            "identity:pin:check:",
            "identity:check:",
            "identity:plan:",
            "identity:handoff:",
        ):
            self.assertIn(task_name, taskfile)
        self.assertIn("internal: true", taskfile)
        self.assertIn('.config/identity/consumer-lock.json', taskfile)
        self.assertIn('--manifest-path "identity/Cargo.toml"', taskfile)
        self.assertIn("- identity:check", project_tasks)

        self.assertIn("submodules: recursive", workflow)
        self.assertIn("Verify immutable consumer pin", workflow)
        self.assertIn('.config/identity/consumer-lock.json', workflow)


if __name__ == "__main__":
    unittest.main()
