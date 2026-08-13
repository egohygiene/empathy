# Mantle provenance

Copyright 2026 Ego Hygiene

SPDX-License-Identifier: MIT

This file records the source lineage and third-party boundary of the Mantle
code tracked in this repository.

## Project lineage

Mantle is Ego Hygiene project code. The standalone Mantle source was
consolidated into the Empathy repository in commit `e53f191`; subsequent work
has restored, validated, and hardened the CLI and shell runtime in place. The
repository history is the authoritative record of authorship and modification.

All maintained Mantle shell sources carry the project copyright notice and an
MIT SPDX identifier. The repository-level [`LICENSE`](LICENSE) contains the
license text.

## Third-party boundary

Mantle currently tracks no vendored third-party executable or library source.
References to external projects fall into these categories:

- Bats Core, ShellCheck, shfmt, shdoc, Fish, and Zsh are validation tools
  discovered from the developer or CI environment; their source is not copied
  into Mantle.
- `config/fastfetch/fastfetch.jsonc` is Mantle configuration that consumes
  Fastfetch's published schema; it is not Fastfetch source code.
- Installer metadata and integration code identify upstream tools and download
  upstream release artifacts at user request. Mantle does not redistribute
  those artifacts, and their upstream licenses continue to apply.
- Branding and audit files are first-party project artifacts, not runtime
  dependencies.

## Contribution requirements

Do not add code of unknown origin. Any vendored, copied, generated-from, or
substantially adapted third-party material must record:

1. The upstream project and canonical source URL.
2. The exact release, revision, or retrieval date.
3. The upstream license and all required notices.
4. Which local files were modified and how.
5. An appropriate SPDX identifier in each maintained source file.

Place required license texts or notices beside the imported material and add a
specific entry to this document. A package name, download URL, or compatible
license alone is not sufficient provenance.

Generated output should be reproducible from a checked-in source and command,
or explicitly document the generator and version. Dependencies fetched at
runtime must be verified where the upstream distribution supplies checksums or
signatures.
