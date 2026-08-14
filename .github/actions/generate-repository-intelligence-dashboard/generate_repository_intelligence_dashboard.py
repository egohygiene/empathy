# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Generate a deterministic static dashboard from normalized report summaries."""

from __future__ import annotations

import argparse
from datetime import UTC, datetime, timedelta
import html
import json
from math import isfinite
import os
from pathlib import Path
import re
import subprocess
import tempfile
from typing import Any
from urllib.parse import urlparse

DASHBOARD_SCHEMA = "egohygiene.repository-intelligence-dashboard/v1"
REPORT_SCHEMA = "egohygiene.repository-report-summary/v1"
PRODUCERS = ("osv", "megalinter", "scorecard")
PRODUCER_NAMES = {
    "osv": "Dependency risk",
    "megalinter": "Code quality",
    "scorecard": "Supply-chain posture",
}
EXECUTION_STATES = {"success", "failure", "cancelled", "unknown"}
FINDING_STATES = {"clear", "attention", "blocked", "unknown"}
AVAILABILITY_STATES = {"available", "unavailable", "invalid"}
FRESHNESS_STATES = {"fresh", "stale", "unknown"}
FULL_SHA_PATTERN = re.compile(r"^[0-9a-f]{40}$")


class DashboardInputError(ValueError):
    """Raised when a dashboard or producer input violates its contract."""


def parse_arguments() -> argparse.Namespace:
    """Parse the standalone builder interface used by the composite action."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", required=True)
    parser.add_argument("--reports-root", required=True)
    parser.add_argument("--output-root", required=True)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--default-branch", required=True)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--as-of", required=True)
    parser.add_argument("--stylesheet-source", required=True)
    return parser.parse_args()


def parse_timestamp(value: str, label: str) -> datetime:
    """Parse an aware RFC 3339 timestamp and normalize it to UTC."""

    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as error:
        raise DashboardInputError(f"{label} must be RFC 3339") from error
    if parsed.tzinfo is None:
        raise DashboardInputError(f"{label} must include a timezone")
    return parsed.astimezone(UTC).replace(microsecond=0)


def format_timestamp(value: datetime) -> str:
    """Render an aware datetime as stable UTC RFC 3339."""

    return value.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def safe_integer(value: Any, *, allow_none: bool = False) -> int | None:
    """Return a non-negative integer without accepting booleans."""

    if value is None and allow_none:
        return None
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise DashboardInputError("finding counts must be non-negative integers or null")
    return value


def metric_integer(value: Any) -> int | None:
    """Return a display-safe non-negative metric integer or unknown."""

    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        return None
    return value


def metric_string(value: Any) -> str | None:
    """Return a display-safe metric string or unknown."""

    return value if isinstance(value, str) and value else None


def metric_score(value: Any) -> int | float | None:
    """Return a finite score in the OpenSSF Scorecard range or unknown."""

    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return value if isfinite(value) and 0 <= value <= 10 else None


def scorecard_weakest_checks(value: Any) -> list[dict[str, Any]]:
    """Project a bounded list of display-safe Scorecard check summaries."""

    if not isinstance(value, list):
        return []
    checks = []
    for candidate in value[:5]:
        if not isinstance(candidate, dict):
            continue
        name = metric_string(candidate.get("name"))
        score = metric_score(candidate.get("score"))
        if name is not None and score is not None:
            checks.append({"name": name, "score": score})
    return checks


def safe_url(value: Any) -> str:
    """Keep only public HTTPS or repository-relative links."""

    if not isinstance(value, str) or not value:
        return ""
    if value.startswith("./") or (value.startswith("/") and not value.startswith("//")):
        return value
    parsed = urlparse(value)
    if parsed.scheme == "https" and parsed.netloc:
        return value
    return ""


def unknown_status(state: str, message: str) -> dict[str, str]:
    """Build one compact status object."""

    return {"state": state, "message": message}


def unavailable_projection(producer: str) -> dict[str, Any]:
    """Represent a producer with no committed summary without implying success."""

    return {
        "producer": producer,
        "name": PRODUCER_NAMES[producer],
        "availability": "unavailable",
        "generated_at": None,
        "commit": None,
        "execution": unknown_status("unknown", "No committed summary is available."),
        "findings": {
            "state": "unknown",
            "total": None,
            "blocking": None,
            "advisory": None,
            "by_severity": {},
        },
        "freshness": unknown_status("unknown", "Freshness cannot be determined."),
        "links": {},
        "metrics": {},
    }


def invalid_projection(producer: str, message: str) -> dict[str, Any]:
    """Represent malformed or incompatible producer data as an execution failure."""

    projection = unavailable_projection(producer)
    projection["availability"] = "invalid"
    projection["execution"] = unknown_status("failure", message)
    return projection


def require_object(document: dict[str, Any], key: str) -> dict[str, Any]:
    """Read a required object from a report document."""

    value = document.get(key)
    if not isinstance(value, dict):
        raise DashboardInputError(f"{key} must be an object")
    return value


def producer_metrics(producer: str, payload: dict[str, Any]) -> dict[str, Any]:
    """Select the compact, public metrics rendered by one producer card."""

    if producer == "osv":
        scan = payload.get("scan", {})
        discovery = payload.get("discovery", {})
        severity = scan.get("severity", {}) if isinstance(scan, dict) else {}
        return {
            "vulnerabilities": metric_integer(scan.get("vulnerabilities"))
            if isinstance(scan, dict)
            else None,
            "affected_packages": metric_integer(scan.get("affected_packages"))
            if isinstance(scan, dict)
            else None,
            "ecosystems": metric_integer(discovery.get("ecosystem_count"))
            if isinstance(discovery, dict)
            else None,
            "threshold": metric_string(payload.get("severity_threshold")),
            "severity": {
                str(key): count
                for key, value in sorted(severity.items())
                if (count := metric_integer(value)) is not None
            }
            if isinstance(severity, dict)
            else {},
        }
    if producer == "megalinter":
        tools = payload.get("tools", {})
        diagnostics = payload.get("diagnostics", {})
        return {
            "profile": metric_string(payload.get("profile")),
            "tools": {
                str(key): count
                for key, value in sorted(tools.items())
                if (count := metric_integer(value)) is not None
            }
            if isinstance(tools, dict)
            else {},
            "diagnostics": {
                str(key): count
                for key, value in sorted(diagnostics.items())
                if (count := metric_integer(value)) is not None
            }
            if isinstance(diagnostics, dict)
            else {},
        }
    return {
        "aggregate_score": metric_score(payload.get("aggregate_score")),
        "aggregate_source": metric_string(payload.get("aggregate_source")),
        "api_status": metric_string(payload.get("api_status")),
        "checks_total": metric_integer(payload.get("checks_total")),
        "checks_needing_attention": metric_integer(payload.get("checks_needing_attention")),
        "weakest_checks": scorecard_weakest_checks(payload.get("weakest_checks")),
    }


def validate_report(
    document: dict[str, Any], producer: str, repository: str, as_of: datetime
) -> dict[str, Any]:
    """Validate and project one normalized producer summary."""

    if document.get("schema") != REPORT_SCHEMA or document.get("schema_version") != 1:
        raise DashboardInputError("Summary uses an incompatible schema.")
    if document.get("producer") != producer:
        raise DashboardInputError("Summary producer does not match its report directory.")
    if document.get("repository") != repository:
        raise DashboardInputError("Summary repository does not match this dashboard.")
    commit = document.get("commit")
    if not isinstance(commit, str) or not FULL_SHA_PATTERN.fullmatch(commit):
        raise DashboardInputError("Summary commit must be a full lowercase SHA.")
    generated_at_raw = document.get("generated_at")
    if not isinstance(generated_at_raw, str):
        raise DashboardInputError("generated_at must be an RFC 3339 string.")
    generated_at = parse_timestamp(generated_at_raw, "generated_at")

    execution = require_object(document, "execution")
    execution_state = execution.get("state")
    if execution_state not in EXECUTION_STATES or not isinstance(execution.get("message"), str):
        raise DashboardInputError("execution contains an unsupported state or message.")

    report_findings = require_object(document, "findings")
    finding_state = report_findings.get("state")
    if finding_state not in FINDING_STATES:
        raise DashboardInputError("findings contains an unsupported state.")
    allow_none = finding_state == "unknown"
    total = safe_integer(report_findings.get("total"), allow_none=allow_none)
    blocking = safe_integer(report_findings.get("blocking"), allow_none=allow_none)
    advisory = safe_integer(report_findings.get("advisory"), allow_none=allow_none)
    if total is not None and blocking is not None and advisory is not None:
        if blocking + advisory != total:
            raise DashboardInputError("blocking and advisory counts must sum to total.")
    by_severity = report_findings.get("by_severity")
    if not isinstance(by_severity, dict):
        raise DashboardInputError("findings.by_severity must be an object.")
    normalized_severity = {
        str(key): safe_integer(value) for key, value in sorted(by_severity.items())
    }

    report_freshness = require_object(document, "freshness")
    expires_at_raw = report_freshness.get("expires_at")
    if not isinstance(expires_at_raw, str):
        raise DashboardInputError("freshness.expires_at must be an RFC 3339 string.")
    expires_at = parse_timestamp(expires_at_raw, "freshness.expires_at")
    stale_after_days = report_freshness.get("stale_after_days")
    if (
        isinstance(stale_after_days, bool)
        or not isinstance(stale_after_days, int)
        or stale_after_days < 1
    ):
        raise DashboardInputError("freshness.stale_after_days must be a positive integer.")
    if expires_at <= generated_at:
        raise DashboardInputError("freshness.expires_at must be after generated_at.")
    freshness_state = "stale" if as_of >= expires_at else "fresh"
    freshness_message = (
        f"Expired at {format_timestamp(expires_at)}."
        if freshness_state == "stale"
        else f"Valid through {format_timestamp(expires_at)}."
    )

    provenance = require_object(document, "provenance")
    if not all(isinstance(provenance.get(key), str) for key in ("event", "workflow")):
        raise DashboardInputError("provenance event and workflow must be strings.")
    run_id = provenance.get("run_id")
    run_attempt = provenance.get("run_attempt")
    if run_id is not None and not isinstance(run_id, str):
        raise DashboardInputError("provenance.run_id must be a string or null.")
    if run_attempt is not None and (
        isinstance(run_attempt, bool) or not isinstance(run_attempt, int) or run_attempt < 1
    ):
        raise DashboardInputError("provenance.run_attempt must be a positive integer or null.")

    report_links = require_object(document, "links")
    link_keys = ("detail", "workflow", "security", "source")
    if not all(isinstance(report_links.get(key), str) for key in link_keys):
        raise DashboardInputError(
            "links must declare detail, workflow, security, and source strings."
        )
    links = {
        key: safe_url(report_links.get(key)) for key in link_keys
    }
    payload = require_object(document, producer)
    return {
        "producer": producer,
        "name": PRODUCER_NAMES[producer],
        "availability": "available",
        "generated_at": format_timestamp(generated_at),
        "commit": commit,
        "execution": {"state": execution_state, "message": execution["message"]},
        "findings": {
            "state": finding_state,
            "total": total,
            "blocking": blocking,
            "advisory": advisory,
            "by_severity": normalized_severity,
        },
        "freshness": {"state": freshness_state, "message": freshness_message},
        "links": {key: value for key, value in links.items() if value},
        "metrics": producer_metrics(producer, payload),
    }


def load_report(
    reports_root: Path, producer: str, repository: str, as_of: datetime
) -> dict[str, Any]:
    """Load one producer summary with explicit unavailable and invalid fallbacks."""

    path = reports_root / producer / "summary.json"
    if not path.is_file() or path.stat().st_size == 0:
        return unavailable_projection(producer)
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return invalid_projection(producer, "Summary is malformed JSON.")
    if not isinstance(document, dict):
        return invalid_projection(producer, "Summary must contain a JSON object.")
    try:
        return validate_report(document, producer, repository, as_of)
    except DashboardInputError as error:
        return invalid_projection(producer, str(error))


def run_git(repository_root: Path, *arguments: str) -> str:
    """Run a read-only Git query and return normalized stdout."""

    result = subprocess.run(
        ["git", "-C", str(repository_root), *arguments],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def collect_vitality(
    repository_root: Path,
    repository: str,
    default_branch: str,
    source_commit: str,
    as_of: datetime,
) -> dict[str, Any]:
    """Collect deterministic repository counts without exposing contributor identities."""

    try:
        resolved_commit = run_git(repository_root, "rev-parse", source_commit)
        if not FULL_SHA_PATTERN.fullmatch(resolved_commit):
            raise DashboardInputError("Git did not resolve a full source commit.")
        committed_at = run_git(
            repository_root, "show", "--no-patch", "--format=%cI", resolved_commit
        )
        subject = run_git(repository_root, "show", "--no-patch", "--format=%s", resolved_commit)
        since_30_days = format_timestamp(as_of - timedelta(days=30))
        since_90_days = format_timestamp(as_of - timedelta(days=90))
        until = format_timestamp(as_of)
        commits_30_days = int(
            run_git(
                repository_root,
                "rev-list",
                "--count",
                f"--since={since_30_days}",
                f"--until={until}",
                resolved_commit,
            )
            or "0"
        )
        contributor_emails = run_git(
            repository_root,
            "log",
            f"--since={since_90_days}",
            f"--until={until}",
            "--format=%aE",
            resolved_commit,
        ).splitlines()
        contributors_90_days = len(
            {email.strip().casefold() for email in contributor_emails if email.strip()}
        )
        tracked_paths = [
            line
            for line in run_git(
                repository_root, "ls-tree", "-r", "--name-only", resolved_commit
            ).splitlines()
            if line
        ]
        tracked_files = len(tracked_paths)
        history_complete = (
            run_git(repository_root, "rev-parse", "--is-shallow-repository") == "false"
        )
        workflow_count = sum(
            path.startswith(".github/workflows/")
            and path.rsplit("/", maxsplit=1)[-1].endswith((".yaml", ".yml"))
            for path in tracked_paths
        )
        action_count = sum(
            path.startswith(".github/actions/")
            and path.endswith("/action.yml")
            and path.count("/") == 3
            for path in tracked_paths
        )
        test_count = sum(
            path.rsplit("/", maxsplit=1)[-1].startswith("test_")
            and path.endswith(".py")
            and not path.startswith(".cache/")
            for path in tracked_paths
        )
    except (DashboardInputError, OSError, subprocess.CalledProcessError, ValueError):
        return {
            "execution": {
                "state": "failure",
                "message": "Repository vitality could not be collected from this checkout.",
            },
            "repository": repository,
            "default_branch": default_branch,
            "source_commit": source_commit,
            "metrics": {},
        }
    return {
        "execution": {
            "state": "success",
            "message": "Repository vitality was collected from the local checkout.",
        },
        "repository": repository,
        "default_branch": default_branch,
        "source_commit": resolved_commit,
        "latest_commit": {
            "short_sha": resolved_commit[:12],
            "committed_at": format_timestamp(parse_timestamp(committed_at, "commit timestamp")),
            "subject": subject,
        },
        "metrics": {
            "commits_30_days": commits_30_days,
            "contributors_90_days": contributors_90_days,
            "tracked_files": tracked_files,
            "workflows": workflow_count,
            "composite_actions": action_count,
            "python_tests": test_count,
            "history_complete": history_complete,
        },
    }


def count_states(producers: dict[str, dict[str, Any]]) -> dict[str, dict[str, int]]:
    """Aggregate independent state dimensions without inventing a global score."""

    counts = {
        "availability": {state: 0 for state in sorted(AVAILABILITY_STATES)},
        "execution": {state: 0 for state in sorted(EXECUTION_STATES)},
        "findings": {state: 0 for state in sorted(FINDING_STATES)},
        "freshness": {state: 0 for state in sorted(FRESHNESS_STATES)},
    }
    for projection in producers.values():
        counts["availability"][projection["availability"]] += 1
        counts["execution"][projection["execution"]["state"]] += 1
        counts["findings"][projection["findings"]["state"]] += 1
        counts["freshness"][projection["freshness"]["state"]] += 1
    return counts


def build_dashboard(
    *,
    repository_root: Path,
    reports_root: Path,
    repository: str,
    default_branch: str,
    source_commit: str,
    as_of: datetime,
) -> dict[str, Any]:
    """Build the complete public dashboard model."""

    if not FULL_SHA_PATTERN.fullmatch(source_commit):
        raise DashboardInputError("source-commit must be a full lowercase SHA")
    if not repository or not default_branch:
        raise DashboardInputError("repository and default-branch must be non-empty")
    producers = {
        producer: load_report(reports_root, producer, repository, as_of)
        for producer in PRODUCERS
    }
    vitality = collect_vitality(
        repository_root, repository, default_branch, source_commit, as_of
    )
    return {
        "schema": DASHBOARD_SCHEMA,
        "schema_version": 1,
        "generated_at": format_timestamp(as_of),
        "repository": {
            "name": repository,
            "default_branch": default_branch,
            "source_commit": source_commit,
        },
        "states": count_states(producers),
        "producers": producers,
        "vitality": vitality,
    }


def escaped(value: Any) -> str:
    """Escape a scalar for safe HTML text or attribute output."""

    return html.escape(str(value), quote=True)


def display_count(value: Any) -> str:
    """Render an optional count without turning missing data into zero."""

    return "—" if value is None else str(value)


def badge(label: str, state: str) -> str:
    """Render a textual state badge whose meaning is not color-only."""

    return (
        f'<span class="badge state-{escaped(state)}">'
        f"{escaped(label)}: {escaped(state)}</span>"
    )


def metric_rows(producer: str, projection: dict[str, Any]) -> list[tuple[str, str]]:
    """Return card-specific metric labels and values."""

    metrics = projection["metrics"]
    if producer == "osv":
        severity = metrics.get("severity", {})
        severe: int | None = 0
        if isinstance(severity, dict):
            critical = metric_integer(severity.get("critical", 0))
            high = metric_integer(severity.get("high", 0))
            severe = critical + high if critical is not None and high is not None else None
        return [
            ("Affected packages", display_count(metrics.get("affected_packages"))),
            ("High or critical", str(severe)),
            ("Ecosystems", display_count(metrics.get("ecosystems"))),
            ("Policy threshold", display_count(metrics.get("threshold"))),
        ]
    if producer == "megalinter":
        tools = metrics.get("tools", {})
        diagnostics = metrics.get("diagnostics", {})
        errors = metric_integer(diagnostics.get("errors"))
        warnings = metric_integer(diagnostics.get("warnings"))
        diagnostic_total = (
            errors + warnings if errors is not None and warnings is not None else None
        )
        return [
            ("Active tools", display_count(tools.get("active"))),
            ("Passing tools", display_count(tools.get("passed"))),
            ("Blocking tools", display_count(tools.get("blocking"))),
            ("Diagnostics", display_count(diagnostic_total)),
        ]
    return [
        ("Aggregate source", display_count(metrics.get("aggregate_source"))),
        ("Checks evaluated", display_count(metrics.get("checks_total"))),
        ("Checks needing attention", display_count(metrics.get("checks_needing_attention"))),
        ("API status", display_count(metrics.get("api_status"))),
    ]


def headline_metric(producer: str, projection: dict[str, Any]) -> str:
    """Return the primary card metric with honest missing-data language."""

    if projection["availability"] != "available":
        return "Data unavailable"
    metrics = projection["metrics"]
    if producer == "osv":
        count = metrics.get("vulnerabilities")
        return f"{display_count(count)} vulnerabilities"
    if producer == "megalinter":
        tools = metrics.get("tools", {})
        passed = display_count(tools.get("passed"))
        active = display_count(tools.get("active"))
        return f"{passed} / {active} tools passing"
    score = metrics.get("aggregate_score")
    return "Aggregate pending" if score is None else f"{score:g} / 10"


def render_links(links: dict[str, str]) -> str:
    """Render allowlisted public links for one producer."""

    labels = {
        "detail": "View details",
        "workflow": "Workflow run",
        "security": "Security findings",
        "source": "Source commit",
    }
    rendered = [
        f'<a href="{escaped(url)}">{labels[key]}</a>'
        for key, url in links.items()
        if key in labels and url
    ]
    return "".join(f"<span>{link}</span>" for link in rendered) or (
        "<span>No public links available.</span>"
    )


def render_producer_card(producer: str, projection: dict[str, Any]) -> str:
    """Render one accessible producer card."""

    rows = "".join(
        f"<div><dt>{escaped(label)}</dt><dd>{escaped(value)}</dd></div>"
        for label, value in metric_rows(producer, projection)
    )
    return f"""<article class="producer-card" aria-labelledby="{producer}-title">
  <p class="card-kicker">{escaped(producer)}</p>
  <h3 id="{producer}-title">{escaped(projection['name'])}</h3>
  <div class="badge-row">
    {badge("Availability", projection['availability'])}
    {badge("Execution", projection['execution']['state'])}
    {badge("Findings", projection['findings']['state'])}
    {badge("Freshness", projection['freshness']['state'])}
  </div>
  <p class="headline-metric">{escaped(headline_metric(producer, projection))}</p>
  <p class="card-message">{escaped(projection['execution']['message'])}</p>
  <dl class="metric-list">{rows}</dl>
  <div class="link-row">{render_links(projection['links'])}</div>
</article>"""


def render_html(dashboard: dict[str, Any]) -> str:
    """Render the complete framework-free dashboard document."""

    repository = dashboard["repository"]
    states = dashboard["states"]
    producer_cards = "\n".join(
        render_producer_card(producer, dashboard["producers"][producer])
        for producer in PRODUCERS
    )
    vitality = dashboard["vitality"]
    vitality_metrics = vitality.get("metrics", {})
    vitality_items = [
        ("Commits", vitality_metrics.get("commits_30_days"), "in the last 30 days"),
        ("Contributors", vitality_metrics.get("contributors_90_days"), "in the last 90 days"),
        ("Tracked files", vitality_metrics.get("tracked_files"), "at the represented commit"),
        ("Workflows", vitality_metrics.get("workflows"), "GitHub Actions workflows"),
        ("Actions", vitality_metrics.get("composite_actions"), "local composite actions"),
        ("Python tests", vitality_metrics.get("python_tests"), "test modules discovered"),
        (
            "History",
            "complete" if vitality_metrics.get("history_complete") else "shallow",
            "checkout depth",
        ),
        ("Default branch", repository["default_branch"], "repository target"),
    ]
    vitality_cards = "".join(
        f"""<article class="vitality-card">
  <p class="card-kicker">{escaped(label)}</p>
  <p class="vitality-value">{escaped(display_count(value))}</p>
  <p class="vitality-label">{escaped(description)}</p>
</article>"""
        for label, value, description in vitality_items
    )
    latest_commit = vitality.get("latest_commit", {})
    commit_subject = latest_commit.get("subject", "Commit details unavailable")
    return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="color-scheme" content="dark" />
    <meta name="description" content="Repository intelligence for {escaped(repository['name'])}." />
    <title>Repository intelligence · {escaped(repository['name'])}</title>
    <link rel="stylesheet" href="./styles.css" />
  </head>
  <body>
    <a class="skip-link" href="#main-content">Skip to dashboard</a>
    <header class="hero">
      <div class="shell">
        <p class="eyebrow">{escaped(repository['name'])}</p>
        <h1 class="gradient-text">Repository intelligence</h1>
        <p class="lede">A transparent view of dependency risk, code quality, supply-chain posture, and repository vitality. Scanner execution and findings remain separate.</p>
        <div class="meta-row">
          <span class="meta-chip">Branch: {escaped(repository['default_branch'])}</span>
          <span class="meta-chip">Commit: {escaped(repository['source_commit'][:12])}</span>
          <span class="meta-chip">As of: {escaped(dashboard['generated_at'])}</span>
        </div>
      </div>
    </header>
    <main id="main-content" class="shell">
      <section class="section" aria-labelledby="state-heading">
        <div class="section-heading">
          <div>
            <p class="eyebrow">Independent dimensions</p>
            <h2 id="state-heading">Current state</h2>
          </div>
          <p>No synthetic health score. These counts preserve what ran, what it found, and whether its evidence is current.</p>
        </div>
        <div class="status-grid">
          <article class="panel">
            <p class="panel-label">Execution</p>
            <p class="panel-value">{states['execution']['success']} successful · {states['execution']['failure']} failed · {states['execution']['cancelled']} cancelled · {states['execution']['unknown']} unknown</p>
          </article>
          <article class="panel">
            <p class="panel-label">Findings</p>
            <p class="panel-value">{states['findings']['clear']} clear · {states['findings']['attention']} attention · {states['findings']['blocked']} blocked · {states['findings']['unknown']} unknown</p>
          </article>
          <article class="panel">
            <p class="panel-label">Freshness</p>
            <p class="panel-value">{states['freshness']['fresh']} fresh · {states['freshness']['stale']} stale · {states['freshness']['unknown']} unknown</p>
          </article>
        </div>
      </section>
      <section class="section" aria-labelledby="producer-heading">
        <div class="section-heading">
          <div>
            <p class="eyebrow">Authoritative producers</p>
            <h2 id="producer-heading">Security and quality signals</h2>
          </div>
          <p>Each card links back to its canonical source rather than duplicating raw reports.</p>
        </div>
        <div class="producer-grid">{producer_cards}</div>
      </section>
      <section class="section" aria-labelledby="vitality-heading">
        <div class="section-heading">
          <div>
            <p class="eyebrow">Local collector</p>
            <h2 id="vitality-heading">Repository vitality</h2>
          </div>
          <p>{escaped(vitality['execution']['message'])}</p>
        </div>
        <div class="vitality-grid">{vitality_cards}</div>
      </section>
      <aside class="panel provenance" aria-label="Dashboard provenance">
        <div>
          <p class="card-kicker">Provenance</p>
          <p><code>{escaped(repository['source_commit'])}</code> · {escaped(commit_subject)}</p>
        </div>
        <p><a href="./summary.json">View public JSON</a></p>
      </aside>
    </main>
  </body>
</html>
"""


def atomic_write_text(path: Path, content: str) -> None:
    """Write one dashboard asset atomically."""

    path.parent.mkdir(parents=True, exist_ok=True)
    file_descriptor, temporary_name = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.")
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(file_descriptor, "w", encoding="utf-8", newline="") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        temporary_path.replace(path)
    except BaseException:
        temporary_path.unlink(missing_ok=True)
        raise


def validate_paths(repository_root: Path, *paths: Path) -> None:
    """Keep all reads and writes inside the checked-out repository."""

    for path in paths:
        try:
            path.relative_to(repository_root)
        except ValueError as error:
            raise DashboardInputError(f"Path must remain inside the repository: {path}") from error


def write_dashboard_bundle(
    output_root: Path, dashboard: dict[str, Any], stylesheet_source: Path
) -> None:
    """Write the public JSON, HTML, and stylesheet as one static bundle."""

    atomic_write_text(
        output_root / "summary.json",
        json.dumps(dashboard, allow_nan=False, indent=2, sort_keys=True) + "\n",
    )
    atomic_write_text(output_root / "index.html", render_html(dashboard))
    atomic_write_text(
        output_root / "styles.css", stylesheet_source.read_text(encoding="utf-8")
    )


def main() -> int:
    """Build and write the deterministic dashboard bundle."""

    args = parse_arguments()
    repository_root = Path(args.repository_root).resolve()
    reports_root = Path(args.reports_root).resolve()
    output_root = Path(args.output_root).resolve()
    stylesheet_source = Path(args.stylesheet_source).resolve()
    if not repository_root.is_dir():
        raise SystemExit(f"Repository root is not a directory: {repository_root}")
    validate_paths(repository_root, reports_root, output_root)
    if not stylesheet_source.is_file():
        raise SystemExit(f"Stylesheet source is unavailable: {stylesheet_source}")
    as_of = parse_timestamp(args.as_of, "as-of")
    dashboard = build_dashboard(
        repository_root=repository_root,
        reports_root=reports_root,
        repository=args.repository,
        default_branch=args.default_branch,
        source_commit=args.source_commit,
        as_of=as_of,
    )
    write_dashboard_bundle(output_root, dashboard, stylesheet_source)
    print(
        f"Generated repository intelligence dashboard at {output_root} "
        f"for {args.repository}@{args.source_commit[:12]}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
