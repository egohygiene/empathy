# Empathy Foundation Ownership Audit — 2026-08-20

## Purpose

This audit reconciles Empathy's historical foundation/incubator role with the current Ego Hygiene repository architecture. It is intentionally a current-state control document rather than a historical narrative.

Empathy is converging on a **strict golden baseline and integration consumer**. It may prove that reusable capabilities work together, but it must not remain the canonical source for specialist implementations that now have durable repositories.

## Status vocabulary

- **delivered** — the intended outcome already exists in the current architecture or repository state.
- **extracted** — the capability now has a specialist repository; Empathy may consume it but does not own its reusable implementation.
- **superseded** — an earlier Empathy-local direction has been replaced by a newer architecture decision.
- **blocked** — useful work remains but an upstream contract or repository must land first.
- **still-owned** — Empathy remains the correct repository for the remaining work.
- **draining** — temporary source remains in Empathy but has an explicit exit path.

## Current ownership map

| Capability / historical audit concern                                          | Current state                                                   | Durable owner                                                            | Empathy responsibility now                                                                                                                    |
| ------------------------------------------------------------------------------ | --------------------------------------------------------------- | ------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------- |
| Universal repository baseline                                                  | still-owned                                                     | Empathy                                                                  | Define and prove the smallest coherent golden baseline and selectable profiles.                                                               |
| Organization rules, ontology, repository catalog, dependency policy            | extracted                                                       | Hygiene                                                                  | Consume accepted organization contracts; do not redefine them locally.                                                                        |
| Repository/template materialization                                            | extracted                                                       | Holon                                                                    | Act as the golden source/consumer used to validate materialization and upgrades.                                                              |
| AI specifications, skills, prompts, instructions, agents, provider projections | extracted                                                       | Aether                                                                   | Consume pinned projections and prove integration; remove duplicated canonical AI source from Empathy as migration completes.                  |
| Lint semantics, rule packs, SARIF/quality policy                               | extracted                                                       | Egolint                                                                  | Consume released Egolint behavior; keep only Empathy-specific configuration/fixtures.                                                         |
| Reusable GitHub Actions and CI/CD mechanics                                    | extracted                                                       | Relay                                                                    | Consume versioned workflows/actions; retain only repository-specific callers/configuration.                                                   |
| Devcontainers, development images, reusable environment profiles               | extracted                                                       | Realm                                                                    | Consume released Realm environments; retain only repository-specific environment intent.                                                      |
| Portable shell/workstation behavior                                            | extracted                                                       | Mantle                                                                   | Consume pinned Mantle releases; do not carry the canonical shell implementation.                                                              |
| Product identity generation and design-token contract                          | extracted                                                       | Identity                                                                 | Keep `.identity` as consumer-owned input/configuration; reusable generation belongs in Identity.                                              |
| Knowledge garden implementation                                                | extracted                                                       | Mindgarden                                                               | Use Empathy as a golden consumer/integration fixture; Mindgarden owns the reusable knowledge system.                                          |
| Research-paper/template tooling                                                | extracted                                                       | Beacon                                                                   | Empathy may host migration evidence/examples until drained; Beacon owns reusable paper tooling.                                               |
| Fleet synchronization/convergence                                              | extracted                                                       | Pace                                                                     | Expose baseline/version evidence that Pace can reconcile; Empathy does not push fleet changes itself.                                         |
| Organization visibility/health                                                 | extracted                                                       | Observatory                                                              | Emit evidence; Observatory aggregates and presents organization state.                                                                        |
| Experiment/incubation workspace                                                | superseded                                                      | Sanctuary (proposed organization repository)                             | Empathy is no longer the general-purpose incubator. Experimental work should graduate out of `.staging` or route to Sanctuary once available. |
| `.staging` contents                                                            | draining                                                        | Mixed, according to ledger                                               | Preserve provenance and safety while issue #59 drains each migration unit; no new unrecorded intake.                                          |
| Assurance/security/privacy baseline                                            | still-owned as integration baseline; specialist ownership split | Empathy + Hygiene/Aether/Relay/Realm/Observatory/Identity                | Prove safe baseline composition and reference behavior without claiming all policy/automation/deployment/visibility ownership.                |
| Website/docs baseline                                                          | blocked                                                         | Empathy baseline, Holon generation, Identity branding, Relay publication | Define the reusable baseline only after required upstream contracts are ready.                                                                |

## Current issue reconciliation

### #51 — enterprise assurance baseline

**State:** still-owned as an Empathy integration epic, but its sub-capabilities have specialist owners.

The issue should not evolve into a monolithic compliance platform inside Empathy. Empathy should retain the reference composition, conformance fixtures, safe defaults, and deployment-neutral examples while canonical policy vocabulary, CI evidence, runtime/deployment controls, posture aggregation, and identity assets flow to their durable owners.

### #59 — drain `.staging`

**State:** draining and still-owned until migration evidence is complete.

This is the controlled exit path for historical incubation content. It must remain non-destructive until destination evidence and deletion gates pass.

### #61 — foundation ownership reconciliation

**State:** delivered by this audit, the ownership ADR, and the compact backlog in this PR once reviewed and merged.

### #62 — universal repository files and profiles

**State:** implemented by the versioned foundation catalog, golden Empathy
manifest, deterministic inventory and resolution checks, generated Hygiene
context, and canonical EgoLint repository-contract projection. Holon retains
materialization ownership; Empathy owns the baseline meaning and fixture.

### #63 — editor/AI/MCP profiles

**State:** blocked by Aether projections, Empathy profiles, and Realm integration. Empathy should prove selectable consumption rather than maintain provider-canonical copies.

### #64 — website/docs baseline

**State:** blocked by Holon, Identity, Relay, and the accepted OptiFlow reference implementation. Empathy owns the baseline composition, not all generators or deployment mechanics.

### #65 — architecture/knowledge golden consumer

**State:** blocked by Hygiene local-context generation and Mindgarden's reusable contract. Empathy remains the correct integration consumer.

## Extracted source still visible in Empathy

The presence of directories such as `mantle/`, `egolint/`, `holon/`, `beacon/`, `mindgarden/`, staged AI material, or related migration remnants does **not** imply canonical ownership. Until issue #59 and related migration work remove or archive them, they are transitional evidence and must not be used as mutable cross-repository source dependencies.

## Baseline definition after reconciliation

Empathy owns four things:

1. **Baseline contract** — what a coherent Ego Hygiene repository looks like at the integration boundary.
2. **Profile composition** — which universal and selectable capability contracts are combined for a repository class.
3. **Golden-consumer evidence** — fixtures/tests proving released specialist capabilities interoperate.
4. **Migration evidence** — temporary, auditable proof needed to drain historical Empathy-owned experiments without losing work.

Everything else should have a durable specialist owner or an explicit unresolved routing state.

## Exit conditions for the foundation cleanup

Empathy is considered reconciled when:

- no specialist repository depends on mutable source inside Empathy;
- no directory name alone is treated as proof of canonical ownership;
- `.staging` is fully covered by the migration ledger and eventually drained through deletion gates;
- baseline/profile contracts are explicit and machine-readable;
- specialist capabilities are consumed by pinned/versioned contracts;
- Empathy can be materialized/validated as the organization's golden baseline without also acting as the implementation monorepo.

## Follow-up ordering

1. Complete #59 staging coverage/drain controls.
2. Merge and release the #62 universal baseline/profile contract.
3. Layer #63, #64, and #65 only when their declared dependencies are satisfied.
4. Split #51 into bounded specialist implementation issues as its architecture is exercised; keep Empathy focused on integration/conformance.
