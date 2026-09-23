#!/usr/bin/env python3
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
# Fixed public-safe CLI diagnostics belong beside their checks; no source values are interpolated.
# ruff: noqa: TRY003

"""Empathy's bounded publication evidence adapters; Relay owns provenance validation."""

from __future__ import annotations

import argparse
from datetime import UTC, datetime
import hashlib
from http import HTTPStatus
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import HTTPRedirectHandler, Request, build_opener

REPOSITORY = "egohygiene/empathy"
SITE_URL = "https://egohygiene.github.io/empathy/"
REPORT_SCHEMA = "egohygiene.repository-report-summary/v1"
MANIFEST_SCHEMA = "egohygiene.relay.repository-intelligence-build-manifest/v1"
BASELINE_SCHEMA = "egohygiene.relay.repository-intelligence-consumer-route-baseline/v1"
REVISION = re.compile(r"[0-9a-f]{40}\Z")
MAX_JSON_BYTES = 2 * 1024 * 1024
MAX_FILE_BYTES = 32 * 1024 * 1024
MAX_SITE_BYTES = 256 * 1024 * 1024
MAX_SITE_FILES = 10000
MAX_LIVE_ATTEMPTS = 12
MAX_RETRY_DELAY_SECONDS = 30
GARDEN_ROUTES = (
    "",
    "dashboard.html",
    "projects/index.html",
    "projects/egohygiene-web-namespace.html",
    "projects/repository-intelligence-dashboard.html",
)
INTELLIGENCE_ROUTES = tuple(
    "intelligence/" + (name + "/" if name else "")
    for name in (
        "",
        "now",
        "roadmap",
        "decisions",
        "journey",
        "dependencies",
        "health",
        "releases",
        "work",
        "search",
        "compare",
        "dashboard",
    )
)
PRODUCERS = {"MegaLinter", "OpenSSF Scorecard", "🔍 OSV Vulnerability Scan"}
EVENTS = {"push", "pull_request", "workflow_run", "workflow_dispatch", "schedule"}
CONCLUSIONS = {
    "success",
    "failure",
    "cancelled",
    "timed_out",
    "neutral",
    "skipped",
    "action_required",
    "stale",
    "startup_failure",
}
FAILURES = {
    "checkout": ("EPI-001", "Retry a complete checkout of the represented revision."),
    "inputs": ("EPI-002", "Review normalized report and pinned publication inputs."),
    "garden": ("EPI-003", "Repair the reviewed-public projection or pinned Quartz build."),
    "intelligence": ("EPI-004", "Review the immutable Relay builder contract and inputs."),
    "composition": ("EPI-005", "Rebuild and verify the manifest and preserved consumer bytes."),
    "deployment": ("EPI-006", "Review the consumer Pages deployment and retry the exact build."),
    "receipt": ("EPI-007", "Verify the retained composition and finalize its separate receipt."),
    "live": ("EPI-008", "Verify the expected deployment is live and retry bounded route checks."),
}


class PublicationError(ValueError):
    """A public-safe consumer publication failure."""


class DuplicateKeyError(PublicationError):
    """Ambiguous JSON must not enter the publisher."""


def _object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise DuplicateKeyError("Duplicate JSON keys are prohibited.")
        value[key] = item
    return value


def parse_json(data: bytes) -> dict[str, Any]:
    """Reject ambiguous or unbounded JSON without reflecting source material."""
    if len(data) > MAX_JSON_BYTES:
        raise PublicationError("JSON exceeds the evidence bound.")
    try:
        value = json.loads(
            data, object_pairs_hook=_object, parse_constant=lambda _: _reject_constant()
        )
    except (UnicodeError, json.JSONDecodeError, RecursionError) as error:
        raise PublicationError("JSON is invalid.") from error
    if not isinstance(value, dict):
        raise PublicationError("JSON evidence must be an object.")
    return value


def _reject_constant() -> None:
    raise PublicationError("Non-finite JSON numbers are prohibited.")


def sha256(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def _read(path: Path, limit: int = MAX_JSON_BYTES) -> bytes:
    if path.is_symlink() or any(parent.is_symlink() for parent in path.parents):
        raise PublicationError("Evidence rejects symbolic links.")
    if not path.is_file() or path.stat().st_size > limit:
        raise PublicationError("Evidence is unavailable or exceeds its bound.")
    return path.read_bytes()


def write_json(path: Path, value: dict[str, Any], *, sites: tuple[Path, ...] = ()) -> None:
    """Keep run-specific evidence outside every declared composed site."""
    target = path.absolute()
    if target.is_symlink() or any(parent.is_symlink() for parent in target.parents):
        raise PublicationError("Evidence rejects symbolic links.")
    for site in sites:
        if target.resolve().is_relative_to(site.resolve()):
            raise PublicationError("Run evidence must remain outside the public site.")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def canonicalize_baseline(path: Path) -> None:
    """Adapt the pinned v1.6 producer's Path ordering to its verifier's lexical order."""
    value = parse_json(_read(path))
    if value.get("schema") != BASELINE_SCHEMA or value.get("schema_version") != 1:
        raise PublicationError("The pinned baseline schema is required.")
    files = value.get("files")
    if not isinstance(files, list) or not files:
        raise PublicationError("Baseline files are missing.")
    paths = []
    for record in files:
        if not isinstance(record, dict) or not isinstance(record.get("path"), str):
            raise PublicationError("Baseline file records are invalid.")
        paths.append(record["path"])
    if len(set(paths)) != len(paths):
        raise PublicationError("Baseline paths are ambiguous.")
    value["files"] = sorted(files, key=lambda record: record["path"])
    write_json(path, value)


def _revision(value: Any) -> str:
    if not isinstance(value, str) or not REVISION.fullmatch(value):
        raise PublicationError("An exact immutable revision is required.")
    return value


def _positive(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (str, int)) and re.fullmatch(r"[1-9][0-9]{0,19}", str(value)):
        return int(value)
    return None


def _git(root: Path, revision: str) -> str:
    # Trusted runner Git, fixed rev-parse operation and HEAD/tree references; never a shell.
    return subprocess.run(  # noqa: S603
        ["git", "-C", str(root), "rev-parse", "--verify", revision],  # noqa: S607
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _enum(value: Any, allowed: set[str]) -> str:
    return value if isinstance(value, str) and value in allowed else "unknown"


def _same_repository(value: Any) -> bool:
    return (
        isinstance(value, dict)
        and isinstance(value.get("full_name"), str)
        and value["full_name"].lower() == REPOSITORY
    )


def normalized_timestamp(value: Any) -> str | None:
    """Retain only valid, timezone-aware instants in one public UTC form."""
    if not isinstance(value, str) or not re.fullmatch(
        r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}"
        r"(?:\.[0-9]{1,6})?(?:Z|[+-][0-9]{2}:[0-9]{2})",
        value,
    ):
        return None
    try:
        instant = datetime.fromisoformat(value)
        return instant.astimezone(UTC).isoformat().replace("+00:00", "Z")
    except (ValueError, OverflowError):
        return None


def workflow_metadata(environment: dict[str, str]) -> dict[str, Any]:
    """Record provider identifiers, never actor names, URLs, raw payloads or tokens."""
    event = environment.get("GITHUB_EVENT_NAME")
    result: dict[str, Any] = {
        "run_id": _positive(environment.get("GITHUB_RUN_ID")),
        "run_attempt": _positive(environment.get("GITHUB_RUN_ATTEMPT")),
        "event": _enum(event, EVENTS),
        "triggering_producer": None,
    }
    if event != "workflow_run":
        return result
    event_path = environment.get("GITHUB_EVENT_PATH")
    if not event_path:
        raise PublicationError("Producer event metadata is unavailable.")
    payload = parse_json(_read(Path(event_path)))
    run = payload.get("workflow_run")
    if not isinstance(run, dict):
        raise PublicationError("Producer event metadata is incompatible.")
    repository = run.get("repository", {})
    head_repository = run.get("head_repository", {})
    same_repository = _same_repository(repository) and _same_repository(head_repository)
    revision = run.get("head_sha")
    producer_event = _enum(run.get("event"), EVENTS)
    name = _enum(run.get("name"), PRODUCERS)
    conclusion = _enum(run.get("conclusion"), CONCLUSIONS)
    candidate = (
        same_repository
        and run.get("head_branch") == "main"
        and producer_event in {"push", "workflow_dispatch", "schedule"}
        and name in PRODUCERS
        and run.get("status") == "completed"
        and isinstance(revision, str)
        and bool(REVISION.fullmatch(revision))
        and _positive(run.get("id")) is not None
    )
    result["triggering_producer"] = {
        "run_id": _positive(run.get("id")),
        "run_attempt": _positive(run.get("run_attempt")),
        "workflow": name,
        "event": producer_event,
        "conclusion": conclusion,
        "head_revision": revision
        if isinstance(revision, str) and REVISION.fullmatch(revision)
        else None,
        "same_repository": bool(same_repository),
        "default_branch": run.get("head_branch") == "main",
        "trusted_refresh_candidate": bool(candidate),
    }
    return result


def report_evidence(path: Path, producer: str, revision: str) -> dict[str, Any]:
    """Observe normalized inputs; the Relay owner remains their schema validator."""
    result: dict[str, Any] = {
        "producer": producer,
        "sha256": None,
        "schema": "unknown",
        "state": "missing",
        "execution": "unknown",
        "source_revision": None,
        "matches_consumer_revision": False,
        "generated_at": None,
        "expires_at": None,
    }
    if not path.exists() and not path.is_symlink():
        return result
    data = _read(path)
    result["sha256"] = sha256(data)
    try:
        report = parse_json(data)
    except DuplicateKeyError:
        raise
    except PublicationError:
        result["state"] = "invalid"
        return result
    if (
        report.get("schema") != REPORT_SCHEMA
        or report.get("schema_version") != 1
        or report.get("producer") != producer
        or report.get("repository") != REPOSITORY
    ):
        result["state"] = "incompatible"
        return result
    result["schema"] = REPORT_SCHEMA
    result["state"] = "recognized-schema"
    result["generated_at"] = normalized_timestamp(report.get("generated_at"))
    freshness = report.get("freshness")
    if isinstance(freshness, dict):
        result["expires_at"] = normalized_timestamp(freshness.get("expires_at"))
    commit = report.get("commit")
    if isinstance(commit, str) and REVISION.fullmatch(commit):
        result["source_revision"] = commit
        result["matches_consumer_revision"] = commit == revision
    execution = report.get("execution")
    if isinstance(execution, dict):
        result["execution"] = _enum(
            execution.get("state"), {"success", "failure", "cancelled", "unknown"}
        )
    return result


def collect_input_evidence(root: Path, environment: dict[str, str]) -> dict[str, Any]:
    supplied_repository = environment.get("GITHUB_REPOSITORY", REPOSITORY)
    if not isinstance(supplied_repository, str) or supplied_repository.lower() != REPOSITORY:
        raise PublicationError("Only Empathy publication evidence is supported.")
    revision = _revision(_git(root, "HEAD"))
    tree = _revision(_git(root, "HEAD^{tree}"))
    profile = _read(root / "mindgarden/profiles/quartz/profile.yaml")
    matches = re.findall(rb"(?m)^quartz_commit: ([0-9a-f]{40})\s*$", profile)
    if len(matches) != 1:
        raise PublicationError("The Quartz revision must be pinned exactly once.")
    return {
        "schema": "empathy.repository-intelligence-publication-inputs/v1",
        "consumer": {"repository": REPOSITORY, "revision": revision, "tree": tree},
        "quartz": {
            "revision": matches[0].decode("ascii"),
            "profile_sha256": sha256(profile),
            "configuration_sha256": sha256(
                _read(root / "mindgarden/profiles/quartz/quartz.config.yaml")
            ),
        },
        "reports": [
            report_evidence(root / ".reports" / name / "summary.json", name, revision)
            for name in ("osv", "megalinter", "scorecard")
        ],
        "workflow": workflow_metadata(environment),
    }


def site_inventory(root: Path) -> list[dict[str, Any]]:
    """Compare full Empathy compositions, using the pinned Relay inventory ordering."""
    if root.is_symlink() or not root.is_dir():
        raise PublicationError("The composed site must be a regular directory.")
    records = []
    total = 0
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            raise PublicationError("Site files reject symbolic links.")
        if path.is_dir():
            continue
        data = _read(path, MAX_FILE_BYTES)
        total += len(data)
        if total > MAX_SITE_BYTES or len(records) >= MAX_SITE_FILES:
            raise PublicationError("Site evidence exceeds its bound.")
        records.append(
            {"path": path.relative_to(root).as_posix(), "bytes": len(data), "sha256": sha256(data)}
        )
    if not records:
        raise PublicationError("The composed site is empty.")
    return records


def inventory_digest(records: list[dict[str, Any]]) -> str:
    return sha256(
        (
            json.dumps(records, ensure_ascii=True, sort_keys=True, separators=(",", ":")) + "\n"
        ).encode()
    )


def compare_sites(left: Path, right: Path) -> dict[str, Any]:
    first, second = site_inventory(left), site_inventory(right)
    if first != second:
        raise PublicationError("Duplicate compositions differ.")
    manifest_bytes = _read(left / "intelligence/build-manifest.json")
    manifest = parse_json(manifest_bytes)
    if manifest.get("schema") != MANIFEST_SCHEMA:
        raise PublicationError("A current build manifest is required.")
    return {
        "schema": "empathy.repository-intelligence-repeatability/v1",
        "identical": True,
        "scope": "two Relay builds on the same Quartz composition and checkout",
        "file_count": len(first),
        "site_digest": inventory_digest(first),
        "manifest_sha256": sha256(manifest_bytes),
    }


class NoRedirects(HTTPRedirectHandler):
    """Probe only fixed Empathy URLs; never follow a server-controlled redirect."""

    # Preserve urllib's override signature; ignoring every argument blocks all redirects.
    def redirect_request(  # noqa: PLR0913, PLR0917
        self,
        req: Any,  # noqa: ARG002
        fp: Any,  # noqa: ARG002
        code: int,  # noqa: ARG002
        msg: str,  # noqa: ARG002
        headers: Any,  # noqa: ARG002
        newurl: str,  # noqa: ARG002
    ) -> None:
        return None


def fetch_public(path: str) -> bytes:
    allowed = set(GARDEN_ROUTES + INTELLIGENCE_ROUTES) | {
        "intelligence/build-manifest.json",
        "intelligence/provenance.json",
    }
    if path not in allowed:
        raise PublicationError("The public route is outside Empathy's fixed probe set.")
    # The fixed HTTPS origin and allowlisted relative routes exclude other URL schemes.
    request = Request(  # noqa: S310
        SITE_URL + path,
        headers={"User-Agent": "Empathy-publication-verifier/1", "Cache-Control": "no-cache"},
    )
    with build_opener(NoRedirects()).open(request, timeout=20) as response:
        if response.status != HTTPStatus.OK or response.geturl() != SITE_URL + path:
            raise PublicationError("The public route did not return an exact successful response.")
        data = response.read(MAX_FILE_BYTES + 1)
        if len(data) > MAX_FILE_BYTES:
            raise PublicationError("The public response exceeds its bound.")
        return data


def _probe_live_routes(site: Path, identity_path: str, expected: bytes) -> list[dict[str, Any]]:
    """Check one complete publication attempt against retained public bytes."""
    actual = fetch_public(identity_path)
    parse_json(actual)
    if actual != expected:
        raise PublicationError("The live deployment differs from the retained build.")
    route_evidence = []
    for route in GARDEN_ROUTES + INTELLIGENCE_ROUTES:
        data = fetch_public(route)
        entrypoint = route + "index.html" if not route or route.endswith("/") else route
        if data != _read(site / entrypoint, MAX_FILE_BYTES):
            raise PublicationError("A live route differs from the retained composition.")
        route_evidence.append(
            {"url": SITE_URL + route, "status": HTTPStatus.OK, "sha256": sha256(data)}
        )
    # Detect a deployment change while the route requests were in flight.
    if fetch_public(identity_path) != expected:
        raise PublicationError("The live deployment changed during verification.")
    return route_evidence


# Keep the explicit CLI identity and bounded retry options together at this boundary.
def verify_live(  # noqa: PLR0913, PLR0917
    site: Path, revision: str, relay_revision: str, mode: str, attempts: int = 12, delay: int = 10
) -> dict[str, Any]:
    _revision(revision)
    _revision(relay_revision)
    if (
        mode not in {"current", "rollback"}
        or not 1 <= attempts <= MAX_LIVE_ATTEMPTS
        or not 0 <= delay <= MAX_RETRY_DELAY_SECONDS
    ):
        raise PublicationError("Live verification options are outside the bounded contract.")
    identity_path = (
        "intelligence/build-manifest.json" if mode == "current" else "intelligence/provenance.json"
    )
    expected = _read(site / identity_path)
    identity = parse_json(expected)
    if mode == "current":
        if (
            identity.get("schema") != MANIFEST_SCHEMA
            or identity.get("consumer") != {"repository": REPOSITORY, "revision": revision}
            or identity.get("generator", {}).get("revision") != relay_revision
        ):
            raise PublicationError("Expected manifest identity does not match the deployment.")
    else:
        consumer = identity.get("consumer", {})
        generator = identity.get("generator", {})
        if (
            consumer.get("repository") != REPOSITORY
            or consumer.get("source_commit") != revision
            or generator.get("source_commit") != relay_revision
        ):
            raise PublicationError("Expected rollback provenance does not match the deployment.")
    for attempt in range(1, attempts + 1):
        try:
            route_evidence = _probe_live_routes(site, identity_path, expected)
            return {
                "schema": "empathy.repository-intelligence-live-verification/v1",
                "mode": mode,
                "consumer_revision": revision,
                "relay_revision": relay_revision,
                "verified_at": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
                "attempt": attempt,
                "identity": {"url": SITE_URL + identity_path, "sha256": sha256(expected)},
                "routes": route_evidence,
            }
        except (PublicationError, OSError, HTTPError, URLError):
            if attempt == attempts:
                raise PublicationError("Bounded live deployment verification failed.") from None
            time.sleep(delay)
    raise PublicationError("Live deployment verification did not complete.")


def failure_report(stage: str, environment: dict[str, str]) -> dict[str, Any]:
    if stage not in FAILURES:
        raise PublicationError("Unknown publication failure stage.")
    code, remediation = FAILURES[stage]
    return {
        "schema": "empathy.repository-intelligence-publication-failure/v1",
        "repository": REPOSITORY,
        "stage": stage,
        "code": code,
        "remediation": remediation,
        "run_id": _positive(environment.get("GITHUB_RUN_ID")),
        "run_attempt": _positive(environment.get("GITHUB_RUN_ATTEMPT")),
        "retention_days": 30,
    }


class SafeParser(argparse.ArgumentParser):
    # argparse requires this signature; never echo its potentially private message.
    def error(self, message: str) -> None:  # noqa: ARG002
        raise PublicationError("Publication command arguments are invalid.")


def main(argv: list[str] | None = None) -> int:
    try:
        parser = SafeParser(description=__doc__)
        commands = parser.add_subparsers(dest="command", required=True)
        baseline = commands.add_parser("canonicalize-baseline")
        baseline.add_argument("--baseline", type=Path, required=True)
        inputs = commands.add_parser("collect-input-evidence")
        inputs.add_argument("--repository-root", type=Path, default=Path())
        inputs.add_argument("--output", type=Path, required=True)
        compare = commands.add_parser("compare-sites")
        compare.add_argument("--left", type=Path, required=True)
        compare.add_argument("--right", type=Path, required=True)
        compare.add_argument("--output", type=Path, required=True)
        live = commands.add_parser("verify-live")
        live.add_argument("--site-root", type=Path, required=True)
        live.add_argument("--consumer-revision", required=True)
        live.add_argument("--relay-revision", required=True)
        live.add_argument("--mode", choices=("current", "rollback"), default="current")
        live.add_argument("--attempts", type=int, default=12)
        live.add_argument("--delay", type=int, default=10)
        live.add_argument("--output", type=Path, required=True)
        failure = commands.add_parser("failure-report")
        failure.add_argument("--stage", choices=tuple(FAILURES), required=True)
        failure.add_argument("--output", type=Path, required=True)
        args = parser.parse_args(argv)
        if args.command == "canonicalize-baseline":
            canonicalize_baseline(args.baseline)
        elif args.command == "collect-input-evidence":
            write_json(
                args.output,
                collect_input_evidence(args.repository_root, dict(os.environ)),
                sites=(args.repository_root / ".cache/mindgarden/site",),
            )
        elif args.command == "compare-sites":
            write_json(
                args.output, compare_sites(args.left, args.right), sites=(args.left, args.right)
            )
        elif args.command == "verify-live":
            write_json(
                args.output,
                verify_live(
                    args.site_root,
                    args.consumer_revision,
                    args.relay_revision,
                    args.mode,
                    args.attempts,
                    args.delay,
                ),
                sites=(args.site_root,),
            )
        else:
            write_json(
                args.output,
                failure_report(args.stage, dict(os.environ)),
                sites=(Path(".cache/mindgarden/site"),),
            )
    except (PublicationError, OSError, subprocess.SubprocessError, TypeError, AttributeError):
        # Intentional fixed public-safe command-line diagnostic.
        print(  # noqa: T201
            "Empathy publication check failed; review the fixed command contract and retained evidence.",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
