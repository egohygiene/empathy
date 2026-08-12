---
schema: aether.architecture-document/v1
id: empathy-methodology
title: Empathy Methodology
kind: architecture-document
version: 0.1.0
status: draft
owners:
  - egohygiene
created: 2026-08-11
updated: 2026-08-11
governed_by:
  - architecture-methodology
depends_on:
  - empathy-principles
  - empathy-epistemology
  - empathy-ai-constitution
  - empathy-foundations
  - empathy-architecture
related:
  - empathy-decisions
  - empathy-roadmap
supersedes: []
---

# Empathy Methodology

## Purpose and Scope

Empathy evolves through an architecture-first, evidence-preserving loop:

> Discover → Design → Specify → Plan → Implement → Validate → Review → Integrate → Reflect

The method coordinates human and AI work across architecture, capabilities, automation, and consumer
profiles. It is not a sprint process, issue backlog, or tool-specific runbook.

## Working Method

### Discover

Inspect current source, configuration, history, reports, audits, upstream owners, consumer needs, and
existing decisions. Classify claims using [`EPISTEMOLOGY.md`](EPISTEMOLOGY.md). Preserve conflicts and
unavailable evidence.

### Design

Define the problem boundary, affected people, canonical owner, system responsibility, interfaces,
dependency direction, states, data flow, permissions, failure behavior, and explicit non-goals.
Update architecture before code when the change alters durable intent.

### Specify

Express the desired behavior as stable inputs, outputs, invariants, requirements, constraints,
applicability, lifecycle, compatibility, and acceptance criteria. Reusable source remains
provider-neutral and consumer identity remains external.

### Plan

Break accepted design into dependency-ordered, reviewable changes. Identify migrations, rollout,
validation, generated artifacts, ownership transfers, risks, and rollback or recovery. Keep proposed
work distinct from accepted decisions.

### Implement

Make the smallest coherent change behind the public capability boundary. Preserve unrelated work,
reuse canonical configuration, avoid parallel systems, and keep source distinct from generated
output.

### Validate

Run the applicable local contract first, then the relevant integration and hosted checks. Prove
configuration loading, positive and negative behavior, applicability, deterministic generation,
security, licensing, accessibility where relevant, and local/CI parity. Record unavailable or
inherited failures honestly.

### Review

Review behavior, architecture alignment, evidence quality, human impact, permissions, scope,
maintainability, compatibility, and downstream migration. Material AI-authored work receives human
review before acceptance.

### Integrate

Merge through the repository's governance boundary, publish only with explicit authority, update
durable decisions and audits, and verify the post-integration state. Generated reports remain
replaceable.

### Reflect

Compare expected and observed outcomes. Classify new evidence, capture drift and recurring friction,
refine tests or contracts, and update architecture only when the underlying model changed.

## Workflow Stages or Loops

### Architecture Loop

Purpose and principles → ontology and personal model → system → architecture → design/methodology →
decisions → roadmap. Downstream changes propagate back to their canonical owners when assumptions no
longer hold.

### Capability Loop

Owner contract → Empathy profile selection → adapter → integration fixture → local/CI execution →
report/audit → consumer projection. A capability that cannot state applicability or ownership does
not enter the universal core.

### Change Loop

Issue or approved request → scoped branch → implementation → fast validation → draft PR → CI and
review → merge → post-merge evidence. Consequential actions stop at explicit human gates.

### Exception Loop

Constraint encountered → narrow exception proposal → evidence and impact → authorized decision →
explicit scope/owner/review trigger → compensating validation → expiration, renewal, or removal.

## Validation Loops

Validation is layered:

1. **Structural:** syntax, metadata, links, schemas, licenses, formatting, and generated drift.
2. **Unit/fixture:** positive, negative, edge, and inapplicability behavior.
3. **Contract:** public task, profile, artifact, and state semantics.
4. **Integration:** capability interactions and local/CI parity.
5. **Security/accessibility:** least privilege, vulnerability evidence, privacy boundaries, and human
   usability where affected.
6. **Consumer:** projection reproducibility, configuration, migration, and exception behavior.

A narrower loop may provide fast feedback but does not replace the holistic loop.

## Feedback and Improvement

Feedback sources include contributor experience, failures, flaky or slow checks, security findings,
audits, dependency changes, consumer adoption, accessibility review, and observed drift. Improvement
targets the owning contract rather than layering local workarounds.

Metrics remain scoped signals. They do not rank people or compress repository health into a single
score. A repeated exception, confusing failure, or expensive manual step is evidence that the
architecture or interface may need revision.

## Human and AI Collaboration Patterns

Humans own purpose, authority, accepted decisions, consequential trade-offs, review, and exception
approval. AI agents may accelerate discovery, drafting, implementation, testing, and audits within
[`AI_CONSTITUTION.md`](AI_CONSTITUTION.md).

The preferred bounded handoff is:

1. architecture and source analysis;
2. specification and acceptance criteria;
3. implementation plan;
4. issue or authorized implementation;
5. tests and validation;
6. independent audit or review;
7. human acceptance.

Agents do not need to be separate processes for every step, but the concerns and evidence remain
distinguishable.

## Boundaries and Exclusions

- This methodology does not mandate a sprint length, project-management framework, or release cadence.
- It does not require every small change to create every document or ceremony.
- It does not authorize autonomous mutation, merge, release, or external communication.
- It does not treat tool output as self-interpreting or AI text as self-validating.
- It does not permit test or policy weakening solely to make CI pass.
- It does not duplicate detailed contribution guides, commands, or operational runbooks.

## Assumptions and Evidence Gaps

- **Observed:** The repository already uses scoped PRs, local Taskfile contracts, layered fast and
  holistic linting, generated artifact checks, and durable audits.
- **Observed:** Current architecture work follows imported specification and skill contracts but lacks
  a dedicated architecture-document validator until this change.
- **Assumed:** Future profile/distribution work can follow the same loop without making the loop tool-
  or provider-specific.
- **Missing evidence:** No external consumer feedback loop is active yet.

## Open Questions

- Which methodology stages must become machine-enforced before a stable distribution?
- What independent review is required for organization-wide profile changes?
- How should consumer feedback enter Empathy without collecting unnecessary personal data?

## Validation

- Governing specification: `architecture-methodology` version `1.1.0`.
- Major stages, feedback, validation, human/AI collaboration, exceptions, and boundaries are explicit.
- The methodology aligns with the architecture and principles while remaining implementation-light.
- Detailed backlog, sprint, and command documentation remain outside this document.
