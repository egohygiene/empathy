---
schema: aether.architecture-document/v1
id: empathy-ontology
title: Empathy Ontology
kind: architecture-document
version: 0.1.0
status: draft
owners:
  - egohygiene
created: 2026-08-11
updated: 2026-08-11
governed_by:
  - architecture-ontology
depends_on:
  - empathy-purpose
  - empathy-vision
  - empathy-principles
  - empathy-epistemology
related:
  - empathy-personal-model
  - empathy-system
  - empathy-architecture
supersedes: []
---

# Empathy Ontology

## Domain Scope

The Empathy domain is the composition, validation, and distribution of a humane repository
foundation. Its concepts describe repository contracts, capability ownership, participants,
artifacts, lifecycle state, execution, and evidence. They do not prescribe a consumer's application
domain or implementation schema.

## Domain Boundaries

- A repository foundation establishes conditions around a project; it is not the project itself.
- Empathy integrates reusable capabilities; canonical capability owners retain their semantic
  ownership.
- A consumer repository owns its identity, private context, product behavior, and selected desired
  state.
- Source artifacts, projections, generated output, reports, and audits are distinct kinds of
  evidence.
- Human participants are not equivalent to accounts, events, profiles, or metrics.

## Canonical Concepts

### Foundation and Composition

| Identifier                      | Canonical term        | Definition                                                                                                                                   | Key relationships                                                             |
| ------------------------------- | --------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| `empathy:repository-foundation` | Repository foundation | A coherent set of social, technical, governance, quality, and automation contracts that establishes how a repository is operated and changed | Composed by Empathy; adopted by a consumer repository                         |
| `empathy:universal-contract`    | Universal contract    | A contract intended to apply to every supported consumer without product-specific assumptions                                                | Member of the universal core; may be realized by one or more source artifacts |
| `empathy:universal-core`        | Universal core        | The minimum set of universal contracts required for a conforming Empathy foundation                                                          | Excludes optional capability profiles                                         |
| `empathy:capability`            | Capability            | A bounded, independently understandable unit of repository behavior with an owner, contract, dependencies, applicability, and validation     | Selected directly or through a capability profile                             |
| `empathy:capability-profile`    | Capability profile    | A named, versioned selection and configuration of capabilities for a class of consumers                                                      | Extends the universal core; does not redefine consumer identity               |
| `empathy:integration-monorepo`  | Integration monorepo  | A repository that assembles multiple capabilities and tests their interactions before or alongside independent distribution                  | Empathy's current repository role                                             |
| `empathy:consumer-repository`   | Consumer repository   | A repository that adopts a versioned foundation and retains its own identity, policy extensions, content, and product behavior               | Chooses profiles and records exceptions                                       |
| `empathy:capability-owner`      | Capability owner      | The canonical authority for a capability's source contract and lifecycle                                                                     | Empathy consumes the capability without duplicating ownership                 |

### Artifacts and Lifecycle

| Identifier                    | Canonical term      | Definition                                                                                             | Key relationships                                                              |
| ----------------------------- | ------------------- | ------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ |
| `empathy:source-artifact`     | Source artifact     | An authoritative, human-reviewable artifact from which projections or generated outputs may be derived | Has provenance and a canonical owner                                           |
| `empathy:projection`          | Projection          | A deterministic consumer- or provider-shaped representation derived from a source artifact             | Must identify source version and transformation                                |
| `empathy:generated-artifact`  | Generated artifact  | Reproducible output derived from source and safe to replace                                            | Must not silently become canonical source                                      |
| `empathy:active-artifact`     | Active artifact     | An artifact included in current repository behavior or a selected profile                              | Has applicable validation and ownership                                        |
| `empathy:staged-artifact`     | Staged artifact     | Preserved candidate material that is classified but intentionally inert                                | Is not active, passing, supported, or distribution-ready                       |
| `empathy:deprecated-artifact` | Deprecated artifact | A supported historical artifact with a preferred successor or planned removal                          | Preserves migration guidance and lineage                                       |
| `empathy:distribution`        | Distribution        | A versioned, reproducible package or projection prepared for a consumer                                | Contains provenance, checksums, and compatibility information when implemented |

### Policy, Execution, and Evidence

| Identifier                    | Canonical term      | Definition                                                                                        | Key relationships                                                            |
| ----------------------------- | ------------------- | ------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| `empathy:contract`            | Contract            | An explicit statement of required behavior, inputs, outputs, boundaries, or validation            | May be human-readable, machine-readable, or both                             |
| `empathy:policy`              | Policy              | An enforceable or governable rule within a defined scope                                          | Is not interchangeable with a principle or manifesto belief                  |
| `empathy:validation-contract` | Validation contract | A reproducible procedure and result model used to evaluate an artifact or capability              | Distinguishes pass, fail, skip, inapplicable, missing, disabled, and blocked |
| `empathy:local-runtime`       | Local runtime       | A contributor-controlled environment that executes canonical repository contracts                 | Should remain in parity with CI for shared rules                             |
| `empathy:ci-runtime`          | CI runtime          | Hosted or self-hosted automation that executes repository contracts with event context            | Must not redefine canonical local policy                                     |
| `empathy:report`              | Report              | Replaceable generated evidence from a tool or workflow                                            | Lives under `.reports/`; not durable architecture truth                      |
| `empathy:audit`               | Audit               | Durable, method-described analysis of findings, risk, and recommendations at a known revision     | Lives under `.audits/`; may consume reports                                  |
| `empathy:decision`            | Decision            | A significant accepted choice with authority, context, rationale, trade-offs, and review triggers | Canonically recorded in `DECISIONS.md` or linked ADRs                        |

### Participants

| Identifier            | Canonical term | Definition                                                                                      | Key relationships                                                          |
| --------------------- | -------------- | ----------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| `empathy:person`      | Person         | A human affected by, participating in, or responsible for repository behavior                   | Remains distinct from any representation or account                        |
| `empathy:maintainer`  | Maintainer     | A person with accepted responsibility and authority in a repository scope                       | Reviews changes and governs decisions within that scope                    |
| `empathy:contributor` | Contributor    | A person or disclosed automation actor proposing an artifact or change                          | Does not gain decision authority merely by contributing                    |
| `empathy:adopter`     | Adopter        | A person or organization selecting and operating an Empathy foundation in a consumer repository | Owns consumer-specific configuration and exceptions                        |
| `empathy:ai-agent`    | AI agent       | An AI system acting under bounded instructions, tools, permissions, and human authority         | Governed by `AI_CONSTITUTION.md`; is not a person or maintainer by default |

## Relationship Model

The core relationships are:

- Empathy **composes** the universal core and capability profiles.
- A capability owner **governs** a capability's source contract.
- A capability profile **selects** and **configures** capabilities.
- A consumer repository **adopts** a distribution or materialized foundation.
- A source artifact **produces** a projection or generated artifact through a recorded transformation.
- A validation contract **evaluates** an applicable artifact in a local or CI runtime.
- A report **supplies evidence to** an audit or decision but does not replace either.
- A maintainer **authorizes or reviews** consequential changes.
- An AI agent **assists** within bounded authority and never acquires human identity through action.

## Ubiquitous Language

Use these terms consistently in documents, issues, code, tasks, workflows, and reports:

- Say **universal core** for the mandatory minimum and **capability profile** for a named optional
  selection.
- Say **active**, **staged**, **deprecated**, or **generated** instead of the ambiguous word
  “included.”
- Say **inapplicable** when a capability does not match the repository and **missing dependency**
  when it applies but cannot run.
- Say **source** and **projection** explicitly; do not call both “the template.”
- Say **report** for disposable tool output and **audit** for durable reviewed analysis.
- Say **consumer repository**, not “managed repository,” unless an accepted management authority
  exists.

## Aliases and Deprecated Terms

| Term             | Treatment                                                    | Preferred term or clarification                                                   |
| ---------------- | ------------------------------------------------------------ | --------------------------------------------------------------------------------- |
| Baseline         | Allowed only with scope                                      | Use **universal core**, **profile**, or **repository foundation**                 |
| Template         | Ambiguous                                                    | Identify a source template, projection, or consumer artifact                      |
| Tool passed      | Incomplete                                                   | State applicable/executed/result; inapplicable is not passing                     |
| Generated source | Contradictory unless code generation is explicitly canonical | Name the canonical source and generated artifact separately                       |
| User             | Contextual                                                   | Prefer maintainer, contributor, adopter, or person affected when the role matters |

## Conceptual Invariants

- Canonical ownership does not change merely because an artifact is copied or colocated.
- A staged artifact has no active effect.
- A generated artifact is replaceable from identified source.
- A capability has one primary owner and explicit applicability.
- A consumer repository retains its identity and may be stricter than the universal foundation.
- A person remains distinct from any account, representation, inference, or metric.
- A decision is not an observation, and a report is not a decision.

## Open Questions

- What is the canonical term for the future materialized unit: bundle, distribution, pack, or
  projection set?
- Will Holon own consumer desired-state manifests while Empathy owns the reusable profile content?
- Which current files under `egolint/.agents/` are source artifacts versus provisional consumer
  projections from Aether?

## Migration Notes

Current references that treat physical placement as ownership should migrate to capability-owner
language. The Aether-derived corpus currently under `egolint/.agents/` must not be described as
Egolint-owned merely because of its path. A future accepted decision should define whether it moves,
is generated, or is replaced by a pinned distribution.

## Validation

- Governing specification: `architecture-ontology` version `2.0.0`.
- Definitions are conceptual rather than class, API, database, or directory schemas.
- Canonical terms have stable identifiers, boundaries, relationships, and invariants.
- Known ambiguity around Aether projection placement remains visible.
