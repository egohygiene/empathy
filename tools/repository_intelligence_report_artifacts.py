#!/usr/bin/env python3
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
# Fixed public-safe diagnostics do not reflect rejected provider material.
# ruff: noqa: TRY003

"""Admit explicitly selected Empathy report artifacts without changing source.

Relay remains the normalizer and report-schema validator. This consumer adapter
binds reviewed artifact identities to one exact trusted producer/source boundary
and stages only the byte-pinned normalized summaries for the native builder.
"""

from __future__ import annotations

import argparse
import hashlib
from http import HTTPStatus
import os
from pathlib import Path
import re
import subprocess  # nosec B404 # Fixed local Git identity, never a shell.
import sys
from typing import TYPE_CHECKING, Any, cast
from urllib.error import HTTPError, URLError
from urllib.request import Request, build_opener

from tools.repository_intelligence_publication import (
    REPORT_SCHEMA,
    REPOSITORY,
    NoRedirects,
    PublicationError,
    normalized_timestamp,
    parse_json,
    write_json,
)

if TYPE_CHECKING:
    from collections.abc import Callable

SELECTION_SCHEMA = "empathy.repository-intelligence-report-artifact-selection/v1"
RECEIPT_SCHEMA = "empathy.repository-intelligence-report-artifact-intake/v1"
PRIVATE_ROOT = Path(".cache/repository-intelligence-publication")
DOWNLOAD_ROOT = PRIVATE_ROOT / "report-artifacts"
REPORT_ROOT = PRIVATE_ROOT / "selected-reports"
MAX_BYTES = 2 * 1024 * 1024
PRODUCERS = {
    "osv": (".github/workflows/osv-scan.yml", "🔍 OSV Vulnerability Scan"),
    "megalinter": (".github/workflows/megalinter.yml", "MegaLinter"),
    "scorecard": (".github/workflows/ossf-scorecard.yml", "OpenSSF Scorecard"),
}
EVENTS = {"push", "schedule", "workflow_dispatch"}
CONCLUSIONS = {"success", "failure", "neutral", "timed_out", "action_required"}
FIELDS = {"producer", "run_id", "run_attempt", "artifact_id", "archive_sha256", "summary_sha256"}


def require(condition: bool) -> None:
    """Fail closed without reflecting rejected provider content or credentials."""
    if not condition:
        raise PublicationError("Selected report artifact admission failed.")


def read(path: Path) -> bytes:
    """Read a bounded regular input without following path aliases."""
    require(not any(p.is_symlink() for p in (path, *path.parents)))
    require(path.is_file() and path.stat().st_size <= MAX_BYTES)
    return path.read_bytes()


def selected(value: dict[str, Any]) -> list[dict[str, Any]]:
    """Accept only an explicit closed, bounded selection of unique producers."""
    require(set(value) == {"schema", "reports"} and value["schema"] == SELECTION_SCHEMA)
    reports = value["reports"]
    require(isinstance(reports, list) and 0 < len(reports) <= len(PRODUCERS))
    seen: set[str] = set()
    for report in reports:
        require(isinstance(report, dict) and set(report) == FIELDS)
        producer = report["producer"]
        require(isinstance(producer, str) and producer in PRODUCERS and producer not in seen)
        seen.add(producer)
        for key in ("run_id", "run_attempt", "artifact_id"):
            require(type(report[key]) is int and 0 < report[key] < 2**53)
        for key in ("archive_sha256", "summary_sha256"):
            require(
                isinstance(report[key], str)
                and re.fullmatch(r"[0-9a-f]{64}", report[key]) is not None
            )
    return cast("list[dict[str, Any]]", reports)


def revision(root: Path) -> str:
    """Resolve only the actual checkout identity; no source override is accepted."""
    value = subprocess.check_output(  # noqa: S603 # nosec B603, B607
        ["git", "-C", str(root), "rev-parse", "HEAD"],  # noqa: S607
        text=True,
    ).strip()
    require(re.fullmatch(r"[0-9a-f]{40}", value) is not None)
    return value


def api(path: str) -> dict[str, Any]:
    """Read bounded metadata only from GitHub's fixed API origin."""
    token = os.environ.get("GH_TOKEN")
    require(bool(token))
    request = Request(
        "https://api.github.com/repos/" + REPOSITORY + "/actions/" + path,
        headers={
            "Authorization": "Bearer " + str(token),
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    with build_opener(NoRedirects()).open(request, timeout=20) as response:
        require(response.status == HTTPStatus.OK)
        raw = response.read(MAX_BYTES + 1)
    return parse_json(raw)


def admit(
    value: dict[str, Any],
    source: str,
    default_branch: str,
    fetch: Callable[[str], dict[str, Any]] = api,
) -> dict[str, Any]:
    """Bind exact artifacts to completed, trusted, same-source producer runs."""
    records = []
    for report in selected(value):
        run = fetch("runs/" + str(report["run_id"]))
        artifact = fetch("artifacts/" + str(report["artifact_id"]))
        workflow, name = PRODUCERS[report["producer"]]
        require(
            run.get("id") == report["run_id"] and run.get("run_attempt") == report["run_attempt"]
        )
        require(run.get("repository", {}).get("full_name") == REPOSITORY)
        require(run.get("head_repository", {}).get("full_name") == REPOSITORY)
        require(run.get("head_sha") == source and run.get("head_branch") == default_branch)
        require(run.get("path") == workflow and run.get("name") == name)
        require(run.get("status") == "completed" and run.get("event") in EVENTS)
        require(run.get("conclusion") in CONCLUSIONS)
        expected_name = (
            f"empathy-report-{report['producer']}-{report['run_id']}-{report['run_attempt']}"
        )
        require(
            artifact.get("id") == report["artifact_id"] and artifact.get("name") == expected_name
        )
        require(artifact.get("expired") is False and type(artifact.get("size_in_bytes")) is int)
        require(0 < artifact["size_in_bytes"] <= MAX_BYTES)
        require(artifact.get("digest") == "sha256:" + report["archive_sha256"])
        artifact_run = artifact.get("workflow_run", {})
        require(
            artifact_run.get("id") == report["run_id"] and artifact_run.get("head_sha") == source
        )
        records.append(
            {
                **report,
                "artifact_name": expected_name,
                "event": run["event"],
                "conclusion": run["conclusion"],
            }
        )
    return {
        "schema": RECEIPT_SCHEMA,
        "repository": REPOSITORY,
        "source_commit": source,
        "reports": records,
        "mode": "selected-artifacts",
    }


def stage(root: Path, receipt: dict[str, Any]) -> None:
    """Stage only exact selected summary bytes; omitted producers stay absent."""
    source = revision(root)
    require(receipt.get("schema") == RECEIPT_SCHEMA and receipt.get("repository") == REPOSITORY)
    require(receipt.get("source_commit") == source and receipt.get("mode") == "selected-artifacts")
    require(set(receipt) == {"schema", "repository", "source_commit", "reports", "mode"})
    reports = receipt["reports"]
    selected(
        {"schema": SELECTION_SCHEMA, "reports": [{k: row[k] for k in FIELDS} for row in reports]}
    )
    downloads, destination = root / DOWNLOAD_ROOT, root / REPORT_ROOT
    require(
        not destination.exists()
        and not any(p.is_symlink() for p in (downloads, *downloads.parents))
    )
    require(
        downloads.is_dir()
        and {p.name for p in downloads.iterdir()} == {r["artifact_name"] for r in reports}
    )
    pending = []
    for report in reports:
        folder = downloads / report["artifact_name"]
        require(
            folder.is_dir()
            and not folder.is_symlink()
            and {p.name for p in folder.iterdir()} == {"summary.json"}
        )
        raw = read(folder / "summary.json")
        require(hashlib.sha256(raw).hexdigest() == report["summary_sha256"])
        summary = parse_json(raw)
        require(
            summary.get("schema") == REPORT_SCHEMA
            and type(summary.get("schema_version")) is int
            and summary.get("schema_version") == 1
        )
        require(summary.get("repository") == REPOSITORY and summary.get("commit") == source)
        require(summary.get("producer") == report["producer"])
        provenance = summary.get("provenance", {})
        require(str(provenance.get("run_id")) == str(report["run_id"]))
        require(
            provenance.get("run_attempt") == report["run_attempt"]
            and provenance.get("event") == report["event"]
        )
        require(provenance.get("workflow") == PRODUCERS[report["producer"]][1])
        require(normalized_timestamp(summary.get("generated_at")) is not None)
        pending.append((report["producer"], raw))
    for producer, raw in pending:
        path = destination / producer / "summary.json"
        path.parent.mkdir(parents=True, exist_ok=False)
        path.write_bytes(raw)


def main() -> int:
    """Run the bounded admission or post-download staging operation."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("admit", "stage"))
    parser.add_argument("--repository-root", type=Path, default=Path())
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--github-output", type=Path)
    args = parser.parse_args()
    try:
        if args.operation == "stage":
            stage(args.repository_root, parse_json(read(args.receipt)))
            return 0
        raw = os.environ.get("REPORT_ARTIFACTS", "")
        require(os.environ.get("GITHUB_REPOSITORY", REPOSITORY) == REPOSITORY)
        require(not raw or os.environ.get("GITHUB_EVENT_NAME") == "workflow_dispatch")
        require(not raw or os.environ.get("DEPLOYMENT_MODE", "current") == "current")
        if raw:
            branch = os.environ.get("DEFAULT_BRANCH", "")
            require(bool(branch))
            receipt = admit(parse_json(raw.encode()), revision(args.repository_root), branch)
        else:
            receipt = {
                "schema": RECEIPT_SCHEMA,
                "repository": REPOSITORY,
                "source_commit": revision(args.repository_root),
                "reports": [],
                "mode": "committed",
            }
        write_json(args.receipt, receipt, sites=(args.repository_root / ".cache/mindgarden/site",))
        require(args.github_output is not None)
        if args.github_output is not None:
            with args.github_output.open("a", encoding="utf-8") as output:
                output.write("selected-artifacts=" + str(bool(raw)).lower() + "\n")
                output.write(
                    "artifact-ids="
                    + ",".join(str(r["artifact_id"]) for r in receipt["reports"])
                    + "\n"
                )
                output.write(
                    "reports-directory=" + (REPORT_ROOT.as_posix() if raw else ".reports") + "\n"
                )
                for report in receipt["reports"]:
                    for key in ("artifact_id", "run_id", "artifact_name"):
                        output.write(
                            report["producer"]
                            + "-"
                            + key.replace("_", "-")
                            + "="
                            + str(report[key])
                            + "\n"
                        )
    except (
        PublicationError,
        OSError,
        subprocess.SubprocessError,
        HTTPError,
        URLError,
        KeyError,
        TypeError,
        AttributeError,
        ValueError,
    ):
        print(  # noqa: T201
            "Empathy report artifact admission failed; inspect the reviewed selection.",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
