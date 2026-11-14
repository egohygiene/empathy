# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Protect immutable owner admission and consumer asset preservation."""

from __future__ import annotations

import json
from pathlib import Path
import tempfile
from typing import TYPE_CHECKING
import unittest
from unittest.mock import patch

from tools import website_baseline as consumer

if TYPE_CHECKING:
    from collections.abc import Callable


class WebsiteBaselineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.owner = self.root / "owner"
        self.owner.mkdir()
        self.inputs = self.root / "inputs"
        self.inputs.mkdir()
        profile = self.owner / "profile.json"
        profile.write_text("{}\n", encoding="utf-8")
        for arguments in (
            ["init", "-q"],
            ["add", "profile.json"],
            [
                "-c",
                "user.name=Consumer Fixture",
                "-c",
                "user.email=fixture@invalid",
                "-c",
                "commit.gpgsign=false",
                "commit",
                "-qm",
                "fixture",
            ],
        ):
            consumer.run(["git", *arguments], cwd=self.owner, capture=True)
        revision = consumer.run(["git", "rev-parse", "HEAD"], cwd=self.owner, capture=True).strip()
        self.pin = {
            "revision": revision,
            "profile": "profile.json",
            "profile_sha256": consumer.sha256(profile),
        }
        self.write_source()
        self.patch = patch.object(consumer, "INPUTS", self.inputs)
        self.patch.start()
        self.addCleanup(self.patch.stop)

    def write_source(self) -> None:
        (self.inputs / "source.json").write_text(json.dumps({"holon": self.pin}), encoding="utf-8")

    def expect_refusal(self, action: Callable[[], object]) -> None:
        try:
            action()
        except consumer.ConsumerError:
            return
        self.fail("Expected the consumer boundary to refuse the operation")

    def test_exact_clean_git_source_and_profile_are_admitted(self) -> None:
        self.assertEqual(consumer.owner_source(self.owner), self.pin)

    def test_dirty_source_is_refused_before_execution(self) -> None:
        (self.owner / "profile.json").write_text('{"local":true}\n', encoding="utf-8")
        self.expect_refusal(lambda: consumer.owner_source(self.owner))

    def test_different_git_revision_is_not_an_accepted_owner(self) -> None:
        self.pin["revision"] = "0" * 40
        self.write_source()
        self.expect_refusal(lambda: consumer.owner_source(self.owner))

    def test_profile_digest_must_match_even_at_the_selected_revision(self) -> None:
        self.pin["profile_sha256"] = "0" * 64
        self.write_source()
        self.expect_refusal(lambda: consumer.owner_source(self.owner))

    def test_symlink_aliases_cannot_redirect_source_or_asset_writes(self) -> None:
        alias = self.root / "alias"
        alias.symlink_to(self.owner, target_is_directory=True)
        self.expect_refusal(lambda: consumer.owner_source(alias))
        asset = self.root / "asset"
        asset.symlink_to(self.owner / "profile.json")
        before = (self.owner / "profile.json").read_bytes()
        self.expect_refusal(lambda: consumer.copy_new(asset, b"replacement"))
        self.assertEqual((self.owner / "profile.json").read_bytes(), before)

    def test_replay_is_idempotent_and_local_asset_changes_are_preserved(self) -> None:
        asset = self.root / "consumer/assets/site.css"
        consumer.copy_new(asset, b"original")
        consumer.copy_new(asset, b"original")
        asset.write_bytes(b"consumer-local-edit")
        self.expect_refusal(lambda: consumer.copy_new(asset, b"new-owner-value"))
        self.assertEqual(asset.read_bytes(), b"consumer-local-edit")


if __name__ == "__main__":
    unittest.main()
