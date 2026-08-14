---
schema: mindgarden.note/v0
id: repository-intelligence-dashboard
title: Repository Intelligence Dashboard
kind: project
status: reviewed
reviewed: true
confidence: high
visibility: public
owners:
  - egohygiene
created: 2026-08-14
updated: 2026-08-14
sources:
  - ../../.github/actions/generate-repository-intelligence-dashboard/README.md
  - ../../.github/actions/generate-repository-intelligence-dashboard/action.yml
  - ../../.github/actions/generate-repository-intelligence-dashboard/repository-intelligence-dashboard.schema.json
  - ../../.github/actions/normalize-repository-report/README.md
  - ../../.github/actions/normalize-repository-report/action.yml
  - ../../.github/actions/normalize-repository-report/repository-report-summary.schema.json
  - ../../.github/workflows/ossf-scorecard.yml
  - ../../.github/workflows/osv-scan.yml
  - ../../.github/workflows/megalinter.yml
  - ../../.github/workflows/mindgarden-pages.yml
  - ../../.staging/github/README.md
related:
  - empathy-garden-dashboard
  - empathy-garden-projects
supersedes: []
tags:
  - dashboard
  - github-actions
  - repository-intelligence
  - security
---

# Repository Intelligence Dashboard

## Decision

Publish one static, repository-scoped dashboard beneath the existing GitHub
Pages site at `/empathy/intelligence/`. It will summarize the authoritative
scanner outputs rather than replace their native reports, SARIF uploads, or
GitHub Security-tab integration.

The dashboard is a public, compact projection. Raw logs, SARIF payloads,
workflow artifacts, and any private workflow context remain outside the site.

## User-facing model

The landing page should answer four questions at a glance:

| Area                           | Canonical source              | Dashboard value                                                                                     |
| ------------------------------ | ----------------------------- | --------------------------------------------------------------------------------------------------- |
| Dependency risk                | OSV summary                   | Severity counts, scanned ecosystems, threshold, freshness, and report link.                         |
| Code and configuration quality | MegaLinter summary            | Passing/failing tool counts, selected profile, freshness, and report link.                          |
| Supply-chain posture           | OpenSSF Scorecard             | Overall score, check-level status, freshness, and source link.                                      |
| Repository vitality            | Deterministic local collector | Default branch, latest commit, contribution/activity metrics, automation posture, and report links. |

Every card must present **execution state** separately from **finding state**.
For example, a successful OSV run can still report vulnerabilities, while a
failed MegaLinter run may still publish a valuable curated snapshot.

## Data contract

Each authoritative workflow publishes a small, versioned JSON summary under
`.reports/<producer>/summary.json`. The dashboard builder reads only those
committed summaries plus repository metadata available in the checkout.

Required common fields:

```json
{
  "schema": "egohygiene.repository-report-summary/v1",
  "schema_version": 1,
  "producer": "osv",
  "repository": "egohygiene/empathy",
  "generated_at": "2026-08-14T12:41:52Z",
  "commit": "<40-character-sha>",
  "freshness": {
    "expires_at": "2026-08-22T12:41:52Z",
    "stale_after_days": 8
  },
  "execution": {
    "state": "success",
    "message": "Canonical OSV JSON and SARIF outputs were validated."
  },
  "findings": {
    "state": "attention",
    "total": 2,
    "blocking": 0,
    "advisory": 2,
    "by_severity": { "medium": 2 }
  },
  "provenance": {
    "event": "push",
    "workflow": "OSV Vulnerability Scan",
    "run_id": "123456789",
    "run_attempt": 1
  },
  "links": {
    "detail": "https://github.com/egohygiene/empathy/tree/<sha>/.reports/osv",
    "workflow": "https://github.com/egohygiene/empathy/actions/runs/123456789",
    "security": "https://github.com/egohygiene/empathy/security/code-scanning",
    "source": "https://github.com/egohygiene/empathy/commit/<sha>"
  },
  "osv": {}
}
```

Producer-specific fields remain namespaced below their own object. Missing,
stale, or schema-incompatible reports render as `unknown` or `stale`; they must
never become a misleading green result.

## Delivery architecture

```text
canonical scanners and collectors
  -> stable .reports/<producer>/summary.json snapshots
  -> composite dashboard builder
  -> .cache/mindgarden/site/intelligence/
  -> existing GitHub Pages deployment
```

The dashboard builder is a composite action when it only validates inputs and
generates deterministic static assets. A reusable workflow belongs in Relay
once it needs repository checkout policy, Pages permissions, or cross-repo
orchestration. Repositories should keep thin caller workflows and local theme
configuration.

## Delivery slices

1. Promote the universal dependency-review gate and record the staging
   migration decisions. **Complete.**
2. Define a shared, versioned producer contract; normalize OSV and MegaLinter;
   and publish a compact OpenSSF Scorecard summary through the existing trusted
   report-publication action. **Complete.**
3. Add a dashboard builder action with fixtures for OSV, MegaLinter, Scorecard,
   repository vitality, and unavailable/stale inputs. Emit `summary.json`,
   `index.html`, and a small accessible stylesheet with no client-side
   framework. **Complete.**
4. Extend the Mindgarden Pages build job to place the generated dashboard at
   `intelligence/` beside the Quartz site and add a garden link to it. **Next.**
5. Extract the stable builder and caller contract to Relay, then instantiate
   it in each repository through its declared capability profile.

## Grafana and Prometheus

GitHub Pages is the right first surface: zero persistent service, public by
default, versioned in Git, and readable when no observability stack is running.

Prometheus and Grafana fit one level up in `observatory`, not inside each
repository. A scheduled collector can read each repository's compact public
summary and expose metrics such as `repository_scan_findings_total`,
`repository_report_age_seconds`, and `repository_workflow_state`, labelled by
repository, producer, severity, and default branch. Grafana then provides
cross-repository trends, alerting, and operational views. Realm can later host
that optional stack for the organization without making it a prerequisite for
repository publishing.

## Guardrails

- Do not scrape or publish raw workflow logs, tokens, artifact download URLs,
  or unreviewed issue data.
- Do not duplicate scanners merely to feed the dashboard.
- Keep raw SARIF in GitHub Code Scanning and stable summaries in `.reports/`.
- Treat report freshness and schema validation as first-class states.
- Keep PRs read-only; only trusted default-branch, scheduled, or manual runs
  may publish stable report snapshots.
- Enable the dependency-review profile only after GitHub Dependency Graph is
  enabled, by setting the repository variable `DEPENDENCY_REVIEW_ENABLED=true`.
