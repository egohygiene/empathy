# MegaLinter remediation report

## Baseline

- Review date: 2026-08-14
- Stored snapshot: `.reports/megalinter/megalinter-summary.md`
- MegaLinter: 10.0.0
- Request ID: `f6a4e498-97cf-11f1-9bf8-42dd6a0ea05a`
- Snapshot state on `main`: `ee6d345e69a012e7a8c487a30803d6a4b19c7941`
- Recorded result: 56 successful linters and 45 failing linters

This report classifies the stored holistic run and records the first remediation
pass. Counts below describe that immutable snapshot; a subsequent holistic run
is required to establish the new baseline.

## Remediated in this pass

### Configuration and execution failures

- Made the shared Yamllint rules compatible with Ansible Lint's required YAML
  profile.
- Removed Dart's obsolete `-c` analyzer flag and added a fixture-local include
  for the canonical analyzer policy.
- Switched the ESLint flat configuration to `createRequire` so MegaLinter's
  `NODE_PATH` packages resolve under native ESM.
- Repaired the Mypy multiline exclusion expression, excluded deliberate
  negative fixtures and colliding `tests/__init__.py` modules, and corrected
  first-party typing defects. The project check now reaches source analysis
  instead of stopping at configuration parsing.
- Removed Pylint's retired `suggestion-mode` option and corrected the simple
  actionable findings identified by the snapshot.
- Removed Pyright's unsupported `$schema` key. The remaining strict-type
  findings are tracked below as refactoring debt.
- Disabled MegaLinter's second generated ls-lint configuration because the
  repository policy already carries the same exclusions and ls-lint cannot
  merge two root-level `ignore` mappings.
- Pointed TFLint at the repository's provider-neutral policy instead of
  MegaLinter's bundled Azure policy.
- Removed duplicate and conflicting TruffleHog arguments already supplied by
  MegaLinter.
- Disabled `TYPESCRIPT_STANDARD`; ESLint owns TypeScript analysis and Prettier
  owns formatting, while ts-standard requires a synthetic root project and
  duplicates both signals.
- Disabled `REPOSITORY_GIT_DIFF`; generated report snapshots necessarily dirty
  the workspace during a holistic run, so this check only reported its own
  output. Source mutation remains disabled through `APPLY_FIXES: none`.
- Added targeted v8r exclusions for tool-owned configuration fragments and
  fixtures that SchemaStore classifies against unrelated schemas.

### Source and fixture cleanup

- Applied Ruff formatting to the one drifted Python test and retained a clean
  43-file Ruff/Ruff Format scope.
- Applied Prettier to 23 JSON evaluation fixtures, the Mantle workflow, and the
  Markdown files named in the stored markdownlint output.
- Applied the canonical clang-format policy to the C and C++ fixtures.
- Removed UTF-8 byte-order marks from both PowerShell configuration files.
- Corrected CSS and HTML class conventions, documented the one Obsidian-owned
  camel-case selector, added the missing Protobuf field comment, and removed the
  extra Lua trailing newline.
- Documented intentional subprocess and trusted-XML boundaries with narrow
  Bandit suppressions. Bandit now reports zero findings for the snapshot's same
  43-file scope.
- Regenerated the MegaLinter policy matrix, profile snapshots, and lint
  architecture artifacts after the ownership changes.

## Deferred findings

### Requires design or policy work

- Pyright's 662 strict-mode findings span legacy agent scripts, test dynamic
  imports, and Mindgarden types. They should be reduced in bounded package-level
  PRs rather than hidden by weakening strict mode.
- Pylint's findings fell from 25 to 15. The remainder are complexity thresholds
  and one broad exception handler; they need refactoring rather than blanket
  suppressions.
- jscpd reports 4.4 percent duplication against a 3 percent threshold. The
  largest clone families should be reviewed for genuine shared abstractions
  before code is consolidated.
- The Rust Clippy descriptor runs from the repository root, which has no root
  Cargo workspace. Identity's dedicated Rust CI remains authoritative until a
  deliberate multi-holon Cargo workspace contract is designed.
- Lychee requires a projection-aware base URL before it can validate Obsidian
  WikiLinks. Choosing a local vault base or the deployed Quartz base is a
  publishing-policy decision.
- Raku, Snakemake, reStructuredText, and TFLint fixture failures include working
  directory, plugin, or extension semantics that need fixture-specific harness
  work.
- Proselint, Vale, and the remaining Markdown findings need a prose baseline
  that distinguishes architecture templates, historical audits, generated
  text, and current first-party documentation.

### Security and supply-chain signals

- Checkov's 57 findings mix intentional negative fixtures, test infrastructure,
  and workflow policy. They require fixture-aware exclusions before the
  remaining workflow findings can be treated as actionable.
- Grype and Trivy identify unresolved advisories in the imported EgoLint lock
  files, including `decompress`, `image-size`, and `ecdsa`. The snapshot lists no
  fixed versions, so this pass does not fabricate dependency upgrades or
  suppress the advisories.
- Copy/paste, dependency vulnerability, and infrastructure findings remain
  blocking signals until their owning policies are explicitly baselined.

## Validation

- `python egolint/scripts/validate_megalinter_policy.py --check`
- `python .github/actions/generate-lint-infographic/generate_lint_infographic.py --check`
- 51 root integration and policy tests
- 27 EgoLint contract tests
- 23 Mindgarden contract tests
- Ruff lint and format checks across the same files selected in the stored run
- Bandit 1.9.4 across the same 43 Python files selected in the stored run
- Mypy 1.19.1 project analysis with the PyYAML stubs MegaLinter installs: zero
  findings across 31 source files
- Pylint 4.0.6 configuration parse and positive Python fixture check
- Prettier 3.9.6, clang-format 22.1.3, and `git diff --check`

## Next measurement

Run the holistic MegaLinter workflow from the resulting merge commit. Compare
the new stable snapshot against this report, then update this file only when a
later remediation pass materially changes the classification or remaining debt.
