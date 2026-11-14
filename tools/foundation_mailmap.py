# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
# ruff: noqa: INP001
"""Plan consumer-owned mailmap composition without changing Git history or files."""

from __future__ import annotations

import hashlib
import json
import re
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pathlib import Path

MAX_INPUT_BYTES = 65536
MAX_HEADER_BYTES = 8192
FORMAT = "empathy.mailmap/v1"
HEADER = "foundation/mailmap/universal.mailmap"
ADDRESS = re.compile(r"<([^<>\s]+@[^<>\s]+)>")


def digest(text: str) -> str:
    """Hash exact UTF-8 bytes, including their final newline."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def mappings(text: Any) -> tuple[list[tuple[str | None, str, str | None, str | None]], list[str]]:
    """Parse Git's four mailmap forms; never infer an alias or canonical identity."""
    if (
        not isinstance(text, str)
        or "\r" in text
        or "\0" in text
        or re.search(r"[\ud800-\udfff]", text)
    ):
        return [], ["mailmap input must be Unicode text without CR, NUL or surrogates"]
    if len(text.encode("utf-8")) > MAX_INPUT_BYTES or (text and not text.endswith("\n")):
        return [], ["mailmap input must be LF-terminated and at most 65536 UTF-8 bytes"]
    rows: list[tuple[str | None, str, str | None, str | None]] = []
    errors = []
    for number, raw_line in enumerate(text.splitlines(), 1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        addresses = list(ADDRESS.finditer(line))
        if len(addresses) not in {1, 2} or addresses[-1].end() != len(line):
            errors.append(
                f"mailmap line {number} must use one of Git's four explicit mapping forms"
            )
            continue
        first = addresses[0]
        proper_name = line[: first.start()].strip() or None
        if proper_name and any(char in proper_name for char in "<>\t"):
            errors.append(f"mailmap line {number} has an invalid canonical name")
            continue
        if len(addresses) == 1:
            if not proper_name:
                errors.append(f"mailmap line {number} does not specify a canonical name or email")
                continue
            rows.append((None, first[1], proper_name, None))
        else:
            second = addresses[1]
            alias_name = line[first.end() : second.start()].strip() or None
            if alias_name and (not proper_name or any(char in alias_name for char in "<>\t")):
                errors.append(f"mailmap line {number} has an invalid name-specific alias")
                continue
            rows.append((alias_name, second[1], proper_name, first[1]))
    return rows, errors


def validate_definition(value: Any) -> list[str]:
    """Keep the portable baseline free of organization identity values."""
    if not isinstance(value, dict) or set(value) != {"format", "header"}:
        return ["mailmap composition must declare only format and header"]
    header = value["header"]
    if (
        value["format"] != FORMAT
        or not isinstance(header, dict)
        or set(header) != {"path", "sha256"}
    ):
        return ["mailmap composition has an unsupported format or header"]
    if (
        header["path"] != HEADER
        or not isinstance(header["sha256"], str)
        or not re.fullmatch(r"[0-9a-f]{64}", header["sha256"])
    ):
        return ["mailmap header must select the canonical path and exact SHA-256"]
    return []


def validate_selection(value: Any) -> list[str]:
    """Require reviewed identities and reject conflicting case-insensitive aliases."""
    if not isinstance(value, dict) or set(value) != {
        "baseline",
        "local_additions",
        "identity_evidence",
    }:
        return [
            "manifest mailmap must declare only baseline, local_additions and identity_evidence"
        ]
    baseline, errors = mappings(value["baseline"])
    local, local_errors = mappings(value["local_additions"])
    errors.extend(local_errors)
    if not baseline:
        errors.append(
            "mailmap baseline needs an explicitly approved identity mapping; no identity is inferred"
        )
    evidence = value["identity_evidence"]
    if (
        not isinstance(evidence, list)
        or not evidence
        or any(
            not isinstance(url, str) or not re.fullmatch(r"https://[^\s\x00-\x1f]+", url)
            for url in evidence
        )
    ):
        errors.append("mailmap identity_evidence must list reviewed public HTTPS references")
    aliases: dict[tuple[str | None, str], tuple[str | None, str | None]] = {}
    for alias_name, alias_email, name, email in [*baseline, *local]:
        key = (alias_name.casefold() if alias_name else None, alias_email.casefold())
        target = (name, email.casefold() if email else None)
        if key in aliases and aliases[key] != target:
            errors.append(
                "mailmap alias has conflicting canonical identities; review the explicit inputs"
            )
        aliases[key] = target
    for (alias_name, alias_email), target in aliases.items():
        broad = aliases.get((None, alias_email))
        if (
            alias_name
            and broad
            and any(
                a is not None and b is not None and a != b
                for a, b in zip(target, broad, strict=True)
            )
        ):
            errors.append("mailmap name-specific alias conflicts with its email-wide baseline")
    return sorted(set(errors))


def compose(
    catalog: dict[str, Any], resolved: dict[str, Any], source_root: Path
) -> tuple[dict[str, Any] | None, list[str]]:
    """Emit a deterministic proposal; Holon remains the filesystem materializer."""
    selection = resolved.get("mailmap")
    errors = validate_selection(selection)
    if errors or not isinstance(selection, dict):
        return None, errors
    artifact = next(row for row in resolved["artifacts"] if row["id"] == "mailmap")
    definition = artifact["composition"]
    path = source_root / HEADER
    try:
        if any(parent.is_symlink() for parent in (path, *path.parents)) or not path.is_file():
            return None, ["mailmap header must be a regular canonical source without symlinks"]
        with path.open("rb") as stream:
            raw = stream.read(MAX_HEADER_BYTES + 1)
        header = raw.decode("utf-8")
    except (OSError, UnicodeError):
        return None, ["mailmap canonical header is unavailable or invalid UTF-8"]
    if len(raw) > MAX_HEADER_BYTES or digest(header) != definition["header"]["sha256"]:
        return None, ["mailmap canonical header digest or size mismatch"]
    header_rows, header_errors = mappings(header)
    if header_errors or header_rows or not header.endswith("\n"):
        return None, [
            "mailmap portable header must contain only LF-terminated comments, never identities"
        ]
    content = (
        header
        + "\n# Repository-owned local mappings and comments.\n"
        + selection["local_additions"]
        + "\n# Consumer-approved baseline.\n"
        + selection["baseline"]
    )

    def canonical(value: Any) -> str:
        return digest(json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")))

    return {
        "format": FORMAT,
        "status": "plan-only",
        "generator": "tools/foundation.py plan-mailmap",
        "foundation": resolved["foundation"],
        "repository": resolved["repository"],
        "source": {
            "owner": catalog["owner"],
            "catalog_sha256": canonical(catalog),
            "resolved_manifest_sha256": canonical(resolved),
            "header": definition["header"],
        },
        "identity_evidence": selection["identity_evidence"],
        "files": [
            {
                "path": ".mailmap",
                "ownership": "repository-owned",
                "content": content,
                "content_sha256": digest(content),
                "baseline_sha256": digest(selection["baseline"]),
                "local_additions_sha256": digest(selection["local_additions"]),
            }
        ],
    }, []
