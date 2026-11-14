#!/usr/bin/env python3
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Consume pinned website owners in an explicitly selected disposable target."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess  # nosec B404 # Fixed owner commands; no shell or credential input.
import sys
from typing import Any, ClassVar

ROOT = Path(__file__).resolve().parents[1]
INPUTS = ROOT / "integrations/website"
IDENTITY_OUTPUT = Path(".cache/website-baseline/identity")


class ConsumerError(ValueError):
    """A source, ownership or overwrite boundary could not be verified."""

    MESSAGES: ClassVar[dict[str, str]] = {
        "json-object": "Consumer input must be a JSON object.",
        "symlink": "Consumer paths must not contain symlinks.",
        "owner-pin": "Holon must be clean at the exact selected immutable revision.",
        "owner-profile": "Holon site profile does not match the selected digest.",
        "asset-drift": "A consumer asset differs; preserve it and review a fresh target.",
        "identity-pin": "Identity executable does not match the selected release asset.",
        "tailwind-contract": "Identity did not emit its supported Tailwind token contract.",
        "default-selection": "The universal baseline must not implicitly select a website.",
    }

    def __init__(self, code: str) -> None:
        super().__init__(self.MESSAGES[code])


def read_json(path: Path) -> dict[str, Any]:
    """Read a closed consumer input as an ordinary JSON object."""
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ConsumerError("json-object")
    return value


def sha256(path: Path) -> str:
    """Identify the exact bytes consumed from a source or released executable."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def regular_path(path: Path) -> None:
    """Reject symlink aliases before invoking an owner or writing a projection."""
    if any(item.is_symlink() for item in (path, *path.parents)):
        raise ConsumerError("symlink")


def run(command: list[str], *, cwd: Path, capture: bool = False) -> str:
    """Execute explicit owner commands without a shell."""
    result = subprocess.run(  # noqa: S603 # nosec B603 # Fixed executable/argument arrays.
        command,
        cwd=cwd,
        check=True,
        text=True,
        stdout=subprocess.PIPE if capture else None,
    )
    return result.stdout or ""


def owner_source(root: Path) -> dict[str, Any]:
    """Require the selected clean, immutable Holon checkout and site contract."""
    regular_path(root)
    selected = read_json(INPUTS / "source.json")["holon"]
    if not isinstance(selected, dict):
        raise ConsumerError("json-object")
    actual = run(["git", "rev-parse", "HEAD"], cwd=root, capture=True).strip()
    status = run(
        ["git", "status", "--porcelain", "--untracked-files=normal"], cwd=root, capture=True
    )
    if actual != selected["revision"] or status:
        raise ConsumerError("owner-pin")
    if sha256(root / selected["profile"]) != selected["profile_sha256"]:
        raise ConsumerError("owner-profile")
    return selected


def owner_command(root: Path, command: str, arguments: list[str]) -> None:
    """Delegate all materialization, ownership and recovery behavior to Holon."""
    owner_source(root)
    run(
        [
            sys.executable,
            str(root / "tools/holon_materialize.py"),
            "site-suite",
            command,
            *arguments,
        ],
        cwd=root,
    )


def copy_new(path: Path, content: bytes) -> None:
    """Allow repeatable identical projection without overwriting local changes."""
    regular_path(path)
    if path.exists():
        if not path.is_file() or path.read_bytes() != content:
            raise ConsumerError("asset-drift")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)


def identity_assets(binary: Path, target: Path, holon: Path) -> dict[str, str]:
    """Generate and verify real Identity assets, then attach consumer-owned inputs."""
    regular_path(binary)
    pin = read_json(INPUTS / "source.json")["identity"]
    if sha256(binary) != pin["asset_sha256"]:
        raise ConsumerError("identity-pin")
    owner_command(holon, "verify", ["--target", str(target)])
    regular_path(ROOT / IDENTITY_OUTPUT)
    for command in ("v1-generate", "v1-verify"):
        run(
            [
                str(binary),
                command,
                "--repository-root",
                str(ROOT),
                "--output-root",
                str(IDENTITY_OUTPUT),
            ],
            cwd=ROOT,
        )
    generated = ROOT / IDENTITY_OUTPUT
    assets = {
        "tokens.css": generated / "packages/tokens/tokens.css",
        "favicon.svg": generated / "web/favicon.svg",
        "social.png": generated / "social/card-1200x630.png",
        "website.css": INPUTS / "identity-bridge.css",
    }
    payloads = {name: path.read_bytes() for name, path in assets.items()}
    payloads["website.css"] = payloads["tokens.css"] + b"\n" + payloads["website.css"]
    for name, payload in payloads.items():
        copy_new(target / "public/assets/identity" / name, payload)
    copy_new(target / ".browserslistrc", (INPUTS / "browserslist").read_bytes())
    # Tailwind remains an optional token consumer, not a required site framework.
    tailwind = read_json(generated / "packages/tokens/tailwind.theme.json")
    if tailwind.get("schema") != "identity.tailwind-theme/v1":
        raise ConsumerError("tailwind-contract")
    return {name: hashlib.sha256(payload).hexdigest() for name, payload in payloads.items()} | {
        "tailwind.theme.json": sha256(generated / "packages/tokens/tailwind.theme.json"),
    }


def main() -> int:
    """Expose selected consumer composition, never automatic installation or Pages."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--holon-source", type=Path, required=True)
    commands = parser.add_subparsers(dest="command", required=True)
    plan = commands.add_parser("plan")
    plan.add_argument("--profile", choices=("generic", "launchkit"), required=True)
    plan.add_argument("--target", type=Path, required=True)
    plan.add_argument("--output", type=Path, required=True)
    render = commands.add_parser("render")
    render.add_argument("--plan", type=Path, required=True)
    render.add_argument("--target", type=Path, required=True)
    for command in ("verify", "rollback"):
        selected = commands.add_parser(command)
        selected.add_argument("--target", type=Path, required=True)
    assets = commands.add_parser("identity-assets")
    assets.add_argument("--identity-binary", type=Path, required=True)
    assets.add_argument("--target", type=Path, required=True)
    args = parser.parse_args()
    try:
        holon = args.holon_source.absolute()
        target = args.target.absolute()
        regular_path(target)
        if args.command == "plan":
            selection = read_json(INPUTS / "profiles.json")
            if selection["default"] is not None:
                raise ConsumerError("default-selection")
            manifest = ROOT / selection["profiles"][args.profile]["manifest"]
            owner_command(
                holon,
                "plan",
                [
                    "--manifest",
                    str(manifest),
                    "--variant",
                    args.profile,
                    "--target",
                    str(target),
                    "--output",
                    str(args.output.absolute()),
                ],
            )
        elif args.command == "render":
            owner_command(
                holon, "render", ["--plan", str(args.plan.absolute()), "--target", str(target)]
            )
        elif args.command == "identity-assets":
            receipt = identity_assets(args.identity_binary.absolute(), target, holon)
            sys.stdout.write(
                json.dumps(
                    {"schema": "empathy.website-assets/v1", "files": receipt}, sort_keys=True
                )
                + "\n"
            )
        else:
            owner_command(holon, args.command, ["--target", str(target)])
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        sys.stderr.write(f"Website consumer failed: {error}\n")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
