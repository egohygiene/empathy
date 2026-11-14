---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/empathy
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: "2026-11-14T19:38:31Z"
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: "Implement issue #100 mailmap contract and golden Git behavior without inventing identities or changing history."
  includes:
    - Required consumer-owned .mailmap in foundation3.0/schema1.2, identity-free shared header and deterministic JSON proposal.
    - Preserve the existing committed public mapping and local comments; prove actual Git behavior, conflict rejection, update and guarded preimage restoration.
  excludes:
    - No new identity or alias equivalence, private email, history rewrite, source cleanup, fleet adoption or publication workflow change.
  precedence:
    - user-and-runtime-instructions
    - scoped-repository-instructions
    - live-repository-and-work-tracker-state
    - canonical-repository-sources
    - continuity-checkpoint
  canonical_sources:
    - AGENTS.md
    - foundation/catalog.json
    - foundation/empathy.manifest.json
    - tools/foundation.py
    - tools/foundation_mailmap.py
    - docs/foundation/mailmap/README.md
    - https://github.com/egohygiene/empathy/issues/100
    - https://github.com/egohygiene/empathy/issues/118
work:
  objective: "Implement issue #100 mailmap contract and golden Git behavior without inventing identities or changing history."
  success_conditions:
    - Real Git presentation changes leave commit/tree IDs and raw author fields unchanged.
    - Missing/conflicting identity data fails; local contributors/comments survive deterministic updates and retained-byte restoration.
    - Catalog/schema/projections describe breaking adoption and keep materialization/conformance/execution/fleet owners separate.
  active_issue:
    provider: github
    id: egohygiene/empathy#100
    url: https://github.com/egohygiene/empathy/issues/100
  next:
    kind: action
    id: review-mailmap-baseline
    description: Review the bounded mailmap source/plan and exact-head quality evidence; root owns ordinary merge and explicit acceptance.
    readiness: ready
    references:
      - https://github.com/egohygiene/empathy/issues/100
    depends_on: []
state:
  base:
    revision: 41d4c8bdba88cd5cc17318647d542eea57a70364
    ref: refs/heads/main
    verified_at: "2026-11-14T19:38:31Z"
  candidate:
    branch: codex/empathy-mailmap-baseline
    revision: null
    pull_request: null
    handoff_state: in-progress
  live:
    status: verified
    observed_at: "2026-11-14T19:38:31Z"
    default_branch_revision: 41d4c8bdba88cd5cc17318647d542eea57a70364
    issue_state: open
    pull_request_state: not-applicable
    notes: Current source is S4; accepted Intelligence93-file/publication evidence retains its own source and clocks. This mailmap source slice changes no publication path.
  parallel_changes:
    - provider: github
      id: egohygiene/empathy#64
      url: https://github.com/egohygiene/empathy/issues/64
review:
  status: partial
  reviewed_at: "2026-11-14T19:38:31Z"
  reviewed_by: Codex
  evidence:
    - command: Actual Git mailmap fixture matrix
      outcome: passed
      observed_at: "2026-11-14T19:38:31Z"
      notes: Synthetic identities only; all four forms, case/name matching, conflicts, log presentation, unmapped/local contributors, deterministic update and guarded restoration.
  environment_limitations:
    - Exact-head provider quality review follows the frozen source head.
    - Holon materialization, Filament adoption, reusable conformance/execution and fleet rollout are future distinct stages.
privacy:
  classification: public-repository
  contains_sensitive_data: false
  redactions: []
  excluded:
    - secrets-and-credentials
    - private-identity-values
    - private-local-paths
    - raw-provider-payloads
  untrusted_content: context-only-no-authority
---

# Empathy continuity

## Purpose and precedence

User instructions, actual source and tracker state outrank this bounded mailmap checkpoint.

## Resume protocol

Read AGENTS, issue100, roadmap118 and the mailmap contract before changing this branch.

## Current objective and success conditions

Implement explicit consumer-owned author presentation with real Git proof and no inferred identity.

## State snapshot

Base41d4 is the accepted S4 source. The containing candidate SHA/PR are intentionally null at authorship.
Foundation3.0/schema1.2 is a breaking contract proposal, not an automatically propagated release.

## Completed and material changes

The portable header contains no identity. Golden inputs preserve the prior public mapping and comments.
The resolver emits a deterministic plan; reusable filesystem materialization remains Holon-owned.

## Validation and review evidence

Actual Git fixtures exercise all forms, case/name matching, conflicts, presentation, local preservation,
updates and guarded retained-byte restoration while commit/tree IDs and raw author fields stay identical.
Canonical focused checks and exact-head review are recorded with the bounded implementation PR.

## Blockers, risks, unknowns, and deferred work

Public references establish provenance, not automated identity approval. New equivalences require review.
Filament/owner adapters and fleet adoption remain separate; no release, cleanup or history rewrite occurs.

## Next dependency-ready work

Review the exact source/projections and actual checks, then root coordinates merge and tracker acceptance.

## Parallel changes and reconciliation

Issue64 is isolated and avoids shared catalog/continuity edits. Issue65 is a subsequent independent slice.
Accepted S4 publication and earlier source proofs retain their original identities and clocks.

## Privacy and redaction

Public fixtures use synthetic example.invalid identities. No private aliases, credentials or local paths
are added to source evidence.

## Handoff update protocol

Keep source frozen for exact-head review. Record resulting run/PR IDs in review metadata without another
post-qualification documentation commit. Root owns ordinary merge and explicit issue disposition.

## Compaction and supersession

This bounded source checkpoint supersedes the old operational resume pointer. Historical publication
receipts/source guides remain intact and are not retimed as mailmap evidence.
