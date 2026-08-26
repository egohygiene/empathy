# Identity consumer integration

Empathy is the golden Identity consumer. The reusable Identity implementation is
owned by [`egohygiene/identity`](https://github.com/egohygiene/identity); Empathy
owns only its project intent under `.identity/`, generated outputs under
`assets/identity/`, and repository-local task/CI adapters.

## Immutable source contract

The `identity/` path is a Git submodule. Its exact commit is stored twice for
reviewability:

1. the repository gitlink at `identity`;
2. `.config/identity/consumer-lock.json`.

Both values must match. Normal validation never follows a branch or mutable tag.
The current reviewed pin is:

```text
repository: egohygiene/identity
revision:   73e7add02dbd11c38cf8a76d03d7ef2219e252ac
```

The lock also records the original Empathy extraction revision, preserving the
chain from incubation to canonical implementation to consumer integration.

## Initialize a checkout

Clone with submodules or initialize the existing checkout explicitly:

```bash
git submodule update --init --recursive "identity"
```

Then run the same integration gate used by repository tasks and CI:

```bash
task identity:check
```

The gate verifies the immutable pin before formatting, Clippy, tests, and
consumer validation. `task identity:plan` and `task identity:handoff` use the
same pinned CLI.

## Review an Identity update

Do not use `git submodule update --remote`; that follows mutable branch state.
Select an exact reviewed canonical commit instead:

```bash
reviewed_revision="<40-character-identity-commit>"

git -C "identity" fetch "origin" "${reviewed_revision}"
git -C "identity" checkout --detach "${reviewed_revision}"
```

Update `.config/identity/consumer-lock.json` to the same revision, then run:

```bash
task identity:check
task identity:plan
task identity:handoff
```

Commit the gitlink and lock together. A pull request is incomplete when only one
of them changes.

## Authority boundaries

| Surface | Owner | Update path |
| --- | --- | --- |
| Identity CLI, contracts, profiles, and reusable tests | `egohygiene/identity` | Canonical Identity pull request and immutable commit |
| `.identity/` project intent and approved sources | `egohygiene/empathy` | Empathy review with human authority |
| `assets/identity/` generated projections | Identity compiler, accepted by Empathy | Reproducible regeneration from pinned source and reviewed intent |
| Task and CI integration | `egohygiene/empathy` | Empathy repository review |

Canonical implementation fixes belong in Identity. Empathy must not patch or
reintroduce a second local implementation.

## Rollback

Revert the Empathy consumer-transition merge commit. Git restores the prior
incubated source tree and its adapters; `.identity/` project intent remains
untouched. After any pin-only update, rollback by restoring the previous gitlink
and consumer lock together, then run:

```bash
git submodule update --init --recursive "identity"
task identity:check
```

Do not delete or rewrite `.identity/` as part of implementation rollback.
