---
schema: aether.architecture-document/v1
id: empathy-design-system
title: Empathy Design System
kind: architecture-document
version: 0.1.0
status: draft
owners:
  - egohygiene
created: 2026-08-11
updated: 2026-08-11
governed_by:
  - architecture-design-system
depends_on:
  - empathy-personal-model
  - empathy-design
related:
  - empathy-ontology
  - empathy-architecture
supersedes: []
---

# Empathy Design System

## Purpose and Scope

This document defines the implementation-independent design language for Empathy's repository
surfaces: Markdown documentation, issue and pull-request forms, command output, workflow summaries,
reports, diagrams, and future interactive experiences.

It defines semantic roles and guarantees from which concrete tokens or components may be derived. It
does not prescribe a CSS framework, component library, renderer, or consumer brand.

## Relationship to DESIGN.md

[`DESIGN.md`](DESIGN.md) owns the desired experience: humane, legible, calm, capable, trustworthy,
recoverable, composable, and consistent. This document translates those qualities into reusable
design-language rules. When a local pattern conflicts with the design philosophy, the philosophy
prevails unless an accepted decision records a bounded exception.

## Design-Language Foundations

- Semantic meaning precedes visual styling.
- Structure works in plain text and common Markdown renderers before enhancement.
- The default path is concise; advanced detail remains discoverable.
- Critical states use text labels and structure, never color or icon alone.
- A consumer may vary expression while preserving accessibility, agency, and status semantics.

## Semantic Roles

| Role               | Meaning                                                    | Typical expression                             |
| ------------------ | ---------------------------------------------------------- | ---------------------------------------------- |
| Primary action     | The next safe action in the current context                | One clearly labeled command or control         |
| Secondary action   | A useful but nonrequired alternative                       | Visually subordinate and separately labeled    |
| Destructive action | An action with difficult-to-recover effects                | Explicit impact language and confirmation      |
| Information        | Neutral context needed for understanding                   | Plain prose, note, or structured metadata      |
| Success            | Applicable work executed and satisfied its contract        | `Passed` plus scope and evidence               |
| Warning            | Review is needed but the current operation may continue    | `Warning` plus consequence and next step       |
| Failure            | An applicable contract did not pass                        | `Failed` plus owner, evidence, and remediation |
| Blocked            | Required authority, evidence, or dependency is unavailable | `Blocked` plus the smallest needed resolution  |
| Inapplicable       | The capability does not apply to the current context       | `Not applicable` plus applicability reason     |
| Staged             | Preserved candidate with no active effect                  | `Staged` plus disposition owner                |
| Deprecated         | Supported historical path with a preferred successor       | `Deprecated` plus migration guidance           |

## Typography

- Use semantic heading levels with exactly one page-level title.
- Use the renderer's readable system sans-serif for generated diagrams and interfaces unless a
  consumer identity specifies an accessible alternative.
- Use monospace only for code, commands, identifiers, paths, hashes, versions, and machine state.
- Preserve zoom, reflow, selectable text, and user font settings.
- Do not simulate hierarchy with bold text when a semantic heading is appropriate.

Exact font families, sizes, and line heights are implementation tokens. They must preserve clear
hierarchy and comfortable long-form reading.

## Color and Contrast

- Define colors by semantic role rather than fixed brand names.
- Text and interactive states meet the consumer's declared accessibility conformance target.
- Success, warning, failure, blocked, staged, and deprecated states include text labels and may also
  use shapes or icons.
- Focus indicators and links remain distinguishable in every theme.
- Consumer themes may change hue and surface expression but may not weaken contrast or remove
  non-color meaning.

Empathy does not yet publish canonical color tokens. A future token set requires visual and
accessibility evidence before becoming active.

## Spacing and Density

- Group related information and separate distinct concerns visibly.
- Prefer a comfortable default density with an optional compact presentation only where content
  volume justifies it.
- Do not encode meaning solely through whitespace.
- Keep line length, list depth, tables, and simultaneous controls within cognitively manageable
  bounds.

## Shape, Surface, Border, and Elevation

Use containment to communicate grouping, hierarchy, selection, or interaction—not decoration alone.
Critical boundaries remain understandable without shadows or color. Consumer themes may vary shape
and surface character while retaining semantic roles.

## Iconography and Imagery

- Icons supplement labels; they do not replace critical text.
- Decorative imagery has empty alternative text; informative imagery has concise equivalent text.
- Diagrams include accessible titles/descriptions and a textual legend or equivalent explanation.
- Avoid imagery that stereotypes people, implies unsupported emotion, or obscures technical content.
- Emoji may support tone or established commit conventions but never carry the only meaning.

## Motion and Transition

- Motion is never required to understand state or complete an action.
- Respect reduced-motion preferences and provide an effectively static alternative.
- Use motion only to explain continuity, causality, progress, or spatial change.
- Avoid flashing, involuntary parallax, excessive looping, and attention capture.
- Repository Markdown and command-line surfaces must remain fully usable without motion.

## Interaction States

Interactive implementations define default, hover where applicable, focus, active, selected,
disabled, busy, success, warning, failure, and recovery states. Keyboard, pointer, touch, screen
reader, and programmatic behavior receive equal semantic treatment where the platform supports them.

Disabled controls explain why when the reason is not otherwise evident. Busy states expose progress
or bounded waiting and do not trap the user.

## Feedback, Errors, and Recovery

Feedback uses this order when practical:

1. result state and affected scope;
2. plain-language explanation;
3. evidence or diagnostic location;
4. smallest safe next action;
5. deeper detail or escalation path.

Errors describe the system or contract, not a person's character. Recovery is proportionate and
preserves work. Retry behavior must be safe or explicitly warn when it is not idempotent.

## Content and Voice Patterns

- Lead with the outcome or decision-relevant fact.
- Use direct, respectful, nonjudgmental language.
- Prefer canonical terms from [`ONTOLOGY.md`](ONTOLOGY.md).
- Name exact targets, versions, paths, states, and owners when they matter.
- Distinguish required, recommended, optional, proposed, and unknown.
- Avoid false urgency, vague “something went wrong” copy, anthropomorphic claims of AI certainty,
  and celebratory language that hides risk.
- Commands use long-form arguments where portable and double quotes where syntax permits.

## Accessibility Requirements

- Semantic document and control structure.
- Keyboard access and visible focus for interactive surfaces.
- Programmatic labels, names, roles, state, and error association.
- Sufficient contrast and non-color communication.
- Zoom, reflow, and responsive text without loss of function.
- Reduced-motion support and no essential animation.
- Alt text or textual equivalents for informative visuals.
- Plain-language summaries for dense technical output.
- No time limit without necessity, warning, and a reasonable extension path.

Concrete implementations document their target standard and validation method. This baseline does not
claim conformance without testing.

## Responsive and Cross-Platform Behavior

The design language must survive GitHub, local Markdown viewers, terminals, editors, generated SVG,
mobile/narrow layouts, and future web surfaces. Wide tables and diagrams require an equivalent
linear explanation. Commands and paths disclose platform constraints.

## Product Identity, Themes, and Variation

Consumers may define typography, palette, illustration, motion personality, tone accents, spacing
scale, shape, and layout patterns. Variants must preserve semantic roles, content order, accessible
states, meaningful control, and canonical status language.

Shared consistency means equivalent meaning and behavior, not identical appearance.

## Governance and Contribution

A reusable pattern enters the design system when it addresses a repeated need, traces to
[`DESIGN.md`](DESIGN.md), documents accessibility and variation, and has implementation evidence in
more than one relevant surface or a compelling universal requirement.

Pattern changes identify affected templates, docs, reports, consumer themes, tests, and migration
needs. Local experiments remain local until reviewed.

## Deprecation and Migration

Deprecated patterns retain a successor, reason, affected surfaces, migration guidance, and removal
or review condition. A visual refresh does not silently change semantic meaning. Consumers receive a
path to adapt identity without losing accessibility or state clarity.

## Implementation Handoff

An implementation derived from this document should specify:

- semantic role mapping;
- platform and renderer;
- concrete tokens or component behavior;
- accessibility target and test method;
- supported interaction/input modes;
- consumer variation points;
- fallbacks for plain text, reduced motion, narrow layouts, and unavailable enhancement;
- provenance back to the governing design rule.

## Coverage Gaps and Open Questions

- Canonical visual tokens and component implementations are intentionally absent.
- The repository has not completed a formal accessibility audit of issue forms, Markdown, terminal
  output, or generated reports.
- Consumer theming and design-system conformance formats are not yet defined.
- The first repeated cross-surface patterns should be validated before this draft becomes active.

## Validation

- Governing specification: `architecture-design-system` version `2.0.0`.
- Semantic roles, content, typography, color, density, imagery, motion, interaction, recovery,
  accessibility, variation, governance, and handoff are addressed.
- Rules remain implementation-independent and trace to [`DESIGN.md`](DESIGN.md).
- Missing tokens and formal accessibility evidence are identified rather than fabricated.
