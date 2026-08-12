# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

from __future__ import annotations

from datetime import date
from pathlib import Path
import re
import unittest

REPOSITORY_ROOT = Path(__file__).parents[1]

ARCHITECTURE_DOCUMENTS = {
    "AI_CONSTITUTION.md": "empathy-ai-constitution",
    "ARCHITECTURE.md": "empathy-architecture",
    "DECISIONS.md": "empathy-decisions",
    "DESIGN.md": "empathy-design",
    "DESIGN_SYSTEM.md": "empathy-design-system",
    "EPISTEMOLOGY.md": "empathy-epistemology",
    "FOUNDATIONS.md": "empathy-foundations",
    "MANIFESTO.md": "empathy-manifesto",
    "META.md": "empathy-meta",
    "METHODOLOGY.md": "empathy-methodology",
    "ONTOLOGY.md": "empathy-ontology",
    "PERSONAL_MODEL.md": "empathy-personal-model",
    "PILLARS.md": "empathy-pillars",
    "PRINCIPLES.md": "empathy-principles",
    "PURPOSE.md": "empathy-purpose",
    "ROADMAP.md": "empathy-roadmap",
    "SYSTEM.md": "empathy-system",
    "VISION.md": "empathy-vision",
}

REQUIRED_FIELDS = {
    "schema",
    "id",
    "title",
    "kind",
    "version",
    "status",
    "owners",
    "created",
    "updated",
    "governed_by",
    "depends_on",
    "related",
    "supersedes",
}

FRONTMATTER_PATTERN = re.compile(r"\A---\n(?P<body>.*?)\n---\n", re.DOTALL)


def parse_simple_frontmatter(path: Path) -> dict[str, str | list[str]]:
    """Parse the scalar/list subset used by architecture-document metadata."""
    text = path.read_text(encoding="utf8")
    match = FRONTMATTER_PATTERN.match(text)
    if match is None:
        raise AssertionError(f"missing YAML frontmatter: {path.relative_to(REPOSITORY_ROOT)}")

    metadata: dict[str, str | list[str]] = {}
    active_list: str | None = None
    for line in match.group("body").splitlines():
        if line.startswith("  - "):
            if active_list is None:
                raise AssertionError(f"orphan list item in {path.relative_to(REPOSITORY_ROOT)}")
            value = line.removeprefix("  - ").strip().strip('"')
            current_values = metadata[active_list]
            if not isinstance(current_values, list):
                raise AssertionError(f"invalid list field {active_list} in {path}")
            current_values.append(value)
            continue

        if ":" not in line:
            raise AssertionError(f"unsupported frontmatter line in {path}: {line}")
        key, raw_value = line.split(":", 1)
        value = raw_value.strip().strip('"')
        if value == "[]":
            metadata[key] = []
            active_list = None
        elif value:
            metadata[key] = value
            active_list = None
        else:
            metadata[key] = []
            active_list = key
    return metadata


def find_dependency_cycle(graph: dict[str, list[str]]) -> list[str] | None:
    """Return one dependency cycle, including the repeated node, when present."""
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str, path: list[str]) -> list[str] | None:
        if node in visiting:
            cycle_start = path.index(node)
            return [*path[cycle_start:], node]
        if node in visited:
            return None

        visiting.add(node)
        for dependency in graph[node]:
            cycle = visit(dependency, [*path, node])
            if cycle is not None:
                return cycle
        visiting.remove(node)
        visited.add(node)
        return None

    for document_id in graph:
        cycle = visit(document_id, [])
        if cycle is not None:
            return cycle
    return None


class ArchitectureDocumentContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.documents = {
            filename: parse_simple_frontmatter(REPOSITORY_ROOT / filename)
            for filename in ARCHITECTURE_DOCUMENTS
        }

    def test_complete_document_set_has_canonical_metadata(self) -> None:
        observed_ids: set[str] = set()
        for filename, expected_id in ARCHITECTURE_DOCUMENTS.items():
            path = REPOSITORY_ROOT / filename
            self.assertTrue(path.is_file(), filename)
            metadata = self.documents[filename]

            self.assertEqual(set(metadata), REQUIRED_FIELDS, filename)
            self.assertEqual(metadata["schema"], "aether.architecture-document/v1", filename)
            self.assertEqual(metadata["id"], expected_id, filename)
            self.assertEqual(metadata["kind"], "architecture-document", filename)
            self.assertEqual(metadata["version"], "0.1.0", filename)
            self.assertEqual(metadata["status"], "draft", filename)
            self.assertEqual(metadata["owners"], ["egohygiene"], filename)
            date.fromisoformat(str(metadata["created"]))
            date.fromisoformat(str(metadata["updated"]))

            document_id = str(metadata["id"])
            self.assertNotIn(document_id, observed_ids, document_id)
            observed_ids.add(document_id)

    def test_document_structure_has_no_template_placeholders(self) -> None:
        placeholder_patterns = [
            "replace-with",
            "Replace With",
            "YYYY-MM-DD",
            "Pillar 1 — Replace",
            "Principle 1 — Replace",
        ]
        for filename in ARCHITECTURE_DOCUMENTS:
            text = (REPOSITORY_ROOT / filename).read_text(encoding="utf8")
            h1_headings = re.findall(r"^# [^#].+$", text, flags=re.MULTILINE)
            self.assertEqual(len(h1_headings), 1, filename)
            self.assertIn("\n## Validation\n", text, filename)
            for placeholder in placeholder_patterns:
                self.assertNotIn(placeholder, text, filename)

    def test_governing_specifications_resolve(self) -> None:
        specification_metadata = {
            str(metadata["id"]): metadata
            for specification_path in (
                REPOSITORY_ROOT / "egolint/.agents/specs/architecture"
            ).rglob("*.spec.md")
            if (metadata := parse_simple_frontmatter(specification_path))
        }
        meta_document = (REPOSITORY_ROOT / "META.md").read_text(encoding="utf8")

        for filename, metadata in self.documents.items():
            governing_ids = metadata["governed_by"]
            self.assertIsInstance(governing_ids, list, filename)
            self.assertEqual(len(governing_ids), 1, filename)
            governing_id = governing_ids[0]
            self.assertIn(governing_id, specification_metadata, filename)
            governing_version = specification_metadata[governing_id]["version"]
            self.assertIn(f"`{governing_id}@{governing_version}`", meta_document, filename)

    def test_relationships_resolve_and_dependencies_are_acyclic(self) -> None:
        known_ids = {str(metadata["id"]) for metadata in self.documents.values()}
        dependency_graph: dict[str, list[str]] = {}

        for filename, metadata in self.documents.items():
            document_id = str(metadata["id"])
            dependencies = metadata["depends_on"]
            related_documents = metadata["related"]
            superseded_documents = metadata["supersedes"]
            self.assertIsInstance(dependencies, list, filename)
            self.assertIsInstance(related_documents, list, filename)
            self.assertIsInstance(superseded_documents, list, filename)
            for relationship in [dependencies, related_documents, superseded_documents]:
                self.assertTrue(set(relationship).issubset(known_ids), filename)
                self.assertNotIn(document_id, relationship, filename)
            dependency_graph[document_id] = dependencies

        self.assertIsNone(find_dependency_cycle(dependency_graph))

    def test_meta_inventory_covers_every_document(self) -> None:
        meta_document = (REPOSITORY_ROOT / "META.md").read_text(encoding="utf8")
        for filename, document_id in ARCHITECTURE_DOCUMENTS.items():
            self.assertIn(f"]({filename})", meta_document, filename)
            self.assertIn(f"`{document_id}`", meta_document, filename)


if __name__ == "__main__":
    unittest.main()
