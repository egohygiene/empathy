---
schema: aether.architecture-document/v1
id: empathy-system
title: Empathy System
kind: architecture-document
version: 0.1.0
status: draft
owners:
  - egohygiene
created: 2026-08-11
updated: 2026-08-19
governed_by:
  - architecture-system
depends_on:
  - empathy-foundations
  - empathy-ontology
related:
  - empathy-architecture
  - empathy-design
  - empathy-methodology
supersedes: []
---

# Empathy System

## Purpose and Scope

This document describes Empathy's logical systems, capability ownership, boundaries, and major
interactions. It answers what the major systems do. [`ARCHITECTURE.md`](ARCHITECTURE.md) separately
defines how those systems are structurally organized and allowed to depend on one another.

The inventory includes implemented systems and explicitly identified target boundaries. It does not
claim that every target capability is independently released today.

## Accepted Repository Role

Empathy is the strict baseline template and reference consumer for universal repository behavior.
It owns baseline content and integration evidence, not the machinery that creates organizations.

- **Sanctuary** owns experimental incubation and graduation evidence.
- **Hygiene** defines the organization rules the baseline satisfies.
- **Holon** resolves and instantiates baseline and specialized templates.
- **Pace** later detects and reconciles drift in instantiated repositories.
- **Aether, Relay, Realm, Egolint, Identity, and other capability repositories** own the reusable
  packages that keep the baseline thin.

Historical incubations may remain physically present during migration, but physical presence does
not grant long-term architectural ownership.

## System Inventory

### Foundation Contract System

Defines the humane universal repository contract: identity, architecture, governance, contribution,
conduct, support, security, maintenance, accessibility, communication, and consumer-profile
semantics.

- **Current evidence:** root documentation, issue and pull-request templates, Copilot instructions,
  license policy, ownership, and this architecture set.
- **State:** partial; several community-health documents and a machine-readable profile model remain
  future work.

### Capability Composition System

Selects compatible capability sources, records universal-versus-optional membership, integrates
their configuration, and validates cross-capability behavior.

- **Current evidence:** the integration monorepo layout, root Taskfile imports, active workflow
  composition, and staged-classification boundary.
- **State:** implemented manually and structurally; no canonical profile manifest or released
  materializer exists yet.

### Quality and Supply-Chain System

Egolint owns cross-language lint policy, formatter and scanner configuration, fixtures, profile
inventories, complementary tools, hooks, editor parity, reports, and the stable quality task API.

- **Current evidence:** `egolint/`, `.mega-linter.yml`, root quality tasks, generated lint
  architecture, tests, and security workflows.
- **Canonical owner:** Egolint, currently encapsulated in this monorepo.

### Automation System

Executes active GitHub event, validation, reporting, security, contributor, and repository
intelligence workflows with bounded permissions and reusable composite actions.

- **Current evidence:** repository-owned `.github/workflows/`, local adapters under
  `.github/actions/`, and immutable actions released by Relay.
- **Canonical owner:** Relay owns independently reusable behavior while Empathy retains profile
  selection, permissions, final artifact composition, and integration tests.

### Intelligence Artifact System

Supplies reusable specifications, skills, agents, templates, evals, catalogs, projections, and
governance for human/AI-assisted architecture and engineering work.

- **Current evidence:** the Aether-derived corpus under `egolint/.agents/`.
- **Canonical owner:** Aether.
- **State:** imported for integration; its current physical placement and source/projection status are
  provisional and must not be interpreted as Egolint ownership.

### Development Environment System

Describes editor, workspace, dev-container, dependency, and local command expectations so a
contributor can reproduce canonical repository behavior.

- **Current evidence:** `.devcontainer/`, `.vscode/`, workspace files, dependency manifests, and
  Taskfile commands.
- **Target owner:** portable environment capabilities should align with Realm; Empathy retains only
  the integration profile and consumer-specific adapter.

### Visual Identity System

Defines project-owned creative intent, canonical source requirements, versioned
platform targets, tool-neutral creative handoffs, and the future deterministic
generation and verification lifecycle for branded assets.

- **Current evidence:** the reusable Rust holon under `identity/`, Empathy's
  `.identity/` consumer contract, target profiles, integration tests, and
  identity validation workflow.
- **Boundary:** designers and AI tools may author candidates, but only explicit
  human approval promotes canonical sources; generated assets never replace
  their source contract.
- **State:** foundation implemented for initialization, validation, planning,
  and handoff; rendering, import, visual checks, framework adapters, and
  Renderflow integration remain future work.

### Evidence and Observability System

Separates ephemeral tool output, normalized reports, durable audits, architecture decisions, and
workflow artifacts so findings can support review without becoming accidental source truth.

- **Current evidence:** `.reports/`, `.audits/`, report-publication actions, SARIF uploads, and
  architecture validation tests.
- **State:** implemented for the quality platform; broader capability health remains future work.

### Staging and Classification System

Preserves imported or candidate material without allowing it to affect active behavior until its
applicability, owner, dependencies, security, and lifecycle are resolved.

- **Current evidence:** `.staging/github/README.md` and categorized inert workflows.
- **State:** implemented as a repository boundary; no general machine-readable disposition catalog
  exists yet.

### Distribution and Consumer Conformance System

Builds versioned foundation distributions, projections, provenance, checksums, migrations, and
consumer conformance results.

- **Current evidence:** source-specific builders inside the imported Aether corpus and existing
  generated-report conventions.
- **State:** target system; Empathy does not yet publish a canonical consumer distribution.

## Responsibilities and Capability Ownership

| Capability                                             | Primary logical owner | Empathy responsibility                                               |
| ------------------------------------------------------ | --------------------- | -------------------------------------------------------------------- |
| Repository foundation identity and profile composition | Empathy               | Define, integrate, validate, and document                            |
| Reusable intelligence artifacts                        | Aether                | Consume a pinned source or projection and test compatibility         |
| Cross-language quality policy                          | Egolint               | Integrate the stable task/configuration boundary                     |
| Reusable GitHub automation                             | Relay                 | Pin releases and prove behavior in the integration profile           |
| Reproducible development environment                   | Realm target          | Define the Empathy profile and validate repository use               |
| Reusable visual-identity compiler                      | Identity holon        | Own the Empathy specification, approve sources, and test projections |
| Organization desired state and materialization         | Holon target          | Supply reusable profile content; do not own consumer identity        |
| Consumer application and policy extensions             | Consumer repository   | Provide documented extension and exception points                    |

Target ownership labels describe the intended architecture and remain provisional until accepted and
implemented in the corresponding repository.

## System Boundaries

- The Foundation Contract System defines what the baseline means; the Composition System selects and
  assembles it.
- Capability systems own their internal policy; Composition invokes stable public boundaries.
- Automation executes contracts but does not own their semantic rules.
- Evidence records outcomes but does not choose architecture.
- Staging preserves candidates but never feeds active execution implicitly.
- Distribution derives consumer artifacts; it does not edit source or consumer identity silently.
- Consumer repositories may extend or strengthen the baseline through explicit configuration and
  exceptions.

## Major Interactions and Runtime Flows

### Contribution Validation Flow

1. A contributor proposes a scoped change.
2. The local Taskfile, hooks, and editor run canonical fast feedback.
3. Pull-request automation runs read-only validation and the fast Egolint profile.
4. Scheduled or manually authorized workflows run holistic policy and supply-chain checks.
5. Workflows upload reports and supported SARIF; trusted default-branch runs may publish curated
   snapshots.
6. A maintainer reviews the change, evidence, known findings, and architecture impact.

### Capability Integration Flow

1. A capability owner publishes or exposes versioned source.
2. Empathy records applicability, dependency, version, and profile membership.
3. Composition supplies the capability through a stable adapter.
4. Integration tests exercise capability interactions locally and in CI.
5. Distribution produces a traceable consumer representation.
6. A consumer adopts the result and records local configuration or exceptions.

Steps 2, 5, and 6 are only partially implemented today.

### AI-Assisted Change Flow

1. A human or repository workflow grants a bounded task.
2. The agent resolves repository instructions, architecture, specifications, and evidence.
3. The agent makes a reversible, scoped change or returns a plan/audit as authorized.
4. Canonical checks produce inspectable validation.
5. Consequential effects stop at the configured human review boundary.

## External System Relationships

- GitHub supplies source hosting, pull requests, permissions, Actions, code scanning, and artifacts.
- Package registries and upstream projects supply dependencies, tools, schemas, and advisories.
- Consumer repositories receive future distributions or projections.
- Ego Hygiene repositories supply capability sources and organization architecture.

External availability or platform behavior must not be mistaken for Empathy-owned guarantees.

## Assumptions and Evidence Gaps

- The system inventory is derived from the current repository and the newest organization ownership
  direction; several target owners are not yet consumed through releases.
- No machine-readable universal/profile manifest proves the complete Composition System today.
- No consumer-conformance run demonstrates the Distribution System end to end.
- The imported Aether corpus contains stale source-relative paths, confirming that its consumer
  projection contract needs reconciliation.

## Open Questions

- What versioned manifest lets Holon resolve Empathy and specialized template deltas without
  duplicating baseline ownership?
- What are the public interfaces between Empathy and Aether, Egolint, and Realm?
- Which producer and deployment workflows should remain repository-specific as Relay expands?

## Validation

- Governing specification: `architecture-system` version `1.1.0`.
- Every major capability has a primary logical owner, responsibility, boundary, and implementation
  state.
- Runtime flows distinguish implemented behavior from target behavior.
- Package and directory layout are evidence, not substitutes for the logical system model.
