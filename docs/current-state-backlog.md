# Empathy Current-State Backlog

This page is the compact execution view for Empathy after the 2026 foundation ownership reconciliation. It intentionally links durable GitHub issues rather than preserving stale pull-request references.

## Execution order

### Now — reconcile and drain historical ownership

- [#59 — Freeze, inventory, and drain `.staging` with deletion gates](https://github.com/egohygiene/empathy/issues/59)
  - Empathy-owned migration safety work.
  - No staged source is deleted without destination evidence and deletion review.
- [#61 — Reconcile foundation ownership and the 2026 audit backlog](https://github.com/egohygiene/empathy/issues/61)
  - Completed by the ownership audit, ADR, and this backlog once the associated PR is merged.

### Next — define the actual golden baseline

- [#62 — Define universal repository files and selectable capability profiles](https://github.com/egohygiene/empathy/issues/62)
  - **Implemented:** versioned artifact inventory, selectable profile catalog,
    golden Empathy manifest, safe preserve overrides, deterministic resolution,
    generated Hygiene context, and canonical EgoLint projection.
  - **Empathy owns:** baseline/profile composition and golden fixtures.
  - **Empathy does not own:** specialist implementation copied from sibling repositories.

### Then — prove optional integration profiles

- [#63 — Create universal editor, AI agent, and MCP integration profiles](https://github.com/egohygiene/empathy/issues/63)
  - **Blocked by:** Aether provider-neutral projections, #62, and Realm integration.
  - Consume Aether projections; do not maintain provider-canonical AI source in Empathy.

- [#64 — Build the universal website and documentation baseline](https://github.com/egohygiene/empathy/issues/64)
  - **Blocked by:** Holon site blueprints, Identity inputs, Relay publication, and the accepted OptiFlow reference.
  - Empathy owns the baseline composition and golden fixture, not every generator/deployer.

- [#65 — Integrate architecture and knowledge surfaces as a golden consumer](https://github.com/egohygiene/empathy/issues/65)
  - **Blocked by:** Hygiene repository-local context generation and Mindgarden's reusable contract.
  - Empathy remains the integration consumer, not the canonical knowledge implementation.

## Parallel epic — assurance baseline

- [#51 — Establish enterprise security, privacy, and compliance baseline](https://github.com/egohygiene/empathy/issues/51)
  - Treat as an integration epic, not a single monolithic Empathy implementation.
  - Split specialist implementation work to the repositories that own policy, automation, runtime infrastructure, posture aggregation, identity assets, and other durable capabilities.
  - Keep Empathy focused on secure defaults, reference composition, examples, conformance fixtures, and claim-language safety.

## Repository rule while this backlog is active

Before adding reusable source to Empathy, ask:

1. Is this part of the universal baseline/profile contract?
2. Is this repository-specific desired state or configuration?
3. Is this a golden-consumer fixture proving an external contract?
4. Is this temporary migration evidence with an explicit exit condition?

If the answer is **no** to all four, route the work to the durable capability owner or organization intake instead of expanding Empathy.

## Completion signal

Empathy's foundation stabilization is complete when:

- `.staging` has a finite, reviewable drain path;
- every reusable capability has one durable owner;
- baseline/profile inputs are machine-readable;
- Empathy consumes specialist capabilities through stable/pinned contracts;
- a disposable or generated repository can reproduce the golden baseline without depending on mutable specialist source inside Empathy.
