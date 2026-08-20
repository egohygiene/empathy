# ADR-0001 — Empathy Owns the Golden Baseline, Not Specialist Implementations

- **Status:** Accepted for review
- **Date:** 2026-08-20
- **Decision owner:** `egohygiene/empathy`
- **Organization authority:** `egohygiene/hygiene`
- **Related issue:** #61

## Context

Empathy historically served several roles at once: baseline repository, experiment incubator, migration workspace, source of reusable tools, and integration testbed. As the Ego Hygiene organization matured, specialist capabilities gained durable repositories including Hygiene, Holon, Aether, Relay, Realm, Mantle, Egolint, Identity, Mindgarden, Beacon, Pace, and Observatory.

Leaving canonical implementations in Empathy after extraction creates ambiguous ownership, duplicated source, divergent fixes, and dependency directions that cannot be safely automated.

The organization also intends Sanctuary to become the permissive incubation boundary, while Empathy converges toward a strict baseline.

## Decision

Empathy is the **golden baseline and golden consumer** for the Ego Hygiene repository ecosystem.

Empathy owns:

1. the repository-level integration baseline;
2. selectable baseline/profile composition;
3. repository-specific configuration needed to consume organization capabilities;
4. conformance fixtures proving released capabilities interoperate;
5. temporary migration evidence required to drain historical Empathy source safely.

Empathy does **not** own the canonical reusable implementation of a capability after that capability has a durable specialist repository.

## Ownership rules

### Rule 1 — one durable source owner

Every reusable capability has exactly one canonical source owner. Empathy may contain a consumer configuration, fixture, generated projection, migration copy, or compatibility adapter, but those artifacts must not silently become a second canonical source.

### Rule 2 — released or pinned consumption

Where practical, Empathy consumes specialist capabilities through versioned releases, immutable revisions, digests, schemas, or generated projections. Mutable default-branch sibling source is not an accepted long-term integration mechanism.

### Rule 3 — repository-local intent remains local

Empathy retains repository-specific configuration and identity inputs. The existence of a reusable generator elsewhere does not move consumer-owned desired state out of Empathy.

### Rule 4 — extracted directories are transitional

Historical directories matching specialist repository names are migration evidence until they are reconciled. Their physical presence does not establish architecture ownership.

### Rule 5 — incubation leaves Empathy

New experimental work without a durable owner should not be added to Empathy as untracked staging. Route it through organization issue intake and, when available, Sanctuary. Existing `.staging` content follows the explicit migration/deletion gates in #59.

### Rule 6 — Empathy proves composition

When a capability becomes reusable, the specialist repository owns implementation and Empathy should become an early consumer that proves the contract works in a realistic repository.

## Specialist ownership map

| Concern | Durable owner | Empathy role |
| --- | --- | --- |
| Organization architecture and policy | Hygiene | consumer/conformance fixture |
| Repository materialization | Holon | golden source/consumer fixture |
| AI artifacts and projections | Aether | consumer |
| CI/CD mechanics | Relay | caller/consumer |
| Development environments | Realm | consumer |
| Shell/workstation behavior | Mantle | consumer |
| Lint semantics | Egolint | consumer + repository overlay |
| Identity generation/tokens | Identity | consumer-owned inputs + integration fixture |
| Knowledge garden | Mindgarden | golden consumer |
| Research-paper tooling | Beacon | consumer/example |
| Fleet convergence | Pace | managed target |
| Fleet visibility | Observatory | evidence producer |
| Incubation | Sanctuary | no ongoing general incubation in Empathy |

## Consequences

### Positive

- Ownership becomes reviewable and automatable.
- Specialist repositories can release independently.
- Empathy becomes smaller and more useful as a template/reference.
- Holon and Pace can reason about generated versus repository-owned files.
- Cross-repository migrations can preserve provenance without creating permanent source copies.

### Costs

- Transitional duplicates cannot be deleted until migration evidence is complete.
- Empathy needs explicit profile/version contracts rather than relying on colocated source.
- Some historically convenient local edits must move to the owning repository first.

## Rejected alternatives

### Keep Empathy as a permanent monorepo of all reusable capabilities

Rejected because it defeats independent ownership, release boundaries, and the organization's holonic repository architecture.

### Delete extracted directories immediately

Rejected because migration provenance, unique files, and unresolved staging dispositions may still exist. Deletion follows explicit evidence gates.

### Let every consumer fork specialist source

Rejected because fixes and policy would drift and Pace could not reason about compatibility safely.

## Validation

This decision is satisfied when:

- current architecture documents describe Empathy as baseline/golden consumer;
- new work routes to durable owners;
- issue #59 accounts for transitional source;
- baseline profiles reference specialist contracts rather than copied implementation;
- no specialist repository requires mutable Empathy source to function.
