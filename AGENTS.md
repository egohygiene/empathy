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
