# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Contract tests for the universal dependency-review workflow."""

from __future__ import annotations

from pathlib import Path
import re
import unittest

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


class DependencyReviewWorkflowTests(unittest.TestCase):
    """Keep the promoted workflow narrow, pinned, and read-only."""

    def test_dependency_review_is_a_pinned_pull_request_gate(self) -> None:
        workflow = (REPOSITORY_ROOT / ".github/workflows/dependency-review.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("pull_request:", workflow)
        self.assertIn("permissions: {}", workflow)
        self.assertIn("contents: read", workflow)
        self.assertNotIn("contents: write", workflow)
        self.assertIn("vars.DEPENDENCY_REVIEW_ENABLED == 'true'", workflow)
        match = re.search(r"actions/dependency-review-action@([0-9a-f]{40})", workflow)
        self.assertIsNotNone(match)
        self.assertIn("fail-on-severity: high", workflow)
        self.assertIn("comment-summary-in-pr: never", workflow)

if __name__ == "__main__":
    unittest.main()
