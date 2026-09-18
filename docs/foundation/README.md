# Empathy repository foundation

Empathy owns the smallest coherent golden repository baseline and the
composition of selectable capability profiles. It does not own Holon's
materialization engine or the reusable implementations selected by those
profiles.

## Contract surfaces

- `foundation/catalog.json` inventories canonical repository artifacts,
  optional surfaces, profile-specific overlays, ownership, safe overrides, and
  generated outputs.
- `foundation/empathy.manifest.json` is the golden-consumer selection and
  repository-owned configuration.
- `schemas/repository-foundation-catalog.v1.schema.json` and
  `schemas/repository-foundation-manifest.v1.schema.json` define the authoring
  contracts.
- `docs/foundation/INVENTORY.md` is the deterministic human-readable
  inventory.
- `foundation/contracts/empathy.repository-contract.toml` is the canonical,
  offline EgoLint presence/ownership projection.
- `foundation/contracts/empathy.gitignore-plan.json` is a deterministic proposal
  with source and output hashes, not active-root adoption evidence.

## Gitignore contract under review

The [layered gitignore contract](gitignore/README.md) registers the universal
baseline and a Rust overlay in foundation `1.1.0`. The manifest explicitly
selects project roots, overlays, and repository-owned local additions. Planning
checks source hashes and emits JSON; Holon retains filesystem materialization
ownership. This is part 2 of
[issue #82](https://github.com/egohygiene/empathy/issues/82).
Golden-root migration and Filament adoption remain subsequent work.

The v1 schema filenames retain their major version; catalog/schema versions and
manifest references advance together to `1.1.0`. The resolver requires an exact
version match. Existing `1.0.0` consumers keep their pinned input and resolver
until explicitly upgraded. The selected Holon contract stays at `1.0.0`.

## Composition boundary

Profiles vary independently across core, governance, quality, risk, release,
publication, agent, language, and repository-class dimensions. Profile
dependencies resolve transitively in stable order. Conflicts, unknown profiles,
duplicate paths, generated artifacts without markers, unsafe paths, and
attempts to preserve generated content fail closed.

An override may only mark a selected non-generated artifact as `preserve`.
That retains repository ownership without changing the universal path or
weakening the existence requirement. Generated paths remain owned by their
source contract and cannot be silently overridden.

## Idempotence

Empathy proves composition idempotence rather than implementing Holon's
filesystem mutation engine. Identical catalog and manifest inputs resolve to
byte-identical JSON and EgoLint TOML. Re-resolving the checked-in Empathy
manifest produces no diff. Holon may later consume this released catalog when
planning and materializing repositories; Pace may propose reviewed upgrades.
The EgoLint projection still describes paths, ownership, executable flags, and
markers; its version bump does not introduce ignore-content conformance.

## Validation

Hygiene-owned generated context is validated by its pinned generator and
marker contract; consumer formatting tools do not rewrite that canonical
projection.

```bash
python3 tools/foundation.py validate-catalog
python3 tools/foundation.py validate-manifest \
  --manifest "foundation/empathy.manifest.json"
python3 tools/foundation.py check-inventory \
  --output "docs/foundation/INVENTORY.md"
python3 tools/foundation.py check-gitignore-plan \
  --manifest "foundation/empathy.manifest.json" \
  --source-root "." \
  --output "foundation/contracts/empathy.gitignore-plan.json"
python3 tools/foundation.py check-contract \
  --manifest "foundation/empathy.manifest.json" \
  --source-revision "<40-character-empathy-commit>" \
  --output "foundation/contracts/empathy.repository-contract.toml"
```
