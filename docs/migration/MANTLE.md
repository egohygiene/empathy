# Mantle source extraction

Parent: [Empathy #79](https://github.com/egohygiene/empathy/issues/79). Related:
[#92](https://github.com/egohygiene/empathy/issues/92) (the Mantle nested-ignore
exception), [#59](https://github.com/egohygiene/empathy/issues/59) (staging drain
contract), and [foundation ownership](../decisions/ADR-0001-foundation-ownership.md).

The canonical implementation is [egohygiene/mantle](https://github.com/egohygiene/mantle).
Empathy's historical `mantle/` tree is a migration snapshot, not a second source
owner. This cleanup removes its relative Taskfile/editor/workflow integration;
Empathy does not replace it with another vendored checkout. Released consumption
through Realm remains a separate future step.

## Source and reconciliation

The reviewed source is Empathy commit
`b344dcbbbd51397cb1e9b1afa6f289af856054f4`, including all 337 files under
`mantle/`. The bounded inventory in
[`migration/mantle-removal.tsv`](../../migration/mantle-removal.tsv) records the
exact path, mode, source Git blob, destination, and disposition for every file.
The original bytes and history remain available at that immutable source revision.

Useful material is reconciled against current standalone Mantle instead of
replacing its six-profile capability graph, recent storage/archive/HLS commands,
startup handling, managed-prefix lifecycle, or current Identity artwork.
Recovered families include literal configuration, inspection/completion helpers,
installer assurance, XDG/history preservation, focused alias groups, validation
and install-smoke tooling, and source provenance/contribution documentation.

Three additional Mantle-owned staging files are handled separately: the stale
Git-branch helper and the two optional shell-session defaults. Their exact-source
approval and owner evidence use the existing staging-removal contract.

No wrong-owner implementation was found inside the reviewed Mantle snapshot.
Material with a different owner belongs in an owner-specific todo area with
provenance rather than in `mantle/`. No such move was needed for this snapshot.
The other 246 Realm-owned staged workstation files remain in their existing
intake area, outside this bounded migration.

## Validation and deletion evidence

Owner implementation: [Mantle PR #40](https://github.com/egohygiene/mantle/pull/40).
The immutable destination revision is
`e776b70eee24f8cbe5ad1760bf1355141cb23c4c`. The inventory records 17 equivalent,
94 reconciled, 222 retained-current, and four superseded source files. Each
destination blob is verified independently with Git's object hashing.

The cleanup removes all 337 files from the historical root `mantle/` tree and
the three additional staged files: **340 source files total**. Exact path/blob
approvals for the latter are in
[`staging-removal-approvals.json`](../../migration/staging-removal-approvals.json).
The staged-file removal gate passed for those three paths before deletion.
The tracked staging count decreases from 9,586 to 9,583; no tracked staged file
remains assigned to Mantle. There is no replacement source checkout in Empathy.

Independent owner validation includes literal-policy/runtime/Fish/Git/installer
tests, all nine strict static groups, the 90-command catalog, offline Fastfetch
validation, and a temporary-prefix install/reinstall/status/doctor/uninstall
smoke test. Native Linux and macOS evidence is attached to the owner PR;
[Test Suite run 39095909596](https://github.com/egohygiene/mantle/actions/runs/39095909596)
validates the published destination revision after the initial macOS portability
findings were corrected. Review the final passing owner checks and merge
the owner PR before merging this source cleanup.

Empathy's focused extraction, gitignore, staging-ledger/removal, and task-catalog
checks pass (24 tests), as do the scoped canonical Ruff, Mypy, and Secretlint
checks. The three low-severity Bandit findings are identical to the base source
(subprocess import and fixed Git argv); no security warning is introduced. Existing
dependency-pin assertions in the root commitlint test and EgoLint MegaLinter
catalog test disagree with the recently updated workflows on the base branch;
those failures are baseline drift outside this migration. Full-profile readiness
still requires the manual holistic run on the exact review head specified by
`AGENTS.md` and the repository-intelligence publication procedure. The PR fast
profile does not establish that readiness.

The snapshot inventory and `.staging` ledger are different evidence surfaces:
the existing staged-file gate applies only to `.staging/` paths. It is not used
to claim approval for the historical root-level `mantle/` snapshot.

Historical dated audits and rule inventories remain intact. Current Task
catalogs are regenerated from their canonical inputs; the retired Mantle
nested-ignore exception no longer affects the active golden fixture. Other
nested-policy exceptions under #92 remain unresolved by this change.

Regeneration also reconciles existing generated drift: TASKS.md gains the
already-defined Identity task while removing eight retired Mantle commands.
The staging CSV drops two image rows for files already absent from the tracked
tree and updates three existing image classifications to the current classifier.
Those images are not moved, read, or deleted by this migration; only the three
approved staged source files are removed here.

## Deferred work

Mantle ADR history backfill (#31) follows this consolidation and its shared
policy/tooling prerequisites. Flow shortcuts (#20) wait for a published Flow
CLI/preset contract, and release integration (#26) remains queued for the agreed
Flow/Realm readiness milestones. This migration does not complete Empathy's
broader incubation or gitignore issues.
