#!/usr/bin/env python3
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Generate and validate the repository's public Task command catalog."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

START_MARKER = "<!-- BEGIN GENERATED TASK CATALOG -->"
END_MARKER = "<!-- END GENERATED TASK CATALOG -->"


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repository-root",
        type=Path,
        default=Path.cwd(),
        help="Repository root containing Taskfile.yml and TASKS.md.",
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="Check the catalog.")
    mode.add_argument("--write", action="store_true", help="Update the catalog.")
    return parser.parse_args()


def task_binary() -> str:
    """Resolve the Task executable used to inspect the live command surface."""
    configured = os.environ.get("TASK_BIN", "task")
    resolved = shutil.which(configured)
    if resolved is None:
        raise RuntimeError(f"Task executable is unavailable: {configured}")
    return resolved


def public_tasks(repository_root: Path) -> list[dict[str, object]]:
    """Return public described tasks from Task's canonical JSON output."""
    completed = subprocess.run(
        [task_binary(), "--dir", str(repository_root), "--list", "--json"],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(completed.stdout)
    tasks = payload.get("tasks", [])
    return sorted(tasks, key=lambda item: str(item["name"]))


def escape_cell(value: object) -> str:
    """Escape a value for a compact Markdown table cell."""
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def render_catalog(tasks: list[dict[str, object]]) -> str:
    """Render the generated Markdown catalog body."""
    lines = [
        START_MARKER,
        "",
        f"_Generated from the live Taskfile graph: {len(tasks)} public commands._",
        "",
        "| Command | Description | Aliases |",
        "| --- | --- | --- |",
    ]
    for task in tasks:
        aliases = task.get("aliases", [])
        alias_text = ", ".join(f"`{escape_cell(alias)}`" for alias in aliases)
        lines.append(
            "| "
            f"`task {escape_cell(task['name'])}` | "
            f"{escape_cell(task.get('desc', ''))} | "
            f"{alias_text or '—'} |"
        )
    lines.extend(["", END_MARKER])
    return "\n".join(lines)


def update_catalog(document: str, catalog: str) -> str:
    """Replace the generated region in TASKS.md."""
    if document.count(START_MARKER) != 1 or document.count(END_MARKER) != 1:
        raise RuntimeError("TASKS.md must contain exactly one generated region")
    prefix, remainder = document.split(START_MARKER, maxsplit=1)
    _, suffix = remainder.split(END_MARKER, maxsplit=1)
    return f"{prefix}{catalog}{suffix}"


def main() -> int:
    """Generate or verify TASKS.md."""
    arguments = parse_arguments()
    repository_root = arguments.repository_root.resolve()
    catalog_path = repository_root / "TASKS.md"
    current = catalog_path.read_text(encoding="utf-8")
    expected = update_catalog(current, render_catalog(public_tasks(repository_root)))

    if arguments.write:
        catalog_path.write_text(expected, encoding="utf-8")
        print(f"Updated {catalog_path.relative_to(repository_root)}")
        return 0

    if current != expected:
        print(
            "TASKS.md is stale; run `task taskfile:catalog:write`.",
            file=sys.stderr,
        )
        return 1

    print("TASKS.md matches the public Taskfile command surface.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
