# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Generate deterministic Egolint architecture artifacts from tool matrices."""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
import hashlib
from html import escape
import json
from pathlib import Path
import sys
from typing import Any

MEGALINTER_MATRIX = Path("egolint/.config/megalinter/tool-matrix.json")
COMPLEMENTARY_MATRIX = Path("egolint/.config/toolchain/tool-matrix.json")
DEFAULT_OUTPUT_DIRECTORY = Path(".reports/egolint/architecture")


@dataclass(frozen=True)
class ArchitectureInventory:
    """Normalized counts used by both generated artifacts."""

    source_digest: str
    megalinter_total: int
    megalinter_enabled: int
    megalinter_conditional: int
    megalinter_disabled: int
    megalinter_fast: int
    megalinter_holistic: int
    complementary_total: int
    complementary_enabled: int
    complementary_conditional: int
    complementary_disabled: int


def parse_args() -> argparse.Namespace:
    """Parse the generator command line."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", default=".")
    parser.add_argument(
        "--output-directory",
        default=DEFAULT_OUTPUT_DIRECTORY.as_posix(),
    )
    operation = parser.add_mutually_exclusive_group(required=True)
    operation.add_argument("--check", action="store_true")
    operation.add_argument("--write", action="store_true")
    return parser.parse_args()


def load_json(path: Path) -> dict[str, Any]:
    """Load one matrix and require a JSON object."""

    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"Unable to load matrix {path}: {error}") from error
    if not isinstance(value, dict):
        raise TypeError(f"Matrix must contain a JSON object: {path}")
    return value


def require_tools(matrix: dict[str, Any], path: Path) -> list[dict[str, Any]]:
    """Return a non-empty list of tool objects from one matrix."""

    tools = matrix.get("tools")
    if not isinstance(tools, list) or not tools:
        raise ValueError(f"Matrix must contain a non-empty tools array: {path}")
    if not all(isinstance(tool, dict) for tool in tools):
        raise ValueError(f"Every tool entry must be an object: {path}")
    return tools


def matrix_digest(repository_root: Path, paths: tuple[Path, ...]) -> str:
    """Return a stable digest over the exact matrix bytes and relative paths."""

    digest = hashlib.sha256()
    for path in paths:
        digest.update(path.as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update((repository_root / path).read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def build_inventory(repository_root: Path) -> ArchitectureInventory:
    """Normalize the two canonical tool matrices into architecture counts."""

    megalinter_path = repository_root / MEGALINTER_MATRIX
    complementary_path = repository_root / COMPLEMENTARY_MATRIX
    megalinter_tools = require_tools(load_json(megalinter_path), megalinter_path)
    complementary_tools = require_tools(load_json(complementary_path), complementary_path)

    configuration_states = Counter(
        str(tool.get("configuration_state")) for tool in megalinter_tools
    )
    complementary_states = Counter(str(tool.get("declared_state")) for tool in complementary_tools)

    unknown_megalinter_states = set(configuration_states) - {
        "enabled",
        "conditional",
        "disabled",
    }
    if unknown_megalinter_states:
        raise ValueError(
            "Unknown MegaLinter configuration state(s): "
            + ", ".join(sorted(unknown_megalinter_states))
        )
    unknown_complementary_states = set(complementary_states) - {
        "enabled",
        "conditional",
        "disabled",
    }
    if unknown_complementary_states:
        raise ValueError(
            "Unknown complementary state(s): " + ", ".join(sorted(unknown_complementary_states))
        )

    fast_count = sum(
        tool.get("profiles", {}).get("fast") == "selected" for tool in megalinter_tools
    )
    holistic_count = sum(
        tool.get("profiles", {}).get("holistic") == "selected" for tool in megalinter_tools
    )
    if fast_count == 0 or holistic_count == 0:
        raise ValueError("Fast and holistic MegaLinter profiles must both select tools")

    return ArchitectureInventory(
        source_digest=matrix_digest(
            repository_root,
            (MEGALINTER_MATRIX, COMPLEMENTARY_MATRIX),
        ),
        megalinter_total=len(megalinter_tools),
        megalinter_enabled=configuration_states["enabled"],
        megalinter_conditional=configuration_states["conditional"],
        megalinter_disabled=configuration_states["disabled"],
        megalinter_fast=fast_count,
        megalinter_holistic=holistic_count,
        complementary_total=len(complementary_tools),
        complementary_enabled=complementary_states["enabled"],
        complementary_conditional=complementary_states["conditional"],
        complementary_disabled=complementary_states["disabled"],
    )


def svg_text(  # noqa: PLR0913
    x: int,
    y: int,
    value: str,
    *,
    size: int = 18,
    fill: str = "#EDE9FE",
    weight: int = 500,
    anchor: str = "start",
    css_class: str = "",
) -> str:
    """Render one escaped SVG text element."""

    class_attribute = f' class="{css_class}"' if css_class else ""
    return (
        f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" '
        f'font-weight="{weight}" text-anchor="{anchor}"{class_attribute}>'
        f"{escape(value)}</text>"
    )


def card(  # noqa: PLR0913, PLR0917
    x: int,
    y: int,
    width: int,
    height: int,
    title: str,
    lines: list[str],
) -> str:
    """Render one architecture card."""

    elements = [
        (
            f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="20" '
            'fill="#15112B" stroke="#6D5DD3" stroke-width="2"/>'
        ),
        svg_text(x + 24, y + 38, title, size=21, fill="#F5D0FE", weight=700),
    ]
    for index, line in enumerate(lines):
        elements.append(svg_text(x + 24, y + 70 + index * 26, line, size=16))
    return "\n".join(elements)


def render_svg(inventory: ArchitectureInventory) -> str:
    """Render the deterministic architecture infographic."""

    parts = [
        (
            '<svg xmlns="http://www.w3.org/2000/svg" width="1440" height="1040" '
            'viewBox="0 0 1440 1040" role="img" aria-labelledby="title description" '
            'font-family="Inter, ui-sans-serif, system-ui, sans-serif">'
        ),
        '<title id="title">Egolint lint platform architecture</title>',
        (
            '<desc id="description">Execution paths, tool profiles, state model, and report '
            "publication flow generated from the canonical tool matrices.</desc>"
        ),
        "<defs>",
        '<linearGradient id="background" x1="0" y1="0" x2="1" y2="1">',
        '<stop offset="0" stop-color="#090719"/>',
        '<stop offset="0.55" stop-color="#181034"/>',
        '<stop offset="1" stop-color="#071A2D"/>',
        "</linearGradient>",
        '<filter id="glow" x="-40%" y="-40%" width="180%" height="180%">',
        '<feGaussianBlur stdDeviation="5" result="blur"/>',
        '<feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>',
        "</filter>",
        "</defs>",
        '<rect width="1440" height="1040" fill="url(#background)"/>',
        '<circle cx="1280" cy="80" r="180" fill="#8B5CF6" opacity="0.08"/>',
        '<circle cx="80" cy="920" r="230" fill="#22D3EE" opacity="0.06"/>',
        svg_text(72, 78, "EGOLINT QUALITY CONSTELLATION", size=34, weight=800),
        svg_text(
            72,
            112,
            "Deterministic architecture generated from the canonical tool matrices",
            size=18,
            fill="#A5B4FC",
        ),
        card(
            72,
            154,
            300,
            152,
            "Local",
            ["Taskfile: public command surface", "Fast, holistic, and direct tools"],
        ),
        card(
            404,
            154,
            300,
            152,
            "Editor",
            ["VS Code delegates to Taskfile", "One formatter per language"],
        ),
        card(
            736,
            154,
            300,
            152,
            "Hooks",
            ["Husky owns Git hooks", "Fast pre-commit + lint-staged"],
        ),
        card(
            1068,
            154,
            300,
            152,
            "CI",
            ["PRs: fast and read-only", "Trusted: holistic and publish"],
        ),
        (
            '<path d="M222 330 H1218" stroke="#6D5DD3" stroke-width="3" '
            'stroke-dasharray="8 10" opacity="0.8"/>'
        ),
        '<path d="M720 330 V376" stroke="#C084FC" stroke-width="4" marker-end="none"/>',
        card(
            72,
            378,
            628,
            220,
            f"MegaLinter-native · {inventory.megalinter_total} tools",
            [
                f"Fast profile: {inventory.megalinter_fast} selected",
                f"Holistic profile: {inventory.megalinter_holistic} selected",
                f"Configured: {inventory.megalinter_enabled} enabled",
                f"Project-aware: {inventory.megalinter_conditional} conditional",
                f"Deferred: {inventory.megalinter_disabled} disabled with reasons",
                "Reports: .reports/megalinter/",
            ],
        ),
        card(
            740,
            378,
            628,
            220,
            f"Complementary · {inventory.complementary_total} tools",
            [
                f"Universal: {inventory.complementary_enabled} enabled",
                f"Project-aware: {inventory.complementary_conditional} conditional",
                f"Disabled: {inventory.complementary_disabled}",
                "Not applicable is distinct from missing dependency",
                "Reports: .reports/complementary/<tool>/",
            ],
        ),
        svg_text(720, 644, "OBSERVABILITY AND PUBLICATION", size=23, weight=800, anchor="middle"),
        card(
            72,
            682,
            396,
            170,
            "Complete artifacts",
            [
                "Every run uploads native output",
                "Run ID and attempt preserve history",
                "30-day retention",
            ],
        ),
        card(
            522,
            682,
            396,
            170,
            "Security findings",
            [
                "Valid SARIF → Code Scanning",
                "OSV keeps its severity gate",
                "Signals retain canonical owners",
            ],
        ),
        card(
            972,
            682,
            396,
            170,
            "Curated latest",
            [
                "Trusted default-branch runs only",
                "Stable snapshots under .reports/",
                "Git history replaces timestamp trees",
            ],
        ),
        '<path d="M468 767 H522" stroke="#22D3EE" stroke-width="4" filter="url(#glow)"/>',
        '<path d="M918 767 H972" stroke="#22D3EE" stroke-width="4" filter="url(#glow)"/>',
        svg_text(72, 910, "STATE MODEL", size=20, weight=800, fill="#A5B4FC"),
        '<rect x="72" y="934" width="18" height="18" rx="5" fill="#34D399"/>',
        svg_text(100, 949, "Enabled / selected / passed", size=15),
        '<rect x="392" y="934" width="18" height="18" rx="5" fill="#FBBF24"/>',
        svg_text(420, 949, "Conditional / not applicable", size=15),
        '<rect x="742" y="934" width="18" height="18" rx="5" fill="#A78BFA"/>',
        svg_text(770, 949, "Disabled / deferred with reason", size=15),
        '<rect x="1080" y="934" width="18" height="18" rx="5" fill="#FB7185"/>',
        svg_text(1108, 949, "Findings / execution error", size=15),
        svg_text(
            72,
            1000,
            f"Source digest: {inventory.source_digest[:16]}",
            size=14,
            fill="#64748B",
        ),
        "</svg>",
    ]
    return "\n".join(parts) + "\n"


def render_markdown(inventory: ArchitectureInventory) -> str:
    """Render the deterministic Markdown legend and source contract."""

    return f"""# Egolint lint architecture

![Egolint lint platform architecture](lint-architecture.svg)

This snapshot is generated from the canonical tool matrices. Edit the source
configuration and regenerate it; do not hand-edit the SVG or this legend.

## Tool inventory

<!-- prettier-ignore -->
| Layer | Total | Enabled / selected | Conditional / disabled |
| --- | ---: | ---: | ---: |
| MegaLinter-native | {inventory.megalinter_total} | {inventory.megalinter_enabled} enabled | {inventory.megalinter_conditional} conditional; {inventory.megalinter_disabled} disabled |
| MegaLinter fast profile | {inventory.megalinter_total} | {inventory.megalinter_fast} selected | {inventory.megalinter_total - inventory.megalinter_fast} excluded |
| MegaLinter holistic profile | {inventory.megalinter_total} | {inventory.megalinter_holistic} selected | {inventory.megalinter_total - inventory.megalinter_holistic} not selected |
| Complementary | {inventory.complementary_total} | {inventory.complementary_enabled} enabled | {inventory.complementary_conditional} conditional; {inventory.complementary_disabled} disabled |

## Execution paths

<!-- prettier-ignore -->
| Path | Contract |
| --- | --- |
| Local | Taskfile exposes fast, holistic, complementary, security, SBOM, and architecture commands. |
| VS Code | Repository tasks delegate to Taskfile and use canonical configuration paths. |
| Git hooks | Husky owns hooks; lint-staged and pre-commit run the bounded fast policy. |
| Pull requests | Read-only fast MegaLinter, commit policy, automation validation, OSV, and architecture generation. |
| Trusted runs | Default-branch pushes, schedules, and manual dispatches run holistic policy and may publish stable snapshots. |

## Result states

<!-- prettier-ignore -->
| State family | Meaning |
| --- | --- |
| Enabled / selected | Policy intentionally activates the tool in that context. |
| Conditional / not applicable | Project markers decide whether the tool should execute. |
| Disabled / deferred | Policy records the exact blocker or ownership reason. |
| Passed / warnings / findings | The tool executed and returned normalized results. |
| Missing / configuration / execution error | The tool could not produce a trustworthy lint result. |

## Report destinations

- MegaLinter native output: `.reports/megalinter/`
- Complementary normalized results: `.reports/complementary/<tool>/latest.json`
- OSV native and normalized output: `.reports/osv/`
- Supply-chain views: `.reports/supply-chain/`
- This architecture snapshot: `.reports/egolint/architecture/`
- Valid SARIF findings: GitHub Code Scanning
- Complete run history: GitHub Actions artifacts and Git history

Only trusted default-branch runs may commit curated `latest` snapshots. Pull
requests never receive report write permissions.

## Generation contract

- MegaLinter source: `{MEGALINTER_MATRIX.as_posix()}`
- Complementary source: `{COMPLEMENTARY_MATRIX.as_posix()}`
- Source digest: `{inventory.source_digest}`
"""


def output_paths(repository_root: Path, output_directory: str) -> tuple[Path, Path]:
    """Resolve safe output paths within the repository."""

    requested = Path(output_directory)
    if requested.is_absolute() or ".." in requested.parts:
        raise ValueError("Output directory must be repository-relative and traversal-free")
    if requested.parts != (".reports", "egolint", "architecture"):
        raise ValueError("Output directory must be .reports/egolint/architecture")
    root = repository_root.resolve()
    destination = (root / requested).resolve()
    if not destination.is_relative_to(root):
        raise ValueError("Output directory escaped the repository root")
    return destination / "README.md", destination / "lint-architecture.svg"


def check_file(path: Path, expected: str) -> bool:
    """Report whether one generated file is current."""

    try:
        current = path.read_text(encoding="utf-8")
    except OSError:
        print(f"Generated architecture artifact is missing: {path}", file=sys.stderr)
        return False
    if current != expected:
        print(f"Generated architecture artifact is stale: {path}", file=sys.stderr)
        return False
    return True


def main() -> int:
    """Run check or write mode."""

    args = parse_args()
    repository_root = Path(args.repository_root).resolve()
    try:
        inventory = build_inventory(repository_root)
        markdown_path, svg_path = output_paths(repository_root, args.output_directory)
    except (TypeError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 2

    rendered_markdown = render_markdown(inventory)
    rendered_svg = render_svg(inventory)
    if args.check:
        current = check_file(markdown_path, rendered_markdown)
        current = check_file(svg_path, rendered_svg) and current
        if not current:
            print("Run the architecture generator with --write.", file=sys.stderr)
            return 1
        print("Lint architecture artifacts are current.")
        return 0

    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.write_text(rendered_markdown, encoding="utf-8")
    svg_path.write_text(rendered_svg, encoding="utf-8")
    print(f"Generated {markdown_path.relative_to(repository_root)}")
    print(f"Generated {svg_path.relative_to(repository_root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
