#!/usr/bin/env python3
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
# Standalone repository-maintenance entry point, not a Python package.

"""Attempt both baseline unittest commands and retain their independent outcomes."""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import json
from pathlib import Path
import subprocess  # nosec B404 - fixed local Python argv, no shell or caller command.
import sys
from typing import Literal

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SUITES = (("repository", "tests"), ("egolint", "egolint/tests"))
SUITE_TIMEOUT_SECONDS = 300


@dataclass(frozen=True)
class SuiteOutcome:
    """Command outcomes only; a zero exit does not certify skipped scenarios."""

    suite: str
    exit_code: int | None
    unavailable: Literal["timeout", "launch-failed"] | None = None

    @property
    def succeeded(self) -> bool:
        """Whether the command completed successfully, independent of acceptance."""
        return self.exit_code == 0 and self.unavailable is None


def run_suites(repository_root: Path, output_directory: Path) -> list[SuiteOutcome]:
    """Run each fixed suite in its own interpreter, including after a failure."""
    output_directory.mkdir(parents=True, exist_ok=True)
    outcomes: list[SuiteOutcome] = []
    for name, directory in SUITES:
        log_path = output_directory / f"{name}.log"
        with log_path.open("w", encoding="utf-8") as log:
            try:
                # Only this interpreter and repository-owned discovery paths execute.
                completed = subprocess.run(  # noqa: S603  # nosec B603
                    [
                        sys.executable,
                        "-m",
                        "unittest",
                        "discover",
                        "--start-directory",
                        directory,
                        "--pattern",
                        "test_*.py",
                        "--verbose",
                    ],
                    cwd=repository_root,
                    stdout=log,
                    stderr=subprocess.STDOUT,
                    check=False,
                    timeout=SUITE_TIMEOUT_SECONDS,
                )
            except subprocess.TimeoutExpired:
                outcomes.append(SuiteOutcome(name, None, "timeout"))
            except OSError:
                outcomes.append(SuiteOutcome(name, None, "launch-failed"))
            else:
                outcomes.append(SuiteOutcome(name, completed.returncode))
        sys.stdout.write(f"\n=== {name} unittest command ===\n")
        sys.stdout.write(log_path.read_text(encoding="utf-8", errors="replace"))
    return outcomes


def render_summary(outcomes: list[SuiteOutcome]) -> str:
    """Keep process status separate from full-profile or required-scenario proof."""
    lines = [
        "## Baseline unittest command results",
        "",
        "| Suite | Command outcome | Exit code |",
        "| --- | --- | --- |",
    ]
    for outcome in outcomes:
        state = outcome.unavailable or ("succeeded" if outcome.succeeded else "failed")
        exit_code = "unavailable" if outcome.exit_code is None else str(outcome.exit_code)
        lines.append(f"| {outcome.suite} | {state} | {exit_code} |")
    lines.extend(
        [
            "",
            (
                "These are independent command outcomes, not full acceptance evidence. "
                "Each verbose log retains actual counts, failures, and environment skips. "
                "Required owner scenarios, Rust disposition (#79), and canonical lint "
                "qualification (#109/#110) remain separate gates."
            ),
            "",
        ],
    )
    return "\n".join(lines)


def main() -> int:
    """Retain results before returning a failing aggregate when either suite fails."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-directory", type=Path, required=True)
    parser.add_argument("--summary", type=Path, help="Append the result table to this file.")
    arguments = parser.parse_args()
    output_directory: Path = arguments.output_directory
    summary_path: Path | None = arguments.summary
    outcomes = run_suites(REPOSITORY_ROOT, output_directory)
    report = {
        "schema": "empathy.baseline-unittest-commands/v1",
        "acceptance": "unqualified",
        "suites": [asdict(outcome) for outcome in outcomes],
    }
    (output_directory / "results.json").write_text(
        json.dumps(report, indent=2) + "\n",
        encoding="utf-8",
    )
    summary = render_summary(outcomes)
    (output_directory / "summary.md").write_text(summary, encoding="utf-8")
    if summary_path is not None:
        with summary_path.open("a", encoding="utf-8") as destination:
            destination.write(summary)
    sys.stdout.write(summary)
    return 0 if all(outcome.succeeded for outcome in outcomes) else 1


if __name__ == "__main__":
    raise SystemExit(main())
