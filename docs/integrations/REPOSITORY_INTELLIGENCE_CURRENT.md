# Current Repository Intelligence candidate

Current source selection is now the
[native Journey/attributed Search candidate](REPOSITORY_INTELLIGENCE_NATIVE_SEARCH.md),
using Relay `9358083e6dd8b15a0f2a3bb23c0b1e2b3ea3b2ff`.
The portable-only source checkpoint below is retained as history from #122;
its old pin and source-disabled description do not describe the new candidate.

## Historical portable-only checkpoint

This is the source handoff for
[Empathy #105](https://github.com/egohygiene/empathy/issues/105), prepared on
2026-11-09 from Empathy main
`1df3f6ab11d724f01d169c13ed2b1acb2babdc6a`.
It selects the shared portable Relay implementation at
`49046d88ef6fe2e31e9a9f443a61157b598efb78`, under review in
[Relay #167](https://github.com/egohygiene/relay/pull/167).
This is an unqualified draft consumer candidate, not deployment or live proof.

## Current source selection

The composed current generator, its duplicate build, and the standalone
artifact-only generator use the same full Relay SHA. Current baseline capture,
composition validation, receipt finalization and the intentional-failure
reusable workflow select that exact source too. The owner-contract checkout,
contract report identity and existing test fixture pin constants match it.
Only their source-selection metadata changes; existing test behavior is retained.
Relay's release metadata still says `v1.6.0`; the full commit above identifies
this candidate and does not assert that a new release was published.

Both consumer calls retain their original inputs. No native ADR/Roadmap
collection, capture plan/artifact intake, Observatory snapshot or comparison is
enabled. Semantic routes and the graph must show unavailable source states
where evidence is absent. Existing `.reports` payloads retain their original
scanner commits, execution states, findings and freshness. In particular,
MegaLinter/OSV source mismatch and missing Scorecard remain
[Empathy #98](https://github.com/egohygiene/empathy/issues/98), not a green claim
created by this pin change.

The existing Mindgarden reviewed/public boundary, Quartz revision, complete
consumer composition, output/work directories, product routes/assets, workflow
events, jobs, status guards, retention, permissions and sole Pages deployer are
preserved. No deployment or producer scheduling is redesigned. The separate
Mindgarden standalone-consumer PR #120 changes other files and remains
independent.

## Historical rollback remains fixed

The completed #94 canary and its historical rollback stay bound to their
recorded evidence. The rollback source is still
`254185272ab27b6858b8b0393af6549c205c9a8d`, Relay is still
`b71b090406a3a9e4cd9f107e9d14a623bbecb127`, and the original complete-site
digest is still
`sha256:1e92a0a74c154bbc3c339a6ef1764852bfcceba1a58b294e238b4a0331f94498`.
The rollback verifier and immutable baseline contract are unchanged. Preserve
the existing `rollback-v1.4` then immediate `current` recovery sequence in the
[publication guide](REPOSITORY_INTELLIGENCE.md#fixed-historical-rollback).
This candidate does not establish a replacement rollback point.

## Review and qualification still required

The user deferred tests, builds, runtime/consumer execution, browser checks and
CI. This handoff records source and syntax inspection only. No generator,
workflow, deployment, live probe, holistic profile or rollback rehearsal was
run for this candidate. Existing policy and workflow gates are unchanged.

Static inspection parsed four changed workflows with duplicate-key rejection
and compared their parsed definitions with the starting source after only the
declared current-pin replacements and explanatory comment. Three existing
Python fixture files parsed and differ only in their current pin constants.
Both publication/rollback helpers retain their exact starting bytes, and
`git diff --check` passed. These checks do not exercise workflow behavior.
An independent source-only peer pass found no scoped must-fix in the pin,
workflow-boundary or documentation changes.

Before readiness, follow the
[publication validation and acceptance sequence](REPOSITORY_INTELLIGENCE.md#validation-and-post-merge-acceptance)
on the exact review head. Keep current and historical rollback compositions
separate; verify consumer route/asset bytes, fresh checkout-name portability,
actual skipped-ancestor scheduling and forbidden/no-op lanes, negative-path
retention, deterministic bundle/provenance and the canonical holistic profile.
The existing twelve core Intelligence live probes are unchanged; qualify the
candidate's additional routes, aliases and graph asset behavior explicitly.
After separate merge/publication authorization, record actual build, upload,
deployment, receipt and live route/asset identity, navigation/logo/favicon,
rollback and restored-current evidence on #105. Preserve #94 as completed and
hand only actual new evidence to Relay #109/#106 and Pace #13.

Refs [organization parent #41](https://github.com/egohygiene/.github/issues/41).
