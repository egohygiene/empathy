#!/usr/bin/env python3
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Validate Mantle's pinned Fastfetch presentation contract without network access."""

from __future__ import annotations

import json
from pathlib import Path
import re
import struct
import sys

MANTLE_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = MANTLE_ROOT / "config/fastfetch/fastfetch.jsonc"
BANNER_PATH = MANTLE_ROOT / "assets/presentation/mantle-banner.png"
TEXT_PATH = MANTLE_ROOT / "assets/presentation/mantle-banner.txt"
EXPECTED_SCHEMA = (
    "https://github.com/fastfetch-cli/fastfetch/raw/2.67.0/doc/json_schema.json"
)
EXPECTED_COMMANDS = (
    "mantle fastfetch runtime",
    "mantle fastfetch workspace",
    "mantle fastfetch toolchains",
    "mantle fastfetch contexts",
)


def strip_json_comments(source: str) -> str:
    """Remove JSONC comments while preserving comment markers inside strings."""
    output: list[str] = []
    index = 0
    in_string = False
    escaped = False

    while index < len(source):
        character = source[index]
        following = source[index + 1] if index + 1 < len(source) else ""

        if in_string:
            output.append(character)
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                in_string = False
            index += 1
            continue

        if character == '"':
            in_string = True
            output.append(character)
            index += 1
            continue
        if character == "/" and following == "/":
            index += 2
            while index < len(source) and source[index] not in "\r\n":
                index += 1
            continue
        if character == "/" and following == "*":
            index += 2
            while index + 1 < len(source) and source[index : index + 2] != "*/":
                if source[index] in "\r\n":
                    output.append(source[index])
                index += 1
            index += 2
            continue

        output.append(character)
        index += 1

    return "".join(output)


def load_config() -> dict[str, object]:
    """Parse the canonical JSONC file using only the Python standard library."""
    source = CONFIG_PATH.read_text(encoding="utf-8")
    without_comments = strip_json_comments(source)
    without_trailing_commas = re.sub(r",\s*([}\]])", r"\1", without_comments)
    payload = json.loads(without_trailing_commas)
    if not isinstance(payload, dict):
        raise AssertionError("Fastfetch config root must be an object")
    return payload


def validate_banner() -> None:
    """Verify the supplied transparent banner contract and text fallback."""
    with BANNER_PATH.open("rb") as banner:
        signature = banner.read(8)
        if signature != b"\x89PNG\r\n\x1a\n":
            raise AssertionError("Mantle banner is not a PNG")
        length = struct.unpack(">I", banner.read(4))[0]
        if banner.read(4) != b"IHDR" or length != 13:
            raise AssertionError("Mantle banner is missing a canonical IHDR")
        width, height, _depth, color_type = struct.unpack(">IIBB", banner.read(10))
    if (width, height) != (400, 134):
        raise AssertionError(f"Mantle banner dimensions changed: {width}x{height}")
    if color_type not in {4, 6}:
        raise AssertionError("Mantle banner no longer declares an alpha channel")
    if not TEXT_PATH.read_text(encoding="utf-8").strip():
        raise AssertionError("Mantle text fallback must not be empty")
    if (MANTLE_ROOT / "assets/presentation/mantle.png").exists():
        raise AssertionError("The future Fastfetch logo mantle.png must not be fabricated")


def validate_config(payload: dict[str, object]) -> None:
    """Validate pinned compatibility, privacy, and command-module boundaries."""
    if payload.get("$schema") != EXPECTED_SCHEMA:
        raise AssertionError("Fastfetch schema must remain pinned to 2.67.0")

    logo = payload.get("logo")
    if not isinstance(logo, dict) or logo.get("source") != "mantle.png":
        raise AssertionError("Fastfetch logo contract must reserve the bare mantle.png name")
    chafa = logo.get("chafa")
    if not isinstance(chafa, dict):
        raise AssertionError("Fastfetch Chafa settings are missing")
    for forced_capability in ("canvasMode", "colorSpace", "ditherMode"):
        if forced_capability in chafa:
            raise AssertionError(f"Chafa capability must be negotiated: {forced_capability}")

    modules = payload.get("modules")
    if not isinstance(modules, list):
        raise AssertionError("Fastfetch modules must be an array")

    module_types: list[str] = []
    command_texts: list[str] = []
    section_keys: list[object] = []
    for module in modules:
        if isinstance(module, str):
            module_types.append(module.lower())
            continue
        if not isinstance(module, dict):
            raise AssertionError("Every Fastfetch module must be an object or shorthand string")
        module_type = str(module.get("type", "")).lower()
        module_types.append(module_type)
        if module_type == "command":
            command_texts.append(str(module.get("text", "")))
        if module_type == "custom" and str(module.get("format", "")).startswith(
            ("╭─", "├─", "╰─")
        ):
            section_keys.append(module.get("key"))

    if tuple(command_texts) != EXPECTED_COMMANDS:
        raise AssertionError(f"Unexpected Fastfetch command modules: {command_texts}")
    if any(key != " " for key in section_keys):
        raise AssertionError("Custom section headers must use a single-space key")
    for forbidden_module in ("publicip", "weather"):
        if forbidden_module in module_types:
            raise AssertionError(f"Network-backed startup module is forbidden: {forbidden_module}")

    serialized = json.dumps(payload)
    if "dsForceDrm" in serialized:
        raise AssertionError("Linux-only dsForceDrm is forbidden in the universal config")


def main() -> int:
    """Run the offline contract validation."""
    validate_banner()
    validate_config(load_config())
    print("Mantle Fastfetch presentation contract is valid.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, json.JSONDecodeError, OSError) as error:
        print(f"mantle-fastfetch-validation: {error}", file=sys.stderr)
        raise SystemExit(1) from error
