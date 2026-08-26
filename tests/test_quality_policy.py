# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

from __future__ import annotations

import json
from pathlib import Path
import subprocess  # nosec B404
import tomllib
import unittest

REPOSITORY_ROOT = Path(__file__).parents[1]
SOURCE_SUFFIXES = {
    ".bash",
    ".c",
    ".cc",
    ".cjs",
    ".cpp",
    ".cs",
    ".css",
    ".go",
    ".h",
    ".hpp",
    ".java",
    ".js",
    ".jsx",
    ".mjs",
    ".php",
    ".py",
    ".rb",
    ".rs",
    ".sh",
    ".ts",
    ".tsx",
    ".zsh",
}
INLINE_HEADER_EXEMPT_PREFIXES = (
    "beacon/templates/",
    "holon/packs/react-vite/template/",
    "notebooks/jupyter/themes/",
)


class QualityPolicyTests(unittest.TestCase):
    def git(
        self, *arguments: str, input_text: str | None = None
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(  # nosec B603 B607
            ["git", *arguments],
            check=False,
            cwd=REPOSITORY_ROOT,
            encoding="utf8",
            input=input_text,
            capture_output=True,
        )

    def test_scratch_and_report_ignore_contract(self) -> None:
        candidate_paths = [
            "temp.txt",
            "nested/temp.txt",
            "temp.md",
            "nested/temp.md",
            ".reports/example.json",
            ".reports/README.md",
        ]
        result = self.git(
            "check-ignore",
            "--no-index",
            "--stdin",
            input_text="\n".join(candidate_paths),
        )
        ignored_paths = set(result.stdout.splitlines())
        self.assertEqual(
            ignored_paths,
            {
                "temp.txt",
                "nested/temp.txt",
                "temp.md",
                "nested/temp.md",
                ".reports/example.json",
            },
        )

    def test_legacy_report_namespace_and_raku_cache_are_absent(self) -> None:
        for policy_path in [".gitignore", ".prettierignore"]:
            policy = (REPOSITORY_ROOT / policy_path).read_text(encoding="utf8")
            self.assertNotIn("\nreports/\n", f"\n{policy}\n")

        tracked_files = self.git("ls-files").stdout.splitlines()
        self.assertFalse(any("/.precomp/" in f"/{path}" for path in tracked_files))

    def test_commit_tools_share_the_emoji_policy(self) -> None:
        canonical_path = "egolint/.config/lint/commits/commitlint.emoji.config.cjs"
        integration_paths = [
            ".github/workflows/commitlint.yml",
            "egolint/package.json",
        ]
        for integration_path in integration_paths:
            content = (REPOSITORY_ROOT / integration_path).read_text(encoding="utf8")
            self.assertIn(Path(canonical_path).name, content)

        commit_message_hook = (REPOSITORY_ROOT / "egolint/.husky/commit-msg").read_text(
            encoding="utf8"
        )
        self.assertIn("run commitlint", commit_message_hook)
        pre_commit_policy = (REPOSITORY_ROOT / "egolint/.pre-commit-config.yaml").read_text(
            encoding="utf8"
        )
        self.assertIn("run commitlint", pre_commit_policy)

        commitizen = json.loads((REPOSITORY_ROOT / ".czrc").read_text(encoding="utf8"))
        commit_types = [item["name"] for item in commitizen["config"]["cz-emoji"]["types"]]
        self.assertEqual(len(commit_types), len(set(commit_types)))
        self.assertTrue({"chore", "feat", "fix", "refactor"}.issubset(commit_types))

    def test_detect_secrets_baseline_contains_no_real_secret(self) -> None:
        baseline = json.loads((REPOSITORY_ROOT / ".secrets.baseline").read_text(encoding="utf8"))
        self.assertEqual(baseline["version"], "1.5.0")
        findings = [
            finding for file_findings in baseline["results"].values() for finding in file_findings
        ]
        self.assertTrue(findings)
        self.assertTrue(all(finding.get("is_secret") is False for finding in findings))

    def test_reuse_and_addlicense_share_the_mit_policy(self) -> None:
        reuse_configuration = tomllib.loads(
            (REPOSITORY_ROOT / "REUSE.toml").read_text(encoding="utf8")
        )
        default_annotation = reuse_configuration["annotations"][0]
        self.assertEqual(default_annotation["SPDX-FileCopyrightText"], "2026 Ego Hygiene")
        self.assertEqual(default_annotation["SPDX-License-Identifier"], "MIT")
        self.assertTrue((REPOSITORY_ROOT / "LICENSES/MIT.txt").is_file())
        self.assertTrue((REPOSITORY_ROOT / "LICENSES/BSD-3-Clause.txt").is_file())

        pre_commit_policy = (REPOSITORY_ROOT / "egolint/.pre-commit-config.yaml").read_text(
            encoding="utf8"
        )
        for expected_argument in ["Ego Hygiene", "-s=only", "mit", '"2026"']:
            self.assertIn(expected_argument, pre_commit_policy)

    def test_first_party_source_has_mit_spdx_headers(self) -> None:
        tracked_files = self.git("ls-files").stdout.splitlines()
        source_paths = [
            Path(path)
            for path in tracked_files
            if Path(path).suffix in SOURCE_SUFFIXES
            and not path.startswith(".reports/")
            and ".staging" not in Path(path).parts
            and not path.startswith("egolint/tests/fixtures/")
            # Reusable template and vendored payloads inherit the repository's
            # global REUSE.toml annotation instead of modifying emitted source.
            and not path.startswith(INLINE_HEADER_EXEMPT_PREFIXES)
        ]
        self.assertTrue(source_paths)

        for source_path in source_paths:
            header = "\n".join(
                (REPOSITORY_ROOT / source_path).read_text(encoding="utf8").splitlines()[:8]
            )
            self.assertIn("Copyright 2026 Ego Hygiene", header, source_path.as_posix())
            license_marker = "SPDX-License" + "-Identifier: MIT"
            self.assertIn(license_marker, header, source_path.as_posix())


if __name__ == "__main__":
    unittest.main()
