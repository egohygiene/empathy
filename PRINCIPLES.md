---
schema: aether.architecture-document/v1
id: empathy-principles
title: Empathy Principles
kind: architecture-document
version: 0.1.0
status: draft
owners:
  - egohygiene
created: 2026-08-11
updated: 2026-08-11
governed_by:
  - architecture-principles
depends_on:
  - empathy-purpose
  - empathy-vision
related:
  - empathy-pillars
  - empathy-foundations
  - empathy-methodology
supersedes: []
---

# Empathy Principles

## Introduction

These principles are durable decision heuristics for Empathy. They guide trade-offs; they do not
replace enforceable policy, accepted decisions, or tool-specific standards.

## Principle 1 — People Before Machinery

Design repository behavior around the dignity, agency, safety, accessibility, and limited attention
of the people affected by it.

- Prefer understandable choices and recovery paths over invisible convenience.
- Do not use automation success, activity, or engagement as a proxy for human benefit.
- When efficiency conflicts with meaningful human control, preserve control.

## Principle 2 — Universal Core, Explicit Capabilities

Keep the mandatory baseline as small as its purpose permits. Make additional opinions explicit,
selectable, and independently removable.

- A capability must declare applicability, dependencies, ownership, and effects.
- Absence or inapplicability must not be reported as success.
- Consumer identity and product-specific assumptions never belong in the universal core.

## Principle 3 — One Canonical Owner, Many Composable Consumers

Every important concern has one authoritative source. Integrations consume or project that source
without silently forking its meaning.

- Prefer references, generated projections, and adapters over duplicated policy.
- Physical placement does not redefine semantic ownership.
- Resolve ownership conflicts before adding a parallel system.

## Principle 4 — Explicit Over Implicit

Make states, dependencies, permissions, applicability, defaults, and exceptions observable.

- Prefer stable commands and machine-readable contracts over undocumented convention.
- A skipped, blocked, missing, failed, staged, and disabled capability must remain distinguishable.
- Surface contradictions instead of smoothing them into a misleading narrative.

## Principle 5 — Evidence Over Appearance

Claims of quality, safety, compatibility, or completion require relevant evidence.

- Preserve valid findings rather than weakening checks to make a branch green.
- Distinguish observations, inferences, assumptions, decisions, and proposals.
- Generated reports are evidence inputs, not durable truth by themselves.

## Principle 6 — Local First, Automation in Parity

Important repository contracts must be understandable and runnable without depending exclusively on
a hosted service.

- Local commands, hooks, editors, and CI should consume the same canonical configuration.
- Hosted automation may add integration context but must not redefine the underlying rule.
- Reproducible, offline validation is preferred when the required evidence is local.

## Principle 7 — Safe, Bounded, and Reversible Automation

Grant only the authority necessary for the requested task and make consequential effects reviewable.

- Pull requests are the default boundary for material changes.
- Read-only and report-only jobs must not acquire write authority.
- Destructive, externally visible, security-sensitive, or difficult-to-reverse actions require
  explicit authorization.

## Principle 8 — Accessibility, Security, and Maintenance Are Foundations

Treat accessibility, privacy, security, licensing, and long-term maintenance as architecture inputs,
not optional polish.

- A fast path may narrow scope, but it may not conceal the existence of the holistic contract.
- Cross-platform and low-cognitive-load behavior are design constraints.
- Exceptions are narrow, documented, reviewable, and temporary when possible.

## Principle Conflicts and Precedence

When principles conflict, apply this order:

1. Protect people, privacy, security, legal obligations, and explicit human authority.
2. Preserve truthfulness, evidence, and reviewability.
3. Preserve canonical ownership and the universal-versus-optional boundary.
4. Optimize reproducibility, simplicity, reuse, and speed.

No principle authorizes violating an accepted policy or concealing a material risk.

## Exceptions

An exception records the affected principle, scope, owner, rationale, evidence, expiration or review
trigger, and compensating control. Repetition does not turn an undocumented exception into policy.

## Open Questions

- What minimum evidence is required before a capability may join the universal core?
- Which consumer exceptions should be portable across repositories?
- How will principle conflicts be represented in future profile manifests?

## Validation

- Governing specification: `architecture-principles` version `2.0.0`.
- Each principle identifies a decision trade-off and remains implementation-independent.
- Precedence and exception handling are explicit.
- The principles derive from [`PURPOSE.md`](PURPOSE.md) and [`VISION.md`](VISION.md) without
  duplicating policy or roadmap content.
