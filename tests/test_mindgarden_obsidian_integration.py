# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

from __future__ import annotations

import json
from pathlib import Path
import unittest

REPOSITORY_ROOT = Path(__file__).parents[1]


class MindgardenObsidianIntegrationTests(unittest.TestCase):
    def test_profile_uses_native_features_and_no_required_community_plugins(self) -> None:
        profile = json.loads(
            (REPOSITORY_ROOT / "mindgarden/profiles/obsidian/profile.json").read_text(
                encoding="utf8"
            )
        )
        self.assertEqual(profile["schema"], "mindgarden.obsidian-profile/v0")
        self.assertEqual(profile["vaultRoot"], ".")
        self.assertIn("bases", profile["nativeFeatures"])
        self.assertEqual(profile["requiredCommunityPlugins"], [])

        optional_plugins = {plugin["id"]: plugin for plugin in profile["optionalCommunityPlugins"]}
        self.assertEqual(optional_plugins["project-manager"]["version"], "1.8.0")
        self.assertEqual(
            optional_plugins["project-manager"]["source"],
            "https://github.com/StepanKropachev/obsidian-pm",
        )

    def test_profile_paths_resolve_in_empathy(self) -> None:
        profile = json.loads(
            (REPOSITORY_ROOT / "mindgarden/profiles/obsidian/profile.json").read_text(
                encoding="utf8"
            )
        )
        for field in (
            "gardenRoot",
            "configurationRoot",
            "templatesRoot",
            "attachmentsRoot",
            "dashboard",
        ):
            self.assertTrue((REPOSITORY_ROOT / profile[field]).exists(), field)

    def test_only_shareable_obsidian_state_is_committed(self) -> None:
        configuration_root = REPOSITORY_ROOT / ".obsidian"
        self.assertFalse((configuration_root / "plugins").exists())
        for local_name in (
            "workspace.json",
            "workspace-mobile.json",
            "workspaces.json",
        ):
            self.assertFalse((configuration_root / local_name).exists(), local_name)

        ignore_policy = (REPOSITORY_ROOT / ".gitignore").read_text(encoding="utf8")
        for ignored_path in (
            ".obsidian/plugins/",
            ".obsidian/workspace*.json",
        ):
            self.assertIn(ignored_path, ignore_policy)

    def test_dashboard_uses_native_base_and_scoped_css(self) -> None:
        dashboard = (REPOSITORY_ROOT / ".garden/dashboard.md").read_text(encoding="utf8")
        base = (REPOSITORY_ROOT / ".garden/views/knowledge.base").read_text(encoding="utf8")
        css = (REPOSITORY_ROOT / ".obsidian/snippets/mindgarden.css").read_text(encoding="utf8")

        self.assertIn("mindgarden-dashboard", dashboard)
        self.assertIn("![[views/knowledge.base#Knowledge]]", dashboard)
        self.assertIn('file.inFolder(".garden")', base)
        self.assertIn("name: Needs review", base)
        self.assertIn("name: Projects", base)
        self.assertIn(".mindgarden-dashboard", css)

    def test_obsidian_profile_schema_is_valid_json(self) -> None:
        schema = json.loads(
            (REPOSITORY_ROOT / "mindgarden/contracts/obsidian-profile.schema.json").read_text(
                encoding="utf8"
            )
        )
        self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")


if __name__ == "__main__":
    unittest.main()
