# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import subprocess  # nosec B404
import sys
import tempfile
import textwrap
from typing import Any
import unittest

REPOSITORY_ROOT = Path(__file__).parents[2]
MODULE_PATH = REPOSITORY_ROOT / "egolint" / "scripts" / "validate_megalinter_policy.py"
ESLINT_CONFIG_PATH = (
    REPOSITORY_ROOT / "egolint" / ".config" / "lint" / "javascript" / "eslint.config.mjs"
)
SPEC = importlib.util.spec_from_file_location("validate_megalinter_policy", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Unable to load MegaLinter policy module from {MODULE_PATH}")
megalinter_policy = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = megalinter_policy
SPEC.loader.exec_module(megalinter_policy)


class MegaLinterPolicyTests(unittest.TestCase):
    catalog: dict[str, Any]
    matrix: dict[str, Any]
    matrix_by_id: dict[str, dict[str, Any]]

    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog = json.loads(megalinter_policy.CATALOG_PATH.read_text(encoding="utf-8"))
        cls.matrix = json.loads(megalinter_policy.MATRIX_PATH.read_text(encoding="utf-8"))
        cls.matrix_by_id = {tool["id"]: tool for tool in cls.matrix["tools"]}

    def test_generated_contracts_are_current(self) -> None:
        result = subprocess.run(  # nosec B603
            [sys.executable, str(MODULE_PATH), "--check"],
            cwd=REPOSITORY_ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, f"{result.stdout}\n{result.stderr}")

    def test_catalog_is_pinned_to_the_workflow_release(self) -> None:
        self.assertEqual(self.catalog["megalinter_release"], "v10.0.0")
        self.assertEqual(
            self.catalog["megalinter_commit"],
            "15e5b45552097e318c93de385779ce3b1084052c",
        )
        workflow = (REPOSITORY_ROOT / ".github/workflows/megalinter.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn(self.catalog["megalinter_commit"], workflow)
        self.assertEqual(len(self.catalog["tools"]), 124)
        self.assertNotIn(
            "unknown",
            {tool["version"] for tool in self.catalog["tools"].values()},
        )

    def test_fast_and_holistic_profile_snapshots_are_explicit(self) -> None:
        fast = json.loads(
            megalinter_policy.PROFILE_SNAPSHOT_PATHS["fast"].read_text(encoding="utf-8")
        )
        holistic = json.loads(
            megalinter_policy.PROFILE_SNAPSHOT_PATHS["holistic"].read_text(encoding="utf-8")
        )
        self.assertEqual(len(fast["selected"]), 12)
        self.assertFalse(fast["validate_all_codebase"])
        self.assertTrue(holistic["validate_all_codebase"])
        self.assertIn("REPOSITORY_BETTERLEAKS", fast["selected"])
        self.assertIn("PYTHON_RUFF_FORMAT", holistic["selected"])
        self.assertIn("ACTION_ZIZMOR", holistic["disabled_by_configuration"])
        self.assertNotIn("REPOSITORY_GITLEAKS", holistic["selected"])

    def test_target_tools_have_truthful_config_and_fixture_contracts(self) -> None:
        expected_configuration_paths = {
            "ACTION_ZIZMOR": "egolint/.config/lint/actions/zizmor.yml",
            "GO_GOLANGCI_LINT": "egolint/.config/lint/go/golangci-lint.yml",
            "JSON_V8R": "egolint/.config/lint/yaml/.v8rrc.yml",
            "MARKDOWN_RUMDL": "egolint/.config/lint/markdown/.rumdl.toml",
            "PYTHON_RUFF_FORMAT": "egolint/.config/lint/python/ruff.toml",
            "REPOSITORY_SEMGREP": "egolint/.config/security/semgrep/semgrep.yml",
            "SPELL_CODESPELL": "egolint/.config/lint/prose/spell/.codespellrc",
        }
        for tool_id, expected_path in expected_configuration_paths.items():
            tool = self.matrix_by_id[tool_id]
            self.assertEqual(tool["configuration_path"], expected_path)
            self.assertTrue((REPOSITORY_ROOT / expected_path).is_file())
            fixture_contract = tool["fixtures"]
            self.assertTrue(
                fixture_contract.get("blocker")
                or (fixture_contract.get("positive") and fixture_contract.get("negative"))
            )

    def test_removed_linter_variables_and_selections_are_rejected(self) -> None:
        deprecated_findings = megalinter_policy.validate_configuration(
            Path("deprecated.yml"),
            {"API_SPECTRAL_CONFIG_FILE": ".spectral.yaml"},
            self.catalog,
        )
        removed_findings = megalinter_policy.validate_configuration(
            Path("removed.yml"),
            {
                "ENABLE": ["API"],
                "ENABLE_LINTERS": ["REPOSITORY_GITLEAKS"],
            },
            self.catalog,
        )
        self.assertTrue(any("removed/deprecated" in finding for finding in deprecated_findings))
        self.assertTrue(any("removed linter" in finding for finding in removed_findings))
        self.assertTrue(any("removed descriptor" in finding for finding in removed_findings))

    def test_resolve_configuration_path_accepts_workspace_anchored_rules(self) -> None:
        expected = (
            REPOSITORY_ROOT / "egolint" / ".config" / "lint" / "terraform" / ".tflint.hcl"
        )
        for rules_path in (
            "${GITHUB_WORKSPACE}/egolint/.config/lint/terraform",
            "/github/workspace/egolint/.config/lint/terraform",
            "/tmp/lint/egolint/.config/lint/terraform",
        ):
            with self.subTest(rules_path=rules_path):
                resolved = megalinter_policy.resolve_configuration_path(
                    rules_path,
                    ".tflint.hcl",
                )
                self.assertEqual(resolved, expected)

    def test_selection_and_result_states_are_distinguishable(self) -> None:
        expected_result_states = {
            "configuration_error",
            "disabled_by_configuration",
            "disabled_by_profile",
            "execution_error",
            "failed_findings",
            "missing_from_image",
            "not_applicable",
            "passed",
            "passed_with_warnings",
            "selected",
            "timed_out",
        }
        self.assertEqual(set(self.matrix["result_statuses"]), expected_result_states)
        self.assertEqual(
            self.matrix_by_id["ACTION_ZIZMOR"]["profiles"]["holistic"],
            "disabled_by_configuration",
        )
        self.assertEqual(
            self.matrix_by_id["PYTHON_RUFF_FORMAT"]["profiles"]["fast"],
            "disabled_by_profile",
        )
        self.assertEqual(
            self.matrix_by_id["PYTHON_RUFF_FORMAT"]["profiles"]["holistic"],
            "selected",
        )

    def test_eslint_config_handles_optional_json_plugin(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_root = Path(tmpdir)
            config_path = temp_root / "eslint.config.mjs"
            config_path.write_text(ESLINT_CONFIG_PATH.read_text(encoding="utf-8"), encoding="utf-8")

            def write_module(module_name: str, source: str) -> None:
                module_path = temp_root / "node_modules" / Path(module_name.replace("/", os.sep))
                module_path.parent.mkdir(parents=True, exist_ok=True)
                module_path.write_text(textwrap.dedent(source).strip() + "\n", encoding="utf-8")

            def write_package_manifest(package_name: str, manifest: dict[str, Any]) -> None:
                package_root = temp_root / "node_modules" / package_name
                package_root.mkdir(parents=True, exist_ok=True)
                (package_root / "package.json").write_text(
                    json.dumps(manifest),
                    encoding="utf-8",
                )

            write_module(
                "@eslint/js/index.js",
                """
                module.exports = {
                  configs: {
                    recommended: {
                      rules: {},
                    },
                  },
                };
                """,
            )
            write_package_manifest(
                "@eslint/js",
                {"name": "@eslint/js", "type": "commonjs", "main": "index.js"},
            )
            write_module(
                "@typescript-eslint/eslint-plugin/index.js",
                """
                module.exports = {
                  configs: {
                    recommended: {
                      rules: {},
                    },
                  },
                };
                """,
            )
            write_package_manifest(
                "@typescript-eslint/eslint-plugin",
                {
                    "name": "@typescript-eslint/eslint-plugin",
                    "type": "commonjs",
                    "main": "index.js",
                },
            )
            write_module(
                "@typescript-eslint/parser/index.js",
                """
                module.exports = {};
                """,
            )
            write_package_manifest(
                "@typescript-eslint/parser",
                {
                    "name": "@typescript-eslint/parser",
                    "type": "commonjs",
                    "main": "index.js",
                },
            )
            write_module(
                "eslint-plugin-react/index.js",
                """
                module.exports = {
                  configs: {
                    recommended: {
                      rules: {},
                    },
                  },
                };
                """,
            )
            write_package_manifest(
                "eslint-plugin-react",
                {"name": "eslint-plugin-react", "type": "commonjs", "main": "index.js"},
            )
            write_module(
                "eslint/config.js",
                """
                module.exports = {
                  defineConfig(config) {
                    return Array.isArray(config) ? config.flat(Infinity) : config;
                  },
                  globalIgnores(patterns, name) {
                    return { ignores: patterns, name };
                  },
                };
                """,
            )
            write_package_manifest(
                "eslint",
                {
                    "name": "eslint",
                    "type": "commonjs",
                    "exports": {"./config": "./config.js"},
                },
            )
            write_module(
                "globals/index.js",
                """
                module.exports = {
                  es2024: {},
                  browser: {},
                  node: {},
                  vitest: {},
                  jest: {},
                  mocha: {},
                };
                """,
            )
            write_package_manifest(
                "globals",
                {"name": "globals", "type": "commonjs", "main": "index.js"},
            )

            node_script = textwrap.dedent(
                f"""
                import config from {json.dumps(config_path.as_posix())};

                const containsJsonConfig = config.some(
                  (entry) =>
                    entry &&
                    typeof entry === "object" &&
                    (
                      String(entry.language ?? "").startsWith("json/") ||
                      (Array.isArray(entry.files) &&
                        entry.files.some((pattern) => /^\\*\\*\\/\\*\\.json(c|5)?$/.test(pattern)))
                    )
                );
                if (containsJsonConfig) {{
                  console.error("JSON config blocks should be omitted when @eslint/json is unavailable.");
                  process.exit(1);
                }}
                """
            )

            result = subprocess.run(  # nosec B603
                ["node", "--input-type=module", "-e", node_script],
                cwd=temp_root,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, f"{result.stdout}\n{result.stderr}")


if __name__ == "__main__":
    unittest.main()
