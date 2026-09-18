# Layered gitignore contract

This is the **part 3 golden-root adoption** for [Empathy #82](https://github.com/egohygiene/empathy/issues/82).
The accepted baseline and composition model now drive Empathy's active root.
The [migration record](MIGRATION-03.md) reconciles all old rules and records the
consumer proof and remaining boundaries. The [iteration checkpoint](ITERATION-01.md) records
the process and next bounded step.

## Contract record

| Field           | Contract                                                                                    |
| --------------- | ------------------------------------------------------------------------------------------- |
| Purpose         | Keep disposable local state out of Git without hiding source or reviewed artifacts.         |
| Consumer path   | `.gitignore`; required and repository-owned in the existing foundation catalog.             |
| Applicability   | Universal baseline in every declared scope, selected profile overlays, and local rules.     |
| Canonical owner | Empathy owns baseline/profile sources; consumers own local additions.                       |
| Content model   | Selected overlays in order, verbatim local additions, then the universal baseline.          |
| Source identity | Foundation `1.1.0`, format `empathy.gitignore/v1`, source IDs/paths and SHA-256 hashes.     |
| Local variation | Narrow project rules and reviewed exceptions that retain baseline protections.              |
| Update behavior | Emit/check a deterministic JSON plan; planning never reads or writes consumer ignore files. |
| Validation      | Catalog/manifest validation, source integrity, repeatability, and actual Git behavior.      |
| Adoption        | Empathy's root matches its plan; Filament adoption remains pending.                         |

## Universal rule decisions

The [universal baseline](../../../foundation/ignore/universal.gitignore) has 27
active rules, including negations. It reserves reviewed OS/editor debris, local
environment patterns, the private `.secrets/` namespace, and `.cache/`, `.tmp/`,
`.venv/`, `__pycache__/`, and `node_modules/` directories at every depth.

- Keep shared `.vscode/` and `.idea/` configuration visible. Ignore only the
  named JetBrains user state covered by its
  [version-control guidance](https://intellij-support.jetbrains.com/hc/en-us/articles/206544839-How-to-manage-projects-under-Version-Control-Systems).
- Ignore `.env` and local variants. Allow `.env.example`, `.env.sample`,
  `.env.template`, and variants ending in those suffixes, including
  `.env.production.example`. Templates contain placeholders, never credentials.
  `.env.example.local` remains ignored, as do templates inside `.secrets/`.
- Preserve lockfiles, public certificates, binary fixtures, archives, patches,
  screenshots, snapshots, fixture logs, and reviewed reports by default.
- Keep ambiguous names such as `bin/`, `build/`, `dist/`, `out/`, `target/`,
  `vendor/`, and `coverage/` out of the universal layer. Profile rules need
  evidence of generated output and an explicit project scope.

The [historical audit](RULE_AUDIT.md) classifies the 176 old root rules.
The [migration fixture](../../../tests/fixtures/gitignore/empathy-migration.json)
reconciles every rule with evidence and actual Git behavior expectations.

## Selection and source identity

The existing `gitignore` artifact in `foundation/catalog.json` has `composition`
metadata. Empathy owns all registered sources. `universal` names the baseline;
`rust-build` selects the [Rust overlay](../../../foundation/ignore/rust.gitignore)
and requires the resolved `language-rust` profile. Source paths are Empathy
inputs, not new required consumer files. Other language profiles do not yet
have ignore overlays.

The optional manifest `gitignore` field declares every planned ignore file:

```json
{
  "gitignore": {
    "scopes": [
      { "root": ".", "overlays": [], "local_additions": "" },
      {
        "root": "apps/rust",
        "overlays": ["rust-build"],
        "local_additions": "# Owner: repository maintainer; reason: reviewed build note.\n!/target/\n/target/*\n!/target/README.md\n"
      }
    ]
  }
}
```

The root `.` must appear once. Roots are normalized repository-relative
directories, unique ignoring case; traversal, absolute paths, Git metadata,
glob characters, and ignore-file/directory collisions are rejected. Profiles
resolve through the existing dependency graph. Selecting `language-rust` alone
installs nothing: each project scope must explicitly select `rust-build`. Use
the Cargo workspace root when that workspace owns the build output. Empathy's
root scope follows its declared Cargo workspace; the
[migration record](MIGRATION-03.md) explains its local additions and imported
project boundaries.

Scopes sort by root. Overlay order within a scope is intentional and preserved.
Duplicate or unknown selections and overlays whose profiles are not selected
fail validation. Omitting `gitignore` remains a valid presence-only manifest;
requesting a plan without scopes fails.

Planning verifies every registered source's raw UTF-8 SHA-256, including
unselected overlays. Missing files, source paths escaping the supplied source
root, duplicate active rules, and unanchored overlay patterns fail. Each overlay
pattern must start with `/` or `!/`, relative to its selected scope. Canonical
fragments and local additions use LF; nonempty text ends in LF.

## Layering and exceptions

Empathy owns baseline/profile policy, consumers own local facts, Holon owns
materialization, EgoLint owns conformance semantics, Relay runs reusable checks,
and Pace owns reviewed fleet convergence.

Each planned file contains selected overlays in manifest order, repository-local
text verbatim, then the universal baseline. Local comments, blank lines, rule
order, and intentional repetitions survive unchanged. The baseline comes last
in **each declared scope**, so local `!.env`, `!/.secrets/`, or `!/node_modules/`
rules cannot undo those protections. Its template exceptions also take
precedence for traversable paths; templates must contain placeholders. Local
additions can override profile outputs but cannot customize the baseline's final
matches. Changes to that policy need review of the canonical source.

Git applies directory scope and pattern order. Later matching rules win at the
same level, while a closer `.gitignore` can override ancestor rules. Slashless
names can match at any depth; a leading slash anchors a rule to the ignore file's
directory. See [Git's documented semantics](https://git-scm.com/docs/gitignore).

For a reviewed file inside the Rust output directory, local additions can use:

```gitignore
!/target/
/target/*
!/target/README.md
```

The first line reopens the directory excluded by the overlay; the next two
ignore its contents and reinclude only the reviewed note. Simply appending
`!/target/README.md` after `/target/` does not work: Git cannot reinclude files
beneath an excluded parent. A global `!**/.gitkeep` has the same limitation.
Document the path, owner, and reason, and test the exception and adjacent output.

## Preservation, updates, and rollback

The plan records `status: plan-only`, generator, foundation version, repository,
resolved profiles, ordered layer owners/IDs/paths/hashes, local text hash, and
each proposed file's content and SHA-256. Catalog and resolved-manifest hashes
use sorted-key compact JSON (`ensure_ascii=False`, separators `,` and `:`, UTF-8,
no trailing newline). Fragment and content hashes cover exact UTF-8 bytes.
Consumers should pin an accepted Empathy commit as well as its contract version;
this part creates no release or downstream upgrade pin.

`.gitignore` stays required and repository-owned. A `preserve` override is carried
into the plan, not treated as permission to overwrite or bypass the baseline.
Planning never reads an existing consumer `.gitignore` and cannot infer which
lines are local. Adoption must review the existing file and represent retained
local rules explicitly in the manifest. Unknown existing text and edits must
be preserved or surfaced as a conflict by a future Holon materializer; this
module does not implement that merge engine.

For a source upgrade, change the reviewed fragment and catalog hash, then
regenerate the plan and inventory. A hash mismatch fails instead of accepting
drift. Keep local additions unless the maintainer explicitly reviews their
change. The plan diff exposes ordering and visibility changes before adoption.
Rollback restores the previous pinned catalog, matching resolver, manifest, and
fragments and regenerates the plan. Restoring an adopted consumer file requires
a reviewed materialization/revert, retaining intervening local edits; reverting
the plan alone does not revert an active file.

The EgoLint TOML is regenerated against a real source commit and advances with
foundation `1.1.0`. It still projects presence, ownership, executable flags, and
markers only. Ignore-content conformance belongs to EgoLint and is not implied
by the plan or presence check.

## Secret boundary and migration gate

Ignore rules do not remove already tracked files, prevent forced additions, or
detect secrets. Tests demonstrate that an unmanaged nested `!.env` can bypass a
root rule. Repeating the baseline protects declared scopes; it does not police
deeper files or arbitrary local patterns. A future EgoLint conformance check
must detect prohibited overrides; this composer does not provide
organization-wide enforcement.

Before replacing the active root, account for every current credential rule.
For `*.key`, keystores, certificates, `*.secrets.*`, and infrastructure state or
variables, identify the real private locations, add narrow profile/local rules,
and test them alongside public/fixture exceptions. Use `.secrets/` for deliberate
private local material; it does not cover secrets stored arbitrarily elsewhere.
Keep secret scanning separate. Do not drop existing protections merely because
an extension is absent from the universal baseline.

Migration must inspect newly exposed untracked paths without printing their
contents or staging them wholesale. An ignored file is never evidence that
deletion is safe. No cleanup is required by this contract.

## Validation

Run from the repository root:

```bash
python3 -m unittest discover \
  --start-directory tests \
  --pattern "test_*ignore*.py" \
  --verbose
python3 tools/foundation.py plan-gitignore \
  --manifest "foundation/empathy.manifest.json" \
  --source-root "." \
  --output "foundation/contracts/empathy.gitignore-plan.json"
python3 tools/foundation.py check-gitignore-plan \
  --manifest "foundation/empathy.manifest.json" \
  --source-root "." \
  --output "foundation/contracts/empathy.gitignore-plan.json"
ruff check \
  --config "egolint/.config/lint/python/ruff.toml" \
  "tools/foundation.py" "tools/foundation_ignore.py" \
  "tests/test_gitignore_baseline.py" "tests/test_foundation_ignore.py"
```

Use the explicit Ruff configuration to match MegaLinter; the root
`pyproject.toml` selects fewer rules. Inspect completed CI before handoff.
The harness installs baseline/composed content into temporary repositories and
uses real untracked fixtures with `git check-ignore --no-index`. Failures show
the winning rule. It isolates inherited Git configuration, templates, and global
excludes. Catalog, manifest, schemas, sources, and composer changes trigger the
automation test suite.

Composition fixtures prove repeatability and Git semantics. A separate golden
adoption test now proves the active root equals the plan and exercises the
[migration cases](MIGRATION-03.md), including existing nested-policy limits.
Keep #82 open until its full acceptance criteria are met. Filament follows the
accepted, immutable upstream contract with its own reviewed local selection.
