# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Exercise effective REUSE metadata without editing retained third-party source."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


@unittest.skipUnless(
    importlib.util.find_spec("reuse"),
    "Install the declared EgoLint REUSE dependency to qualify attribution metadata",
)
class AttributionTests(unittest.TestCase):
    def metadata(self, root: Path, path: str) -> tuple[set[str], set[str]]:
        # The qualification dependency is optional for the ordinary offline suite.
        from reuse.project import Project  # noqa: PLC0415

        info = Project.from_directory(root).reuse_info_of(root / path)
        return (
            {str(value) for row in info for value in row.spdx_expressions},
            {str(value) for row in info for value in row.copyright_notices},
        )

    def test_unresolved_intake_never_inherits_first_party_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            shutil.copyfile(ROOT / "REUSE.toml", root / "REUSE.toml")
            for path in (
                ".staging/generated/new.svg",
                "beacon/.staging/unreviewed/readme.txt",
                "egolint/unreviewed.txt",
                "holon/unreviewed.txt",
                "other-owner/new.txt",
            ):
                with self.subTest(path=path):
                    target = root / path
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_text("unresolved source\n", encoding="utf-8")
                    self.assertEqual((set(), set()), self.metadata(root, path))

    def test_verified_baseline_and_explicit_headers_keep_their_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            shutil.copyfile(ROOT / "REUSE.toml", root / "REUSE.toml")
            for path in ("foundation/example.json", "docs/foundation/example.md"):
                target = root / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("baseline\n", encoding="utf-8")
                licenses, notices = self.metadata(root, path)
                self.assertEqual({"MIT"}, licenses)
                self.assertTrue(any("Ego Hygiene" in item for item in notices))
            path = "other-owner/source.py"
            target = root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(
                "# SPDX-FileCopyrightText: 2020 Synthetic upstream\n"
                "# SPDX-License-Identifier: BSD-3-Clause\n",
                encoding="utf-8",
            )
            licenses, notices = self.metadata(root, path)
            self.assertEqual({"BSD-3-Clause"}, licenses)
            self.assertFalse(any("Ego Hygiene" in item for item in notices))

    def test_reviewed_samples_keep_declared_license_and_original_author(self) -> None:
        deedy = "beacon/.staging/latex/CVs and Resumes/Deedy-Resume/README.md"
        licenses, notices = self.metadata(ROOT, deedy)
        self.assertEqual({"Apache-2.0"}, licenses)
        self.assertTrue(any("Debarghya Das" in item for item in notices))
        self.assertFalse(any("Ego Hygiene" in item for item in notices))
        licenses, notices = self.metadata(
            ROOT, "beacon/.staging/latex/Community/TeXtured/README.md"
        )
        self.assertEqual({"CC0-1.0"}, licenses)
        self.assertEqual(set(), notices, "No unsupported author claim is invented")
        for path in (
            ".staging/tools/emoji-precache/assets/emojis/noto_261d_1f3fe_svg.svg",
            ".staging/tools/emoji-precache/assets/emojis/noto_1faf0_svg.pdf",
        ):
            self.assertEqual((set(), set()), self.metadata(ROOT, path))


if __name__ == "__main__":
    unittest.main()
