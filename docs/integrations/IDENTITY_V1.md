# Identity v1 consumer integration

Empathy is the calm, content-and-documentation-oriented pilot for Identity v1.
It inherits the pinned Ego Hygiene token layer and changes its primary accent
and semantic action alias. The reviewed mark, guidance, and profile selection
remain consumer-owned under [`.identity/`](../../.identity/).

## Immutable package boundary

The [`identity/` Git submodule](../../identity) and
[consumer lock](../../.config/identity/consumer-lock.json) pin the same reviewed
Identity commit. The [Identity workflow](../../.github/workflows/identity.yml)
validates the committed source at that revision, generates the complete package,
verifies its snapshot, and uploads the output as workflow evidence.

## Clean-checkout verification

Use Git, Task, Python 3, and Cargo. From the Empathy repository root, initialize
the pinned submodule and validate the committed source:

```bash
git submodule update --init --recursive "identity"
task identity:v1:check
```

Generate the disposable package, then verify that snapshot:

```bash
task identity:v1:generate
task identity:v1:verify
```

The verify task reports missing, stale, or modified output without rewriting
files. A clean checkout needs generation before snapshot verification.
`assets/identity/.identity-manifest.json` records the generated state, and
`assets/identity/packages/brand-kit/checksums.json` records the package checksums.
Keep disposable output out of source commits.

## Upgrade and rollback

1. Update the Git submodule and consumer lock together to a reviewed immutable
   Identity commit.
2. Check the source, generate the package, review the results, and verify the
   generated snapshot.
3. Commit reviewed changes to the consumer inputs, Git submodule, and lock.
   Attach applicable generated evidence to the review.

To roll back, restore the previous consumer inputs, submodule pin, and lock.
Refresh the pinned checkout and regenerate and verify the package from the
restored sources.

## Compatibility and diagnostics

The pinned revision validates profile IDs and versions in
`.identity/targets/profiles.json`. Identity reports stable diagnostics for an
invalid override, wrong layer digest, incompatible profile, source provenance
mismatch, or generated-state drift. Route schema and compiler changes to
[Identity](https://github.com/egohygiene/identity).
