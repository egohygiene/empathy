---
schema: aether.architecture-document/v1
id: empathy-roadmap
title: Empathy Roadmap
kind: architecture-document
version: 0.1.0
status: draft
owners:
  - egohygiene
created: 2026-08-11
updated: 2026-08-19
governed_by:
  - architecture-roadmap
depends_on:
  - empathy-vision
  - empathy-pillars
  - empathy-architecture
  - empathy-decisions
related:
  - empathy-methodology
  - empathy-meta
supersedes: []
---

# Empathy Roadmap

## Accepted Direction: Baseline Convergence

Empathy is converging from a fast-moving integration and incubation workspace into the strict
universal baseline template.

The convergence sequence is:

1. freeze and inventory baseline candidates;
2. move experiments and unfinished capabilities to Sanctuary;
3. graduate reusable capabilities to their canonical repositories;
4. express specialized templates as explicit inheritance deltas;
5. publish an independently versioned Empathy baseline;
6. let Holon instantiate and Pace later reconcile consumer repositories.

This direction is accepted; exact migration mechanics and release gates remain roadmap work.

## Strategic Context

Empathy has completed a substantial integration foundation for GitHub automation and Egolint, but it
does not yet provide a stable, versioned repository-foundation distribution. The current strategic
work is to turn a capable integration monorepo into an explicit composition model without losing the
quality evidence already established.

The roadmap is capability- and outcome-oriented. It does not promise dates, issue ordering, or a
specific implementation before the corresponding architecture decisions are accepted.

## Now — Make the Foundation Explicit

### Establish the Architecture Source of Truth

- Complete and validate the root architecture-document graph.
- Resolve terminology, human/AI authority, system boundaries, design language, decision governance,
  and change propagation.
- Integrate architecture validation into the canonical local and CI contracts.

**Outcome:** maintainers, contributors, and agents can determine what Empathy is, what it owns, and
how a durable change is evaluated.

**Primary pillars:** Architecture and Evidence Intelligence; Humane Repository Governance.

### Reconcile the Imported Aether Corpus

- Classify files under `egolint/.agents/` as source, provisional integration copy, or consumer
  projection.
- Repair source-relative assumptions needed for current validation without erasing provenance.
- Decide the durable Aether-to-Empathy interface and prevent path-based ownership drift.

**Outcome:** reusable intelligence artifacts have one canonical owner and a reproducible consumption
path.

**Primary pillars:** Architecture and Evidence Intelligence; Composable and Bounded Automation.

### Complete the Universal Community-Health Contract

- Inventory missing contribution, conduct, support, security, maintenance, accessibility,
  communication, governance, and community-health artifacts.
- Separate universally required contracts from optional organization or product extensions.
- Add evidence-based templates and validation without copying stale profile content.

**Outcome:** the “humane repository foundation” claim is supported beyond CI and linting.

**Primary pillar:** Humane Repository Governance.

## Next — Make Composition and Adoption Reproducible

### Define the Universal Core and Capability Profiles

- Create a versioned profile and capability manifest with ownership, source, version, dependencies,
  applicability, configuration, files, generated projections, validation, and lifecycle state.
- Define consumer exceptions and stricter local policy without allowing silent weakening.
- Add representative profile fixtures and conflict tests.

**Outcome:** universal and optional behavior is machine-distinguishable and reviewable.

### Establish Source, Projection, and Distribution Contracts

- Produce deterministic distributions with provenance, checksums, compatibility, and migration data.
- Validate source-to-projection drift and prevent generated artifacts from becoming accidental source.
- Exercise adoption, upgrade, removal, and local extension against consumer fixtures.

**Outcome:** a consumer can reproduce and inspect what it adopts.

### Harden the Reproducible Development Experience

- Replace the minimal development container with an intentional Realm-aligned profile or explicitly
  document why it remains minimal.
- Verify supported local platforms, tool prerequisites, bootstrap, cache boundaries, and editor
  behavior.
- Keep Taskfile, hooks, editor, container, and CI contracts in parity.

**Outcome:** a clean checkout reaches meaningful validation through a documented, cross-platform
path.

### Complete Egolint Product Boundaries

- Define the public Egolint configuration/schema, CLI or adapter surface, container/action packaging,
  and independent versioning.
- Preserve the validated fast/holistic/complementary/reporting architecture during extraction.
- Consume the released boundary back into Empathy integration tests.

**Outcome:** Empathy integrates Egolint as an independently consumable capability rather than a
permanent embedded subsystem.

## Later — Extract, Orchestrate, and Prove the Ecosystem

### Extract Reusable Automation and Environment Capabilities

- Move reusable GitHub actions/workflows to Relay with immutable consumption and integration
  fixtures.
- Move portable development-environment capabilities to Realm while retaining the Empathy profile.
- Keep Empathy-specific selection and tests in Empathy.

**Outcome:** capability ownership matches organization architecture without losing end-to-end proof.

### Resolve the Holon Boundary

- Decide whether Holon compiles organization desired state using Empathy profile content or absorbs
  more of Empathy's composition role.
- Keep Ego Hygiene and future Incompris instances separate in identity, content, policy, and desired
  state.
- Preserve local-first inspection, plan-before-mutation, exceptions, diagnostics, and audit.

**Outcome:** repository-foundation content and organization-state orchestration have nonoverlapping
canonical owners.

### Validate Real Consumer Adoption

- Pilot the universal core and selected profiles in repositories with different languages, sizes,
  governance needs, and release models.
- Gather repository-level feedback without person-level scoring or unnecessary telemetry.
- Promote contracts to stable only when adoption, migration, accessibility, security, and maintenance
  evidence support the claim.

**Outcome:** stability reflects consumer evidence rather than internal completeness alone.

### Establish Release and Compatibility Governance

- Define semantic versioning and compatibility for foundation, profile, and capability changes.
- Automate changelogs, migration guidance, provenance, signed or attestable artifacts, and rollback.
- Define deprecation windows and consumer conformance reporting.

**Outcome:** adopters can upgrade deliberately and understand risk.

## Maybe — Evidence-Gated Expansion

The following remain intentionally uncommitted until evidence and ownership justify them:

- a hosted catalog or marketplace for profiles and capabilities;
- a visual organization-health dashboard;
- autonomous synchronization or mutation of consumer repositories;
- subjective repository scoring;
- cross-provider AI-agent deployment beyond reproducible source projections.

These ideas must not block the local-first, versioned foundation.

## Dependencies and Risks

| Dependency or risk                 | Impact                                            | Current response                                                      |
| ---------------------------------- | ------------------------------------------------- | --------------------------------------------------------------------- |
| Aether source/projection ambiguity | Ownership drift and nonreproducible imports       | Classify and decide the interface before broader distribution         |
| Missing profile schema             | Universal and optional behavior remain implicit   | Make the manifest the first composition capability                    |
| Monorepo coupling                  | Extraction becomes harder as integration grows    | Enforce stable boundaries and consume released owners back into tests |
| Holon overlap                      | Duplicate desired-state and composition authority | Record an accepted boundary before implementation                     |
| Unresolved dependency advisories   | Security signal remains red                       | Preserve evidence; upgrade when real fixed versions exist             |
| Limited accessibility evidence     | Humane-design claims remain provisional           | Audit active surfaces and consumer journeys                           |
| No external consumer               | Stability claims are internally biased            | Use diverse consumer fixtures and pilots before stable release        |

## Assumptions and Evidence Gaps

- Current integration quality is sufficient to preserve while architecture and distribution mature.
- The order may change as owner repositories and consumer evidence evolve.
- “Now,” “Next,” and “Later” describe dependency and maturity, not calendar commitments.
- No roadmap item is automatically accepted implementation authority.

## Open Questions

- Which repository should host the first independent consumer fixture?
- What minimum release unit can prove the source/projection/consumer loop?
- Which current staged workflows are valuable capabilities versus historical reference?
- When should the architecture documents move from draft to active?

## Validation

- Governing specification: `architecture-roadmap` version `1.1.0`.
- Initiatives align with [`VISION.md`](VISION.md), [`PILLARS.md`](PILLARS.md), and the current
  architecture gaps.
- Outcomes and dependencies lead the roadmap; issue lists, sprint detail, and unsupported dates are
  absent.
- Uncommitted expansions are explicitly separated from planned capability evolution.
