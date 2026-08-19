#!/usr/bin/env python3
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Verify that exact staged files have evidence-backed removal approval."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import sys
from typing import Any


def load_audit_module(repository_root: Path):
    path = repository_root / "tools" / "staging_home_audit.py"
    specification = importlib.util.spec_from_file_location("staging_home_audit", path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot load staging audit module: {path}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


def load_approvals(path: Path) -> dict[str, dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != "1.0.0" or not isinstance(data.get("approvals"), list):
        raise ValueError("removal approvals must use schema version 1.0.0")
    approvals: dict[str, dict[str, Any]] = {}
    for approval in data["approvals"]:
        source_path = approval.get("source_path") if isinstance(approval, dict) else None
        if not isinstance(source_path, str) or not source_path.startswith(".staging/"):
            raise ValueError("every approval needs a .staging source_path")
        if source_path in approvals:
            raise ValueError(f"duplicate removal approval: {source_path}")
        approvals[source_path] = approval
    return approvals


def validate_removals(rows, approvals, source_paths: list[str]) -> list[str]:
    by_path = {row.source_path: row for row in rows}
    errors: list[str] = []
    required = (
        "git_blob",
        "destination",
        "destination_revision",
        "validation_evidence",
        "provenance_resolution",
        "sensitivity_resolution",
        "approved_by",
        "approved_at",
    )
    for source_path in source_paths:
        row = by_path.get(source_path)
        if row is None:
            errors.append(f"not a tracked staged file: {source_path}")
            continue
        approval = approvals.get(source_path)
        if approval is None:
            errors.append(f"missing removal approval: {source_path}")
            continue
        missing = [field for field in required if not approval.get(field)]
        if missing:
            errors.append(f"{source_path} approval missing: {', '.join(missing)}")
        if approval.get("git_blob") != row.git_blob:
            errors.append(f"{source_path} approval blob does not match current source")
        if approval.get("destination") != row.canonical_home:
            errors.append(f"{source_path} approval destination does not match the ledger")
    return sorted(errors)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", type=Path, default=Path.cwd())
    parser.add_argument(
        "--approvals",
        type=Path,
        default=Path("migration/staging-removal-approvals.json"),
    )
    parser.add_argument("--source-path", action="append", required=True)
    return parser.parse_args()


def main() -> int:
    arguments = parse_arguments()
    root = arguments.repository_root.resolve()
    approvals_path = arguments.approvals
    if not approvals_path.is_absolute():
        approvals_path = root / approvals_path
    try:
        audit = load_audit_module(root)
        rows = audit.build_rows(root)
        approvals = load_approvals(approvals_path)
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as error:
        print(f"removal gate failed: {error}", file=sys.stderr)
        return 2
    errors = validate_removals(rows, approvals, arguments.source_path)
    if errors:
        for error in errors:
            print(f"removal gate failed: {error}", file=sys.stderr)
        return 1
    print(f"removal gate passed for {len(arguments.source_path)} staged file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
