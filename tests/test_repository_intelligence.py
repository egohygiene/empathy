from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

MODULE_PATH = (
    Path(__file__).parents[1]
    / ".github"
    / "actions"
    / "generate-repository-intelligence"
    / "generate_repository_intelligence.py"
)
SPEC = importlib.util.spec_from_file_location("repository_intelligence", MODULE_PATH)
assert SPEC and SPEC.loader
repository_intelligence = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(repository_intelligence)


class RepositoryIntelligenceTests(unittest.TestCase):
    def test_normalizes_and_removes_empty_exclusions(self) -> None:
        self.assertEqual(
            repository_intelligence.normalize_excluded_paths(" .git, /dist/ ,, build "),
            [".git", "dist", "build"],
        )

    def test_build_tree_is_sorted_and_excludes_named_directories(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            repository_root = Path(temporary_directory)
            (repository_root / "zeta.txt").write_text("zeta\n", encoding="utf-8")
            (repository_root / "alpha").mkdir()
            (repository_root / "alpha" / "value.txt").write_text("value\n", encoding="utf-8")
            (repository_root / "node_modules").mkdir()
            (repository_root / "node_modules" / "ignored.js").write_text(
                "ignored\n", encoding="utf-8"
            )

            tree = repository_intelligence.build_tree(
                path=repository_root,
                repo_root=repository_root,
                excluded_paths=["node_modules"],
                max_depth=5,
            )

            self.assertEqual(
                [child["name"] for child in tree["children"]],
                ["alpha", "zeta.txt"],
            )

    def test_write_outputs_produces_parseable_json(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            output_root = Path(temporary_directory)
            tree = {
                "name": "example",
                "path": ".",
                "type": "directory",
                "children": [],
            }

            repository_intelligence.write_outputs(output_root, tree)

            json_output = output_root / "tree" / "repo.json"
            self.assertEqual(json.loads(json_output.read_text(encoding="utf-8")), tree)
            self.assertTrue((output_root / "visualization" / "repository.svg").is_file())


if __name__ == "__main__":
    unittest.main()
