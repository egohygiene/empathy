# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
# ruff: noqa: INP001
# This module supports the standalone tools/foundation.py CLI.

"""Compose reviewable ignore plans without materializing consumer files."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path, PurePosixPath
import re
from typing import Any

FORMAT = "empathy.gitignore/v1"
IDENTIFIER = re.compile(r"^[a-z][a-z0-9-]+$")
DIGEST = re.compile(r"^[0-9a-f]{64}$")


def digest(contents: str) -> str:
    return hashlib.sha256(contents.encode("utf-8")).hexdigest()


def object_digest(value: Any) -> str:
    """Hash canonical JSON: sorted keys, compact separators, UTF-8, no newline."""
    return digest(json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")))


def _safe_path(value: Any, *, root: bool = False) -> bool:
    if not isinstance(value, str) or not value:
        return False
    if value == ".":
        return root
    if any(not char.isprintable() or char in '\\:*?[]<>|"!' for char in value):
        return False
    path = PurePosixPath(value)
    return (
        not path.is_absolute()
        and str(path) == value
        and all(
            part == part.strip() and part.casefold() not in {".", "..", ".git"}
            for part in path.parts
        )
        and (not root or ".gitignore" not in {part.casefold() for part in path.parts})
    )


def _source_errors(source: Any, *, overlay: bool, profiles: set[str]) -> list[str]:
    fields = {"id", "path", "sha256"} | ({"profile"} if overlay else set())
    if not isinstance(source, dict) or set(source) != fields:
        return [f"ignore source must declare only {', '.join(sorted(fields))}"]
    errors = []
    if not isinstance(source["id"], str) or not IDENTIFIER.fullmatch(source["id"]):
        errors.append("ignore source id must be a lowercase identifier")
    if not _safe_path(source["path"]):
        errors.append("ignore source path must be normalized and repository-relative")
    if not isinstance(source["sha256"], str) or not DIGEST.fullmatch(source["sha256"]):
        errors.append("ignore source sha256 must be 64 lowercase hexadecimal characters")
    if overlay and (not isinstance(source["profile"], str) or source["profile"] not in profiles):
        errors.append("ignore overlay must select a known profile")
    return errors


def validate_definition(definition: Any, profiles: set[str]) -> list[str]:
    """Validate the catalog-owned source registry, not consumer paths."""
    if not isinstance(definition, dict) or set(definition) != {"format", "baseline", "overlays"}:
        return ["gitignore composition must declare only format, baseline, and overlays"]
    errors = []
    if definition["format"] != FORMAT:
        errors.append(f"gitignore composition format must be {FORMAT}")
    errors.extend(_source_errors(definition["baseline"], overlay=False, profiles=profiles))
    if not isinstance(definition["overlays"], list):
        return [*errors, "gitignore overlays must be an array"]
    for overlay in definition["overlays"]:
        errors.extend(_source_errors(overlay, overlay=True, profiles=profiles))
    if not errors:
        sources = [definition["baseline"], *definition["overlays"]]
        for field in ("id", "path"):
            values = [source[field].casefold() for source in sources]
            if len(values) != len(set(values)):
                errors.append(f"ignore source {field} values must be unique ignoring case")
    return sorted(set(errors))


def _scope_errors(scope: Any, overlays: dict[str, Any], profiles: list[str]) -> list[str]:
    if not isinstance(scope, dict) or set(scope) != {"root", "overlays", "local_additions"}:
        return ["each gitignore scope must declare only root, overlays, and local_additions"]
    errors = []
    if not _safe_path(scope["root"], root=True):
        errors.append(
            "gitignore scope root must be '.' or a normalized repository-relative directory"
        )
    selected = scope["overlays"]
    if not isinstance(selected, list) or any(not isinstance(item, str) for item in selected):
        errors.append("gitignore scope overlays must be an array of identifiers")
    else:
        if len(selected) != len(set(selected)):
            errors.append("gitignore scope overlays must not contain duplicates")
        for identifier in selected:
            if identifier not in overlays:
                errors.append(f"unknown gitignore overlay: {identifier}")
            elif overlays[identifier]["profile"] not in profiles:
                errors.append(
                    f"gitignore overlay {identifier} requires selected profile {overlays[identifier]['profile']}"
                )
    local = scope["local_additions"]
    if (
        not isinstance(local, str)
        or "\r" in local
        or "\0" in local
        or (local and not local.endswith("\n"))
    ):
        errors.append(
            "gitignore local_additions must be empty or LF-terminated text without CR or NUL"
        )
    return errors


def validate_selection(
    selection: Any, definition: dict[str, Any], profiles: list[str]
) -> list[str]:
    """Require explicit project scopes and explicit local text."""
    if not isinstance(selection, dict) or set(selection) != {"scopes"}:
        return ["manifest gitignore must declare only scopes"]
    scopes = selection["scopes"]
    if not isinstance(scopes, list) or not scopes:
        return ["gitignore scopes must be a non-empty array"]
    overlays = {source["id"]: source for source in definition["overlays"]}
    errors = []
    for scope in scopes:
        errors.extend(_scope_errors(scope, overlays, profiles))
    if not errors:
        roots = [scope["root"].casefold() for scope in scopes]
        if len(roots) != len(set(roots)):
            errors.append("gitignore scope roots must be unique ignoring case")
        if "." not in roots:
            errors.append("gitignore scopes must include the repository root '.'")
    return sorted(set(errors))


def _read_source(source: dict[str, Any], source_root: Path) -> tuple[str, list[str]]:
    path = source["path"]
    try:
        target = (source_root / path).resolve()
        if not target.is_relative_to(source_root.resolve()):
            return "", [f"ignore source escapes source root: {path}"]
        raw = target.read_bytes()
        contents = raw.decode("utf-8")
    except (OSError, RuntimeError, UnicodeError) as error:
        return "", [f"cannot read ignore source {path}: {error}"]
    errors = []
    if hashlib.sha256(raw).hexdigest() != source["sha256"]:
        errors.append(f"ignore source digest mismatch: {path}")
    if "\r" in contents or "\0" in contents or not contents.endswith("\n"):
        errors.append(f"ignore source must be LF-terminated text without CR or NUL: {path}")
    rules = [line for line in contents.splitlines() if line and not line.startswith("#")]
    if not rules or len(rules) != len(set(rules)):
        errors.append(f"ignore source must have nonempty, unique active rules: {path}")
    if "profile" in source and any(not rule.removeprefix("!").startswith("/") for rule in rules):
        errors.append(
            f"ignore overlay rules must be anchored to their selected project root: {path}"
        )
    return contents, errors


def compose(
    catalog: dict[str, Any], resolved: dict[str, Any], source_root: Path
) -> tuple[dict[str, Any] | None, list[str]]:
    """Plan validated selections; read canonical sources, never consumer files."""
    if "gitignore" not in resolved:
        return None, ["manifest must select gitignore scopes before planning"]
    artifact = next(item for item in resolved["artifacts"] if item["id"] == "gitignore")
    definition = artifact["composition"]
    sources = [definition["baseline"], *definition["overlays"]]
    contents_by_id = {}
    errors = []
    # Check every registered source, including overlays not selected by this consumer.
    for source in sources:
        contents, source_errors = _read_source(source, source_root)
        contents_by_id[source["id"]] = contents
        errors.extend(source_errors)
    if errors:
        return None, sorted(set(errors))
    sources_by_id = {source["id"]: source for source in sources}
    files = []
    for scope in resolved["gitignore"]["scopes"]:
        layers = []
        chunks = ["# Composed ignore rules; see the foundation plan for source hashes.\n"]
        for identifier in scope["overlays"]:
            source = sources_by_id[identifier]
            layers.append({"kind": "overlay", "owner": catalog["owner"], **source})
            chunks.extend([f"\n# Profile: {identifier}\n", contents_by_id[identifier]])
        local = scope["local_additions"]
        layers.append({"kind": "local", "owner": resolved["repository"], "sha256": digest(local)})
        chunks.extend(["\n# Repository-owned local additions.\n", local])
        baseline = definition["baseline"]
        layers.append({"kind": "baseline", "owner": catalog["owner"], **baseline})
        chunks.extend(
            [
                "\n# Universal baseline (last in every declared scope).\n",
                contents_by_id[baseline["id"]],
            ]
        )
        contents = "".join(chunks)
        files.append(
            {
                "path": str(PurePosixPath(scope["root"]) / ".gitignore"),
                "ownership": artifact["effective_ownership"],
                "override": artifact["override"],
                "layers": layers,
                "content": contents,
                "content_sha256": digest(contents),
            }
        )
    return {
        "format": FORMAT,
        "status": "plan-only",
        "generator": "tools/foundation.py plan-gitignore",
        "foundation": resolved["foundation"],
        "repository": resolved["repository"],
        "profiles": resolved["profiles"],
        "source": {
            "owner": catalog["owner"],
            "catalog_sha256": object_digest(catalog),
            "resolved_manifest_sha256": object_digest(resolved),
        },
        "files": files,
    }, []
