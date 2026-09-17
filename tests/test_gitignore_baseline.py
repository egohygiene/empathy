# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Exercise the proposed universal baseline with Git's own ignore engine."""

from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess  # nosec B404
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / "foundation" / "ignore" / "universal.gitignore"


class GitignoreBaselineTests(unittest.TestCase):
    """Check untracked files in isolated repositories, independent of Empathy."""

    def setUp(self) -> None:
        self.git_executable = shutil.which("git")
        self.assertIsNotNone(self.git_executable, "Git is required for behavior checks")
        temporary = tempfile.TemporaryDirectory(prefix="empathy-ignore-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.environment = {
            key: value for key, value in os.environ.items() if not key.startswith("GIT_")
        }
        self.environment.update(
            GIT_CONFIG_NOSYSTEM="1",
            GIT_CONFIG_GLOBAL=os.devnull,
            GIT_ATTR_NOSYSTEM="1",
        )
        template = self.root / "empty-git-template"
        template.mkdir()
        self.git("init", "--quiet", "--initial-branch=main", f"--template={template}")
        self.git("config", "--local", "core.excludesFile", os.devnull)
        self.git("config", "--local", "core.ignoreCase", "false")
        self.write(".gitignore", BASELINE.read_text(encoding="utf-8"))

    def git(self, *arguments: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        """Run Git without a shell or inherited Git configuration overrides."""
        # An absolute Git executable receives only test-owned arguments, without a shell.
        return subprocess.run(  # noqa: S603  # nosec B603
            [self.git_executable, *arguments],
            cwd=self.root,
            env=self.environment,
            capture_output=True,
            encoding="utf-8",
            timeout=10,
            check=check,
        )

    def write(self, relative_path: str, content: str = "fixture\n") -> None:
        """Create a real fixture, including its parent directories."""
        path = self.root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def assert_paths(self, paths: tuple[str, ...], *, ignored: bool) -> None:
        """Check expected visibility and report the winning rule on failure."""
        for path in paths:
            with self.subTest(path=path, ignored=ignored):
                self.write(path)
                result = self.git("check-ignore", "--quiet", "--no-index", "--", path, check=False)
                expected = 0 if ignored else 1
                if result.returncode != expected:
                    diagnostic = self.git(
                        "check-ignore", "--verbose", "--no-index", "--", path, check=False
                    )
                    self.fail(
                        f"{path}: expected return code {expected}, got {result.returncode}; "
                        f"{diagnostic.stdout or diagnostic.stderr or result.stderr}"
                    )

    def test_operating_system_and_editor_local_state_is_ignored(self) -> None:
        self.assert_paths(
            (
                ".DS_Store",
                "nested/.DS_Store",
                ".AppleDouble/metadata",
                ".LSOverride",
                "nested/._document",
                "Thumbs.db",
                "nested/Desktop.ini",
                "$RECYCLE.BIN/deleted.txt",
                "notes.md~",
                "nested/.notes.swp",
                "nested/.notes.swo",
                ".idea/workspace.xml",
                "project/.idea/workspace.xml",
                ".idea/usage.statistics.xml",
                "project/.idea/shelf/change.patch",
            ),
            ignored=True,
        )

    def test_reserved_caches_and_dependencies_are_ignored_at_any_depth(self) -> None:
        self.assert_paths(
            (
                ".cache/tool/state.json",
                "project/.cache/tool/state.json",
                ".tmp/scratch.txt",
                "project/.tmp/scratch.txt",
                ".venv/pyvenv.cfg",
                "project/.venv/pyvenv.cfg",
                "__pycache__/example.cpython-312.pyc",
                "project/__pycache__/example.cpython-312.pyc",
                "node_modules/package/index.js",
                "project/node_modules/package/index.js",
                "node_modules/.gitkeep",
            ),
            ignored=True,
        )

    def test_local_environments_and_private_namespace_are_ignored(self) -> None:
        self.assert_paths(
            (
                ".env",
                ".env.local",
                ".env.production",
                "project/.env.production.local",
                ".env.example.local",
                ".env.template.backup",
                ".env.production.sample.local",
                ".secrets/private.key",
                "project/.secrets/private.p12",
                ".secrets/.env.example",
            ),
            ignored=True,
        )

    def test_explicit_environment_template_suffixes_stay_visible(self) -> None:
        self.assert_paths(
            tuple(
                f"{directory}{name}"
                for directory in ("", "project/")
                for name in (
                    ".env.example",
                    ".env.sample",
                    ".env.template",
                    ".env.production.example",
                    ".env.production.sample",
                    ".env.production.template",
                )
            ),
            ignored=False,
        )

    def test_shared_configuration_and_lockfiles_stay_visible(self) -> None:
        self.assert_paths(
            (
                ".vscode/settings.json",
                ".vscode/tasks.json",
                ".vscode/launch.json",
                ".vscode/extensions.json",
                ".vscode/project.code-snippets",
                ".vscode/custom-shared.json",
                "project/.vscode/settings.json",
                ".idea/codeStyles/Project.xml",
                ".idea/inspectionProfiles/Project_Default.xml",
                "project/.idea/modules.xml",
                ".fleet/settings.json",
                "Cargo.lock",
                "package-lock.json",
                "pnpm-lock.yaml",
                "yarn.lock",
                "poetry.lock",
                "uv.lock",
                ".terraform.lock.hcl",
                "project/Cargo.lock",
                ".yarn/cache/reviewed-package.zip",
                ".secrets.baseline",
            ),
            ignored=False,
        )

    def test_ambiguous_paths_and_reviewed_artifacts_stay_visible(self) -> None:
        self.assert_paths(
            (
                *(
                    f"{directory}/source.txt"
                    for directory in (
                        "bin",
                        "build",
                        "dist",
                        "lib",
                        "out",
                        "pkg",
                        "public",
                        "reports",
                        "target",
                        "vendor",
                        "coverage",
                        "temp",
                        "tmp",
                        "venv",
                        "obj",
                        "Pods",
                        "project/bin",
                        "project/build",
                        "project/dist",
                        "project/target",
                    )
                ),
                "fixtures/reference.zip",
                "fixtures/reference.tar.gz",
                "fixtures/reference.patch",
                "fixtures/reference.orig",
                "fixtures/reference.rej",
                "fixtures/reference.bak",
                "fixtures/reference.log",
                "fixtures/reference.seed",
                "fixtures/public.key",
                "fixtures/public.pem",
                "fixtures/public.crt",
                "fixtures/binary sample.p12",
                "fixtures/reference.pfx",
                "fixtures/reference.jks",
                "fixtures/reference.keystore",
                "fixtures/reference.pyd",
                "fixtures/reference.whl",
                "fixtures/reference.apk",
                "fixtures/reference.test",
                "screenshots/reference.png",
                "snapshots/reference.snap",
                "docs/generated/reference.md",
                ".reports/accepted-evidence.json",
                "temp.md",
                "temp.txt",
                "infra/reviewed.tfvars",
            ),
            ignored=False,
        )

    def test_nested_project_rule_only_ignores_its_own_output(self) -> None:
        self.write("projects/rust/.gitignore", "/target/\n")
        self.assert_paths(("projects/rust/target/debug/example",), ignored=True)
        self.assert_paths(
            ("target/source.rs", "projects/other/target/source.rs", "projects/rust/src/lib.rs"),
            ignored=False,
        )

    def test_profile_exception_keeps_reviewed_output_visible(self) -> None:
        self.write("project/.gitignore", "/build/*\n!/build/README.md\n")
        self.assert_paths(("project/build/generated.js",), ignored=True)
        self.assert_paths(("project/build/README.md", "build/source.txt"), ignored=False)

    def test_negation_cannot_reinclude_a_file_beneath_an_excluded_parent(self) -> None:
        self.write("project/.gitignore", "/build/\n!/build/README.md\n")
        self.assert_paths(("project/build/README.md",), ignored=True)

    def test_nested_rules_can_weaken_baseline_without_a_conformance_validator(self) -> None:
        self.write("project/.gitignore", "!.env\n")
        self.assert_paths(("project/.env",), ignored=False)
        self.assert_paths(("other/.env",), ignored=True)

    def test_ignore_rules_do_not_protect_already_tracked_files(self) -> None:
        self.write(".env")
        self.git("add", "--force", "--", ".env")
        result = self.git("check-ignore", "--quiet", "--", ".env", check=False)
        self.assertEqual(1, result.returncode)
        self.assert_paths((".env",), ignored=True)

    def test_baseline_has_no_duplicate_active_rules(self) -> None:
        rules = [
            line
            for line in BASELINE.read_text(encoding="utf-8").splitlines()
            if line and not line.startswith("#")
        ]
        self.assertEqual(len(rules), len(set(rules)))


if __name__ == "__main__":
    unittest.main()
