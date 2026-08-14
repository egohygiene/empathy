---
schema: aether.architecture-document/v1
id: empathy-design
title: Empathy Design
kind: architecture-document
version: 0.1.0
status: draft
owners:
  - egohygiene
created: 2026-08-11
updated: 2026-08-14
governed_by:
  - architecture-design
depends_on:
  - empathy-purpose
  - empathy-vision
  - empathy-principles
  - empathy-personal-model
related:
  - empathy-design-system
  - empathy-ontology
  - empathy-system
supersedes: []
---

# Empathy Design

## Design Philosophy

Empathy should feel like a calm, capable collaborator: clear about expectations, honest about
limits, respectful of attention, and willing to help a person recover when something goes wrong.

The foundation expresses rigor through legibility and feedback rather than ceremony or intimidation.
Its design is primarily the experience of reading, choosing, contributing, validating, and
maintaining—not a specific graphical interface.

## Intended Experience

A maintainer should be able to understand what the foundation owns, select only relevant
capabilities, and see the consequence of a change before it becomes durable.

A contributor should be able to find the next meaningful action, run the same core checks as CI,
understand a failure without knowing the whole platform, and ask for help or correction without
shame.

An adopter should be able to distinguish the universal core from profiles, inspect provenance,
override or omit an optional capability explicitly, and upgrade without surrendering repository
identity.

An AI agent should encounter canonical sources, bounded authority, stable task interfaces, and
objective completion checks rather than infer hidden conventions.

## Experience Qualities

- **Humane:** language and process acknowledge that people have different contexts and capacity.
- **Legible:** states, ownership, dependencies, defaults, and next actions are visible.
- **Calm:** information hierarchy and progressive disclosure reduce unnecessary urgency and noise.
- **Capable:** advanced behavior remains available without burdening the default path.
- **Trustworthy:** claims connect to evidence; limitations and known findings remain visible.
- **Recoverable:** ordinary errors have safe explanations, remediation, and retry paths.
- **Composable:** adopters can understand and remove optional capabilities without collateral damage.
- **Consistent:** local, editor, hook, CI, and documentation language describe the same contracts.

## Interaction Philosophy

Interactions follow a preview-or-plan, act, validate, and review rhythm. Defaults should be safe and
conservative. Consequential actions require explicit confirmation at the point of impact. Automated
behavior must make its trigger, scope, result, and recovery path inspectable.

Progressive disclosure is preferred: the common path is concise, while rationale, advanced options,
and complete evidence remain reachable. “Magic” that removes a person's ability to understand or
control a repository is not a design success.

## Communication Philosophy

Use direct, plain, technically precise language. Describe the artifact or contract that failed rather
than judging the person. Say what happened, why it matters, what evidence exists, what is known or
unknown, and what action is available.

Status words use canonical ontology. “Passed,” “failed,” “inapplicable,” “skipped,” “blocked,”
“staged,” and “deprecated” are not interchangeable. Avoid false urgency, vague reassurance,
gratuitous jargon, and blame-oriented copy.

## Accessibility Philosophy

Accessibility is a foundation constraint. Repository documents, templates, generated visuals, and
future interfaces should support semantic structure, keyboard use, screen readers, sufficient
contrast, non-color status communication, zoom/reflow, reduced motion, and understandable language.

Alternative paths should exist when a graphical, interactive, networked, or automated experience is
not available. No critical meaning should depend only on color, motion, iconography, or a hover state.

## Agency and Meaningful Control

- Explain what optional automation will do before it acts.
- Allow profile choices and exceptions to be explicit and reviewable.
- Keep destructive and externally visible actions outside implicit defaults.
- Provide a human review or escalation path for consequential automated output.
- Do not require telemetry, profiling, or unnecessary disclosure to use the foundation.

## Cognitive Load

The design should minimize simultaneous decisions, duplicated instructions, and inconsistent paths.
Stable commands, predictable document locations, concise summaries, and ordered architecture reduce
the amount a person must remember.

Complexity that protects important capability or evidence should be organized, not hidden. The
universal core should not expose every optional tool to every contributor by default.

## Trust, Feedback, and Recovery

Feedback should be timely, scoped, and actionable. A failure identifies the responsible contract and
the smallest useful next step. When a check cannot run, the system reports missing dependency or
inapplicability rather than a false pass.

Recovery favors branches, drafts, idempotent generation, atomic replacement, backups or history,
and explicit retries. Generated artifacts identify how to reproduce them.

## Aesthetic Direction

The shared aesthetic is clean, warm, spacious, and information-first. It may use subtle expressive
details, but never at the cost of readability or product individuality. Consumer projects may adopt
distinct visual worlds while preserving the same semantic and accessibility commitments.

Empathy now defines a project-specific creative direction in `.identity/brief.md`, while shared
consumer commitments remain semantic and brand-neutral. No candidate artwork or branded token
palette is canonical yet. Current generated visuals use accessible semantic hierarchy and a system
sans-serif stack; exact implementation values remain downstream until human-approved identity
sources exist.

## Design Anti-Goals

- Dark patterns, coercive defaults, or consent hidden in setup flow.
- Gamification of contributors, maintainers, security, or repository “health.”
- Dense dashboards that collapse distinct evidence into one score.
- Error messages that blame people or omit recovery.
- Mandatory animation, color-only state, or aesthetics that obscure content.
- A rigid visual identity imposed on consumer repositories.
- Delight that delays task completion, hides risk, or makes behavior unpredictable.

## Product Identity and Shared Commitments

Empathy defines shared experience commitments, not a universal product brand. A consumer may vary
voice, visual identity, density, motion, and layout only within the accessibility, agency, evidence,
and semantic boundaries in this document and [`DESIGN_SYSTEM.md`](DESIGN_SYSTEM.md).

## Evidence and Assumptions

- **Observed:** The active repository emphasizes stable Taskfile commands, editor/CI parity,
  explicit report namespaces, status distinctions, and accessible generated SVG metadata.
- **Observed:** Issue templates separate architecture, DX, research, CI, and task concerns rather than
  forcing one generic form.
- **Assumed:** The same experience philosophy can support CLI, documentation, GitHub, generated
  reports, and future interfaces without a single component implementation.
- **Missing evidence:** No formal accessibility audit or external adopter study has been completed.

## Open Questions

- What accessibility conformance level will be required for generated docs and future sites?
- Which user journeys should be tested first with non-Ego-Hygiene adopters?
- How much visual identity belongs in Empathy itself versus consumer themes?

## Downstream Implications

This philosophy constrains templates, CLI messages, issue forms, workflows, reports, generated
architecture, documentation sites, profile selection, error recovery, and any future UI. Changes to
these surfaces should trace decisions to an experience quality or explicit exception.

## Validation

- Governing specification: `architecture-design` version `2.0.0`.
- Experience qualities, accessibility, agency, cognitive load, trust, recovery, aesthetic direction,
  anti-goals, evidence, and product-identity boundaries are explicit.
- No framework components, tokens, or screen layouts define the philosophy.
