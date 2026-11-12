# Dependency ownership and update coverage

Implementation checkpoint for [Empathy #113](https://github.com/egohygiene/empathy/issues/113),
under [#118](https://github.com/egohygiene/empathy/issues/118). This checkpoint adds
root Node update coverage and dispositions for retained dependency inputs. It
does not establish remediation, exploitability, or final issue acceptance.

## Evidence boundary

The source inspection uses Empathy
`058d92a0f8c970f98a58d446408716936e593c99`. The checked-in normalized receipt
[summary.json](../../.reports/osv/summary.json) identifies:

- scanner: OSV Scanner `2.5.0`;
- source: `18d22e113e87c306b76d24873841249d41358c77`;
- generated: `2026-11-11T11:34:05Z`, with a declared expiry of
  `2026-11-19T11:34:05Z`;
- provider: [run 43012917456](https://github.com/egohygiene/empathy/actions/runs/43012917456);
- execution: report validation succeeded; findings state is `blocked`;
- 645 grouped advisory occurrences, including 34 critical and 279 high.

The seven scanned dependency files and `osv-scanner.toml` have the same Git blobs
at that scan source and the inspection base. This supports a source comparison;
it does not refresh the advisory database or qualify the changed updater config.
The 313 blocking occurrences are the sum of high and critical groups at that
receipt. They are neither 313 unique vulnerabilities nor 313 demonstrated
production exploits. Issue #113's 208 occurrences describe an earlier run and
must remain dated historical evidence.

The [blocking ledger](data/dependency-blockers-2026-11-11.csv) is a static
projection of [native latest.json](../../.reports/osv/latest.json), bound by the
Git blob IDs in [the evidence identities](data/dependency-evidence-2026-11-11.json).
Its grain is **source path × package/version × native advisory group** with
`max_severity >= 7`. Alias IDs stay in the same row; the same advisory can occur
in multiple dependency paths or versions. Every row has an owner and a named
unresolved disposition. Advisory-declared fixed versions are extracted from the
matching package's affected ranges across the group's member records. They can
describe different branches; they are candidates for owner review, without
registry-publication checks, compatibility review, or an upgrade recommendation.
An empty candidate field means none was recorded, not that no remedy exists.

No scanner, audit, registry probe, install, repository helper, tests, builds,
or CI were executed for this change. The source JSON/TOML/YAML and Git metadata
were read statically. Native and normalized receipts remain unchanged.

## Retained roots and owners

The [manifest inventory](data/dependency-manifests-2026-11-12.csv) lists tracked
package/lock/config inputs with their Git blobs, scope, owner, and disposition
at the pinned 058 inspection. It includes manifests that the scan skipped or did not discover;
discovery is not proof that a dependency graph was scanned.

| Input | Actual applicability | Owner and update disposition |
| --- | --- | --- |
| Root `package.json`, `pnpm-lock.yaml` | Active Empathy tooling; 2 declared dependencies and 157 development dependencies. Package metadata uses pnpm `11.17.0`; lock format is `9.0`. | Empathy owns this retained baseline graph. Root `npm` Dependabot entry added. Root manifest declares no workspace package globs; nested specialist sources are not enrolled. |
| Root `pyproject.toml` | Empathy metadata; empty project dependencies, no dependency groups or root Python lock. | Existing root `pip` entry retained as baseline coverage for future additions; it currently has no dependency graph to update. |
| Root `Cargo.toml` | Declares `tests/fixtures/clippy`, which is absent at this base; no root lock. | Empathy owns the broken root composition reference. Defer Cargo enrollment until [#109](https://github.com/egohygiene/empathy/issues/109) establishes a usable root; do not fabricate or copy a fixture. |
| `egolint/package.json`, `egolint/pnpm-lock.yaml` | Active embedded lint toolchain: root Task composition installs/invokes this graph. 178 development dependencies; pnpm `11.21.0`, lock format `9.0`. | [EgoLint](https://github.com/egohygiene/egolint) owns reusable tooling; Empathy owns its consumption. Route dependency changes to the canonical owner and consume a reviewed immutable result under [#110](https://github.com/egohygiene/empathy/issues/110)/[#79](https://github.com/egohygiene/empathy/issues/79). No automated local fork or claim of owner updater coverage. |
| `egolint/pyproject.toml`, `egolint/uv.lock` | Embedded optional docs/test/lint/security/dev/architecture/notebook groups. Empty runtime project dependencies do not make these installed tools inert. | EgoLint owner refresh and Empathy adoption under #110/#79. No root pip entry is claimed to update this uv graph. Owner revision correspondence and hosted updater support remain unresolved. |
| `egolint/Cargo.toml`, `egolint/Cargo.lock`, `egolint/tests/fixtures/**`, `egolint/.config/lint/python/pyproject.toml` | Embedded policy and intentional positive/negative tool fixtures; Cargo workspace points at its own existing Clippy fixture. | EgoLint owns fixture semantics. Do not mechanically upgrade negative fixtures or treat zero reported findings as fixture qualification. |
| `holon/packs/react-vite/template/**` | Optional runnable template scenario included by root Task setup/build. The nested Dependabot YAML is template content; GitHub does not schedule it for Empathy. | [Holon](https://github.com/egohygiene/holon) owns template maintenance; Empathy owns optional integration evidence under #79. Require immutable owner refresh before consumer adoption. Not a root npm workspace or recursively updated by this change. |
| `beacon/Cargo.toml` | Optional root Task build includes this retained specialist source. No tracked Beacon lock; no Beacon graph appears in this OSV receipt. | [Beacon](https://github.com/egohygiene/beacon) owns implementation; Empathy owns adoption under #79. No invented clean scan, updater result, or dependency fix. Nested `beacon/.staging/**` remains specialist intake. |
| `.staging/**` manifests/locks | Frozen intake. The active dependency prohibition remains; some staged locks are still scanned recursively. | Use the existing [staging ledger](../../.audits/data/2026-08-15-staging-file-disposition.csv), not directory-name guesses: staged API → Holon, emoji-precache → Renderflow, community skill tools → Aether, Realm roots → Realm. Owner migration evidence and separate deletion approval are required. No updater enrollment or scan exclusion. |
| `identity` Git submodule | Separate repository pinned at `481e284a77e0a7cc3bf25f40dc91a71120d036ef`. Its dependency files are outside the tracked superproject inventory. | [Identity](https://github.com/egohygiene/identity) owns packages/updaters. Empathy reviews the consumed pin; no recursive coverage claim. |

Canonical owner assignments follow [ADR-0001](../decisions/ADR-0001-foundation-ownership.md).
Embedded source blobs identify what is retained here, not the specialist's
current upstream revision. No owner HEAD or owner package fix was selected by
this checkpoint. Frozen intake stays preserved under the [staging contract](../migration/STAGING.md).
Container base images and Actions pins are separate supply-chain inputs, not
silently covered by the package/lock inventory.

## Reported blocker dispositions

| Native source path | Critical | High | Scope | Named unresolved disposition |
| --- | ---: | ---: | --- | --- |
| `pnpm-lock.yaml` | 11 | 101 | Active Empathy tooling | `empathy-root-remediation`: owner review of each ledger row's dependency parent, candidate branch and published release; root updater is intake, not proof of a fix. |
| `egolint/pnpm-lock.yaml` | 11 | 72 | Active embedded EgoLint tooling | `egolint-owner-refresh`: canonical owner remediation, exact owner revision, then Empathy consumption and scanner evidence; #110/#79. |
| `egolint/uv.lock` | 7 | 56 | Embedded optional tooling groups | `egolint-owner-refresh`: establish group/command exposure and owner remedy; consume the owner result without local dependency forks; #110/#79. |
| `.staging/devenvironment/containers/services/api/poetry.lock` | 5 | 42 | Inert staged Holon API intake | `holon-staged-migration`: preserve findings and source, review at canonical destination, record migration proof under #79. No active-runtime or exploitability assertion. |
| `.staging/tools/emoji-precache/package-lock.json` | 0 | 8 | Inert staged Renderflow tool intake | `renderflow-staged-migration`: same preserved-source review and migration boundary, with Renderflow as owner. |
| **Total** | **34** | **279** | **313 grouped occurrences** | **All rows remain unresolved; none is a reviewed exploitability exception.** |

The scanned EgoLint Cargo lock and staged Aether CacheGenerator project have
no advisory groups in this receipt. Other discovered inputs were skipped,
including unexpanded manifests, fixtures, template packages, and an SBOM. Those
are coverage/applicability investigations, not negative findings. The normalized
receipt retains all 49 discovered inputs, seven scanned files and 42 skipped
files; this change does not drop them or widen any scanner exclusion.

## Updater behavior and Actions coordination

[`.github/dependabot.yml`](../../.github/dependabot.yml) uses Dependabot's
`npm` ecosystem for the root pnpm graph. Weekly Monday `09:30 UTC` intake is
separate from the existing Actions `09:00` and root pip `09:15` schedules.
Production and development minor/patch updates have separate groups; major
version updates stay individual. A distinct `security-updates` group keeps
security grouping separate from scheduled version grouping. The five-PR
version-update limit stays bounded; hosted security-update limits and alert
availability remain GitHub configuration concerns.

Configuration follows the [Dependabot options reference](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference)
and [supported ecosystems](https://docs.github.com/en/code-security/reference/supply-chain-security/supported-ecosystems-and-repositories),
read on `2026-11-12`. The ecosystem table lists pnpm `11` under `npm`;
the options reference supports the selected group dependency types, minor/patch
limits and security-update grouping. Actual hosted acceptance of this root,
lock `9.0` regeneration, root hook/settings handling, and update PR behavior
remain deferred qualification items. No downgrade, second package manager, or
lock rewrite is introduced to
claim support. If the hosted updater rejects the root graph, retain the finding
and select a reviewed supported root-updater path under #113 before claiming
coverage works.

[Actions PR #121](https://github.com/egohygiene/empathy/pull/121) was open at
head `2888a23443b720cab1f7e3e327abed313da4708e` during this inspection. Its
group already proposes six Actions updates across 16 files. This change leaves
the existing Actions group and all action pins unchanged. Recheck that PR's
current state before later integration; no duplicate bump, merge, comment or
acceptance action is part of this checkpoint.

## Suppression and acceptance gates

The [exception review register](../../.github/security/dependabot-dismissals.md)
now accounts for all nine configured IDs, including the previously unlisted
`image-size` and `httpie` entries and root lock occurrences. The OSV policy IDs
and reasons are unchanged. Historical registry-availability assertions have not
been freshly verified, so this checkpoint does not renew an exception approval.
Policy is advisory-ID based and does not enforce the source-path descriptions
in the register; aliases and additional paths must be reviewed before reuse.

Before #113 acceptance:

1. Empathy owner and each named specialist owner review ledger rows against
   current advisory records, dependency parents, package registry availability,
   and actual invoked tooling groups. Record an immutable owner fix or a
   narrowly justified, time-bounded reviewed exception. A recorded fixed event
   alone does not establish a published or compatible release.
2. Revisit all nine ignored IDs at the next dependency refresh or upstream fix,
   and before accepting this checkpoint. Remove obsolete suppressions rather
   than extending a global ID to unrelated source paths. Reconcile hosted
   Dependabot alert state independently; this register does not query it.
3. Qualify root updater behavior and resolve owner-managed graph intake with
   #110/#79. Root Cargo composition belongs to #109; optional/staged sources
   retain their explicit ownership and migration gates.
4. Run the canonical native OSV workflow at the final reviewed source, retain
   native JSON/SARIF and normalized summary with source/run identities, and
   reconcile every remaining blocker and skipped input. [#98](https://github.com/egohygiene/empathy/issues/98)
   owns report alignment; it does not remediate dependencies.
5. Perform the deferred repository validation/holistic review required by
   `AGENTS.md`. [#51](https://github.com/egohygiene/empathy/issues/51) retains the
   assurance boundary. Keep #113 open until its fresh-evidence acceptance is met.

## Source integration — 2026-11-12

This source integrates after PR #120 (optional Mindgarden),125 (typed Intelligence
feeds),121 (Actions),130 (baseline evidence) and131 (staging receipts). The
existing Actions group configuration is retained. PR #121 merged at
`946364370e9c39637d6d0de49c297c3f81776590`; its approved immutable selection
is a source update, not fresh runtime/catalog or vulnerability evidence. The
original open-PR observation above remains historical at its recorded head.

The dated JSON/CSV evidence remains byte-identical to its original inspection
against `058d92a0f8c970f98a58d446408716936e593c99`. In particular, its staging
CSV identity (`03aaab30d752d2ebfe57cc41ce42bf6d6a5acc52`, SHA-256
`839477a6de4a5163b15aa00a142d15ee7b644885832d24565c4023dfc68ca6b1`)
is historical. PR #131's separately authorized inert canonical refresh changed
only one ROADMAP duplicate-metadata row in the current rolling staging ledger,
which now has SHA-256
`c3d0d967a8a1cb326fb9fcfeef6beae284d2ad955fc9b762089080b9f7e1bb22`.
That generation changes neither the older dependency evidence nor the preserved
staged source or approval records. No new scan or exception renewal occurred.

PR #120 also adds `requirements/mindgarden-standalone.txt`, an isolated optional
VCS-pinned engine install lane absent from the dated inventory of 54 manifest inputs.
The consumer reviews that immutable pin explicitly under #65; current hosted
updater discovery/coverage of this additional requirements path is unverified.
Do not infer recursive coverage from the existing root pip entry or replace
the historical inventory with an unexecuted current audit. Root/specialist graph
coverage and the new root npm intake still require the acceptance work above.

The only source-generation exceptions during this merge batch were canonical
Task-list catalog refresh and inert staging inventory refresh. Tests, installs,
registry probes, scanner/audit runs, builds, native/helper consumer qualification
and CI remain deferred. Source integration does not remediate the reported
occurrences or qualify the hosted updater.
