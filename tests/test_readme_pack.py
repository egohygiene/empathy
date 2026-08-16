# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import unittest

REPOSITORY_ROOT = Path(__file__).parents[1]
VALIDATOR_PATH = REPOSITORY_ROOT / "holon/packs/readme/tools/validate.py"
SPEC = importlib.util.spec_from_file_location("readme_pack_validator", VALIDATOR_PATH)
assert SPEC is not None
assert SPEC.loader is not None
validator = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = validator
SPEC.loader.exec_module(validator)


class ReadmePackTests(unittest.TestCase):
    def test_pack_contract_is_valid(self) -> None:
        self.assertEqual(validator.validate(), [])

    def test_templates_are_distinct_authoring_surfaces(self) -> None:
        project = validator.PROJECT_TEMPLATE.read_text(encoding="utf-8")
        profile = validator.PROFILE_TEMPLATE.read_text(encoding="utf-8")

        self.assertIn("{{PROJECT_NAME}}", project)
        self.assertIn("{{PROFILE_NAME}}", profile)
        self.assertNotEqual(project, profile)

    def test_profile_generated_regions_are_balanced(self) -> None:
        profile = validator.PROFILE_TEMPLATE.read_text(encoding="utf-8")
        self.assertEqual(
            validator.validate_generated_regions(profile, validator.PROFILE_TEMPLATE),
            [],
        )


if __name__ == "__main__":
    unittest.main()
