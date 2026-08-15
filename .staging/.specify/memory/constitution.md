# Ego Hygiene Constitution

## Core Principles

### I. Local-First and Privacy-Preserving

Private sources, conversations, browser state, and Mindgarden notes remain local
by default. External transmission, publication, and sharing require an explicit
user decision. Secrets are redacted before derived artifacts are persisted.

### II. Provenance Before Fluency

Knowledge and synapse outputs must remain traceable to stable source segments.
The system preserves caveats, contradictions, uncertainty, sensitivity, and
coverage instead of replacing them with confident prose.

### III. Deterministic Contracts

Boundaries between capture, normalization, extraction, synapse derivation,
validation, and gardenization use versioned schemas and stable identifiers.
Model output is untrusted until parsed and validated against its contract.

### IV. Reversible Human-Controlled Change

Agents preserve user changes and request confirmation for destructive actions,
publishing, commits, pushes, dependency installation, or transmission of private
data. Generated files support idempotent reruns and version history.

### V. Test the Failure Modes

Tests cover malformed sources, partial extraction, hidden conversation nodes,
attachments, contradictions, redaction, interrupted runs, and duplicate reruns.
Verification reports both success and known omissions.

### VI. Extensible by Strategy, Not Conditionals

Source-specific capture and normalization behavior implements stable interfaces.
Adding a new source type must not require rewriting the orchestration pipeline or
weakening existing contracts.

## Operating Boundaries

- `.github/specs/` contains authoritative specifications.
- `mindgarden/` contains durable navigable knowledge.
- `.cache/` contains ignored runtime and review artifacts.
- Authentication profiles remain outside the repository.
- Interactive agents assist development and review; deterministic application
  code owns repeatable extraction and gardenization.

## Governance

Changes that weaken privacy, provenance, schema validation, or reversibility
require an explicit specification update and migration plan. When guidance
conflicts, the narrower applicable specification wins unless it violates this
constitution.

**Version**: 1.0.0 | **Ratified**: 2026-07-19 | **Last Amended**: 2026-07-19
