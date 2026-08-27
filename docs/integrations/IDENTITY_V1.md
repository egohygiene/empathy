# Identity v1 consumer integration

Empathy is the calm, content-and-documentation-oriented pilot for Identity v1.
It inherits the pinned Ego Hygiene token layer and changes only its primary
accent and the semantic action alias. The source mark, reviewed guidance, and
profile selection remain consumer-owned under [`.identity/`](../../.identity/).

## Immutable package boundary

The `identity/` Git submodule and `.config/identity/consumer-lock.json` pin the
same reviewed Identity commit. CI validates the v1 source with that revision,
then verifies the committed compiler manifest and generated package checksums.
No task follows a branch or mutable tag, and Empathy does not import Identity's
`src/` implementation.

## Normal check and regeneration

```bash
task identity:v1:check
task identity:v1:verify
```

The first command validates the source contract. The second command detects a
missing, stale, or modified generated file without writing anything. A reviewed
source or compatible Identity update is regenerated explicitly:

```bash
task identity:v1:generate
task identity:v1:verify
```

The compiler first plans every creation, replacement, removal, or drifted file;
it never repairs assets silently. `assets/identity/.identity-manifest.json` is
the exact generated-state record, while `packages/brand-kit/checksums.json` is
the portable package evidence.

## Upgrade and rollback

1. Select a reviewed immutable Identity commit and update the gitlink and
   consumer lock together.
2. Run `task identity:v1:check`, review the generated plan, and run
   `task identity:v1:generate`.
3. Commit the source change, generated manifest/package, gitlink, and lock in
   one consumer review.

Rollback restores the previous consumer commit (or the preceding gitlink,
lock, and generated projection set together), then runs `task identity:v1:verify`.
Canonical `.identity/` input is not edited or reconstructed as part of a
rollback; there is no manual asset surgery.

## Compatibility and diagnostics

Profile IDs and versions are declared in `.identity/targets/profiles.json` and
are checked against the pinned Identity revision. A rejected override, wrong
layer digest, incompatible profile version, source provenance mismatch, or
generated-state drift fails the task with a stable Identity diagnostic and a
recovery path. Schema additions and behavior changes belong in the versioned
Identity contracts, not in an Empathy-specific adapter.
