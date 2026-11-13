# Shared gitignore consumer qualification — 2026-11-13

This checkpoint supplies the accepted shared-owner proof for
[Empathy #92](https://github.com/egohygiene/empathy/issues/92), following
[the root migration](MIGRATION-03.md). The public
[receipt](data/shared-integration-20261113.json) records the exact inputs,
consumer/state hashes, native check results, and current nested-policy inventory.
The assessment source is Empathy `772efa7f66a3285dc70a14480249f386b471d798`.

Two disposable consumers completed the accepted **foundation 1.1** integration.
Neither the current foundation 2.0 upgrade nor whole-repository conformance is
implied. No active consumer, imported source, workflow, approval, or ignore rule
was changed by qualification.

## Exact accepted owners and representations

| Role | Immutable source |
| --- | --- |
| Empathy producer and foundation 1.1 catalog | `b44f798bb49259f9f48416b4ffebde1103e135c0` |
| Holon materialization CLI, accepted through PR #60 | `660b941f99618806fcadd589bcdae61c519f96e4` |
| EgoLint native semantic validator, accepted through PR #62 | `ec97ed8b3f1a4a2198aec03355600ea6c9caa1e1` |
| Filament's accepted manual pilot | `c3eb64b8087face7504e7571dc8396c19525649f` |

The golden fixture was recomposed with that Empathy producer and its golden
manifest. Its ignore bytes equal the current Empathy root exactly:
`75ccd106992da2dac355e64f8b77defb510fce7eeb96dcf626e5b39fdb315bed`.
The Filament fixture was recomposed from Holon's checked-in
`tests/fixtures/gitignore/filament/manifest.json`; its ignore bytes equal the
actual pilot commit:
`3637ea33004215037e745cf898f59e7c2a3195f8b66df5bae0921186ec731373`.
Each fixture also contained authored CRLF README bytes, checked for exact
preservation throughout the lifecycle. These are bounded representations,
not executions in either live consumer checkout.

## Observed lifecycle

Both fixtures completed the following public CLI sequence:

1. Recompose the selected manifest with `tools/foundation.py plan-gitignore`;
   compare the complete parsed composition with the accepted checked-in plan.
2. Create a request with the exact source revision, resolved profiles/scopes,
   canonical composition SHA, and explicit adoption of the existing file hash.
3. Run Holon `gitignore plan`, `check-plan`, and `apply` using the reviewed
   `plan_id`. Adoption preserves the ignore file and README bytes.
4. Generate a **fresh** identical plan and apply it. Both results report `noop`,
   preserving the exact state and file bytes. Keep the identical `adopt` list:
   clearing it changes reviewed request provenance and is not an unchanged replay.
5. Run the accepted native EgoLint command against that same representation.
6. Add the explicit local rule `/scratch-new/` to the manifest, recompose through
   Empathy, clear the completed adoption request, then plan/check/apply the
   update. Native validation passes again, and Holon `verify` passes.
7. Append an unreviewed ignore-file edit. Guarded rollback returns nonzero and
   retains the edit. Restore only the known disposable fixture bytes; rollback
   then restores the exact prior ignore file, state, and README.

All four native positive runs returned zero with `status=valid`; every check
passed and each diagnostic list was empty. Initial representations evaluated
128 behavior probes each; updated ones evaluated 129. The native executable was
built from the selected owner with locked dependencies and Cargo 1.97.1.
Its executable digest is retained in the receipt. The evaluation date was
2026-11-13. This does not certify every possible future pathname.

## Reproduction using the owner CLIs

Use separate clean checkouts at the four exact revisions above, Python 3.12,
Git, and the native EgoLint built from its selected source. Keep requests, plans,
and compositions outside the disposable target. Authenticate the Git heads
before starting; do not substitute current foundation 2.0 for the accepted source.

```sh
python3 -B "$EMPATHY_SOURCE/tools/foundation.py" \
  --catalog "$EMPATHY_SOURCE/foundation/catalog.json" plan-gitignore \
  --manifest "$MANIFEST" --source-root "$EMPATHY_SOURCE" --output "$COMPOSITION"
```

For the golden case, select `foundation/empathy.manifest.json` and compare with
`foundation/contracts/empathy.gitignore-plan.json` in the accepted Empathy source.
For Filament, select the manifest and composition in Holon's fixture directory.
Construct the closed request as specified by the pinned
[Holon CLI contract](https://github.com/egohygiene/holon/blob/660b941f99618806fcadd589bcdae61c519f96e4/docs/gitignore-materialization.md).
Copy the composition's exact content into the disposable `.gitignore` and bind
it through `adopt[].before_sha256`.

```sh
python3 -B "$HOLON_SOURCE/tools/holon_materialize.py" gitignore plan \
  --request "$REQUEST" --composition "$COMPOSITION" \
  --empathy-source "$EMPATHY_SOURCE" --target "$TARGET" --output "$PLAN"
python3 -B "$HOLON_SOURCE/tools/holon_materialize.py" gitignore check-plan \
  --request "$REQUEST" --composition "$COMPOSITION" \
  --empathy-source "$EMPATHY_SOURCE" --target "$TARGET" --plan "$PLAN"
python3 -B "$HOLON_SOURCE/tools/holon_materialize.py" gitignore apply \
  --request "$REQUEST" --composition "$COMPOSITION" \
  --empathy-source "$EMPATHY_SOURCE" --target "$TARGET" --plan "$PLAN" \
  --reviewed-plan-id "$PLAN_ID"
python3 -B "$HOLON_SOURCE/tools/holon_materialize.py" gitignore verify --target "$TARGET"
python3 -B "$HOLON_SOURCE/tools/holon_materialize.py" gitignore rollback \
  --target "$TARGET" --expected-state-sha256 "$CURRENT_STATE_SHA256"
```

For native validation, stage the accepted foundation catalog and fragments as
regular source artifacts inside the fixture, outside its report directory.
Use the pinned
[EgoLint policy contract](https://github.com/egohygiene/egolint/blob/ec97ed8b3f1a4a2198aec03355600ea6c9caa1e1/docs/repository-gitignore.md):
the policy binds that source, composition SHA, exact profiles/scopes/local text,
and explicit local-rule probes. The clean representations need no approval records.

```sh
"$EGOLINT" --workspace "$TARGET" gitignore \
  --policy gitignore-policy.toml --evaluation-date 2026-11-13
```

Inspect every native `checks` member as well as exit status and `status`.
Holon rollback prints human-readable output, not a JSON report.

## Current inherited-policy dispositions

The dated receipt inventories **16 nested policies plus the root**, with exact
policy-file digests. Thirteen inherited policies remain preserved and unassessed
by this checkpoint; preservation grants no semantic approval. The three known
deviations have these explicit dispositions:

| Current consumer path | Actual behavior and disposition |
| --- | --- |
| `.devcontainer/.gitignore` | `!.env` exposes matching untracked `.env` files; the existing tracked `.devcontainer/.env` remains tracked and visible independently. Empathy owns consumer reconciliation, coordinated with Realm's environment boundary. Defer its tracked-file/private-material disposition to that review; no payload inspection or invented approval occurs here. Ignore rules alone cannot protect a tracked file. |
| `holon/packs/react-vite/template/.gitignore` | The old imported template exposes `.env.sample.local` and hides valid `.env.production.sample` suffix templates, among other broad rules. The accepted Holon source's `blueprints/react-vite/files/.gitignore` has only build rules and no prefix-style environment exemptions. Consume the owner source through reviewed source migration; do not silently patch the preserved template copy. |
| `egolint/.gitignore` | Unanchored `target` hides `egolint/examples/target/source.rs`. The accepted EgoLint source already uses `/target/`. Consume that owner correction through reviewed source adoption, preserving other imported differences. |

These are **deferred source-adoption/reconciliation work**, not approved
exceptions or a conformant consumer policy. Empathy #59's ownership/migration
boundary remains relevant. No blanket requirement to finish every #79 or #110
activity is imposed on the accepted shared file-level proof. Mantle's case is
retired by its [actual source extraction](../../migration/MANTLE.md); the current
root still ignores `mantle/.env.example.local`.

A separate disposable negative fixture copied exactly those three policies,
with authored nonsecret placeholders and one fixture-only tracked `.env`.
Native EgoLint returned `invalid`/exit 1: effective behavior failed, tracked-file
protection failed, and nested-policy ownership evidence was incomplete. Source,
composition, presence, content, and bounded inventory coverage still passed.
The selected winning-rule observations are in the receipt. No approval URL,
expiry, tracked-file exception, or deletion authority was synthesized. Complete
inventory coverage in that fixture does not certify all Empathy content.

## Current catalog boundary and remaining acceptance

Current foundation 2.0 retains byte-identical root, universal, and Rust ignore
content, but has a different accepted catalog identity. Supplying the current
catalog to the pinned Holon CLI fails before creating a plan:
`Empathy catalog digest mismatch; supply the accepted pinned source`.
The accepted EgoLint profile likewise names the 1.1 source/catalog explicitly.
This is an observed **future owner-upgrade boundary**, not a prerequisite added
to the successful 1.1 proof. No pin or compatibility record was rewritten.

The two historical unchecked #82 criteria remain distinct:

- Environment behavior: clean accepted compositions pass native validation;
  current inherited deviations remain explicit and unapproved as listed above.
- Complete repository validation: the 19 focused Git behavior tests pass here;
  this is not a complete-suite or holistic-profile pass. The current baseline
  validation work (#109), canonical adoption plan (#110), and existing
  catalog/runtime selection constraints retain their own evidence and owners.
  Direct MegaLinter bootstrap repair is outside this qualification.

The [stage ledger](../../../ROADMAP.md) records the bounded shared proof while
keeping full foundation/release states unchanged. #92 remains open pending
accepted disposition of its three inherited deviations. This checkpoint does
not establish fleet rollout, organization-wide conformance, full-baseline
release, or human acceptance of the deferred exceptions.
