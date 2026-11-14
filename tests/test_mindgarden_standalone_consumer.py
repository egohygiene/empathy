# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
# ruff: noqa: PT027
# Keep real owner qualification fixtures on dependency-free unittest.
"""Real external-owner golden integration; absent optional owner input is explicit."""

from __future__ import annotations

import importlib.metadata
import json
from pathlib import Path
import sys
import tempfile
from typing import TYPE_CHECKING
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
if TYPE_CHECKING:
    from tools import mindgarden_consumer as consumer
else:
    import mindgarden_consumer as consumer


class CorpusInputTests(unittest.TestCase):
    def test_drift_and_private_overlay_paths_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "source.md").write_text("new bytes\n", encoding="utf-8")
            for row in [
                {"path": "source.md", "sha256": "0" * 64},
                {"path": "../private.md", "sha256": "0" * 64},
                {"path": ".garden.local/private.md", "sha256": "0" * 64},
            ]:
                with self.subTest(row=row), self.assertRaises(ValueError):
                    consumer.source_bytes(root, row)

    def test_canonical_destination_is_refused(self) -> None:
        for destination in [ROOT / ".garden/new-export", ROOT / ".cache/../.garden/new-export"]:
            with (
                self.subTest(destination=destination),
                self.assertRaisesRegex(ValueError, "canonical knowledge"),
            ):
                consumer.build(ROOT, destination)
        with tempfile.TemporaryDirectory() as directory:
            alias = Path(directory) / "canonical-alias"
            alias.symlink_to(ROOT / ".garden", target_is_directory=True)
            with self.assertRaisesRegex(ValueError, "symlink alias"):
                consumer.build(ROOT, alias / "new-export")


class InstalledMindgardenGoldenTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        try:
            consumer.engine(ROOT)
        except (importlib.metadata.PackageNotFoundError, ValueError):
            message = "Optional pinned standalone Mindgarden absent; run selected standalone qualification"
            raise unittest.SkipTest(message) from None

    def test_corpus_is_deterministic_and_retains_source_review_states(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            parent = Path(directory)
            first = consumer.build(ROOT, parent / "first")
            second = consumer.build(ROOT, parent / "second")
            self.assertEqual(first, second)
            self.assertEqual(
                (parent / "first/index.json").read_bytes(),
                (parent / "second/index.json").read_bytes(),
            )
            self.assertEqual(19, first["source_count"])
            self.assertEqual(24, first["indexed_notes"])
            self.assertEqual(5, first["public_notes"])
            index = json.loads((parent / "first/index.json").read_text())
            captures = [note for note in index["notes"] if note["id"].startswith("capture-")]
            self.assertEqual(19, len(captures))
            self.assertTrue(
                all(note["status"] == "proposed" and not note["reviewed"] for note in captures)
            )
            self.assertTrue(first["canonical_input_hashes_unchanged"])
            with self.assertRaisesRegex(ValueError, "destination must be new"):
                consumer.build(ROOT, parent / "first")

    def test_private_and_unreviewed_evidence_cannot_enter_public_exchange(self) -> None:

        publishing = importlib.import_module("mindgarden.adapters.publishing")
        with tempfile.TemporaryDirectory() as directory:
            parent = Path(directory)
            consumer.build(ROOT, parent / "first")
            stage = parent / "first/repository"
            original = (stage / ".garden/home.md").read_text()
            private = (
                original.replace("id: empathy-garden-home", "id: private-fixture").replace(
                    "visibility: public", "visibility: private"
                )
                + "\nPRIVATE-CANARY-SYNTHETIC\n"
            )
            (stage / ".garden/inbox/private-fixture.md").write_text(private)
            result = parent / "safe-public"
            contract_error = importlib.import_module("mindgarden.domain.validation").ContractError
            with self.assertRaisesRegex(contract_error, "public garden cannot commit private"):
                publishing.project_garden(
                    stage, result, Path("mindgarden/profiles/quartz/profile.yaml")
                )
            self.assertFalse(result.exists())
            safe = parent / "first/public"
            text = "\n".join(path.read_text() for path in safe.rglob("*.md"))
            self.assertNotIn("PRIVATE-CANARY-SYNTHETIC", text)
            self.assertNotIn("Unreviewed imported source", text)
            self.assertFalse((safe / "sources").exists())

    def test_openwiki_and_obsidian_file_round_trips_do_not_promote_imports(self) -> None:
        for target in ["openwiki", "obsidian"]:
            with self.subTest(target=target), tempfile.TemporaryDirectory() as directory:
                parent = Path(directory)
                report = consumer.build(ROOT, parent / "exchange", target)
                self.assertEqual(target, report["exchange_prototype"])
                self.assertEqual("not-exercised", report["exchange_host_acceptance"])
                self.assertEqual(
                    (parent / "exchange/public/index.md").read_bytes(),
                    (parent / "exchange" / target / "index.md").read_bytes(),
                )
                note = (
                    parent / "exchange/repository/.garden/sources" / ("exchange-" + target + ".md")
                )
                self.assertIn("status: proposed\nreviewed: false", note.read_text())
                self.assertFalse(report["canonical_source_mutation"])


if __name__ == "__main__":
    unittest.main()
