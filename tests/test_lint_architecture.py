# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Contract tests for the generated lint architecture artifacts."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import unittest
import xml.etree.ElementTree as ET

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = (
    REPOSITORY_ROOT / ".github/actions/generate-lint-infographic/generate_lint_infographic.py"
)
SPECIFICATION = importlib.util.spec_from_file_location(
    "generate_lint_infographic",
    SCRIPT_PATH,
)
if SPECIFICATION is None or SPECIFICATION.loader is None:
    raise RuntimeError(SCRIPT_PATH)
GENERATOR = importlib.util.module_from_spec(SPECIFICATION)
sys.modules[SPECIFICATION.name] = GENERATOR
SPECIFICATION.loader.exec_module(GENERATOR)


class LintArchitectureContractTests(unittest.TestCase):
    """Verify source fidelity, determinism, and artifact validity."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.inventory = GENERATOR.build_inventory(REPOSITORY_ROOT)
        cls.markdown_path = REPOSITORY_ROOT / ".reports/egolint/architecture/README.md"
        cls.svg_path = REPOSITORY_ROOT / ".reports/egolint/architecture/lint-architecture.svg"

    def test_inventory_reads_both_canonical_matrices(self) -> None:
        self.assertEqual(self.inventory.megalinter_total, 124)
        self.assertEqual(self.inventory.megalinter_fast, 12)
        self.assertEqual(self.inventory.megalinter_holistic, 107)
        self.assertEqual(self.inventory.complementary_total, 18)
        self.assertEqual(
            self.inventory.megalinter_enabled
            + self.inventory.megalinter_conditional
            + self.inventory.megalinter_disabled,
            self.inventory.megalinter_total,
        )
        self.assertEqual(
            self.inventory.complementary_enabled
            + self.inventory.complementary_conditional
            + self.inventory.complementary_disabled,
            self.inventory.complementary_total,
        )

    def test_generated_artifacts_are_current(self) -> None:
        self.assertEqual(
            self.markdown_path.read_text(encoding="utf-8"),
            GENERATOR.render_markdown(self.inventory),
        )
        self.assertEqual(
            self.svg_path.read_text(encoding="utf-8"),
            GENERATOR.render_svg(self.inventory),
        )

    def test_svg_is_valid_xml_with_accessible_metadata(self) -> None:
        # The parsed SVG is a trusted artifact generated in this test suite.
        root = ET.parse(self.svg_path).getroot()  # noqa: S314
        namespace = {"svg": "http://www.w3.org/2000/svg"}
        self.assertIsNotNone(root.find("svg:title", namespace))
        self.assertIsNotNone(root.find("svg:desc", namespace))
        self.assertEqual(root.attrib["role"], "img")

    def test_legend_documents_every_execution_and_report_path(self) -> None:
        markdown = self.markdown_path.read_text(encoding="utf-8")
        for phrase in (
            "Taskfile",
            "VS Code",
            "Git hooks",
            "Pull requests",
            "Trusted runs",
            ".reports/megalinter/",
            ".reports/complementary/<tool>/latest.json",
            ".reports/osv/",
            "GitHub Code Scanning",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, markdown)

    def test_output_directory_rejects_traversal(self) -> None:
        with self.assertRaises(ValueError):  # noqa: PT027
            GENERATOR.output_paths(REPOSITORY_ROOT, "../architecture")

    def test_output_directory_rejects_nested_destinations(self) -> None:
        with self.assertRaises(ValueError):  # noqa: PT027
            GENERATOR.output_paths(
                REPOSITORY_ROOT,
                ".reports/egolint/architecture/history",
            )


if __name__ == "__main__":
    unittest.main()
