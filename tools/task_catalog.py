#!/usr/bin/env python3
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
# Standalone repository-maintenance entry point, not a Python package.
# ruff: noqa: INP001

"""Generate and validate the repository's public Task command catalog."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess  # nosec B404 - explicit local Task executable, fixed argv, no shell.
import sys
from typing import TypedDict

START_MARKER = "<!-- BEGIN GENERATED TASK CATALOG -->"
END_MARKER = "<!-- END GENERATED TASK CATALOG -->"


class TaskRecord(TypedDict):
    """The Task-owned fields this Markdown projection consumes."""

    name: str
    desc: str
    aliases: list[str]


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
        message = f"Task executable is unavailable: {configured}"
        raise RuntimeError(message)
    return resolved


def parse_tasks(payload: object) -> list[TaskRecord]:
    """Validate the consumed JSON fields instead of stringifying malformed data."""
    if not isinstance(payload, dict):
        message = "Task JSON must contain a tasks array"
        raise ValueError(message)
    entries: object = payload.get("tasks")
    if not isinstance(entries, list):
        message = "Task JSON must contain a tasks array"
        raise TypeError(message)
    records: list[TaskRecord] = []
    seen: set[str] = set()
    for task in entries:
        if not isinstance(task, dict):
            message = "Each Task entry must be an object"
            raise TypeError(message)
        name: object = task.get("name")
        description: object = task.get("desc", "")
        alias_values: object = task.get("aliases")
        if not isinstance(name, str) or not name.strip() or name in seen:
            message = "Task names must be nonempty, unique strings"
            raise ValueError(message)
        if not isinstance(description, str):
            message = "Task descriptions must be strings"
            raise TypeError(message)
        # Task's Go JSON output may encode an absent alias slice as null.
        if alias_values is None:
            alias_values = []
        if not isinstance(alias_values, list):
            message = "Task aliases must be an array of strings or null"
            raise TypeError(message)
        aliases: list[str] = []
        for alias in alias_values:
            if not isinstance(alias, str):
                message = "Task aliases must be strings"
                raise TypeError(message)
            aliases.append(alias)
        records.append({"name": name, "desc": description, "aliases": aliases})
        seen.add(name)
    return sorted(records, key=lambda task: task["name"])


def public_tasks(repository_root: Path) -> list[TaskRecord]:
    """Return public described tasks from Task's canonical JSON output."""
    # TASK_BIN is an explicit operator override; no shell or Task expression is accepted.
    completed = subprocess.run(  # noqa: S603  # nosec B603
        [task_binary(), "--dir", str(repository_root), "--list", "--json"],
        check=True,
        capture_output=True,
        text=True,
    )
    payload: object = json.loads(completed.stdout)
    return parse_tasks(payload)


def escape_cell(value: object) -> str:
    """Escape a value for a compact Markdown table cell."""
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def render_catalog(tasks: list[TaskRecord]) -> str:
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
        aliases = task["aliases"]
        alias_text = ", ".join(f"`{escape_cell(alias)}`" for alias in aliases)
        lines.append(
            "| "
            f"`task {escape_cell(task['name'])}` | "
            f"{escape_cell(task['desc'])} | "
            f"{alias_text or '—'} |"
        )
    lines.extend(["", END_MARKER])
    return "\n".join(lines)


def update_catalog(document: str, catalog: str) -> str:
    """Replace the generated region in TASKS.md."""
    if document.count(START_MARKER) != 1 or document.count(END_MARKER) != 1:
        message = "TASKS.md must contain exactly one generated region"
        raise RuntimeError(message)
    prefix, remainder = document.split(START_MARKER, maxsplit=1)
    _, suffix = remainder.split(END_MARKER, maxsplit=1)
    return f"{prefix}{catalog}{suffix}"


def main() -> int:
    """Generate or verify TASKS.md."""
    arguments = parse_arguments()
    repository_root: Path = arguments.repository_root.resolve()
    catalog_path = repository_root / "TASKS.md"
    current = catalog_path.read_text(encoding="utf-8")
    expected = update_catalog(current, render_catalog(public_tasks(repository_root)))

    if arguments.write:
        catalog_path.write_text(expected, encoding="utf-8")
        sys.stdout.write(f"Updated {catalog_path.relative_to(repository_root)}\n")
        return 0

    if current != expected:
        sys.stderr.write("TASKS.md is stale; run `task taskfile:catalog:write`.\n")
        return 1

    sys.stdout.write("TASKS.md matches the public Taskfile command surface.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
