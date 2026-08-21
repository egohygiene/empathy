#!/usr/bin/env python3
# ruff: noqa: PERF401, PLR0911, PLR0912, PLR0915, S101, T201, TRY003
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Validate and resolve the Empathy repository foundation contract."""

from __future__ import annotations

import argparse
import json
from pathlib import Path, PurePosixPath
import re
import sys
from typing import Any

SCHEMA_VERSION = "1.0.0"
FOUNDATION_REFERENCE = "empathy/repository-foundation@1.0.0"
REVISION_PATTERN = re.compile(r"^[0-9a-f]{40}$")
REQUIRED_CATEGORIES = {
    "agent-context",
    "community-health",
    "documentation",
    "metadata",
    "quality",
    "release",
    "security",
}


def load_json(path: Path) -> dict[str, Any]:
    """Load a dependency-free JSON object."""

    with path.open("r", encoding="utf-8") as stream:
        value = json.load(stream)
    if not isinstance(value, dict):
        raise TypeError(f"{path} must contain a JSON object")
    return value


def _unique_strings(value: Any, path: str, *, allow_empty: bool = True) -> list[str]:
    if not isinstance(value, list):
        return [f"{path} must be an array"]
    errors: list[str] = []
    if not allow_empty and not value:
        errors.append(f"{path} must not be empty")
    if any(not isinstance(item, str) or not item.strip() for item in value):
        errors.append(f"{path} must contain non-empty strings")
    strings = [item for item in value if isinstance(item, str)]
    if len(strings) != len(set(strings)):
        errors.append(f"{path} must not contain duplicates")
    return errors


def _safe_path(value: Any) -> bool:
    if not isinstance(value, str) or not value or "\\" in value:
        return False
    path = PurePosixPath(value)
    return not path.is_absolute() and all(part not in {"", ".", ".."} for part in path.parts)


def validate_catalog(catalog: dict[str, Any]) -> list[str]:
    """Return stable semantic errors for the foundation catalog."""

    errors: list[str] = []
    if catalog.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION}")
    if catalog.get("id") != "empathy/repository-foundation":
        errors.append("catalog id must be empathy/repository-foundation")
    if catalog.get("version") != SCHEMA_VERSION:
        errors.append(f"catalog version must be {SCHEMA_VERSION}")
    if catalog.get("owner") != "egohygiene/empathy":
        errors.append("catalog owner must be egohygiene/empathy")

    categories = catalog.get("categories")
    errors.extend(_unique_strings(categories, "categories", allow_empty=False))
    if isinstance(categories, list) and set(categories) != REQUIRED_CATEGORIES:
        errors.append("categories must cover all version-1 repository concerns")

    profiles = catalog.get("profiles")
    if not isinstance(profiles, list) or not profiles:
        return sorted({*errors, "profiles must be a non-empty array"})
    profile_ids = [profile.get("id") for profile in profiles if isinstance(profile, dict)]
    if len(profile_ids) != len(profiles) or any(not isinstance(item, str) for item in profile_ids):
        errors.append("every profile must have a string id")
        profile_names: set[str] = set()
    else:
        profile_names = set(profile_ids)
        if len(profile_names) != len(profile_ids):
            errors.append("profile ids must be unique")
    graph: dict[str, list[str]] = {}
    for index, profile in enumerate(profiles):
        prefix = f"profiles[{index}]"
        if not isinstance(profile, dict):
            errors.append(f"{prefix} must be an object")
            continue
        for field in ("dimension", "description"):
            if not isinstance(profile.get(field), str) or not profile[field].strip():
                errors.append(f"{prefix}.{field} must be a non-empty string")
        for field in ("requires", "conflicts"):
            errors.extend(_unique_strings(profile.get(field), f"{prefix}.{field}"))
        name = profile.get("id")
        if not isinstance(name, str):
            continue
        requires = profile.get("requires", [])
        conflicts = profile.get("conflicts", [])
        if isinstance(requires, list) and isinstance(conflicts, list):
            unknown = (set(requires) | set(conflicts)) - profile_names
            if unknown:
                errors.append(f"profile {name} references unknown profiles: {', '.join(sorted(unknown))}")
            if name in requires or name in conflicts:
                errors.append(f"profile {name} cannot require or conflict with itself")
            graph[name] = [item for item in requires if isinstance(item, str)]

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(name: str, stack: list[str]) -> None:
        if name in visiting:
            start = stack.index(name)
            errors.append(f"profile dependency cycle: {' -> '.join([*stack[start:], name])}")
            return
        if name in visited:
            return
        visiting.add(name)
        for dependency in graph.get(name, []):
            visit(dependency, [*stack, name])
        visiting.remove(name)
        visited.add(name)

    for profile_name in sorted(profile_names):
        visit(profile_name, [])

    artifacts = catalog.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        return sorted({*errors, "artifacts must be a non-empty array"})
    ids: list[str] = []
    paths: list[str] = []
    for index, artifact in enumerate(artifacts):
        prefix = f"artifacts[{index}]"
        if not isinstance(artifact, dict):
            errors.append(f"{prefix} must be an object")
            continue
        identifier = artifact.get("id")
        path = artifact.get("path")
        if not isinstance(identifier, str) or not identifier:
            errors.append(f"{prefix}.id must be a non-empty string")
        else:
            ids.append(identifier)
        if not _safe_path(path):
            errors.append(f"{prefix}.path must be normalized and repository-relative")
        else:
            paths.append(path)
        if artifact.get("kind") not in {"file", "directory"}:
            errors.append(f"{prefix}.kind is invalid")
        if artifact.get("category") not in REQUIRED_CATEGORIES:
            errors.append(f"{prefix}.category is invalid")
        presence = artifact.get("presence")
        if presence not in {"required", "optional", "profile"}:
            errors.append(f"{prefix}.presence is invalid")
        ownership = artifact.get("ownership")
        if ownership not in {"generated", "required", "repository-owned"}:
            errors.append(f"{prefix}.ownership is invalid")
        artifact_profiles = artifact.get("profiles")
        errors.extend(_unique_strings(artifact_profiles, f"{prefix}.profiles"))
        if isinstance(artifact_profiles, list):
            unknown = set(artifact_profiles) - profile_names
            if unknown:
                errors.append(f"{prefix}.profiles references unknown profiles")
            if presence == "profile" and not artifact_profiles:
                errors.append(f"{prefix} profile artifact must select at least one profile")
            if presence != "profile" and artifact_profiles:
                errors.append(f"{prefix} non-profile artifact must not select profiles")
        markers = artifact.get("markers")
        errors.extend(_unique_strings(markers, f"{prefix}.markers"))
        if ownership == "generated" and not markers:
            errors.append(f"{prefix} generated artifact must declare deterministic markers")
        if artifact.get("executable") and artifact.get("kind") != "file":
            errors.append(f"{prefix} directory cannot be executable")
        if not isinstance(artifact.get("description"), str) or not artifact["description"].strip():
            errors.append(f"{prefix}.description must be a non-empty string")
    if len(ids) != len(set(ids)):
        errors.append("artifact ids must be unique")
    if len(paths) != len(set(paths)):
        errors.append("artifact paths must be unique")

    fields = catalog.get("repository_owned_fields")
    if not isinstance(fields, list) or not fields:
        errors.append("repository_owned_fields must be a non-empty array")
    else:
        field_ids = [field.get("id") for field in fields if isinstance(field, dict)]
        if len(field_ids) != len(fields) or len(field_ids) != len(set(field_ids)):
            errors.append("repository-owned field ids must be present and unique")
        for index, field in enumerate(fields):
            if not isinstance(field, dict) or field.get("type") not in {"string", "string-array"}:
                errors.append(f"repository_owned_fields[{index}] has an invalid type")
            if isinstance(field, dict) and not isinstance(field.get("required"), bool):
                errors.append(f"repository_owned_fields[{index}].required must be boolean")

    outputs = catalog.get("generated_outputs")
    if not isinstance(outputs, list) or not outputs:
        errors.append("generated_outputs must be a non-empty array")
    else:
        output_paths: list[str] = []
        for index, output in enumerate(outputs):
            if not isinstance(output, dict) or not _safe_path(output.get("path")):
                errors.append(f"generated_outputs[{index}].path is invalid")
                continue
            output_paths.append(output["path"])
        if len(output_paths) != len(set(output_paths)):
            errors.append("generated output paths must be unique")
    return sorted(set(errors))


def _resolve_profiles(catalog: dict[str, Any], selected: list[str]) -> tuple[list[str], list[str]]:
    profiles = {profile["id"]: profile for profile in catalog["profiles"]}
    unknown = set(selected) - profiles.keys()
    if unknown:
        return [], [f"manifest references unknown profiles: {', '.join(sorted(unknown))}"]
    resolved = set(selected)
    queue = sorted(selected)
    while queue:
        name = queue.pop(0)
        for dependency in profiles[name]["requires"]:
            if dependency not in resolved:
                resolved.add(dependency)
                queue.append(dependency)
    errors: list[str] = []
    for name in sorted(resolved):
        conflicts = set(profiles[name]["conflicts"]) & resolved
        if conflicts:
            errors.append(f"profile {name} conflicts with: {', '.join(sorted(conflicts))}")
    return sorted(resolved), sorted(set(errors))


def resolve_manifest(
    catalog: dict[str, Any], manifest: dict[str, Any]
) -> tuple[dict[str, Any] | None, list[str]]:
    """Resolve profile closure and safe ownership overrides."""

    errors = validate_catalog(catalog)
    if manifest.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"manifest schema_version must be {SCHEMA_VERSION}")
    if manifest.get("foundation") != FOUNDATION_REFERENCE:
        errors.append(f"manifest foundation must be {FOUNDATION_REFERENCE}")
    repository = manifest.get("repository")
    if not isinstance(repository, str) or repository.count("/") != 1:
        errors.append("manifest repository must use owner/name form")
    selected = manifest.get("selected_profiles")
    errors.extend(_unique_strings(selected, "selected_profiles", allow_empty=False))
    resolved_profiles: list[str] = []
    if isinstance(selected, list) and all(isinstance(item, str) for item in selected):
        resolved_profiles, profile_errors = _resolve_profiles(catalog, selected)
        errors.extend(profile_errors)

    artifacts = {artifact["id"]: artifact for artifact in catalog.get("artifacts", [])}
    selected_artifacts = {
        identifier: artifact
        for identifier, artifact in artifacts.items()
        if artifact["presence"] == "required"
        or (
            artifact["presence"] == "profile"
            and set(artifact["profiles"]) & set(resolved_profiles)
        )
    }
    overrides = manifest.get("overrides")
    if not isinstance(overrides, list):
        errors.append("overrides must be an array")
        overrides = []
    override_ids: list[str] = []
    for index, override in enumerate(overrides):
        if not isinstance(override, dict) or set(override) != {"artifact", "mode"}:
            errors.append(f"overrides[{index}] must declare only artifact and mode")
            continue
        identifier = override.get("artifact")
        override_ids.append(identifier)
        if override.get("mode") != "preserve":
            errors.append(f"overrides[{index}].mode must be preserve")
        if identifier not in selected_artifacts:
            errors.append(f"override artifact is not selected: {identifier}")
        elif selected_artifacts[identifier]["ownership"] == "generated":
            errors.append(f"generated artifact cannot be preserved by override: {identifier}")
    if len(override_ids) != len(set(override_ids)):
        errors.append("override artifact ids must be unique")

    repository_owned = manifest.get("repository_owned")
    if not isinstance(repository_owned, dict):
        errors.append("repository_owned must be an object")
        repository_owned = {}
    field_contract = {field["id"]: field for field in catalog.get("repository_owned_fields", [])}
    unknown_fields = repository_owned.keys() - field_contract.keys()
    if unknown_fields:
        errors.append(f"unknown repository-owned fields: {', '.join(sorted(unknown_fields))}")
    for identifier, field in field_contract.items():
        value = repository_owned.get(identifier)
        if field["required"] and value is None:
            errors.append(f"required repository-owned field is missing: {identifier}")
            continue
        if value is None:
            continue
        if field["type"] == "string" and (not isinstance(value, str) or not value.strip()):
            errors.append(f"repository-owned field {identifier} must be a non-empty string")
        if field["type"] == "string-array":
            errors.extend(_unique_strings(value, f"repository_owned.{identifier}"))

    if errors:
        return None, sorted(set(errors))
    resolved_artifacts = []
    override_set = set(override_ids)
    for identifier, artifact in sorted(
        selected_artifacts.items(), key=lambda item: (item[1]["path"], item[0])
    ):
        resolved_artifacts.append(
            {
                **artifact,
                "effective_ownership": (
                    "repository-owned" if identifier in override_set else artifact["ownership"]
                ),
                "override": "preserve" if identifier in override_set else None,
            }
        )
    optional_artifacts = [
        artifact["id"]
        for artifact in sorted(catalog["artifacts"], key=lambda artifact: artifact["id"])
        if artifact["presence"] == "optional"
    ]
    return {
        "schema_version": SCHEMA_VERSION,
        "foundation": FOUNDATION_REFERENCE,
        "repository": repository,
        "profiles": resolved_profiles,
        "artifacts": resolved_artifacts,
        "optional_artifacts": optional_artifacts,
        "repository_owned": {key: repository_owned[key] for key in sorted(repository_owned)},
    }, []


def render_resolved(resolved: dict[str, Any]) -> str:
    """Render stable resolved JSON for idempotence and review."""

    return json.dumps(resolved, indent=2, ensure_ascii=False, sort_keys=True) + "\n"


def render_inventory(catalog: dict[str, Any]) -> str:
    """Render a stable human inventory of canonical and generated surfaces."""

    lines = [
        "# Generated repository foundation inventory",
        "",
        "> Generated from `foundation/catalog.json`. Do not edit by hand.",
        "",
        f"- Contract: `{catalog['id']}@{catalog['version']}`",
        f"- Canonical owner: `{catalog['owner']}`",
        f"- Canonical artifacts: `{len(catalog['artifacts'])}`",
        "",
        "| Path | Category | Presence | Ownership | Profiles | Description |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for artifact in sorted(catalog["artifacts"], key=lambda item: item["path"]):
        profiles = ", ".join(artifact["profiles"]) or "—"
        description = artifact["description"].replace("|", "\\|")
        lines.append(
            f"| `{artifact['path']}` | {artifact['category']} | {artifact['presence']} | "
            f"{artifact['ownership']} | {profiles} | {description} |"
        )
    lines.extend(
        [
            "",
            "## Generated outputs",
            "",
            "| Path | Owner | Canonical input | Checked in |",
            "| --- | --- | --- | --- |",
        ]
    )
    for output in sorted(catalog["generated_outputs"], key=lambda item: item["path"]):
        lines.append(
            f"| `{output['path']}` | `{output['owner']}` | `{output['source']}` | "
            f"`{str(output['checked_in']).lower()}` |"
        )
    lines.append("")
    return "\n".join(lines)


def render_egolint_contract(resolved: dict[str, Any], source_revision: str) -> str:
    """Render the selected golden foundation as EgoLint repository-contract TOML."""

    if not REVISION_PATTERN.fullmatch(source_revision):
        raise ValueError("source revision must be a 40-character lowercase Git commit")
    lines = [
        "schema-version = 1",
        'id = "empathy-universal-foundation"',
        'version = "1.0.0"',
        'profile = "empathy/golden-foundation"',
        "provisional = false",
        "",
        "[source]",
        'repository = "egohygiene/empathy"',
        f'revision = "{source_revision}"',
        'revision-kind = "git-commit"',
        'path = "foundation/catalog.json"',
        'decision = "https://github.com/egohygiene/empathy/issues/62"',
        "",
    ]
    for artifact in resolved["artifacts"]:
        lines.extend(
            [
                "[[requirements]]",
                f'id = "{artifact["id"]}"',
                f'path = "{artifact["path"]}"',
                f'kind = "{artifact["kind"]}"',
                f'ownership = "{artifact["effective_ownership"]}"',
            ]
        )
        if artifact["executable"]:
            lines.append("executable = true")
        if artifact["markers"]:
            lines.append("markers = [")
            for marker in artifact["markers"]:
                lines.append(f"  {json.dumps(marker)},")
            lines.append("]")
        lines.append("")
    return "\n".join(lines)


def validate_workspace(root: Path, resolved: dict[str, Any]) -> list[str]:
    """Verify the selected golden fixture without modifying repository content."""

    errors: list[str] = []
    for artifact in resolved["artifacts"]:
        target = root / artifact["path"]
        expected = artifact["kind"]
        if expected == "file" and not target.is_file():
            errors.append(f"required file is missing: {artifact['path']}")
            continue
        if expected == "directory" and not target.is_dir():
            errors.append(f"required directory is missing: {artifact['path']}")
            continue
        if expected == "file" and artifact["markers"]:
            contents = target.read_text(encoding="utf-8")
            for marker in artifact["markers"]:
                if marker not in contents:
                    errors.append(f"{artifact['path']} is missing marker: {marker}")
    return sorted(errors)


def _write(path: Path, contents: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(contents, encoding="utf-8")


def _check(path: Path, contents: str) -> bool:
    return path.exists() and path.read_text(encoding="utf-8") == contents


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=Path("foundation/catalog.json"))
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("validate-catalog")
    for command in ("validate-manifest", "resolve", "verify-workspace"):
        subparser = subparsers.add_parser(command)
        subparser.add_argument("--manifest", type=Path, required=True)
        if command == "resolve":
            subparser.add_argument("--output", type=Path, required=True)
        if command == "verify-workspace":
            subparser.add_argument("--workspace", type=Path, default=Path())
    for command in ("render-inventory", "check-inventory"):
        subparser = subparsers.add_parser(command)
        subparser.add_argument("--output", type=Path, required=True)
    for command in ("render-contract", "check-contract"):
        subparser = subparsers.add_parser(command)
        subparser.add_argument("--manifest", type=Path, required=True)
        subparser.add_argument("--source-revision", required=True)
        subparser.add_argument("--output", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    arguments = build_parser().parse_args(argv)
    try:
        catalog = load_json(arguments.catalog)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"foundation catalog load failed: {error}", file=sys.stderr)
        return 2
    errors = validate_catalog(catalog)
    if errors:
        for error in errors:
            print(f"foundation catalog validation failed: {error}", file=sys.stderr)
        return 1
    if arguments.command == "validate-catalog":
        print(
            f"foundation catalog valid: {len(catalog['profiles'])} profiles, "
            f"{len(catalog['artifacts'])} artifacts"
        )
        return 0
    if arguments.command in {"render-inventory", "check-inventory"}:
        rendered = render_inventory(catalog)
        if arguments.command == "render-inventory":
            _write(arguments.output, rendered)
            print(f"wrote {arguments.output}")
            return 0
        if not _check(arguments.output, rendered):
            print(f"generated inventory is stale: {arguments.output}", file=sys.stderr)
            return 1
        print(f"generated inventory current: {arguments.output}")
        return 0
    try:
        manifest = load_json(arguments.manifest)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"foundation manifest load failed: {error}", file=sys.stderr)
        return 2
    resolved, errors = resolve_manifest(catalog, manifest)
    if errors:
        for error in errors:
            print(f"foundation manifest validation failed: {error}", file=sys.stderr)
        return 1
    assert resolved is not None
    if arguments.command == "validate-manifest":
        print(
            f"foundation manifest valid: {len(resolved['profiles'])} profiles, "
            f"{len(resolved['artifacts'])} selected artifacts"
        )
        return 0
    if arguments.command == "resolve":
        _write(arguments.output, render_resolved(resolved))
        print(f"wrote {arguments.output}")
        return 0
    if arguments.command == "verify-workspace":
        errors = validate_workspace(arguments.workspace, resolved)
        if errors:
            for error in errors:
                print(f"golden workspace validation failed: {error}", file=sys.stderr)
            return 1
        print(f"golden workspace valid: {resolved['repository']}")
        return 0
    try:
        rendered = render_egolint_contract(resolved, arguments.source_revision)
    except ValueError as error:
        print(f"foundation contract generation failed: {error}", file=sys.stderr)
        return 2
    if arguments.command == "render-contract":
        _write(arguments.output, rendered)
        print(f"wrote {arguments.output}")
        return 0
    if not _check(arguments.output, rendered):
        print(f"generated EgoLint contract is stale: {arguments.output}", file=sys.stderr)
        return 1
    print(f"generated EgoLint contract current: {arguments.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
