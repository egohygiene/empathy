# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

from __future__ import annotations

import configparser
import json
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import tomllib
import unittest

REPOSITORY_ROOT = Path(__file__).parents[1]
IDENTITY_ROOT = REPOSITORY_ROOT / "identity"
PROJECT_SPEC_PATH = REPOSITORY_ROOT / ".identity" / "identity.toml"
CONSUMER_LOCK_PATH = REPOSITORY_ROOT / ".config" / "identity" / "consumer-lock.json"
GITMODULES_PATH = REPOSITORY_ROOT / ".gitmodules"
IDENTITY_WORKTREE_INITIALIZED = (IDENTITY_ROOT / "Cargo.toml").is_file()
REQUIRES_IDENTITY_WORKTREE = unittest.skipUnless(
    IDENTITY_WORKTREE_INITIALIZED,
    "Identity submodule is not initialized in this checkout.",
)


def run_git(*arguments: str) -> str:
    """Run Git using its resolved executable and return stripped standard output."""

    git_executable = shutil.which("git")
    if git_executable is None:
        raise RuntimeError("Git is required to validate the Identity consumer contract.")

    completed_process = subprocess.run(
        [git_executable, *arguments],
        cwd=REPOSITORY_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed_process.stdout.strip()


class IdentityIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.specification = tomllib.loads(PROJECT_SPEC_PATH.read_text(encoding="utf-8"))
        self.consumer_lock = json.loads(CONSUMER_LOCK_PATH.read_text(encoding="utf-8"))

    def test_identity_source_is_pinned_as_an_immutable_gitlink(self) -> None:
        self.assertEqual(self.consumer_lock["schema"], "identity.consumer-lock/v1")
        self.assertEqual(self.consumer_lock["consumer"], "egohygiene/empathy")
        self.assertEqual(self.consumer_lock["repository"], "egohygiene/identity")
        self.assertEqual(self.consumer_lock["revision_kind"], "git-commit")
        self.assertEqual(self.consumer_lock["path"], "identity")
        self.assertRegex(self.consumer_lock["revision"], r"^[0-9a-f]{40}$")
        self.assertRegex(self.consumer_lock["source_extraction_revision"], r"^[0-9a-f]{40}$")

        gitmodules = configparser.ConfigParser()
        gitmodules.read(GITMODULES_PATH, encoding="utf-8")
        section = "submodule \"identity\""
        self.assertTrue(gitmodules.has_section(section))
        self.assertEqual(gitmodules[section]["path"], "identity")
        self.assertEqual(
            gitmodules[section]["url"],
            "https://github.com/egohygiene/identity.git",
        )

        tree_entry = run_git("ls-tree", "HEAD", "identity")
        mode, object_type, revision_and_path = tree_entry.split(maxsplit=2)
        tree_revision, tree_path = revision_and_path.split("\t", maxsplit=1)
        self.assertEqual(mode, "160000")
        self.assertEqual(object_type, "commit")
        self.assertEqual(tree_path, "identity")
        self.assertEqual(tree_revision, self.consumer_lock["revision"])

    @REQUIRES_IDENTITY_WORKTREE
    def test_initialized_identity_worktree_matches_the_consumer_lock(self) -> None:
        worktree_revision = run_git(
            "-C",
            str(IDENTITY_ROOT),
            "rev-parse",
            "HEAD",
        )
        self.assertEqual(worktree_revision, self.consumer_lock["revision"])

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

    @REQUIRES_IDENTITY_WORKTREE
    def test_profiles_resolve_unique_safe_targets_and_declared_sources(self) -> None:
        declared_sources = {
            source["role"] for source in self.specification["sources"]["required"]
        }
        declared_sources.update({"identity-brief", "project-spec"})
        paths: set[str] = set()

        for profile_id in self.specification["profiles"]["enabled"]:
            profile_path = IDENTITY_ROOT / "profiles" / f"{profile_id}.json"
            profile = json.loads(profile_path.read_text(encoding="utf-8"))
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

    @REQUIRES_IDENTITY_WORKTREE
    def test_platform_profiles_capture_foundational_constraints(self) -> None:
        github = json.loads(
            (IDENTITY_ROOT / "profiles" / "github.json").read_text(encoding="utf-8")
        )
        social_preview = next(
            target
            for target in github["targets"]
            if target["id"] == "repository-social-preview"
        )
        self.assertEqual((social_preview["width"], social_preview["height"]), (1280, 640))
        self.assertEqual(social_preview["maximum_bytes"], 1_000_000)

        pwa = json.loads(
            (IDENTITY_ROOT / "profiles" / "pwa.json").read_text(encoding="utf-8")
        )
        purposes = {target.get("purpose") for target in pwa["targets"]}
        self.assertTrue({"any", "maskable", "monochrome"}.issubset(purposes))
        raster_sizes = {
            (target.get("width"), target.get("height"))
            for target in pwa["targets"]
            if target["format"] == "png"
        }
        self.assertTrue({(192, 192), (512, 512)}.issubset(raster_sizes))

    @REQUIRES_IDENTITY_WORKTREE
    def test_identity_v0_contracts_are_present(self) -> None:
        for contract_name in (
            "candidate-manifest.schema.json",
            "handoff-manifest.schema.json",
            "profile.schema.json",
            "project.schema.json",
        ):
            contract = json.loads(
                (IDENTITY_ROOT / "contracts" / contract_name).read_text(encoding="utf-8")
            )
            self.assertEqual(
                contract["$schema"],
                "https://json-schema.org/draft/2020-12/schema",
            )

    def test_consumer_paths_are_present(self) -> None:
        for path_key in ("brief", "source_root"):
            path = REPOSITORY_ROOT / self.specification["paths"][path_key]
            self.assertTrue(path.exists(), path_key)
        for context_path in self.specification["context"]["files"]:
            self.assertTrue((REPOSITORY_ROOT / context_path).is_file(), context_path)

        integration_document = (
            REPOSITORY_ROOT / "docs" / "integrations" / "IDENTITY.md"
        )
        self.assertTrue(integration_document.is_file())

    def test_task_and_ci_contracts_use_the_pinned_consumer(self) -> None:
        root_taskfile = (REPOSITORY_ROOT / "Taskfile.yml").read_text(encoding="utf-8")
        taskfile = (REPOSITORY_ROOT / ".tasks/identity.yml").read_text(encoding="utf-8")
        project_tasks = (REPOSITORY_ROOT / ".tasks/project.yml").read_text(
            encoding="utf-8"
        )
        workflow = (REPOSITORY_ROOT / ".github/workflows/identity.yml").read_text(
            encoding="utf-8"
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
        self.assertIn(".config/identity/consumer-lock.json", taskfile)
        self.assertIn("--manifest-path \"identity/Cargo.toml\"", taskfile)
        self.assertIn("- identity:check", project_tasks)

        self.assertIn("submodules: recursive", workflow)
        self.assertIn("Verify immutable consumer pin", workflow)
        self.assertIn(".config/identity/consumer-lock.json", workflow)


if __name__ == "__main__":
    unittest.main()
