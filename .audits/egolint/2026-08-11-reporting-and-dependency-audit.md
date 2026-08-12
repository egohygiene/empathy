# Reporting architecture and dependency convergence audit

**Date:** 2026-08-11

**Scope:** CI action runtimes, trusted report publication, architecture
generation, and fixable Node dependency vulnerabilities

**Outcome:** Publication controls complete; every registry-published Node fix
applied

## Reporting contract

Pull-request jobs remain read-only and publish complete run output as workflow
artifacts. Scheduled, manual, and default-branch runs may also update curated
stable snapshots beneath `.reports/` through the guarded
`publish-report-snapshot` action.

The publisher rejects pull-request events, non-default branches, paths outside
`.reports/`, traversal, and timestamped `history` directories. Only publication
jobs receive `contents: write`; scanners and generators retain read-only access.
Report commits carry `[skip ci]`, and report paths are excluded from relevant
push triggers, so snapshot refreshes cannot recursively launch report workflows.

## Architecture source of truth

The generated architecture snapshot joins the canonical MegaLinter and
complementary tool matrices. Its Markdown legend and SVG identify fast and
holistic coverage, execution surfaces, result states, and report destinations.
The generator is deterministic and fails `task lint:contracts` when checked-in
output is stale.

## GitHub Actions runtime migration

JavaScript actions use immutable revisions whose action metadata selects the
Node 24 runtime. Docker and composite actions remain pinned to immutable
revisions. The third-party Commitlint wrapper was removed; CI now invokes the
repository-pinned Commitlint installation directly under Node 26.5.0, satisfying
the repository engine contract while removing an extra action runtime.

## Dependency convergence

The PR 3 OSV artifact reported 59 Node findings. Direct dependency refreshes and
targeted pnpm overrides reduce `pnpm audit` to six advisory records. Overrides
are limited to published fixed versions, and pnpm's minimum-release-age policy
records the security versions that must remain installable during the embargo
window.

No advisory is ignored or suppressed. The six remaining records map to four
transitive packages whose advisory-declared patched releases were not published
in the npm registry as of the audit date:

| Package                 | Current | Advisory fix | Dependency owner                         | Records |
| ----------------------- | ------- | ------------ | ---------------------------------------- | ------: |
| `vue-template-compiler` | 2.7.16  | 3.0.0        | `documentation`                          |       1 |
| `elliptic`              | 6.6.1   | 6.6.2        | Docusaurus/Webpack and Secretlint graphs |       1 |
| `decompress`            | 4.2.1   | 4.2.2        | `shellcheck`                             |       2 |
| `image-size`            | 2.0.2   | 2.0.3        | Docusaurus MDX loader                    |       2 |

These are preserved as real scanner findings. A future dependency refresh can
remove them as soon as an upstream owner publishes a viable fixed release.

The separate Python audit likewise retains the existing `ecdsa` 0.19.2 timing
finding and `httpie` 3.2.4 certificate-validation finding. Neither currently
has a published fixed release, so this change does not suppress or relabel
either result.

## Validation evidence

- pnpm 11.21.0 lockfile resolution: passed with 3,939 entries.
- pnpm supply-chain policy verification: passed.
- Full frozen pnpm install: 3,637 packages installed successfully.
- Root and Egolint Python contracts: 26 and 27 tests passed.
- Commit policy: 4 canonical fixture tests passed.
- GitHub automation policy: 10 workflows and 12 actions passed; action,
  workflow, and Taskfile schemas passed.
- Publisher trust-boundary and local commit/push fixtures: passed.
- Ruff, Prettier, ShellCheck, shfmt 3.13.1, Detect Secrets, addlicense, and
  REUSE checks for the changed surface: passed.
- Registry-published fixed versions: applied without blanket overrides or
  audit ignores.
- Remaining npm audit metadata: 1 critical, 2 high, 2 moderate, and 1 low
  advisory record, all awaiting unpublished upstream versions.

The dedicated OSV workflow remains the CI source of truth for cross-ecosystem
manifest and lockfile scanning, normalized JSON, Markdown summaries, and SARIF.
