# Scoped nested-policy adoption — 2026-11-13

This is the current file-specific reconciliation for
[Empathy #92](https://github.com/egohygiene/empathy/issues/92), following the
[accepted shared-interface proof](SHARED-INTEGRATION-04.md). It does not replace
that proof's original source clocks, negative fixture or receipt.

The [source-adoption record](data/nested-adoptions-20261113.json) binds each
actual consumer file before/after, its immutable owner resource and the exact
scope of the change. No exception approval, expiry or tracked-file exemption
was invented. The thirteen other inherited policies remain preserved and
unassessed; this checkpoint does not certify their entire contents.

## Resolved source cases

| Case                                 | Actual consumer reconciliation                                                                                                                                                                                                                                                                                             |
| ------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Devcontainer environment marker      | Retire the tracked `.devcontainer/.env` after matching its exact known digest and confirming that it contains only the marker key. Both existing `devcontainer.json` environment declarations retain the same semantic truth and exact file bytes. The obsolete `!.env` exemption is removed.                              |
| Imported EgoLint target rule         | Consume the accepted owner's `/target/` correction from `ec97ed8b3f1a4a2198aec03355600ea6c9caa1e1`. All other imported bytes remain unchanged. Build output is ignored while `egolint/examples/target/source.rs` and equivalent source fixtures remain visible.                                                            |
| Imported Holon environment templates | The accepted owner at `660b941f99618806fcadd589bcdae61c519f96e4` delegates environment policy to Empathy. Replace only the obsolete prefix-exemption block with the exact accepted universal suffix block. All unrelated imported rules remain unchanged; this is scoped adoption, not a complete imported-source refresh. |
| Former Mantle case                   | Remains retired by the existing [actual extraction](../../migration/MANTLE.md); no Mantle copy or new exception is introduced.                                                                                                                                                                                             |

Only `devcontainer.json` actively references the marker. The checked-in
Dockerfile and Compose file contain comments, with no marker-loading directive;
the lifecycle initializer's optional environment creation addresses root `.env`.
Removing the redundant tracked file therefore preserves the explicit active
declarations. The payload is not reproduced in this record. A real container
build or repair of those existing stubs is not claimed.

## Actual Git behavior and current golden selection

The updated tests exercise the complete existing nested precedence using real
Git. Local `.env`, `.env.sample.local`, `.env.example.local` and
`.env.template.backup` stay ignored; `.env.production.example`,
`.env.production.sample` and the other deliberate suffix templates stay visible.
Target-named source remains visible and the imported EgoLint build root remains
ignored. Source hashes require future policy changes to update their explicit
adoption record.

The coordinated #109 correction removes the orphan root Cargo workspace and
default Rust profile/unused overlay, retaining explicit root cache intent in
the golden manifest. The original 176 historical rule dispositions and their
visibility probes remain. Retired Cargo evidence is identified by its immutable
source rather than falsely requiring that obsolete file on the current disk.
Rust remains an opt-in profile.

## Fresh accepted-owner qualification

The [new receipt](data/shared-requalification-20261113.json) records fresh runs
through the same accepted Empathy `b44f798bb49259f9f48416b4ffebde1103e135c0`,
Holon `660b941f99618806fcadd589bcdae61c519f96e4` and EgoLint
`ec97ed8b3f1a4a2198aec03355600ea6c9caa1e1` inputs. The executable was rebuilt
from the clean exact EgoLint source with locked dependencies; its new digest is
`918cbca72b94af09e03209d0bec4abd53308940fe5a1fa3bed3376c2c2f17dcc`.
The historical executable receipt is preserved rather than silently rebound.

Three disposable representations passed adoption, fresh identical no-op,
explicit local-rule update, native validation, verify, guarded rollback refusal
and exact prior ignore/state/authored-CRLF-README restoration:

1. The accepted foundation 1.1 golden selection.
1. Filament's already accepted pilot selection.
1. An explicitly labeled comparison of the corrected current ignore bytes,
   using an isolated manifest retargeted to supported foundation 1.1.

All six native runs returned `valid`/zero and every check passed. No semantic or
tracked-file exception was supplied. The third representation's ignore bytes
equal the actual current golden root; it does **not** claim that the unchanged
owner adapters accept the current foundation 2.1 catalog. That later local-CI
catalog selection was accepted separately in #142; the original qualification
receipts retain their earlier source and catalog identities. Its isolated root
representation also does not certify the full imported nested-policy tree.
The current nested tests provide the separate known-case behavior evidence.
Reproduce the CLI sequence using the preceding guide's accepted owner contract;
the new receipt retains the actual outcomes and source boundaries.

## Acceptance and wider findings

The [qualification record](data/nested-qualification-20261113.json) records
focused Git/foundation checks, the equipped root suite and selected canonical
lint/security/link results. The required feature-branch holistic workflow is a
separate exact-head provider observation recorded in the PR discussion; it must
not publish report snapshots from the feature branch.

The historical #82 environment criterion now has explicit source correction and
accepted shared semantic evidence for its scoped cases. Full-suite/profile
findings remain separate: #109 owns baseline diagnostics and profile intent,
Issue #110 retains its direct bootstrap/runtime hold, and foundation 2.x adapter
adoption remains a future owner upgrade. No full holistic pass or whole-Empathy
conformance is inferred from these file-specific results.

The master file-contract epic
[organization #32](https://github.com/egohygiene/.github/issues/32) must reconcile
this scoped checkpoint after source integration and explicit issue disposition.
Shared execution/release remains with Relay #5/#49. Fleet adoption remains with
Pace #30. `EMP-Q04`/`EMP-Q05` remain planned; this work supplies neither a complete
foundation materialization nor a baseline release.

Decision impact: reference the existing foundation ownership ADR-0001. These are
bounded consumer corrections within accepted ownership, not a new owner,
exception authority or architecture decision.
