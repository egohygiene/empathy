# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest

MODULE_PATH = (
    Path(__file__).parents[1]
    / ".github"
    / "actions"
    / "validate-automation"
    / "validate_automation.py"
)
SPEC = importlib.util.spec_from_file_location("validate_automation", MODULE_PATH)
assert SPEC is not None
assert SPEC.loader is not None
validate_automation = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = validate_automation
SPEC.loader.exec_module(validate_automation)


class ValidateAutomationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.repository_root = Path(self.temporary_directory.name)
        (self.repository_root / ".github" / "workflows").mkdir(parents=True)
        (self.repository_root / ".github" / "actions").mkdir(parents=True)

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def write_workflow(self, content: str, name: str = "ci.yml") -> Path:
        path = self.repository_root / ".github" / "workflows" / name
        path.write_text(content, encoding="utf-8")
        return path

    def test_accepts_pinned_least_privilege_workflow(self) -> None:
        self.write_workflow(
            """---
name: CI
on: workflow_dispatch
permissions:
  contents: read
jobs:
  validate:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@d23441a48e516b6c34aea4fa41551a30e30af803
"""
        )

        self.assertEqual(validate_automation.validate(self.repository_root), [])

    def test_rejects_mutable_action_reference(self) -> None:
        path = self.write_workflow(
            """---
name: CI
on: workflow_dispatch
permissions:
  contents: read
jobs:
  validate:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v6
"""
        )

        findings = validate_automation.check_workflow(path)

        self.assertTrue(
            any("full commit SHA" in finding.message for finding in findings),
            findings,
        )

    def test_rejects_mutable_container_action(self) -> None:
        path = self.write_workflow(
            """---
name: CI
on: workflow_dispatch
permissions: {}
jobs:
  validate:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: docker://alpine:3.22
"""
        )

        findings = validate_automation.check_workflow(path)

        self.assertTrue(
            any("SHA-256 image digest" in finding.message for finding in findings),
            findings,
        )

    def test_validates_yaml_workflow_extension(self) -> None:
        self.write_workflow(
            """---
name: CI
on: workflow_dispatch
permissions:
  contents: read
jobs:
  validate:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v7
""",
            name="ci.yaml",
        )

        findings = validate_automation.validate(self.repository_root)

        self.assertTrue(
            any("full commit SHA" in finding.message for finding in findings),
            findings,
        )

    def test_rejects_missing_job_timeout(self) -> None:
        path = self.write_workflow(
            """---
name: CI
on: workflow_dispatch
permissions: {}
jobs:
  validate:
    runs-on: ubuntu-latest
    steps: []
"""
        )

        findings = validate_automation.check_workflow(path)

        self.assertTrue(
            any("timeout-minutes" in finding.message for finding in findings),
            findings,
        )

    def test_rejects_multiple_yaml_documents(self) -> None:
        path = self.write_workflow(
            """---
name: First
on: workflow_dispatch
permissions: {}
jobs: {}
---
name: Second
"""
        )

        findings = validate_automation.check_workflow(path)

        self.assertTrue(
            any("exactly one YAML document" in finding.message for finding in findings),
            findings,
        )


if __name__ == "__main__":
    unittest.main()
