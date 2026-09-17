# File-contract iteration 01: gitignore

This checkpoint captures the first use of the process in
[the organization master epic](https://github.com/egohygiene/.github/issues/32).
Keep cross-repository status in that epic and implementation evidence in
[Empathy #82](https://github.com/egohygiene/empathy/issues/82) and its PRs.

## Working agreement

Work on one logical file and one bounded outcome per PR. Supporting tests and
documentation belong with that outcome. Present the PR and stop for maintainer
review and merge. After the maintainer syncs, verify the actual merged state
before taking the next part. Do not close an issue from a partial PR.

## Repeatable process

1. **Inspect:** read live issues/PRs, instructions, architecture, decisions,
   contracts, roadmap, and any continuity record. Record the source revision and
   existing failures. Reuse an existing issue when its scope matches.
2. **Define:** record purpose, applicability, canonical owner, content model,
   permitted variation, update behavior, and validation. Choose the smallest
   reviewable outcome and identify real prerequisites.
3. **Implement and prove:** change the canonical source and add meaningful
   behavioral checks. Include both required behavior and content that must
   remain usable. Update affected projections only through their generators.
4. **Review and checkpoint:** inspect the whole diff, run relevant checks, link
   the PR, distinguish new failures from existing ones, and record incomplete
   acceptance criteria and the exact next action. Keep the epic ledger current.
5. **Resume after merge:** reread review decisions and live default branches;
   confirm what actually landed. Update the checkpoint and continue to the
   next bounded part. Adopt in Filament only after the upstream contract is ready.

This is a working example of the epic's process, not a new organization policy
or a separate universal continuity-file requirement. Extract portable guidance
into its established owner after more file iterations prove it useful.

## Part 1 checkpoint at original handoff

| Item            | Recorded state                                                                                                             |
| --------------- | -------------------------------------------------------------------------------------------------------------------------- |
| Date            | 2026-09-17                                                                                                                 |
| Source          | Empathy `16f260324219f2d437b2a4c19c961896274e29df`                                                                         |
| Scope           | Existing-rule audit, universal candidate, actual Git behavior checks, and this process record.                             |
| Review decision | Accept or revise the 27 candidate rules, proposed relocations, environment-template suffixes, and private local namespace. |
| Root/catalog    | Existing root, catalog, golden manifest, inventory, and EgoLint projection are unchanged in this part.                     |
| Consumer        | Filament adoption is pending the completed upstream contract.                                                              |
| Architecture    | Preserves existing foundation/specialist ownership; proposed choices remain under review.                                  |
| Roadmap         | Contributes to `EMP-Q04`; does not complete its profile acceptance criteria or advance strategic status.                   |
| Continuity      | No root `CONTINUITY.md` was present at inspection; this scoped checkpoint and the epic provide the handoff.                |
| Evidence        | Commands and exact results belong in the linked PR; no claim of all-green CI or complete #82 acceptance.                   |

## Merge verification and validation correction

[PR #85](https://github.com/egohygiene/empathy/pull/85) merged on 2026-09-17 as
`52d7231413b5920a6de410460710dbea73a58daf`. The baseline source proposal and
audit are accepted; profile composition and consumer adoption remain pending.

Post-merge inspection found two new Ruff findings in the test harness in the
[completed MegaLinter run](https://github.com/egohygiene/empathy/actions/runs/35226310235).
The original local check used the root configuration, while CI uses
`egolint/.config/lint/python/ruff.toml`. The follow-up uses tuple unpacking for
the fixture cases and documents a call-specific `S603` exception for the
test-controlled Git subprocess. The Git behavior and fixture coverage stay the same.

This changes the process: validate with the actual CI configuration and inspect
completed CI results. A passing local command or a merged PR does not establish
that those checks passed. The known catalog/workflow pin mismatch remains a
separate failure; this correction does not claim all-green repository CI.

After the correction is reviewed, take profile composition and contract
integration as the next bounded PR. Keep golden-root adoption in a later PR so
the composition model can be reviewed before its migration effects.

## Edges learned in this part

- File presence and content conformance are separate. The catalog already
  requires `.gitignore`; that alone does not establish safe rules.
- A broad ignore can hide source as easily as generated output. Test visible
  paths as carefully as ignored ones, using actual untracked fixtures.
- Git negations and excluded parents need behavior checks. Text inspection
  alone would miss ineffective `.gitkeep` exceptions and nested overrides.
- Private file extensions need a migration plan before live protections change.
  An experimental candidate is not a drop-in replacement for the active root.
- Full repository tests need the complete checkout: sparse paths initially
  caused missing-fixture errors. Rechecking the complete unchanged base separated
  those checkout artifacts from the real existing MegaLinter pin mismatch.
- A candidate source must trigger CI even before it is used by a consumer.
- Merging this part accepts a bounded source proposal; it does not prove
  materialization, reusable CI conformance, or fleet adoption.

## Next bounded part after review

Reverify the merged part 1 PR and its validation correction. Then prepare one
Empathy PR for scoped profile composition and deterministic contract integration:

- Define the artifact identity, composition order, preservation, provenance,
  and rollback behavior using the existing foundation catalog/manifest model.
- Give applicable overlays explicit owners, selection conditions, and project
  roots. A selected Rust project can ignore its own `/target/` without hiding
  source under an unrelated `target/` directory.
- Regenerate affected inventory/EgoLint projections and prove repeatability,
  profile scope, and local exceptions in composition fixtures.

A subsequent PR migrates Empathy's active root. Before that change, resolve every
remaining audit relocation against actual project roots and keep private-material
protection explicit and tested. Check for newly visible untracked files without
exposing contents. Keep #82 open until its full acceptance criteria are met.
Holon and Pace follow-ups and the Filament PR come after contract acceptance,
as #82 requires.

Fresh-chat entry: open the master epic, follow iteration 01 to the latest PR,
verify whether it merged, read its review decisions and this checkpoint, then
continue exactly one authorized part. Do not infer acceptance from this document
or start a different file without the maintainer selecting it.
