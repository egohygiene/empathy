# Miscellaneous staging disposition audit

## Decision

Four explicitly authorized miscellaneous intake files were removed on
2026-08-16 after their disposition was resolved. The Mantle Fastfetch source
was retired only after the complete presentation path was implemented and
tested. The MegaLinter checklist already had a corrected canonical copy. The
creative-architecture note and terminal-capture specification were intentionally
discarded at maintainer direction rather than silently promoted to unrelated
owners.

The three user-provided README authoring artifacts were polished into the
reusable [Holon README pack](../holon/packs/readme/README.md), with source
checksums and transformations recorded in the pack's
[provenance file](../holon/packs/readme/PROVENANCE.md).

## Source evidence

- Recoverable repository source commit: `f18897e8a9d7e32b12a563a33346732b3efdec4c`
- Removed files: 4
- Removed bytes: 28,252
- Mantle issue artifact SHA-256:
  `2a4f0385c8c8e5d005a92e13280601cc1ef8a61d6c43723bcb4391942cd5503e`

| Source | Bytes | SHA-256 |
| --- | ---: | --- |
| `.staging/misc/fastfetch.jsonc` | 9,841 | `c9fd027013592d28f95a9cfb52a1cff8c425373d4449260723ce21806c910d23` |
| `.staging/misc/future-anime-compiler-architecture-notes.md` | 1,499 | `220ce63eb276b71cb5f8cd0ef750ccc701f11569cc49a12f36abc50832db9333` |
| `.staging/misc/megalinter-remediation-checklist-indented.md` | 6,785 | `4e50907d33569825918b0c09380323f4478337042fbc148ec5aa093555f4fee0` |
| `.staging/misc/terminal-execution-capture.spec.md` | 10,127 | `65d4ffb6a0af72d1f742320ead0b5943aa4a8c562f5b2860ccc7c739417f575c` |

## Disposition

| Source | Classification | Final disposition |
| --- | --- | --- |
| `fastfetch.jsonc` | Superseded Mantle intake | Removed after `mantle/config/fastfetch/fastfetch.jsonc`, canonical banner assets, four collectors, shared `shell-banner` orchestration, once-per-session Bash/Zsh/Fish integration, installation coverage, documentation, and offline contract validation were completed. |
| `megalinter-remediation-checklist-indented.md` | Near-duplicate Egolint audit | Removed. `.audits/egolint/megalinter-remediation-checklist.md` preserves the content with the canonical Egolint title and current `.reports/megalinter/` path. |
| `future-anime-compiler-architecture-notes.md` | Unpromoted creative research note | Removed at maintainer direction. No Dreamscape, Aniflow, or Renderflow implementation claim was created from the note. |
| `terminal-execution-capture.spec.md` | Unpromoted organization-spec candidate | Removed at maintainer direction. No Aether or Mantle contract claims support for the discarded specification. |

## Mantle completion evidence

Mantle now owns the complete portable presentation behavior:

- `assets/presentation/mantle-banner.png` remains the canonical transparent
  400×134 image, with `mantle-banner.txt` as the ANSI-free fallback.
- `config/fastfetch/fastfetch.jsonc` remains pinned to the Fastfetch 2.67.0
  schema, keeps Chafa negotiation portable, reserves `mantle.png`, and invokes
  only the four concise Mantle collectors.
- `mantle fastfetch runtime|workspace|toolchains|contexts` reports
  deterministic, local, privacy-conscious values.
- `bin/shell-banner` renders banner then Fastfetch, supports forced replay,
  component-only modes, overrides, dry-run, and diagnostics, and treats optional
  failures as nonfatal.
- Bash, Zsh, and Fish invoke the same orchestrator and export
  `MANTLE_PRESENTATION_SHOWN=1` so nested shells do not retry.
- Copy and symlink installs include the assets and explicit config while leaving
  user-owned Fastfetch configuration and unrelated logos untouched.
- The Linux/macOS CI matrix downloads the official Fastfetch 2.67.0 archives,
  verifies their published SHA-256 checksums, and executes the canonical config
  with Mantle's collectors on `PATH`.

Realm may provision Fastfetch, Chafa, fonts, or terminal packages later. It does
not own the presentation behavior.

## Recovery

Original staging sources remain inspectable through Git history:

```sh
git show f18897e8a9d7e32b12a563a33346732b3efdec4c:.staging/misc/fastfetch.jsonc
git show f18897e8a9d7e32b12a563a33346732b3efdec4c:.staging/misc/future-anime-compiler-architecture-notes.md
git show f18897e8a9d7e32b12a563a33346732b3efdec4c:.staging/misc/megalinter-remediation-checklist-indented.md
git show f18897e8a9d7e32b12a563a33346732b3efdec4c:.staging/misc/terminal-execution-capture.spec.md
```
