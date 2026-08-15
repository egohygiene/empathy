<!-- SPDX-FileCopyrightText: 2026 Ego Hygiene -->
<!-- SPDX-License-Identifier: MIT -->

# Staging deduplication and VS Code reconciliation

## Scope

This audit records the bounded reconciliation of the staged VS Code profiles and
the exact-content duplicate scan requested on 2026-08-15. It distinguishes
content equality from same-name or semantically related material so unique
staged source is not removed accidentally.

The scan compared tracked regular files without following symlinks. Empty files
were excluded from staged-to-active duplicate deletion because an empty package
initializer, placeholder, or directory sentinel is not made redundant by an
unrelated empty file elsewhere.

## VS Code reconciliation

The four common files under `.staging/.vscode/` and `.staging/.vscode2/` were
byte-for-byte identical. `.vscode2/` additionally contained a `cspell.json`
shim whose import path did not match Empathy's encapsulated Egolint layout.

Applicable repository-neutral settings were merged into the active `.vscode/`
profile:

- GitHub Actions, HTMLHint, CODEOWNERS, Bats, Dev Containers, SchemaStore, and
  Task extension recommendations;
- advanced diffing and whitespace-insensitive diff display;
- final-newline enforcement;
- watcher and search exclusions for generated, report, dependency, and Rust
  build trees while keeping `.staging/` searchable for ongoing intake work;
- cSpell configuration merging and Git-ignore behavior; and
- the repository's existing shfmt formatter for Bats files.

The active Egolint configuration paths and formatter choices remain canonical.
The staged personal editor defaults, cosmetic preferences, absolute macOS Dart
SDK path, C/C++ defaults, and conflicting Biome/Prettier/Shell Format settings
were not promoted.

The staged Flutter launch and task entries targeted the absent
`apps/egohygiene` application. Empathy's active Taskfile-backed tasks already
provide the repository-local execution contract, so those source-specific
entries were not copied into the active profile.

After reconciliation, both staged VS Code directories were removed.

## Exact duplicates removed

| Removed staged source | Canonical or retained source | Evidence |
| --- | --- | --- |
| `.staging/specs2/**` | `.staging/.github/specs/**` | All 53 tracked files matched byte-for-byte at the same relative path. |
| Seven shared files under `.staging/.github/skills2/flutter/` | `.staging/.github/skills2/flutter-engineering/references/` | `architecture.md`, `design-system.md`, `localization.md`, `notifications.md`, `routing.md`, `state-management.md`, and `testing.md` matched byte-for-byte. |
| `.staging/.vscode2/{extensions,launch,settings,tasks}.json` | `.staging/.vscode/` before active reconciliation | The four pairs matched byte-for-byte. |
| `.staging/misc/banner.png` | `mantle/assets/presentation/mantle-banner.png` | Non-empty binary content had the same SHA-256 digest. |

The two remaining files under `.staging/.github/skills2/flutter/` were retained:
`ai-providers.md` and `offline-first.md` differ from the same-name
`flutter-engineering/references/` files and therefore require later semantic
classification.

## Intentional package-local repetition retained

Some exact content is repeated inside otherwise independent staged skill
packages. It is not treated as removable staging duplication in this pass:

- `LICENSE.txt` is repeated in three independently packaged Azure skills; each
  package must retain its own license evidence.
- `ax-setup.md` and `ax-profiles.md` are repeated across seven Arize skills;
  each skill links to its package-local copy and must remain self-contained
  until the collection has an accepted shared-reference contract.

## Same-name active material retained

The scan found staged specifications and agents with names related to the
provisional Aether corpus under `egolint/.agents/`. They are not exact or
formatting-only copies. The active files contain evolved schemas, versions,
metadata, requirements, and structure, while the staged files preserve earlier
source material. They remain staged for a later provenance and supersession
decision.

## Result

- The duplicate `specs2` and `.vscode2` imports are eliminated.
- The active VS Code profile gains only applicable, repository-neutral behavior.
- No non-empty staged file remains byte-for-byte identical to an active
  repository file.
- No exact staged agent duplicate remains.
- Unique, conflicting, package-local, and merely similar material is preserved.

This audit is a disposition record for this cleanup only. It does not transfer
ownership of staged specifications, skills, or agents to Empathy.
