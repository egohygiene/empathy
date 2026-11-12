# Immutable staging diff and durable receipt bindings

Refs [Empathy #112](https://github.com/egohygiene/empathy/issues/112), parent
[#118](https://github.com/egohygiene/empathy/issues/118), graduation
[#79](https://github.com/egohygiene/empathy/issues/79).

This implements the existing [staging migration contract](STAGING.md) and
[foundation ownership boundary](../decisions/ADR-0001-foundation-ownership.md).
It adds no production deletion, owner acceptance, human ratification or
destination validation. A valid binding is evidence for review; it is not
authorization to remove material.

## Three separate evidence surfaces

| Surface | Authority and retention |
| --- | --- |
| `.audits/data/2026-08-15-staging-file-disposition.csv` | Generated current intake/classification, including exact path, Git mode/blob and proposed canonical home. Removed rows leave this inventory. |
| `migration/staging-removal-receipts.json` | Canonical append-only source/destination/authority **claims** for future cleanup. Existing records cannot be changed or dropped when a current row disappears. Initially empty: this implementation invents no approvals. |
| `migration/staging-removal-approvals.json` | Preserved historical Mantle evidence. Its bytes remain unchanged; it is not automatically upgraded into a new exact-source receipt or reused as current authority. |

The current CSV's reserved destination/deletion-approval fields remain compatible
with their existing blank values. They are not a second editable approval store.
The reconciled gate report preserves canonical and legacy claims even when the
current inventory has no matching row. It distinguishes present exact preimages,
removed paths and changed source, with human authority explicitly unauthenticated.
Historical legacy matches are blob-only because that older contract has no mode
or source-revision field; they cannot satisfy the new gate.

## Receipt contract

The closed [schema](../../schemas/staging-removal-receipts.v1.schema.json) uses
`egohygiene.empathy.staging-removal-receipts/v1`. The stdlib gate independently
validates that fixed data contract, including duplicate keys, required/unknown
fields, sorted unique IDs, exact source identities, bounded text and evidence
URL syntax. Generic JSON Schema shape validation does not verify human approval
or the destination repository's results.

Each `receipts` entry has:

- A stable `STG-...` ID; records are sorted by ID. One path/mode/blob preimage
  cannot receive ambiguous duplicate records.
- `source`: a full reachable Empathy `revision`, exact `.staging/` `path`, Git
  `mode` and full Git `blob`. The immutable source commit must contain exactly
  that preimage. No checkout, rename heuristic or caller-supplied current row
  substitutes for it.
- `destination`: the `canonical_home`, full immutable destination `revision`
  and `validation_evidence` URL. When used for removal, the home must equal the
  exact **base** CSV's home for that path/mode/blob. A head classifier edit
  cannot retarget existing approval to a different destination.
- `provenance_resolution` and `sensitivity_resolution`: explicit reviewed
  source/license and sensitive-content disposition claims.
- `authority`: `kind: human-claim`, `actor`, `recorded_at` in UTC seconds and
  `evidence` URL. Only `human-claim` is supported; a `verified` field, actor name,
  accepted-sounding text, prior merge or green CI does not authenticate a person.

New evidence URLs use bounded HTTPS syntax with no whitespace, backslash,
userinfo or non-HTTPS/default-443 port, and a bounded DNS-shaped hostname.
This is syntax admission only: the gate does not fetch a URL, verify an actor,
resolve DNS, establish public visibility or inspect a destination run. A human
must review the actual evidence and authority through the owning migration.
The JSON Schema describes URI shape; these additional syntax constraints and
source/ledger relationships are enforced by the gate.

## Exact base/head gate

`tools/staging_diff_gate.py` enumerates both immutable Git trees. It reports
additions and requires a receipt for every removed or replaced staged preimage,
including content edits, mode/type changes and the removed side of a rename.
It uses no rename similarity detection and cannot transfer approval to an
unrelated path with the same bytes.

For a destructive change, the complete exact receipt must already be present
**unchanged in the reviewed base**. A receipt added alongside a deletion cannot
self-approve that deletion. Prepare and review destination evidence and the
receipt first, then propose cleanup in a later change. The new receipt file is
append-only across base/head. Historical approval bytes are frozen separately.
This ordering is a deterministic integrity boundary, not an assertion that a
base commit was approved by a particular human.

The base must be an ancestor of the exact head. This is intentional: if main
advances beyond a PR's ancestry, update/rebase the review branch and review the
new exact base/head pair. The gate refuses a diverged or unavailable base; it
does not silently substitute a merge base, retime a receipt or bless a stale
review. It needs complete local source history and a Git version supporting
`--no-lazy-fetch`. Missing objects fail instead of fetching credentials/remotes.

The current ledger check requires the represented head checkout/index and exact
staged file bytes, then compares the committed CSV to the canonical generator's
output. This detects stale inventory after addition, replacement or removal.
Historical receipt destination claims remain intact when classifiers change;
only a proposed destructive use is compared to its reviewed base ledger.

Both tools read staged files as inert data. They do not source a shell file,
follow staged symlinks, execute an intake program, inspect providers, write a
consumer repository or remove staged content. Git hooks, fsmonitor, signature
helpers, replacement objects and lazy network reads are disabled for the new
gate's fixed metadata operations. Git subprocesses have finite timeouts and a
post-write spool-size check; this is **not** a claimed global disk quota.

## Operator path

1. Reconcile one bounded group with its canonical destination owner, preserving
   source history, licensing, useful content and sensitivity evidence.
2. Obtain actual owner validation and actual human disposition evidence. Record
   the exact source preimage and immutable destination in a proposed receipt.
   Review that receipt separately; no source is removed in its preparation PR.
3. After the receipt is present in the selected reviewed base, prepare the exact
   cleanup change. Regenerate the current CSV using `staging_home_audit.py`.
   Leave the durable receipt and historical approval bytes intact.
4. Review the actual base/head gate result and reconciled receipt report. A pass
   means source/data bindings match; human authority remains unauthenticated.
5. Complete the repository's holistic and owner-specific acceptance separately
   before any accepted drain or issue closeout. Keep remaining holds explicit.

Commands below are instructions for the later qualification phase; they were
not executed as part of this source implementation:

```bash
python3 tools/staging_home_audit.py --repository-root . \
  --output .audits/data/2026-08-15-staging-file-disposition.csv

python3 tools/staging_diff_gate.py --repository-root . \
  --base FULL_REVIEWED_BASE_SHA --head FULL_REVIEWED_HEAD_SHA \
  --report /tmp/empathy-staging-diff.json
```

The report is a new explicit file and is never overwritten. Using the same
exact commit for base/head produces a no-change reconciliation including
retained receipts. The old `staging_removal_gate.py --source-path` interface is
historical compatibility only; it is not the actual-diff CI gate.

## Workflow scheduling and qualification

The existing `Validate automation` workflow now schedules for `.staging/**`,
`migration/**`, both staging schema families, `tools/staging_*.py`, migration
docs, current `.audits` ledger changes and existing `tests/**` changes on both
PRs and main pushes. Its independent read-only `staging` job uses the exact PR
base/head, push before/after, or explicitly supplied manual `staging_base`.
It fetches complete source history without persisting checkout credentials.
The existing validation job remains independent, so a staging denial does not
suppress baseline-suite evidence. Publisher/security workflows and permissions
are unchanged; this job has no release, Pages, OIDC or deletion capability.

`tests/test_staging_diff_gate.py` authors disposable Git histories for denied
deletion/replacement/rename, same-change approval, stale blob, wrong destination,
receipt loss, stale generated ledger, dirty source, malformed authority/URL and
a valid Mantle-like exact-source binding. The fixture identities and destination
SHA are synthetic and never become production receipts. Tests do not edit,
delete, install or execute production staged files. Source scheduling checks
cover both filter lists; actual hosted scheduling remains separate evidence.

At the original functional checkpoint, only source/AST/JSON/schema/YAML metadata
review was performed. The later source-integration exception below records inert
inventory generation separately. Fixture execution, gate execution, canonical Ruff,
Mypy, Bandit, Secretlint, Lychee, holistic build/profile and hosted trigger/event
qualification remain unrun. No green gate, migration completion, authenticated
human acceptance or successful destination validation is claimed. Keep #112,
#118 and #79 open for their actual remaining acceptance.

ADR disposition: reference ADR-0001. This enforces the already documented
source-preservation and separately reviewed migration boundary without changing
specialist ownership or deciding a human lifecycle state.

## Source integration — 2026-11-12

This source composes merged baseline PR130 and Actions PR121. The original
validation job is retained, and the added staging job selects the same approved
Harden Runner `1d88384fd173af6ecb012dfd0264a306b711241a` with its existing
read-only/audit boundary. No staged source is removed or replaced.

The maintainer explicitly authorized necessary inert canonical CSV generation:

```bash
python3 tools/staging_home_audit.py --repository-root . \
  --output .audits/data/2026-08-15-staging-file-disposition.csv
```

The generator writes 9,583 inventory rows. The only row changed from the prior
current ledger is `.staging/misc/ROADMAP.md`: its preserved blob
`63816b7a5ef39aaa4970961c61a83e700ba484d3` differs from current
`tools/ROADMAP.md` blob `f46fa1ed9a7d41a8fb2a6db94d56941d805d742f`.
Its obsolete `duplicate_of` and duplicate-action metadata are cleared. The
classifier's explanatory note now identifies a historical duplicate candidate
and leaves current equality to the actual `duplicate_of` field. Other row
fields, source path/mode/blob identities, historical approvals and the new empty
receipt ledger are unchanged. A candidate classification is not removal proof.

This generation repairs pre-existing derived drift; it does not execute the
new gate, tests, fixtures or staged code, authenticate authority, validate a
destination, or demonstrate hosted scheduling. All qualification gates above
remain separate. Dated dependency inspection against source058 retains its
original CSV identity and is not rewritten as a new audit.
