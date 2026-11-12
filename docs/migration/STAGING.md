# Staging migration contract

Status: frozen for unrecorded intake  
Contract version: 1.0.0  
Freeze accepted: 2026-08-18  
Tracking issue: <https://github.com/egohygiene/empathy/issues/59>

## Purpose

`.staging/` is a finite intake reservoir used while independently owned Ego
Hygiene capabilities are extracted and reconciled. It is not an active source
tree and no active build, task, hook, workflow, or runtime path may depend on
it.

The existing file-level audit remains the canonical disposition ledger:

```text
.audits/data/2026-08-15-staging-file-disposition.csv
```

The date in the filename identifies the audit series, not a frozen snapshot.
The generator refreshes it as approved migrations and newly classified intake
land.

## Freeze rule

New intake is permitted only when the same pull request:

1. explains why the material cannot go directly to its owner;
2. adds a specific classifier rule with owner, incubation home, canonical home,
   trust class, disposition, merge group, and exit criteria;
3. refreshes the checked-in file ledger;
4. keeps executable, privileged, community, generated, and secret-adjacent
   material inert; and
5. adds or updates contract tests.

An unclassified path fails validation. A broad `manual-review` bucket does not
count as classification.

## Ledger fields

Every tracked staged file records:

- Git blob identity, mode, byte size, and detected kind;
- canonical owner, incubation path, proposed canonical path, and merge group;
- trust class, sensitivity, duplicate relationship, and provenance state;
- migration state and explicit exit criteria; and
- destination evidence and deletion approval fields, which remain empty until
  a later migration is verified.

The generated CSV is reviewable in Git. JSON and summary JSON projections are
available for automation without adding another canonical data source.

## Migration states

- `inventoried`: assigned and inert, with semantic migration still required.
- `quarantined`: third-party, executable, prompt, generated, or otherwise
  restricted material requiring additional review.
- `candidate-removal`: a duplicate or obsolete candidate, not permission to
  delete it.
- `verified`: reserved for a later migration after destination evidence and
  owner validation are recorded.

## Drain workflow

Migrate one bounded merge group at a time:

1. Copy or reconstruct the material in the owner's repository without
   activating unreviewed content.
2. Preserve upstream source, revision, license, authorship, and the Empathy
   source blob where applicable.
3. Refactor and validate the owner-owned result independently.
4. Record the immutable destination revision and validation evidence.
5. Open a separate Empathy cleanup change.
6. Prepare the exact source/destination receipt and actual human evidence in a
   separate review, before the cleanup base. Historical approval claims remain
   preserved; the new receipt file initially contains no invented approvals.
7. Review the actual immutable base/head preimages through the
   [durable receipt and diff gate](STAGING_RECEIPTS.md). A receipt introduced in
   the deletion change cannot authorize that change; the gate never authenticates
   human authority.
8. Refresh the ledger and confirm the file count decreases by the intended
   amount only.

Never clear `.staging` in a bulk cleanup commit.

## Commands

Refresh and verify the canonical CSV:

```bash
python3 tools/staging_home_audit.py \
  --repository-root "." \
  --output ".audits/data/2026-08-15-staging-file-disposition.csv"

python3 tools/staging_home_audit.py \
  --repository-root "." \
  --output ".audits/data/2026-08-15-staging-file-disposition.csv" \
  --check
```

Produce a non-canonical summary for review:

```bash
python3 tools/staging_home_audit.py \
  --repository-root "." \
  --format "summary-json" \
  --output "/tmp/empathy-staging-summary.json"
```

The historical manual path interface remains available for compatibility:

```bash
python3 tools/staging_removal_gate.py \
  --repository-root "." \
  --approvals "migration/staging-removal-approvals.json" \
  --source-path ".staging/example/path"
```

New cleanup changes use `tools/staging_diff_gate.py --base FULL_BASE_SHA --head
FULL_HEAD_SHA` as described in the [operator path](STAGING_RECEIPTS.md). It checks
actual removed/replaced Git preimages, immutable source/receipt bindings and
committed current-ledger freshness. Durable receipt claims survive regeneration
and removal of the corresponding current CSV row. No production deletion or
approval is performed by either command.

## Definition of drained

Staging is drained only when the tracked file count is zero, every migration
has immutable owner evidence, rejected material has an approved archival or
deletion disposition, and active Empathy consumes released owner artifacts
instead of relative source copies.
