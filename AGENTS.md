# Repository agent context

Before architecture-changing work in this repository:

1. Read [`docs/ecosystem/CONTEXT.md`](docs/ecosystem/CONTEXT.md).
2. Read [`ARCHITECTURE.md`](ARCHITECTURE.md).
3. Read the relevant record under [`docs/decisions/`](docs/decisions/).
4. Preserve the ownership boundaries in
   [`docs/decisions/ADR-0001-foundation-ownership.md`](docs/decisions/ADR-0001-foundation-ownership.md).

Empathy owns the golden repository baseline, selectable profile composition,
and integration evidence. It does not absorb reusable implementations owned by
Hygiene, Holon, Aether, Relay, Realm, Mantle, EgoLint, Identity, Mindgarden,
Beacon, Pace, Observatory, or product repositories.

Generated files identify their source and generator. Change their canonical
input or regenerate them; do not silently edit generated ownership fields.

Before changing Repository Intelligence or Pages publication, read
[`docs/integrations/REPOSITORY_INTELLIGENCE.md`](docs/integrations/REPOSITORY_INTELLIGENCE.md).
Preserve the producer refresh and public-review boundaries, and verify actual
provider job scheduling, including skipped ancestors and explicit prerequisite
results. A green workflow does not prove that deployment or live verification
ran. Scope repeatability claims to declared inputs and checkout context; the
portable checkout-name follow-up is tracked in Relay #109.
For Python changes, run Ruff against `egolint/.config/lint/python/ruff.toml`,
the canonical policy used by MegaLinter; the root Python defaults are narrower.
The PR fast profile and focused checks do not establish full-profile readiness.
Before declaring a change ready, run the canonical holistic profile on the exact
review head, resolve introduced gating findings, and review warning-only
diagnostics. Include Mypy, Bandit, Secretlint, and Lychee in that review. Record
unrelated baseline failures separately; repository lint debt does not make a new
finding pre-existing. Follow the publication
document's feature-branch procedure to obtain holistic evidence without publishing
report snapshots.

Use reference-only issue links in implementation PRs (`Refs #<issue-number>`
and an explicit parent reference). Avoid automatic issue-closing keywords, including
negated examples. Change acceptance issue state explicitly after the required
post-merge deployment evidence is recorded.
