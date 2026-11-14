#!/usr/bin/env python3
# ruff: noqa: T201, TRY003
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Bind Empathy's selected local CI composition to its immutable Realm owner."""

from __future__ import annotations

import argparse
from contextlib import redirect_stdout
import hashlib
import io
import json
from pathlib import Path
import re
import runpy
import shlex
import shutil
import subprocess  # nosec B404
import sys
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from tools import foundation
else:
    import foundation

ROOT = Path(__file__).resolve().parents[1]
PIN_PATH = "integrations/realm/local-ci.source.json"
MANIFEST_PATH = "config/local-ci.json"
OWNER_FILES = {
    "config/act.v1.json",
    "tools/realm_act.py",
    "tools/realm_act_network.py",
    "tools/realm_local_ci.py",
}
PLATFORM_ARGUMENT_COUNT = 2


def digest(path: Path) -> str:
    """Hash exact bytes without rewriting source configuration."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def selection(root: Path) -> dict[str, Any] | None:
    """Resolve applicability with the existing foundation owner."""
    catalog = foundation.load_json(root / "foundation/catalog.json")
    manifest = foundation.load_json(root / "foundation/empathy.manifest.json")
    resolved, errors = foundation.resolve_manifest(catalog, manifest)
    if errors or resolved is None:
        raise ValueError("invalid foundation selection: " + "; ".join(errors))
    return resolved if "local-ci" in resolved["profiles"] else None


def selected_platforms(manifest: dict[str, Any]) -> dict[str, str]:
    """Select the concrete image bindings reviewed by this act consumer."""
    platforms: dict[str, str] = {}
    checks = manifest.get("checks")
    if not isinstance(checks, list) or any(not isinstance(check, dict) for check in checks):
        raise ValueError("local CI checks must be an array of objects")
    for check in checks:
        if check.get("kind") == "act":
            mappings = check.get("platforms")
            if not isinstance(mappings, dict):
                raise ValueError("selected runner mappings must be an object")
            for label, image in mappings.items():
                if (
                    not isinstance(image, str)
                    or re.fullmatch(r"[^\s]+@sha256:[0-9a-f]{64}", image) is None
                ):
                    raise ValueError("selected runner image must have an immutable SHA-256 digest")
                if label in platforms and platforms[label] != image:
                    raise ValueError("selected runner mappings disagree")
                platforms[label] = image
    if not platforms:
        raise ValueError(
            "local-ci selects act; use native commands without this profile to opt out"
        )
    return platforms


def configuration(root: Path) -> dict[str, Any]:
    """Review consumer project defaults; Realm still validates the check schema."""
    manifest = foundation.load_json(root / MANIFEST_PATH)
    platforms = selected_platforms(manifest)
    defaults: dict[str, str] = {}
    for line in (root / ".actrc").read_text(encoding="utf-8").splitlines():
        words = shlex.split(line, comments=True)
        if not words:
            continue
        if words in (["--json"], ["--rm"], ["--pull=false"]):
            continue
        if len(words) != PLATFORM_ARGUMENT_COUNT or words[0] != "--platform" or "=" not in words[1]:
            raise ValueError(
                "unreviewed .actrc option; host configuration belongs to Realm's launcher"
            )
        label, image = words[1].split("=", 1)
        if label in defaults:
            raise ValueError("duplicate .actrc runner mapping")
        defaults[label] = image
    if defaults != platforms:
        raise ValueError(".actrc mappings must match the explicit selected manifest")
    return manifest


def source_pin(root: Path, checkout: Path) -> dict[str, Any]:
    """Verify owner identity and every invoked source before delegating execution."""
    pin = foundation.load_json(root / PIN_PATH)
    if (
        set(pin) != {"schema_version", "repository", "revision", "act_version", "files"}
        or pin["schema_version"] != "empathy.realm-local-ci-source/v1"
        or pin["repository"] != "egohygiene/realm"
        or not isinstance(pin["revision"], str)
        or re.fullmatch(r"[0-9a-f]{40}", pin["revision"]) is None
        or not isinstance(pin["act_version"], str)
        or re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", pin["act_version"]) is None
        or not isinstance(pin["files"], dict)
        or set(pin["files"]) != OWNER_FILES
    ):
        raise ValueError("unsupported Realm source pin")
    git = shutil.which("git")
    if git is None:
        raise ValueError("Git is required to verify the selected Realm source")
    # The command uses a fixed Git operation and the caller's explicit checkout.
    revision = subprocess.run(  # noqa: S603  # nosec B603
        [git, "-C", str(checkout), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        timeout=15,
        check=False,
    )
    if revision.returncode or revision.stdout.strip() != pin["revision"]:
        raise ValueError("Realm checkout must match the recorded immutable revision")
    for relative, expected in pin["files"].items():
        path = checkout / relative
        if (
            not isinstance(expected, str)
            or re.fullmatch(r"[0-9a-f]{64}", expected) is None
            or any(part.is_symlink() for part in (path, *path.parents) if part != checkout.parent)
            or not path.is_file()
            or digest(path) != expected
        ):
            raise ValueError("Realm source bytes differ from the reviewed pin: " + relative)
    act_pin = foundation.load_json(checkout / "config/act.v1.json")
    if act_pin.get("version") != pin["act_version"]:
        raise ValueError("Realm act pin differs from the selected consumer version")
    return pin


def provenance(root: Path, pin: dict[str, Any]) -> dict[str, Any]:
    """Keep consumer bindings alongside, rather than rewriting, owner reports."""
    return {
        "schema_version": "empathy.local-ci-consumer/v1",
        "realm": pin,
        "configuration_sha256": {
            relative: digest(root / relative)
            for relative in (
                PIN_PATH,
                MANIFEST_PATH,
                ".actrc",
                "foundation/catalog.json",
                "foundation/empathy.manifest.json",
                "tools/local_ci.py",
                ".github/act/local-validation.yml",
            )
        },
        "coverage": "Only the explicit manifest selection; not complete hosted-CI qualification",
    }


def invoke_owner(script: Path, arguments: list[str]) -> tuple[int, str]:
    """Keep Realm's own signal handling and cleanup in this process."""
    previous = sys.argv
    output = io.StringIO()
    try:
        sys.argv = [str(script), *arguments]
        with redirect_stdout(output):
            try:
                runpy.run_path(str(script), run_name="__main__")
            except SystemExit as status:
                return int(status.code or 0), output.getvalue()
        return 0, output.getvalue()
    finally:
        sys.argv = previous


def operate(args: argparse.Namespace) -> int:
    """Delegate mechanics and statuses after reviewing local composition."""
    if selection(ROOT) is None:
        if args.operation != "plan":
            raise ValueError("local-ci is not selected; use the repository's native commands")
        print(json.dumps({"applicability": "not-selected", "checks": []}, sort_keys=True))
        return 0
    configuration(ROOT)
    if args.realm_checkout is None:
        raise ValueError("select an explicit --realm-checkout at the recorded revision")
    if args.operation == "run":
        if args.output is None:
            raise ValueError("run requires --output naming a new report directory")
        if args.output.exists() or args.output.is_symlink():
            raise ValueError("report directory already exists; choose a new output")
    checkout = args.realm_checkout.resolve()
    pin = source_pin(ROOT, checkout)
    receipt = provenance(ROOT, pin)
    arguments = [
        args.operation,
        "--repository",
        str(ROOT),
        "--manifest",
        MANIFEST_PATH,
        "--act",
        args.act,
    ]
    if args.output is not None:
        arguments.extend(("--output", str(args.output.resolve())))
    if args.cloud_network:
        arguments.append("--cloud-network")
    # Execution, timeouts, credential handling and reports remain owned by Realm.
    status, output = invoke_owner(checkout / "tools/realm_local_ci.py", arguments)
    if args.operation in {"plan", "doctor"} and status == 0:
        print(json.dumps({"consumer": receipt, args.operation: json.loads(output)}, indent=2))
    else:
        print(output, end="")
    if (
        args.operation == "run"
        and status in {0, 1, 130, 143}
        and args.output is not None
        and (args.output / "report.json").is_file()
    ):
        with (args.output / "consumer-source.json").open("x", encoding="utf-8") as stream:
            stream.write(json.dumps(receipt, indent=2) + "\n")
    return status


def main(argv: list[str] | None = None) -> int:
    """Parse the bounded consumer interface and report invalid inputs."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("plan", "doctor", "run"))
    parser.add_argument("--realm-checkout", type=Path)
    parser.add_argument("--act", default="act")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--cloud-network", action="store_true")
    args = parser.parse_args(argv)
    try:
        return operate(args)
    except (OSError, ValueError, TypeError, subprocess.TimeoutExpired) as error:
        print(f"local CI consumer failed: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
