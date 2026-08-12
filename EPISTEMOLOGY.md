---
schema: aether.architecture-document/v1
id: empathy-epistemology
title: Empathy Epistemology
kind: architecture-document
version: 0.1.0
status: draft
owners:
  - egohygiene
created: 2026-08-11
updated: 2026-08-11
governed_by:
  - architecture-epistemology
depends_on:
  - empathy-purpose
  - empathy-principles
related:
  - empathy-ai-constitution
  - empathy-ontology
  - empathy-decisions
supersedes: []
---

# Empathy Epistemology

## Scope

This document defines how Empathy classifies claims, evaluates evidence, preserves provenance,
expresses uncertainty, resolves conflict, and revises canonical working knowledge. It applies to
human and AI contributions, architecture documents, audits, reports, decisions, and claims about
repository behavior.

It does not prescribe which technical conclusions must be accepted.

## Claim States

| State      | Meaning                                                    | Required treatment                                   |
| ---------- | ---------------------------------------------------------- | ---------------------------------------------------- |
| Observed   | Directly present in inspectable evidence                   | Cite or name the evidence and its scope              |
| Inferred   | Reasoned from observations                                 | Identify the supporting observations and uncertainty |
| Decided    | Accepted by an authorized maintainer or governance process | Link the canonical decision and acceptance state     |
| Proposed   | Offered for review but not accepted                        | Do not present as current architecture               |
| Assumed    | Used temporarily when evidence is unavailable              | State the assumption and its consequence             |
| Unverified | Plausible but not checked                                  | Keep out of completion or safety claims              |
| Disputed   | Supported by conflicting credible evidence                 | Preserve the conflict and assign review ownership    |
| Superseded | Previously canonical but replaced                          | Preserve lineage and identify the successor          |

A statement may change state as evidence or authority changes. Confidence does not turn a proposal
into a decision or an inference into an observation.

## Evidence and Source Evaluation

Evidence is evaluated by relevance, directness, recency, provenance, reproducibility, and authority
within the claim's scope. A typical repository-behavior ordering is:

1. Reproducible execution against the current revision and inspectable source or configuration.
2. Merged, accepted decisions and governing contracts that define intended behavior.
3. Deterministic tests, validation output, signed or immutable build evidence, and primary upstream
   specifications.
4. Durable audits that record method, revision, findings, and limitations.
5. Generated reports, workflow artifacts, issues, implementation plans, and secondary sources.
6. Unattributed recollection or generated prose without inspectable provenance.

This order is contextual, not absolute. Current implementation proves what happens, not necessarily
what should happen. An accepted decision proves intent, not successful implementation. A conflict
between them is architecture drift and must remain visible.

External technical claims should prefer primary sources such as official specifications,
documentation, advisories, release metadata, and original research. Source popularity is not proof.

## Provenance

Material claims record enough context to reproduce their interpretation:

- artifact path or source URL;
- revision, version, or retrieval date when relevant;
- whether the artifact is source, projection, generated output, report, audit, or proposal;
- the transformation applied to source information;
- known limitations or excluded evidence.

Unavailable provenance is labeled; it is never reconstructed from guesswork.

## Confidence and Uncertainty

Empathy uses qualitative confidence only when it improves a decision:

- **High:** direct, current, reproducible evidence with no material conflict found.
- **Moderate:** relevant evidence supports the claim, but it is indirect, incomplete, or not fully
  reproduced.
- **Low:** the claim depends materially on assumptions, sparse evidence, or unresolved conflict.

Confidence is scoped to a claim. It is not a score for a person, contributor, repository, or source.
Unknown is a valid state.

## Conflict Resolution

When credible claims conflict:

1. preserve each claim and its provenance;
2. identify whether the conflict concerns fact, intent, interpretation, scope, or time;
3. prefer direct and reproducible evidence for observed behavior;
4. prefer the authorized, non-superseded record for accepted intent;
5. seek missing primary evidence or reproduce the behavior;
6. record a decision when evidence alone cannot choose between valid alternatives;
7. retain a disputed state until the conflict is actually resolved.

Coherence, confidence of tone, or AI consensus does not resolve a conflict.

## Canonical Working Knowledge

Knowledge becomes canonical within Empathy when its scope and owner are explicit, its provenance is
inspectable, required review has occurred, and it resides in the artifact type that owns the concern.

- Architecture documents own durable intent and boundaries.
- `DECISIONS.md` owns significant accepted choices and rationale.
- Source and configuration own current executable behavior.
- Tests own repeatable assertions about behavior.
- `.audits/` owns durable findings and recommendations.
- `.reports/` contains replaceable generated evidence, not architectural truth.
- `.staging/` contains candidates that are not active contracts.

Physical presence in the repository does not alone make an artifact canonical.

## Revision and Deprecation

Canonical knowledge remains revisable. A material revision records the reason, affected downstream
artifacts, evidence, and whether it corrects, supersedes, or narrows the prior claim. Historical
rationale is not rewritten to appear better informed than it was.

## Examples

- “The fast profile selects 12 linters” is observed only when supported by the current generated
  inventory and its validation test.
- “This capability belongs in Relay” is proposed until accepted through the repository's decision
  process, even if it aligns with organization architecture.
- “OSV passed” is false when scanning completed but the severity gate reported unresolved findings;
  those states must be described separately.
- An imported Aether path may be observed under `egolint/.agents/` while its long-term ownership and
  projection path remain unresolved.

## Open Questions

- Which external architecture artifacts will Empathy pin by version rather than copy?
- What provenance fields will future distribution manifests require?
- Which decisions require more than maintainer review because they affect organization-wide state?

## Validation

- Governing specification: `architecture-epistemology` version `2.0.0`.
- Claim states, confidence, conflict handling, canonicalization, and revision are operationally
  defined.
- AI-generated material is not self-validating, and private reasoning is not required evidence.
- The model applies to both intended architecture and observed implementation without collapsing the
  distinction.
