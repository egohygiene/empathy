from __future__ import annotations

import argparse
from collections.abc import Iterable
import html
import json
import os
from pathlib import Path
import tempfile
from typing import Any
import xml.etree.ElementTree as ET

DEFAULT_EXCLUDED_PATHS = [
    ".git",
    ".staging",
    ".cache",
    ".venv",
    "docs/generated",
    "node_modules",
    "vendor",
    "dist",
    "build",
    "coverage",
    "__pycache__",
    "site",
]


Node = dict[str, Any]


def positive_integer(raw_value: str) -> int:
    value = int(raw_value)
    if value < 1:
        raise argparse.ArgumentTypeError("must be at least 1")
    return value


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate repository intelligence tree artifacts.")
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--output-root", required=True)
    parser.add_argument("--max-depth", type=positive_integer, default=10)
    parser.add_argument(
        "--excluded-paths",
        default=",".join(DEFAULT_EXCLUDED_PATHS),
        help="Comma-separated repository-relative paths to exclude.",
    )
    return parser.parse_args()


def normalize_excluded_paths(raw_paths: str) -> list[str]:
    excluded: list[str] = []

    for raw_path in raw_paths.split(","):
        candidate = raw_path.strip().strip("/")

        if candidate:
            excluded.append(candidate)

    return excluded


def is_excluded(relative_path: Path, excluded_paths: Iterable[str]) -> bool:
    relative_path_string = relative_path.as_posix()

    for excluded_path in excluded_paths:
        if "/" not in excluded_path and excluded_path in relative_path.parts:
            return True
        if relative_path_string == excluded_path or relative_path_string.startswith(
            f"{excluded_path}/"
        ):
            return True

    return False


def build_tree(
    path: Path,
    repo_root: Path,
    excluded_paths: list[str],
    max_depth: int,
    depth: int = 0,
) -> Node:
    is_root = path == repo_root
    node_type = "directory" if path.is_dir() else "file"
    node: Node = {
        "name": repo_root.name if is_root else path.name,
        "path": "." if is_root else path.relative_to(repo_root).as_posix(),
        "type": node_type,
    }

    if node_type != "directory":
        return node

    if depth >= max_depth:
        node["truncated"] = True
        node["children"] = []
        return node

    children: list[Node] = []

    for child in sorted(
        path.iterdir(),
        key=lambda current: (
            not current.is_dir(),
            current.name.casefold(),
            current.name,
        ),
    ):
        relative_child = child.relative_to(repo_root)

        if is_excluded(relative_child, excluded_paths):
            continue

        if child.is_symlink():
            children.append(
                {
                    "name": child.name,
                    "path": relative_child.as_posix(),
                    "type": "symlink",
                }
            )
            continue

        children.append(
            build_tree(
                path=child,
                repo_root=repo_root,
                excluded_paths=excluded_paths,
                max_depth=max_depth,
                depth=depth + 1,
            )
        )

    node["children"] = children
    return node


def node_label(node: Node) -> str:
    suffix = "/" if node["type"] == "directory" else ""
    return f"{node['name']}{suffix}"


def render_ascii_tree(node: Node) -> str:
    lines = [node_label(node)]

    def walk(children: list[Node], prefix: str) -> None:
        for index, child in enumerate(children):
            is_last = index == len(children) - 1
            connector = "└── " if is_last else "├── "
            lines.append(f"{prefix}{connector}{node_label(child)}")

            if child.get("type") == "directory":
                nested_prefix = f"{prefix}{'    ' if is_last else '│   '}"
                nested_children = list(child.get("children", []))

                if child.get("truncated"):
                    lines.append(f"{nested_prefix}└── …")
                    continue

                walk(nested_children, nested_prefix)

    walk(list(node.get("children", [])), "")
    return "\n".join(lines) + "\n"


def append_xml(parent: ET.Element, node: Node) -> None:
    element_name = "directory" if node["type"] == "directory" else node["type"]
    element = ET.SubElement(
        parent,
        element_name,
        {
            "name": str(node["name"]),
            "path": str(node["path"]),
        },
    )

    if node.get("truncated"):
        element.set("truncated", "true")

    for child in list(node.get("children", [])):
        append_xml(element, child)


def render_xml(tree: Node) -> str:
    root = ET.Element(
        "repository",
        {
            "name": str(tree["name"]),
            "path": str(tree["path"]),
        },
    )

    for child in list(tree.get("children", [])):
        append_xml(root, child)

    ET.indent(root, space="  ")
    return ET.tostring(root, encoding="unicode", xml_declaration=True)


def render_html(ascii_tree: str, repository_name: str) -> str:
    escaped_tree = html.escape(ascii_tree)
    escaped_name = html.escape(repository_name)
    return f"""<!DOCTYPE html>
<html lang=\"en\">
  <head>
    <meta charset=\"utf-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
    <title>{escaped_name} Repository Structure</title>
    <style>
      body {{
        font-family: ui-monospace, SFMono-Regular, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
        margin: 2rem;
        line-height: 1.5;
      }}

      pre {{
        overflow-x: auto;
        white-space: pre;
      }}
    </style>
  </head>
  <body>
    <h1>Repository Structure</h1>
    <pre>{escaped_tree}</pre>
  </body>
</html>
"""


def render_markdown(ascii_tree: str) -> str:
    return "# Repository Structure\n\n```text\n" + ascii_tree + "```\n"


def render_svg(tree: Node) -> str:
    top_level_children = list(tree.get("children", []))
    preview_items = [node_label(child) for child in top_level_children[:6]]
    preview_text = " • ".join(preview_items) if preview_items else "Repository is empty."
    width = 960
    height = 220
    escaped_preview = html.escape(preview_text)
    escaped_name = html.escape(str(tree["name"]))
    escaped_count = html.escape(str(len(top_level_children)))

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
  <title id="title">{escaped_name} repository visualization</title>
  <desc id="desc">Deterministic repository visualization generated from the top-level repository tree.</desc>
  <rect width="{width}" height="{height}" rx="16" ry="16" fill="#0f172a" />
  <text x="32" y="64" fill="#e2e8f0" font-family="Arial, sans-serif" font-size="30" font-weight="700">{escaped_name}</text>
  <text x="32" y="104" fill="#94a3b8" font-family="Arial, sans-serif" font-size="20">Top-level entries: {escaped_count}</text>
  <text x="32" y="148" fill="#cbd5e1" font-family="Arial, sans-serif" font-size="18">{escaped_preview}</text>
  <text x="32" y="188" fill="#64748b" font-family="Arial, sans-serif" font-size="16">Generated locally without a third-party rendering service.</text>
</svg>
"""


def atomic_write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    file_descriptor, temporary_name = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
    )
    temporary_path = Path(temporary_name)

    try:
        with os.fdopen(file_descriptor, "w", encoding="utf-8", newline="") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, path)
    except BaseException:
        temporary_path.unlink(missing_ok=True)
        raise


def write_outputs(output_root: Path, tree: Node) -> None:
    tree_output_dir = output_root / "tree"
    visualization_output_dir = output_root / "visualization"
    tree_output_dir.mkdir(parents=True, exist_ok=True)
    visualization_output_dir.mkdir(parents=True, exist_ok=True)

    ascii_tree = render_ascii_tree(tree)

    atomic_write_text(tree_output_dir / "repo.tree", ascii_tree)
    atomic_write_text(
        tree_output_dir / "repo.md",
        render_markdown(ascii_tree),
    )
    atomic_write_text(
        tree_output_dir / "repo.json",
        json.dumps(tree, indent=2) + "\n",
    )
    atomic_write_text(
        tree_output_dir / "repo.xml",
        render_xml(tree) + "\n",
    )
    atomic_write_text(
        tree_output_dir / "repo.html",
        render_html(ascii_tree, str(tree["name"])),
    )
    atomic_write_text(
        visualization_output_dir / "repository.svg",
        render_svg(tree),
    )


def main() -> None:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    output_root = Path(args.output_root).resolve()
    if not repo_root.is_dir():
        raise SystemExit(f"Repository root is not a directory: {repo_root}")
    try:
        output_root.relative_to(repo_root)
    except ValueError as error:
        raise SystemExit(f"Output root must be inside the repository: {output_root}") from error

    excluded_paths = normalize_excluded_paths(args.excluded_paths)
    # Create the destination before scanning so a first run and a subsequent
    # run observe the same directory topology.
    output_root.mkdir(parents=True, exist_ok=True)

    tree = build_tree(
        path=repo_root,
        repo_root=repo_root,
        excluded_paths=excluded_paths,
        max_depth=args.max_depth,
    )
    write_outputs(output_root=output_root, tree=tree)


if __name__ == "__main__":
    main()
