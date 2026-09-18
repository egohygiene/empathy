# Golden-root gitignore migration

This is part 3 of [Empathy #82](https://github.com/egohygiene/empathy/issues/82).
[PR #87](https://github.com/egohygiene/empathy/pull/87) merged on 2026-09-18 as
`8e1b748c5b72c0036763e1528f1ffe14cecd99df`, accepting the foundation `1.1.0`
composition model. This part adopts that model at Empathy's root. The PR base
includes the subsequent report-only refreshes through
`3e0b740a423b722790b3fb9a07f35407864b9b63`.

## Source and scope

The old root still matched the historical [176-rule audit](RULE_AUDIT.md), blob
`2dee7a36db8b554ee7b959da5c38c62636204980`, at the verified merge. The new root
has **80 active rules**: one selected Rust rule, 52 Empathy-local rules, and the
27-rule universal baseline last. No duplicate active rules remain.

[`foundation/empathy.manifest.json`](../../../foundation/empathy.manifest.json)
is the authoring source for Empathy's local additions. The checked-in
[composition plan](../../../foundation/contracts/empathy.gitignore-plan.json)
is regenerated, and its proposed root content is explicitly adopted as
[`.gitignore`](../../../.gitignore). A golden integration test compares exact
bytes. The composer still only writes a JSON plan; it does not become a Holon
materialization engine. Its file header now describes composed rules so it
remains accurate before and after adoption.

Foundation schema/catalog versions remain `1.1.0`: selection facts and consumer
adoption changed, not the authoring format or universal/profile rules. The
catalog inventory and EgoLint presence/ownership projection resolve unchanged.
The plan remains `plan-only` because planning does not inspect a consumer;
the separate golden test establishes this repository's adoption evidence.

## Complete reconciliation

The [migration fixture](../../../tests/fixtures/gitignore/empathy-migration.json)
accounts for **all 176 old rules exactly once**, in 39 disposition groups. Each
group records its decision, repository evidence, and actual ignored/visible
path examples. The tests compare this inventory with the historical audit and
exercise all **269 path expectations** with Git. Test repositories include the
17 existing nested ignore files so their precedence is represented honestly.

| Concern                            | Adopted disposition and evidence                                                                                                                                                                                                                                                 |
| ---------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Universal clutter and environments | Retain the accepted baseline, its precise template suffixes, and `.secrets/` at every depth.                                                                                                                                                                                     |
| Editors and reviewed fixtures      | Shared VS Code/JetBrains settings, patch/backup files, public certificates, archives, wheels, screenshots, and snapshots are visible outside inherited project exclusions.                                                                                                       |
| Scratch and arbitrary output names | Disposable data uses `.tmp/` and `.cache/`. `temp.md`, `temp.txt`, generic `build/`, `dist/`, `out/`, `bin/`, `obj/`, `vendor/`, and reviewed coverage stay visible.                                                                                                             |
| Quality reports                    | Retain all ten existing root rules and curated exceptions from `.reports/README.md`. Trusted snapshot publication retains its separate force-add contract.                                                                                                                       |
| Repository intelligence            | Retain `/docs/generated/`, the explicit output default in `.github/workflows/repository-intelligence.yml`.                                                                                                                                                                       |
| Mindgarden/Obsidian                | Scope private `.garden.local/`, generated `.garden/.index/`, plugins, and workspace layouts to the selected root vault described by `.garden/garden.yaml` and `.obsidian/README.md`.                                                                                             |
| Rust                               | Select `/target/` at the root Cargo workspace; local paths protect `beacon/target/` and `.staging/devenvironment/realm/target/`. EgoLint already has a nested Cargo ignore policy.                                                                                               |
| Python                             | Retain the observed root Ruff cache and the configured pytest project's cache. Canonical tooling uses `.cache/`; baseline rules cover modern bytecode and `.venv/`. Imported project policies retain their own packaging/tool state.                                             |
| Raku and Dart                      | Scope `.precomp/` to the Raku fixture, and `.dart_tool/` plus `.packages` to the Dart analyzer fixture.                                                                                                                                                                          |
| .NET                               | Scope `bin/` and `obj/` to the imported `winmd-api-search/scripts/cache-generator/CacheGenerator.csproj` directory. Mantle CLI/test source needs no compensating negations.                                                                                                      |
| Node/framework builds              | Root `package.json` has `dist` export declarations but no build script; root npm tasks cache in `.cache/npm`. Existing Holon/API nested policies own their output. Unselected frameworks and Yarn Zero-Install fixtures remain trackable.                                        |
| TeX                                | The staged paper's `.latexmkrc` writes to `.cache/aux` and `.cache/out`. Existing imported TeX ignores remain local. Reviewed bibliography and output fixtures elsewhere stay visible.                                                                                           |
| Unselected ecosystems              | No tracked Gradle/Android or Xcode project selects an application build; no root publication, Pulumi, Serverless, or SAM project is selected. Their old global patterns are removed rather than treated as proof of applicability. Future projects must declare their own scope. |

The Cargo root is evidence of its declared output ownership, not successful
compilation: its existing `tests/fixtures/clippy` member is absent from the root
checkout (the fixture lives under `egolint/`). That pre-existing build wiring is
outside this ignore migration. The fixtures prove Git behavior, not tool builds.

## Private-material replacements

These are consumer-owned storage rules, not a claim that an extension reveals
whether a file contains secrets.

- The imported Apache configuration mounts `cert.key` from its certificate tree.
  `/.staging/devenvironment/containers/services/apache/certs/**/*.key` protects
  that existing private namespace, including local CA keys. Public `.crt` and
  `.pem` certificates remain visible, as do reviewed key/keystore fixtures
  elsewhere.
- The three Terraform fixture roots are `egolint/tests/fixtures/kics/terraform`,
  `egolint/tests/fixtures/tflint`, and
  `egolint/tests/fixtures/negative/terraform-fmt`. Their `.terraform/`, default
  state and state-lock names, plans, and automatically loaded variable files are
  ignored. Each root is tested. Reviewed variable/state examples outside those
  names and scopes remain visible.
- There is no other discovered private keystore or `local.properties` producer.
  The imported IDE's `idea64.vmoptions` writes heap dumps to the user's `.cache`
  outside the repository. Private keys, keystores, arbitrary secrets files,
  nondefault private infrastructure files, property files, and captured dumps
  stored in the checkout must use `.secrets/` (or an explicitly documented
  private scope). Disposable diagnostics may use `.cache/`. Tests exercise the
  formerly protected extensions inside those namespaces and public fixtures
  outside them.
- The selected root `.garden.local/` remains a private overlay. Local `.env`
  protections and exact template suffixes retain the accepted baseline policy;
  example files must contain placeholders.

This deliberately removes the assumption that an arbitrary `*.key`, `*.tfvars`,
or `*.hprof` anywhere in a repository is either safe to publish or necessarily
private. Existing checkouts must inspect newly visible paths before upgrading.
Secret scanning remains separate, and ignored content must never be assumed
safe to delete. This PR reads no private file contents and removes no files.

## Nested-policy boundary

This part changes the root and its composition inputs. Existing imported nested
ignore policies remain visible in the evidence and retain their current
ownership; the root cannot overrule them.

Measured pre-existing exceptions include `.devcontainer/.gitignore` allowing its
tracked `.env`, Mantle and the Holon React template allowing prefix-style
`.env.example.*`/`.env.sample.*` variants, and EgoLint's unanchored `target` rule
hiding target-named source within its subtree. A test reproduces these limits
rather than reporting whole-repository content conformance. Fresh Filament
adoption must select its own local rules and must not copy these imported
policies. Reconciliation of inherited content and reusable enforcement stays
with the owning contract and EgoLint; Holon retains merging/materialization.

## Working-copy inspection

Before replacing the root, the path-only inspection found 62 ignored untracked
files in this agent checkout, all in cache/environment/bytecode locations. None
matched the old private-key/keystore/state/variable/heap-dump file patterns.
Rechecking the same paths after replacement found **zero newly visible files**.
No ignored untracked payload was read, staged, removed, or migrated. This observation is
specific to this checkout and does not certify another developer's filesystem.

During adoption in another checkout, record ignored/untracked paths before the
change, re-evaluate those paths afterward with Git, and inspect the names of
anything newly visible before staging selected files. Keep private payloads out
of logs. Restore the previous root and matching manifest/plan to roll back this
consumer change; preserve intervening local edits for explicit review.

## Validation and next action

The migration proof uses isolated Git configuration and real untracked files.
It verifies the byte-identical golden root, complete historical disposition,
source evidence paths, duplicate absence, ignored/visible behavior, and the
existing nested-policy limits. The existing quality-policy test now uses the
reserved scratch namespace and expects ordinary temp-named source to be visible.

Run the normal repository tests and the CI-configured Ruff checks before
handoff. Inspect completed PR CI and keep existing failures separate. Exact
commands/results belong in the linked PR and the owning issue's checkpoint.
The full MegaLinter snapshot published after #87 also exposes typing/import
resolution and assertion-security findings in the earlier foundation code.
A passing fast PR profile does not prove the full profile passes; reconcile
that debt before claiming complete #82 validation.

After maintainer review and merge, verify this adoption and reconcile the
remaining #82 acceptance items, including the existing CI failures and the
recorded content-conformance boundary. Then prepare the accepted, pinned
Filament pilot and any necessary owner-specific integration follow-ups. This
part does not close #82 or the master epic, and does not advance `EMP-Q04` to
complete.
