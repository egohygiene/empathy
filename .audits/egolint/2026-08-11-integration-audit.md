# Egolint Monorepo Integration Audit

**Date:** 2026-08-11

**Scope:** Empathy root plus the imported `egolint/` subsystem

**Outcome:** Integrated with follow-up work explicitly recorded

## Executive summary

Egolint is now an encapsulated quality subsystem rather than a second repository
laid inside Empathy. The monorepo root owns orchestration and GitHub Actions;
`egolint/` owns linter rules, scanner configuration, fixtures, dependencies,
the MegaLinter wrapper, and the Taskfile implementation.

The root MegaLinter profile extends Egolint's complete policy and selects a
12-linter universal baseline for routine pull requests. The holistic profile is
preserved intact and remains available through `task lint:holistic`. No imported
linter was removed merely to make the baseline smaller.

Disposable output now belongs under `.reports/`. Durable analysis, remediation
state, and architectural decisions belong under `.audits/`.

## Ownership and execution model

| Concern                      | Canonical owner                 | Root integration                     |
| ---------------------------- | ------------------------------- | ------------------------------------ |
| Complete MegaLinter policy   | `egolint/.mega-linter.yml`      | `.mega-linter.yml` extends it        |
| Routine MegaLinter selection | Root `.mega-linter.yml`         | 12 universal linters                 |
| Local lint commands          | `egolint/tasks/lint.yml`        | Imported by root `Taskfile.yml`      |
| Container execution          | `egolint/scripts/megalinter.sh` | Invoked through root tasks           |
| Linter and scanner rules     | `egolint/.config/`              | Referenced by root CI                |
| GitHub Actions               | Root `.github/workflows/`       | No nested workflow tree              |
| Disposable output            | Root `.reports/`                | Ignored and uploaded as CI artifacts |
| Durable findings             | Root `.audits/`                 | Tracked in Git                       |

The routine profile enables:

- Actionlint;
- Bash executable-bit, ShellCheck, and shfmt checks;
- EditorConfig validation;
- JSON syntax and Prettier checks;
- Markdownlint;
- Ruff;
- Gitleaks;
- YAML Prettier and yamllint checks.

The routine profile disables direct GitHub comments and statuses inherited from
the holistic policy. Workflow summaries, SARIF, and uploaded artifacts provide
feedback without expanding ordinary pull-request permissions.

## Promoted staging material

The six imported `egolint/.staging/` artifacts were resolved as follows:

| Staged artifact         | Resolution                                                                       |
| ----------------------- | -------------------------------------------------------------------------------- |
| Actionlint policy       | Consolidated at `egolint/.config/lint/actions/actionlint.yml`                    |
| Commitlint config       | Consolidated into an ESM universal policy plus a preserved optional emoji policy |
| Commitlint workflow     | Merged into the root commitlint workflow with an explicit Egolint config path    |
| MegaLinter workflow     | Merged into the root workflow with summary, SARIF, and `.reports/` artifacts     |
| MegaLinter fix workflow | Merged into the root manual workflow with scoped fix input and review patch      |
| Remediation checklist   | Promoted to `.audits/egolint/megalinter-remediation-checklist.md`                |

`egolint/.staging/` is empty after promotion.

## Configuration repairs

### Pre-commit

The imported `.pre-commit-config.yaml` contained three YAML documents and
multiple historical repository profiles concatenated into one file. Duplicate
top-level keys meant there was no single dependable policy.

It is now one canonical document with current filesystem checks, Gitleaks,
Ruff, notebook checks, Biome, Markdownlint, mdformat, ShellCheck, Hadolint,
Bashate, schema checks, spelling checks, Commitlint, and REUSE validation.

Capabilities from the historical documents that were not activated are kept in
this deferred register:

- `detect-secrets` requires a reviewed baseline before activation;
- `addlicense` requires a single approved license-header policy;
- a MegaLinter pre-commit hook duplicates the root Taskfile contract and is too
  expensive for the default commit path;
- Black and isort hooks conflict with Ruff's current formatting ownership;
- local LaTeX and metadata hooks referenced scripts that were not imported.

The corresponding linter configurations and dependencies were not discarded.

### Commit messages

The root workflow now uses
`egolint/.config/lint/commits/commitlint.config.mjs`, which is compatible with
the v6 Commitlint GitHub action's ESM configuration requirement. Its type list
is the union of the staged conventional types and the imported historical type
catalog. The former emoji-required policy remains available as
`commitlint.emoji.config.cjs` without making emoji mandatory in CI.

### Paths and generated output

Nested rule paths were rebased for the monorepo, including MegaLinter rule
directories, CSpell dictionaries and cache, security scanner output, native
Taskfile tools, and CI artifacts. Active generated output uses `.reports/`.
Legacy `reports/` ignores remain only as a migration safeguard.

The root formatter task now uses Egolint's Prettier configuration. Generated
lockfiles, Clang's own formatter policy, and editor workspace metadata are
excluded from Prettier ownership.

## Dependency state

Existing package and Python dependency declarations were preserved. Missing
runtime dependencies referenced by the imported configs were added.

Node additions cover Commitlint types, CSpell, HTMLHint, Markdown link checks,
Markdownlint CLI 2, Groovy and package metadata linting, Pyright, the complete
Remark rule set referenced by `.remarkrc.json`, and Secretlint. MegaLinter and
pnpm were aligned to v10.0.0 and v11.21.0 respectively.

Python additions cover Ansible Lint, Black, CloudFormation Lint, Flake8, isort,
rstcheck, and Checkov. Black, Flake8, and isort remain available for compatibility
and targeted comparison even though the holistic MegaLinter policy selects Ruff
as the primary Python owner.

The new `egolint/pnpm-lock.yaml` contains 4,028 package records and passed pnpm's
frozen lockfile and supply-chain policy verification. A Poetry lockfile was not
invented because the imported project did not contain one and the complete
Python environment was not resolved in this integration pass.

## Repository hygiene

The following generated or redundant files were removed:

- `egolint/.editorconfig copy`, which was byte-identical to the canonical file;
- a tracked Raku `.precomp/` cache, including its compiled binary and lock data.

The Raku source fixture remains. `.precomp/` is now ignored so regeneration does
not dirty the repository. All removed material remains recoverable from Git
history.

## Validation evidence

| Validation                          | Result                            |
| ----------------------------------- | --------------------------------- |
| Root unit tests                     | 9 passed                          |
| Egolint wrapper unit tests          | 5 passed                          |
| Automation policy                   | 9 workflows and 10 actions passed |
| YAML syntax and duplicate keys      | 147 files passed                  |
| JSON syntax                         | 31 files passed                   |
| TOML syntax                         | 16 files passed                   |
| Canonical pre-commit document count | 1                                 |
| Bash and POSIX shell syntax         | Passed                            |
| JavaScript configuration syntax     | Passed                            |
| Canonical Prettier check            | Full repository passed            |
| Canonical Markdownlint check        | Full repository passed            |
| Commitlint policy smoke test        | Passed                            |
| pnpm frozen lockfile verification   | 4,028 records passed              |
| Git whitespace check                | Passed                            |

A full local MegaLinter container run was not possible because this workspace
does not provide Docker or Podman. The wrapper's command construction, path
containment, report contract, and dry-run behavior are covered by unit tests.
The root GitHub workflow is the production execution environment for the pinned
MegaLinter image.

The imported Node manifest requires Node 26.5 or newer. The validation runtime
provided Node 24, so dependency resolution used pnpm's explicit `--force` only
for lockfile verification; it did not weaken the committed engine contract.

## Remaining debt and recommendations

### Priority 1: close policy gaps

1. Add `ACTION_ZIZMOR` after its existing-workflow findings are triaged. It
   complements Actionlint with GitHub Actions security analysis.
2. Add `PYTHON_RUFF_FORMAT` to the routine profile after applying one reviewed
   Python formatting baseline. Ruff lint is active today, but CI does not yet
   enforce Ruff formatting.
3. Wire `SPELL_CODESPELL` into the holistic profile. Its dependency and config
   already exist, so this is primarily a noise-baseline exercise.
4. Add `JSON_V8R` for SchemaStore-backed validation of supported JSON and YAML
   metadata after documenting explicit schema exceptions.

### Priority 2: deepen security without duplicating signals

1. Evaluate `REPOSITORY_SEMGREP` for semantic security rules with a measured
   runtime and false-positive budget.
2. Trial exactly one of `REPOSITORY_BETTERLEAKS` or
   `REPOSITORY_KINGFISHER` beside Gitleaks; avoid enabling multiple equivalent
   secret scanners without distinct ownership.
3. Consider `ENV_DOTENV_LINTER` for committed example environment files.
4. Keep OSV Scanner in its dedicated workflow rather than enabling the
   equivalent MegaLinter descriptor twice.

### Priority 3: language-conditional quality

- Add `HTML_DJLINT` if template-heavy HTML enters the monorepo.
- Evaluate `deptry`, `vulture`, `interrogate`, and `complexipy` when production
  Python packages appear; fixtures alone do not justify them.
- Enable Bicep, Kubernetes, Terraform security, SBOM, and license profiles only
  for repositories or paths that actually own those artifacts.

### Structural follow-up

- Decide whether the preserved `egohygiene` package names, URLs, publishing
  metadata, and broad application dependencies should become Egolint-specific.
  Renaming or pruning them was intentionally out of scope because it changes
  product identity rather than lint integration.
- Review the 4,028-record Node dependency graph. It includes unrelated
  application, documentation, release, and test tooling plus deprecated
  transitive packages and peer warnings. Split it into purpose-specific groups
  before treating Egolint as an independently publishable package.
- Resolve or formally accept the upstream-disabled API Spectral and Checkmake
  integrations. Terrascan is deprecated; preserve its config only while a
  migration target is chosen.
- Run the holistic profile on a schedule or manual dispatch before promoting
  more descriptors into the pull-request baseline.

## References

- [MegaLinter configuration](https://megalinter.io/latest/configuration/)
- [MegaLinter supported linters](https://megalinter.io/latest/linters/)
- [Taskfile includes](https://taskfile.dev/docs/guide#including-other-taskfiles)
- [Commitlint GitHub Action configuration](https://github.com/wagoid/commitlint-github-action)
