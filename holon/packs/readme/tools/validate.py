#!/usr/bin/env python3
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Validate the reusable Holon README pack without external dependencies."""

from __future__ import annotations

from pathlib import Path
import re
import sys

PACK_ROOT = Path(__file__).resolve().parents[1]
PROJECT_TEMPLATE = PACK_ROOT / "templates/project/README.md"
PROFILE_TEMPLATE = PACK_ROOT / "templates/profile/README.md"
RESEARCH = PACK_ROOT / "references/research-and-design.md"
REQUIRED_FILES = (
    PACK_ROOT / "README.md",
    PACK_ROOT / "PROVENANCE.md",
    PACK_ROOT / "pack.yaml",
    PROJECT_TEMPLATE,
    PROFILE_TEMPLATE,
    RESEARCH,
)
TOKEN_PATTERN = re.compile(r"\{\{([A-Z][A-Z0-9_]*)\}\}")
ANY_TOKEN_PATTERN = re.compile(r"\{\{([^{}]+)\}\}")


def heading_ids(source: str) -> set[str]:
    """Return GitHub-style identifiers for Markdown ATX headings."""
    identifiers: set[str] = set()
    for line in source.splitlines():
        if not line.startswith("#"):
            continue
        title = line.lstrip("#").strip().lower()
        identifier = re.sub(r"[^a-z0-9 _-]", "", title)
        identifiers.add(re.sub(r"[ _]+", "-", identifier))
    return identifiers


def validate_template(path: Path, required_sections: tuple[str, ...]) -> list[str]:
    """Validate one source template and return human-readable failures."""
    failures: list[str] = []
    source = path.read_text(encoding="utf-8")
    h1_lines = [line for line in source.splitlines() if line.startswith("# ")]
    if len(h1_lines) != 1:
        failures.append(f"{path}: expected exactly one H1, found {len(h1_lines)}")

    malformed_tokens = {
        match.group(0)
        for match in ANY_TOKEN_PATTERN.finditer(source)
        if TOKEN_PATTERN.fullmatch(match.group(0)) is None
    }
    if malformed_tokens:
        failures.append(f"{path}: malformed placeholders: {sorted(malformed_tokens)}")
    if not TOKEN_PATTERN.search(source):
        failures.append(f"{path}: source template has no placeholders")
    if "example.com" in source:
        failures.append(f"{path}: example.com must not appear in a publishing template")

    identifiers = heading_ids(source)
    for required in required_sections:
        if required not in identifiers:
            failures.append(f"{path}: missing required section #{required}")

    if re.search(r"!\[\]\(", source):
        failures.append(f"{path}: Markdown image has empty alt text")
    if re.search(r"<img\s+(?![^>]*\balt=)[^>]*>", source, flags=re.IGNORECASE):
        failures.append(f"{path}: HTML image has no alt attribute")
    return failures


def validate_generated_regions(source: str, path: Path) -> list[str]:
    """Require each named generated-region marker to be balanced."""
    failures: list[str] = []
    starts = re.findall(r"<!--\s*([a-z0-9:-]+):START\s*-->", source)
    ends = re.findall(r"<!--\s*([a-z0-9:-]+):END\s*-->", source)
    if sorted(starts) != sorted(ends):
        failures.append(f"{path}: generated region markers are unbalanced")
    return failures


def validate() -> list[str]:
    """Return every pack validation failure."""
    failures: list[str] = []
    for required_file in REQUIRED_FILES:
        if not required_file.is_file() or required_file.stat().st_size == 0:
            failures.append(f"missing or empty pack artifact: {required_file}")
    if failures:
        return failures

    failures.extend(
        validate_template(
            PROJECT_TEMPLATE,
            (
                "why-project-name",
                "highlights",
                "quick-start",
                "usage",
                "compatibility",
                "development",
                "security",
                "support",
                "contributing",
                "license",
            ),
        )
    )
    failures.extend(
        validate_template(
            PROFILE_TEMPLATE,
            (
                "thirty-second-brief",
                "proof-at-a-glance",
                "selected-impact",
                "featured-systems",
                "engineering-capabilities",
                "experience",
                "contact",
            ),
        )
    )
    profile_source = PROFILE_TEMPLATE.read_text(encoding="utf-8")
    for stale_personal_fact in ("Alan Szmyt", "MIT Lincoln Laboratory"):
        if stale_personal_fact in profile_source:
            failures.append(
                f"{PROFILE_TEMPLATE}: reusable template contains {stale_personal_fact!r}"
            )
    failures.extend(validate_generated_regions(profile_source, PROFILE_TEMPLATE))

    manifest = (PACK_ROOT / "pack.yaml").read_text(encoding="utf-8")
    for required_reference in (
        "./templates/project/README.md",
        "./templates/profile/README.md",
        "./references/research-and-design.md",
        "./PROVENANCE.md",
    ):
        if required_reference not in manifest:
            failures.append(f"pack.yaml does not reference {required_reference}")
    if "snapshot" not in RESEARCH.read_text(encoding="utf-8").lower():
        failures.append("research brief must identify its corpus as a snapshot")
    return failures


def main() -> int:
    """Run validation and report failures."""
    failures = validate()
    if failures:
        for failure in failures:
            print(f"readme-pack: {failure}", file=sys.stderr)
        return 1
    print("Holon README pack is valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
