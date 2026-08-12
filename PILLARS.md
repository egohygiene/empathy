---
schema: aether.architecture-document/v1
id: empathy-pillars
title: Empathy Pillars
kind: architecture-document
version: 0.1.0
status: draft
owners:
  - egohygiene
created: 2026-08-11
updated: 2026-08-11
governed_by:
  - architecture-pillars
depends_on:
  - empathy-purpose
  - empathy-vision
  - empathy-principles
related:
  - empathy-manifesto
  - empathy-foundations
  - empathy-roadmap
supersedes: []
---

# Empathy Pillars

## Introduction

The pillars are the enduring capabilities Empathy must keep healthy to fulfill its purpose. They are
not projects, repositories, tools, or roadmap phases.

## Pillar 1 — Humane Repository Governance

Repositories need explicit, accessible ways to participate, request help, report harm or
vulnerabilities, understand maintenance expectations, and contest consequential automation.

- **Includes:** contribution, conduct, support, security, maintenance, accessibility, communication,
  and decision-governance contracts.
- **Excludes:** consumer-specific product policy and organization identity.
- **Contribution:** makes trust and agency part of the baseline rather than an informal maintainer
  convention.
- **Health signals:** required concerns have canonical owners; paths to help and escalation are
  discoverable; language remains accessible and non-coercive.

## Pillar 2 — Reproducible Developer Experience

Contributors and maintainers need a predictable path from checkout to validated change.

- **Includes:** stable task interfaces, local and CI parity, editor integration, environment
  declarations, cross-platform behavior, and deterministic dependency management.
- **Excludes:** a mandatory personal workstation configuration or one universal application stack.
- **Contribution:** reduces onboarding and maintenance cost without hiding how the repository works.
- **Health signals:** canonical checks run locally; prerequisites and failures are explainable;
  environment assumptions are explicit.

## Pillar 3 — Trustworthy Quality and Supply Chain

The foundation must make quality, security, licensing, and dependency state observable without
equating a green badge with truth.

- **Includes:** Egolint policy, fixtures, security scanning, provenance, SBOM responsibilities,
  report normalization, and durable audits.
- **Excludes:** suppressing legitimate findings or claiming universal risk elimination.
- **Contribution:** turns policy into executable evidence while preserving unresolved risk.
- **Health signals:** tools prove configuration ownership; passed and inapplicable states differ;
  exceptions are narrow; report and audit semantics remain separate.

## Pillar 4 — Composable and Bounded Automation

Automation should be reusable, least-privileged, observable, and safe to adopt incrementally.

- **Includes:** active GitHub workflows, composite actions, permissions, timeouts, immutable
  references, manual guards, and future reusable Relay extraction.
- **Excludes:** autonomous mutation without authorization or product-specific workflows in the
  universal baseline.
- **Contribution:** enables repeatability without surrendering human authority.
- **Health signals:** pull-request jobs are read-only; write paths are explicit; staged automation is
  inert; reusable units have stable inputs and outputs.

## Pillar 5 — Architecture and Evidence Intelligence

People and agents need shared language, bounded system models, accepted decisions, provenance, and a
visible path from intent to validation.

- **Includes:** architecture documents, decision records, Aether-authored intelligence artifacts,
  machine-readable catalogs, validation, and change propagation.
- **Excludes:** treating generated text or private reasoning as canonical evidence.
- **Contribution:** makes the foundation explainable and evolvable instead of merely copied.
- **Health signals:** the architecture graph resolves; ownership conflicts are visible; source and
  projections are distinguishable; decisions preserve their rationale.

## Relationships Between Pillars

The pillars reinforce one another. Governance defines the human contract. Developer experience makes
that contract usable. Quality supplies evidence. Automation executes bounded workflows.
Architecture intelligence preserves meaning and coordinates change across all four.

No pillar may optimize itself by undermining another. For example, automation speed cannot override
governance, and quality tooling cannot impose irrelevant project assumptions merely to maximize
coverage.

## Initiative Alignment

Every roadmap initiative should name at least one primary pillar and any affected secondary pillars.
An initiative that cannot explain its contribution to this set should not become part of Empathy's
strategic roadmap.

## Open Questions

- Which governance contracts are complete enough to serve as the universal profile?
- What health evidence will be gathered from the first non-Ego-Hygiene consumer?
- Should architecture intelligence remain a pillar if Empathy becomes a Holon-managed profile?

## Validation

- Governing specification: `architecture-pillars` version `2.0.0`.
- The five pillars are capability-oriented, mutually distinguishable, and independent of current
  repository layout.
- Each pillar defines scope, non-scope, strategic contribution, and qualitative health signals.
- Temporary PRs, tools, and extraction projects are not pillars.
