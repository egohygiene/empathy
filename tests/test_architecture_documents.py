# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
"""Consume pinned Aether authority rather than maintaining a second validator."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
from typing import Any, ClassVar
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ArchitectureDocumentTests(unittest.TestCase):
    owner: ClassVar[Any]
    schema: ClassVar[dict[str, Any]]
    documents: ClassVar[list[Any]]

    @classmethod
    def setUpClass(cls) -> None:
        selected = os.environ.get("AETHER_ROOT")
        if not selected:
            message = "Pinned Aether owner input unavailable; run garden:architecture:check with AETHER_ROOT"
            raise unittest.SkipTest(message)
        root = Path(selected).resolve()
        inputs = json.loads(
            (ROOT / "integrations/mindgarden/architecture-source-comparison.json").read_text()
        )
        for row in inputs["validation_inputs"]:
            source = root / row["path"]
            if (
                source.is_symlink()
                or hashlib.sha256(source.read_bytes()).hexdigest() != row["sha256"]
            ):
                message = "Aether validation source does not match the selected immutable input"
                raise ValueError(message)
        validator = root / inputs["validation_inputs"][0]["path"]
        spec = importlib.util.spec_from_file_location("selected_aether_architecture", validator)
        if spec is None or spec.loader is None:
            message = "Selected Aether validator cannot be loaded"
            raise ValueError(message)
        cls.owner = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = cls.owner
        spec.loader.exec_module(cls.owner)
        if cls.owner.jsonschema is None:
            message = "Selected native qualification requires the owner's jsonschema prerequisite"
            raise RuntimeError(message)
        cls.schema = json.loads((root / inputs["validation_inputs"][1]["path"]).read_text())
        cls.documents, errors = cls.owner.discover(ROOT)
        if errors:
            raise ValueError(errors)

    def test_current_documents_pass_actual_owner_contract(self) -> None:
        self.assertEqual([], self.owner.validate_schema(self.documents, self.schema))
        self.assertEqual([], self.owner.validate_markdown(ROOT, self.documents))
        self.assertEqual([], self.owner.validate_graph(self.documents))
        self.assertEqual([], self.owner.validate_meta(self.documents))

    def test_indexed_identities_match_the_actual_native_documents(self) -> None:
        selection = json.loads((ROOT / "integrations/mindgarden/corpus.json").read_text())
        expected = {row["artifact_id"] for row in selection["sources"] if "/" not in row["path"]}
        self.assertEqual(expected, {document.metadata["id"] for document in self.documents})

    def test_missing_metadata_is_rejected_by_owner(self) -> None:
        document = copy.deepcopy(self.documents[0])
        del document.metadata["id"]
        errors = self.owner.validate_schema([document], self.schema)
        self.assertTrue(errors)
        self.assertTrue(any("id" in error for error in errors))

    def test_valid_version_and_lifecycle_are_not_frozen_to_old_draft_fixture(self) -> None:
        document = copy.deepcopy(self.documents[0])
        document.metadata["version"] = "2.7.0"
        document.metadata["status"] = "active"
        self.assertEqual([], self.owner.validate_schema([document], self.schema))

    def test_duplicate_and_cyclic_identities_are_rejected_by_owner(self) -> None:
        first = copy.deepcopy(self.documents[0])
        second = copy.deepcopy(self.documents[1])
        second.metadata["id"] = first.metadata["id"]
        self.assertTrue(
            any("duplicate id" in error for error in self.owner.validate_graph([first, second]))
        )
        first.metadata.update(id="fixture-one", depends_on=["fixture-two"])
        second.metadata.update(id="fixture-two", depends_on=["fixture-one"])
        self.assertTrue(
            any("dependency cycle" in error for error in self.owner.validate_graph([first, second]))
        )


if __name__ == "__main__":
    unittest.main()
