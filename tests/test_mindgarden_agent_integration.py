# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
# pylint: disable=wrong-import-position

from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest

REPOSITORY_ROOT = Path(__file__).parents[1]
MINDGARDEN_ROOT = REPOSITORY_ROOT / "mindgarden"
sys.path.insert(0, str(MINDGARDEN_ROOT))

from scripts.garden_agent import (  # noqa: E402
    build_index,
    canonical_json,
    load_context_pack,
    render_context_markdown,
    render_llms_txt,
)
from scripts.validate_garden import validate_repository  # noqa: E402


class MindgardenAgentIntegrationTests(unittest.TestCase):
    def test_repository_agent_projection_is_current_and_deterministic(self) -> None:
        self.assertEqual(validate_repository(REPOSITORY_ROOT), 4)
        first = canonical_json(build_index(REPOSITORY_ROOT))
        second = canonical_json(build_index(REPOSITORY_ROOT))
        self.assertEqual(first, second)

        index = json.loads(first)
        expected_llms = render_llms_txt(REPOSITORY_ROOT, index)
        self.assertEqual(
            (REPOSITORY_ROOT / "llms.txt").read_text(encoding="utf8"),
            expected_llms,
        )

    def test_default_context_pack_is_reviewed_and_bounded(self) -> None:
        index = build_index(REPOSITORY_ROOT)
        _, profile = load_context_pack(REPOSITORY_ROOT, "empathy-agent-default")
        rendered = render_context_markdown(REPOSITORY_ROOT, index, profile)

        self.assertLessEqual(len(rendered), profile["max_characters"])
        self.assertNotIn("reviewed=`false`", rendered)
        self.assertIn("<mindgarden-note", rendered)

    def test_task_contract_exposes_agent_verification(self) -> None:
        root_taskfile = (REPOSITORY_ROOT / "Taskfile.yml").read_text(encoding="utf8")
        taskfile = (REPOSITORY_ROOT / ".tasks/mindgarden.yml").read_text(encoding="utf8")
        self.assertIn("taskfile: ./.tasks/mindgarden.yml", root_taskfile)
        self.assertIn("mindgarden/scripts/garden_agent.py", taskfile)
        self.assertIn("garden:index:", taskfile)
        self.assertIn("garden:context:", taskfile)
        self.assertIn("garden:llms:write:", taskfile)


if __name__ == "__main__":
    unittest.main()
