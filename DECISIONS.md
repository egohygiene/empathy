---
schema: aether.architecture-document/v1
id: empathy-decisions
title: Empathy Decisions
kind: architecture-document
version: 0.1.0
status: draft
owners:
  - egohygiene
created: 2026-08-11
updated: 2026-08-19
governed_by:
  - architecture-decisions
depends_on:
  - empathy-principles
  - empathy-epistemology
  - empathy-foundations
  - empathy-system
  - empathy-architecture
related:
  - empathy-ai-constitution
  - empathy-methodology
  - empathy-roadmap
supersedes: []
---

# Empathy Decisions

## Purpose

This document preserves significant accepted Empathy architecture decisions and their rationale. It
does not replace source, policy, specifications, issues, implementation plans, or meeting notes.

The initial records reconstruct only decisions directly evidenced by the merged repository state on
2026-08-11. Rationale that cannot be established from that evidence is not invented.

## Decision Governance

A decision belongs here when it materially changes purpose, ownership, system boundaries,
dependencies, public contracts, security/privacy/accessibility posture, distribution, compatibility,
or a difficult-to-reverse trade-off.

Accepted decisions require an authorized maintainer review. Proposed choices remain in issues or
plans until accepted. Corrections append or amend factual metadata; changed choices create a
superseding record and preserve lineage.

## Storage Mode

Empathy currently uses an inline log. If records become difficult to review, `DECISIONS.md` will
remain the canonical index and detailed records will move to `docs/decisions/` through an accepted
migration decision.

## Status Definitions

- **Proposed:** under review; not current architecture.
- **Accepted:** current authorized choice.
- **Deprecated:** still discoverable but discouraged pending replacement.
- **Superseded:** replaced by another identified decision.
- **Rejected:** considered and explicitly not selected.

## Decision Index

| ID       | Title                                                                 | Status   | Accepted   | Supersedes | Superseded by |
| -------- | --------------------------------------------------------------------- | -------- | ---------- | ---------- | ------------- |
| ADR-0001 | Use Empathy as the repository-foundation integration monorepo         | Accepted | 2026-08-11 | —          | —             |
| ADR-0002 | Encapsulate cross-language quality policy behind Egolint              | Accepted | 2026-08-11 | —          | —             |
| ADR-0003 | Keep imported product-specific automation staged and inert            | Accepted | 2026-08-11 | —          | —             |
| ADR-0004 | Use Taskfile as the stable local repository interface                 | Accepted | 2026-08-11 | —          | —             |
| ADR-0005 | Separate disposable reports from durable audits                       | Accepted | 2026-08-11 | —          | —             |
| ADR-0006 | Keep pull-request automation read-only and trusted publication narrow | Accepted | 2026-08-11 | —          | —             |
| ADR-0007 | Make Empathy the strict baseline and move incubation to Sanctuary     | Accepted | 2026-08-19 | —          | —             |

## Active Decisions

### ADR-0001 — Use Empathy as the Repository-Foundation Integration Monorepo

#### Metadata

- **Status:** Accepted
- **Accepted:** 2026-08-11
- **Owners:** `egohygiene`
- **Scope:** repository role and composition boundary
- **Review triggers:** stable external distributions, Holon integration, or independent capability
  extraction changes the repository's role

#### Context

The repository needed a place to reconcile a universal baseline and optional capabilities before
independently versioned components and consumer materialization were complete.

#### Decision

Empathy acts as the integration monorepo for Ego Hygiene's repository foundation. It composes
universal contracts and selectable capability profiles while preserving the identity and ownership
of independently reusable capabilities.

#### Rationale and Evidence

The role is stated in [`README.md`](README.md) and realized through root integrations for GitHub
automation and Egolint. A monorepo permits interaction testing while boundaries are still being
defined.

#### Alternatives, Trade-Offs, and Consequences

A repository containing only static templates would reduce integration complexity but would not
prove capability interactions. Immediate independent release of every capability would preserve
ownership but create coordination overhead before interfaces are stable.

The accepted choice enables consolidation and evidence gathering, but risks accidental permanent
coupling. Capability ownership, profile membership, and extraction must remain explicit.

#### Observed Outcomes and Related Artifacts

The repository now has root task composition, active workflows, Egolint integration, reports, audits,
and staging. A machine-readable profile model and consumer distribution remain missing.

Related: [`PURPOSE.md`](PURPOSE.md), [`SYSTEM.md`](SYSTEM.md),
[`ARCHITECTURE.md`](ARCHITECTURE.md).

### ADR-0002 — Encapsulate Cross-Language Quality Policy Behind Egolint

#### Metadata

- **Status:** Accepted
- **Accepted:** 2026-08-11
- **Owners:** `egohygiene`
- **Scope:** linting, formatting, security-quality, hooks, editor parity, fixtures, and tool inventory
- **Review triggers:** Egolint becomes an independently consumed release or its public interface
  changes incompatibly

#### Context

Quality tooling spanned many languages, scanners, hooks, editor extensions, reports, and runtime
dependencies. Direct root ownership would duplicate tool knowledge and make extraction difficult.

#### Decision

Egolint owns the complete quality-policy catalog and exposes stable Taskfile and configuration
boundaries to the Empathy root. MegaLinter-native and complementary tools keep distinct ownership
without duplicate execution.

#### Rationale and Evidence

The boundary is documented in [`egolint/README.md`](egolint/README.md) and implemented through
`egolint/tasks/`, tool matrices, fixtures, wrappers, and root Taskfile imports.

#### Alternatives, Trade-Offs, and Consequences

Root-level standalone workflows per tool would be simpler individually but create drift and false
parity. Treating MegaLinter as the owner of all tools would misrepresent project-aware and
complementary capabilities.

Encapsulation creates a large subsystem and dependency graph, but provides one truthful interface and
an extraction path.

#### Observed Outcomes and Related Artifacts

Fast and holistic profiles, complementary state modeling, editor parity, security ownership, and
generated architecture are integrated. Egolint is still physically embedded rather than released.

Related: [`SYSTEM.md`](SYSTEM.md), [`ARCHITECTURE.md`](ARCHITECTURE.md),
[`.reports/egolint/architecture/README.md`](.reports/egolint/architecture/README.md).

### ADR-0003 — Keep Imported Product-Specific Automation Staged and Inert

#### Metadata

- **Status:** Accepted
- **Accepted:** 2026-08-11
- **Owners:** `egohygiene`
- **Scope:** imported GitHub workflows and scripts without universal applicability
- **Review triggers:** an artifact gains a canonical owner, applicability contract, dependencies, and
  integration evidence

#### Context

Imported automation included application, container, documentation, release, security, and
source-specific assumptions that were unsafe to activate as a universal foundation.

#### Decision

Preserve uncertain material under `.staging/github/`, categorize it, and keep it outside active
GitHub discovery paths until explicitly adopted or retired.

#### Rationale and Evidence

[`.staging/github/README.md`](.staging/github/README.md) defines the inert classification boundary.
Active workflows live only under `.github/workflows/`.

#### Alternatives, Trade-Offs, and Consequences

Deleting candidates would reduce clutter but lose useful evidence. Activating everything would grant
irrelevant permissions and dependencies. Staging preserves review opportunity at the cost of ongoing
classification work.

#### Observed Outcomes and Related Artifacts

The active automation surface is reviewable and product-specific candidates remain inert. A general
machine-readable staging disposition contract is still absent.

Related: [`FOUNDATIONS.md`](FOUNDATIONS.md), [`SYSTEM.md`](SYSTEM.md).

### ADR-0004 — Use Taskfile as the Stable Local Repository Interface

#### Metadata

- **Status:** Accepted
- **Accepted:** 2026-08-11
- **Owners:** `egohygiene`
- **Scope:** contributor-facing local commands and subsystem composition
- **Review triggers:** Taskfile no longer supports required platforms or a replacement provides a
  materially better stable interface with a migration path

#### Context

Tools use different runtimes, arguments, configuration paths, and installation mechanisms. Direct
commands in documentation, hooks, editors, and CI would drift.

#### Decision

Expose stable repository operations through root Taskfile tasks and delegate capability-specific
behavior to owner task files or adapters. Editors and hooks call the same interface where practical.

#### Rationale and Evidence

[`Taskfile.yml`](Taskfile.yml) composes Egolint and complementary tasks and exposes validation,
security, SBOM, report, hook, and tool-state commands. Root and subsystem documentation use these
commands.

#### Alternatives, Trade-Offs, and Consequences

Raw tool commands reduce one dependency but spread configuration knowledge. Make or custom scripts
could provide a similar boundary but would require another migration without current benefit.

Taskfile becomes a required developer tool and must remain explicit, portable, and thin.

#### Observed Outcomes and Related Artifacts

Local, hook, editor, and CI policy share more configuration and tasks. Some workflows still invoke
implementation commands where event-specific orchestration requires it.

Related: [`METHODOLOGY.md`](METHODOLOGY.md), [`.vscode/tasks.json`](.vscode/tasks.json).

### ADR-0005 — Separate Disposable Reports From Durable Audits

#### Metadata

- **Status:** Accepted
- **Accepted:** 2026-08-11
- **Owners:** `egohygiene`
- **Scope:** generated quality/security evidence and reviewed findings
- **Review triggers:** report retention, external archival, or compliance requirements change

#### Context

Tool output is reproducible, noisy, and tied to a revision. Architectural findings and remediation
guidance need durable context and review. Mixing them creates stale source and unclear history.

#### Decision

Use `.reports/` for replaceable generated output and workflow artifacts, and `.audits/` for durable,
reviewed findings and recommendations. Reports may inform audits but do not become canonical
architecture.

#### Rationale and Evidence

The distinction is documented in [`egolint/README.md`](egolint/README.md) and
[`.reports/README.md`](.reports/README.md), and implemented by report-publication automation and
Egolint audits.

#### Alternatives, Trade-Offs, and Consequences

Committing every timestamped report preserves history but creates noise and accidental truth. Keeping
all output only as ephemeral CI artifacts reduces repository churn but loses curated latest-state
discoverability. The accepted split preserves both uses with different lifecycles.

#### Observed Outcomes and Related Artifacts

Quality and OSV output use stable report namespaces; audits record remediation context. Report
publication remains limited to trusted runs.

Related: [`EPISTEMOLOGY.md`](EPISTEMOLOGY.md),
[`Relay publish-report-snapshot`](https://github.com/egohygiene/relay/tree/ca6e9319d5133615c1b9e0b5ea5a4f5d3a113210/actions/publish-report-snapshot).

### ADR-0006 — Keep Pull-Request Automation Read-Only and Trusted Publication Narrow

#### Metadata

- **Status:** Accepted
- **Accepted:** 2026-08-11
- **Owners:** `egohygiene`
- **Scope:** GitHub Actions permissions, report publication, and untrusted change validation
- **Review triggers:** GitHub permission semantics change or a new PR write requirement is proposed

#### Context

Pull requests may contain untrusted code and configuration. Some default-branch workflows need to
publish curated reports or code-scanning results.

#### Decision

Pull-request jobs remain read-only. Complete reports are uploaded as artifacts and valid findings as
SARIF. Only guarded trusted default-branch jobs may perform narrow report-only writes, with recursion
prevention and concurrency handling.

#### Rationale and Evidence

The active workflow policy, automation validator, and report-publisher action enforce event,
permission, path, and branch constraints. This preserves validation without exposing write authority
to untrusted changes.

#### Alternatives, Trade-Offs, and Consequences

Allowing PR workflows to write would simplify automated fixes but materially increase supply-chain
risk. Eliminating all publication would reduce risk but remove curated default-branch evidence. The
accepted design adds guarded complexity in exchange for a narrow, reviewable write surface.

#### Observed Outcomes and Related Artifacts

PR checks publish artifacts without repository writes. Trusted report publication is centralized and
covered by policy tests.

Related: [`AI_CONSTITUTION.md`](AI_CONSTITUTION.md),
[`tests/test_report_publication.py`](tests/test_report_publication.py).

## ADR-0007 — Make Empathy the Strict Baseline and Move Incubation to Sanctuary

### Metadata

- **Status:** Accepted
- **Accepted:** 2026-08-19
- **Owners:** `egohygiene`
- **Scope:** repository role, template inheritance, incubation, and capability graduation
- **Review triggers:** the organization adopts a different canonical template model or evidence shows
  the separation prevents reliable integration testing

### Context

Empathy accumulated baseline files, reusable capabilities, product-specific experiments, and staged
migration material while the organization architecture was still emerging. That accelerated
learning, but it left one repository responsible for incompatible lifecycle states and made its
future boundary ambiguous.

### Decision

Empathy is the canonical strict baseline repository template. Sanctuary owns experimentation and
incubation. Reusable capabilities graduate to their canonical repositories; specialized repository
templates inherit from Empathy through explicit deltas. Holon resolves and instantiates templates,
while Pace later reconciles desired state in consumer repositories.

Temporary physical presence in Empathy does not establish durable ownership.

### Rationale and Evidence

A strict baseline makes Hygiene conformance testable, keeps Holon generation deterministic, lets
capability repositories version independently, and gives experimental work a safe home without
polluting every generated repository.

### Alternatives, Trade-Offs, and Consequences

Keeping Empathy as both baseline and incubator maximizes short-term convenience but makes universal
applicability impossible to prove. Moving all integration responsibility into Holon would mix
template content with generation mechanics. The accepted split adds migration work and a Sanctuary
lifecycle, but creates clearer ownership and release boundaries.

### Observed Outcomes and Related Artifacts

This record changes target ownership immediately. Source migration, template manifests, Sanctuary
creation, and release automation remain follow-up work.

Related: [`PURPOSE.md`](PURPOSE.md), [`SYSTEM.md`](SYSTEM.md),
[`ARCHITECTURE.md`](ARCHITECTURE.md), and [`ROADMAP.md`](ROADMAP.md).

## Deprecated and Superseded Decisions

None recorded.

## Historical Decisions

No earlier decision records with sufficient provenance were found in the current repository.

## Evidence Gaps and Open Questions

The following choices are not accepted decisions in this log:

- whether Aether source is relocated, pinned, or projected into Empathy;
- whether Realm extraction uses releases, source references, or generated distributions;
- whether Holon owns Empathy profile composition or only organization desired state;
- which contracts form the universal core and which profiles are first-party;
- the compatibility and migration policy for the first stable consumer distribution.

Governing specification: `architecture-decisions` version `2.0.0`.

## Validation

- Every accepted record has a stable identifier, authority, acceptance date, context, decision,
  rationale, trade-offs, consequences, evidence, and review trigger.
- Reconstructed decisions cite current merged repository evidence and do not invent unavailable
  historical motives or alternatives.
- Proposed unresolved choices remain outside the accepted index.
- Supersession, deprecation, and historical sections remain available even when empty.
