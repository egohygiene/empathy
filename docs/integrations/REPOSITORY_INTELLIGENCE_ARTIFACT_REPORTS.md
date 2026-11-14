# Exact-source report artifacts

Refs [Empathy #98](https://github.com/egohygiene/empathy/issues/98),
[#105](https://github.com/egohygiene/empathy/issues/105) and
[parent #118](https://github.com/egohygiene/empathy/issues/118).

## Source boundary and ownership

An actual scan of source **S** does not describe a later Git snapshot commit
**P**. Relay's existing source equality remains mandatory. The normalizers and
native report reader are unchanged; this consumer adds explicit provider
admission and a private input directory for their original summary bytes.

Each existing producer retains a dedicated immutable artifact containing only
its normalized `summary.json`. Its name is
`empathy-report-<producer>-<run-id>-<attempt>`. Existing raw artifacts and stable
snapshot defaults remain. Manual producer input `publish-snapshot` defaults
to **true**; explicitly setting it to **false** denies the sole snapshot-write
job while retaining the actual scan, native normalization and summary artifact.
Scorecard normalization runs in a read-only job at the actual scanned source;
its separate write job consumes that same-run normalized artifact.

For artifact-only runs, the existing normalizer's `detail-url` input links to
the actual producer run, which holds the source-bound summary. It does not link
to an older committed summary under the same path. Generation time, freshness,
source, execution and finding states remain literal original report evidence.

## Explicit selection

The standalone and composed workflows accept optional manual input
`report-artifacts`. Empty input retains the original committed `.reports`
selection. A nonempty input is a JSON object with exactly:

- `schema`: `empathy.repository-intelligence-report-artifact-selection/v1`;
- `reports`: one to three entries, with no duplicate producer.

Each entry has exactly these fields:

| Field                   | Required identity                                       |
| ----------------------- | ------------------------------------------------------- |
| `producer`              | `osv`, `megalinter` or `scorecard`                      |
| `run_id`, `run_attempt` | Actual positive integer producer run and attempt        |
| `artifact_id`           | Actual positive integer dedicated-summary artifact ID   |
| `archive_sha256`        | Lowercase SHA-256 of the retained ZIP, without a prefix |
| `summary_sha256`        | Lowercase SHA-256 of its exact `summary.json` bytes     |

The one local [consumer action](../../.github/actions/report-artifacts/action.yml)
admits only completed runs of the three named workflows, from this repository
and its default branch, at the **actual current checkout SHA**. The reviewed
attempt, artifact name/ID, expiry, bounded size, digest and artifact run/source
binding must all match. Failed producer conclusions can supply truthful failed
execution or finding evidence; cancellation and unfinished runs are rejected.

The existing pinned download action uses `digest-mismatch: error`. Afterward,
the adapter requires exactly one regular `summary.json` per selected artifact,
checks its reviewed payload digest and original source/run/provenance, and
stages its unchanged bytes under ignored
`.cache/repository-intelligence-publication/selected-reports`. Omitted producers
remain absent in this explicit selection. Invalid selections fail the build;
they cannot silently fall back to committed historical evidence.

Only the existing Relay reader validates and projects report semantics. Both
current composed builds consume the same staged directory, so duplicate
generation uses identical reports. Selection provenance and input hashes stay
outside the public site. The composed workflow copies the unchanged admission
receipt into its existing private publication evidence directory, preserving
the archive root expected by receipt finalization and live-verification jobs.
The rollback generator call and original #94 bytes, pins, digest and recovery
order are unchanged. A nonempty artifact selection
is rejected for historical rollback.

## Frozen-source execution

1. Review and integrate all consumer changes before freezing source **S**. Do
   not add a report-selection Git commit after the scans: selections are
   explicit manual inputs, and their receipts are retained artifacts.
1. Dispatch the existing three producers on main at **S**, each with
   `publish-snapshot: false`. Keep ordinary severity and lint policies. Wait
   for actual scan, normalization and artifact stages; verify each snapshot
   writer is skipped and main remains **S**.
1. Inspect the actual retained artifact archives and compute both digests.
   Build the closed selection above from those real provider identities.
1. Dispatch the standalone Intelligence workflow on main with that selection.
   Review its summary, source identity, exact inputs and native report states
   before publication. Standalone remains artifact-only.
1. After root review, dispatch `Publish Mindgarden`, `mode: current`, on the
   same source with the same selection. Inspect build, upload, deployment,
   separate receipt and live verification individually. A green workflow with
   skipped descendants does not establish publication.
1. During the separately authorized fixed rollback rehearsal, retain the real
   old identity and restore `current` immediately. Supply the same selection
   on the restored current run while source **S** remains unchanged.
1. Record final external run/artifact/live evidence in the work tracker and
   organization review packet. A documentation-only Empathy commit after the
   freeze creates a new source boundary and needs fresh evidence.

Ordinary producer-refresh behavior remains independent. A failed trusted
producer can still trigger the existing refresh and preserve failure metadata;
the final explicitly selected build must run after those refreshes. No report
snapshot is relabelled, retimed or promoted into a successful scan.

## Qualification checkpoint

Initial real feature-branch runs at source
`2202636a1957ee7598359465b4ae562e1c67358a` reached native source collection:
[standalone 43528374754](https://github.com/egohygiene/empathy/actions/runs/43528374754)
and [composed 43528378294](https://github.com/egohygiene/empathy/actions/runs/43528378294).
Capture, retention and typed review feed passed; Quartz also passed in the
composed run. Both builders then denied `collection-validation-normalization`.
Publication/configuration/deployment were correctly skipped. These are
historical negative/control receipts; they do not establish live qualification.

Independent native replay identified missing relationship-policy admission for
the declared Empathy-to-Mantle and Empathy-to-EgoLint dependencies. Hygiene
[#119](https://github.com/egohygiene/hygiene/pull/119) reconciles only those
memberships. A separate actual PR-source failure exposed a native Journey
frontier discrepancy: 256 original objects were captured but only 255 inspected.
Relay [#183](https://github.com/egohygiene/relay/pull/183) authenticates all 256
original objects in disjoint reachable batches under one bounded deadline;
[#184](https://github.com/egohygiene/relay/pull/184) combines the compatible exact
Hygiene profile and chronological event composition. The preceding combined
source was immutable Relay `d7604056e36633a59735318454f20f2984602726`. Its actual captured
Empathy previews at `382508fe2fbdfb37777a005aa71ddd3af56485c3` denied the typed
feed with `PIN`: the current Hygiene627 admission differed from the historical
Hygiene496 profile locked by Observatory. Relay
[#185](https://github.com/egohygiene/relay/pull/185) separately authenticates
that historical profile, preserving strict equality, public ownership and
original Observatory contracts while retaining the current dependency profile.
Current consumers select immutable Relay `95105a9f5d99239af0d44d7dbd796fd1507fef31`.
Dependencies remain enabled, selected Journey objects are not pruned, and source
equality is unchanged. Owner replay and different-checkout byte equality do not
replace final aggregate consumer, provider and live qualification.

The caller retains only the owner's closed `source-build-failure/v1`
diagnostic when available. Raw native working trees, captures, exceptions,
credentials and filesystem paths do not enter that diagnostic artifact.

Local focused checks cover strict provider/source/artifact admission, literal
payload staging, missing/extra/symlink/digest/provenance failures, guarded
artifact-only producers and unchanged native mismatch/rollback protections.
The exact review-head holistic run and actual frozen-source producer → preview
→ live cycle remain separate acceptance evidence. #98 and #105 stay open until
their complete required evidence is observed.

Decision impact: **ADR not required**. This is Empathy-owned admission and
qualification of existing pinned producer/reader contracts under
[ADR-0001](../decisions/ADR-0001-foundation-ownership.md); it changes no canonical
owner, report schema, source equality, human disposition or deployment owner.
