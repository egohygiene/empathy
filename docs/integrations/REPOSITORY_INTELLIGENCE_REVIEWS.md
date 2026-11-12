# Typed public Audits and Sanity feed

Refs [Empathy #105](https://github.com/egohygiene/empathy/issues/105),
[Pace #13](https://github.com/egohygiene/pace/issues/13) and
[organization #41](https://github.com/egohygiene/.github/issues/41).

Current source selection is Relay `d7c60473626f8dcc901210a208ad01a6474e8c1d`, the
documentation-only successor selected by PR #132. All current builder, capture,
feed, provenance, check and fixture references match that pin. The original
source-comparison receipt remains bound to its original PR #125 inputs below.

The original source-only consumer checkpoint starts from actual Empathy main
`eefbd80636544e34c69aa3038f3567f4f858b33a`, preserving the concurrent work after
the earlier source-feed integration. At that PR #125 checkpoint, builders, source/feed producers,
baseline/composition/receipt helpers, failure workflow and owner-contract/fixture
references select reviewed Relay `5d27be5ce1599df883e31f14cd894eb18622c18c`. The historical
rollback selections remain independently fixed.

## Explicit source plan and owner boundary

`.config/repository-intelligence/review-plan.json` is the typed public selection
plan. It currently selects no audit or sanity reports: both arrays are empty.
That is an explicit unavailable-evidence configuration, not a successful audit,
healthy repository, architecture acceptance or human ratification. No generated
report, artifact identity, baseline, placeholder source revision or future
approval is invented to populate the pages.

The `review-plan` manual input may select another committed, repository-relative
plan at the exact represented source. The default plan also applies to current
push captures. Plan schema is `egohygiene.relay.typed-review-plan/v1`, version
`1.0.0-alpha.1`, with exact public repository identity and `audits`/`sanity`
arrays of `{path, sha256}` selections. Report paths and raw byte digests must
refer to real immutable source Git objects. The runtime represented SHA is a
separate action input; a checked-in guessed/future SHA is never substituted.

Relay reads only selected immutable Git blobs, executes the exact pinned owner
validation/normalization closure outside the consumer and returns repository
Audits/Sanity models separately from fleet models. Empathy passes only the
repository model paths to the existing builder's `observatory-audits` and
`observatory-sanity` inputs. Canonical Markdown/report, profiles, classifications,
original report times, uncertainty and human-governance meanings remain with
Aether/Hygiene/Observatory. Empathy supplies no competing auditor or evaluator.

## Same source and clock as the native build

Only the existing `matrix.mode == current` push/manual source-capture paths
invoke the feed in Mindgarden. Its represented commit is the exact existing
`identity` output and its `as-of` is the actual `public_sources` capture output.
Both native generator calls reuse the exact same source artifact ID/digest,
review model paths and evaluation boundary. Duplicate generation does not rerun
the feed or acquire new reports under another clock. Actual original report
revisions and timestamps remain unchanged; a source capture does not make an
older report current or ratify its recommendation.

The standalone Intelligence workflow uses the same default/override plan only
on manual dispatch, binds `github.sha` and the same actual producer clock, and
passes its repository models to its existing generator. PRs, trusted
`workflow_run` events and the fixed historical rollback continue to skip the
capture/feed seam. Existing fork/event allowlists, matrix modes, producer refresh
semantics, job/step guards, permissions, dependencies and sole publisher remain.
Compare remains unselected without real compatible retained pairs and lease.

The feed model/receipt directory stays outside `.cache/mindgarden/site`.
A separate ordinary artifact retains it for seven days. Mindgarden also copies
the feed receipt into its existing composition evidence; the standalone sanitized
report artifact retains the receipt for30 days. No raw source packet, private
runtime or feed transport metadata is copied into Pages. Builder-owned normalized
receipts and full bundle inventory bind the public view to its admitted model.
Fixed `EMRI-012` diagnostics report only admission/retention failures, never
source paths, rejected identities, raw report text or provider exceptions.
Only the new feed retention steps use `always()` with a nonempty produced-path
guard, so the shared feed's bounded denial receipt can survive failed admission.
This preserves evidence without authorizing a skipped builder or changing the
existing publication job's required results.

## Preserved history and qualification

The original source checkpoints in the neighboring guides retain their historical
pins and observations. The original typed-feed selection above is historical;
the current documentation-only successor is recorded at the top. The frozen
consumer SHA `254185272ab27b6858b8b0393af6549c205c9a8d`, Relay
`b71b090406a3a9e4cd9f107e9d14a623bbecb127`, complete-site digest
`sha256:1e92a0a74c154bbc3c339a6ef1764852bfcceba1a58b294e238b4a0331f94498`,
verifier bytes, rollback mode, basename/timezone constraints and recovery ordering
remain unchanged. The public product mount remains `/empathy/`; no publication
origin, gate, deployment authority or retained rollback point is changed.

ADR-0001 governs pinned specialist consumption; this changes consumer source
selection and composition within that existing boundary, so no new ADR is
required. Current test fixture pin constants follow the same owner source;
test assertions/behavior and canonical scanner payloads are preserved.

Only static source, unique-key YAML/JSON, embedded script parsing and exact old
guard/frozen-byte comparisons are authoring evidence. Tests, holistic lint,
owner/native/helper execution, builds, actual provider/artifact transport, CI,
browser/publication/recovery checks and new baseline selection remain deferred
at the maintainer's request. Source implementation does not close acceptance.
The [source comparison record](REPOSITORY_INTELLIGENCE_REVIEW_SOURCE_PROOF.json)
retains the exact starting revision, unchanged guard counts, helper/frozen-byte
hashes and deferred checks. This is a review candidate; no merge, deployment or
new live qualification is claimed.

## Documentation-only source reconciliation — 2026-11-12

PR #132 starts from Empathy `0f0669739ae173ec8b374103a915c71968ac9304`.
The owner diff from the original typed-feed source to the selected successor
contains exactly one commit and only `CONTINUITY.md`. Every executable action,
workflow, helper, owner lock and contract retains its exact bytes. This does not
turn a reachable candidate into an upstream release, merge or runtime result.

The automatic update changed eight uses across three workflows. Consumer
reconciliation also binds all three native builders, the current environment
revision, explicit provenance inputs, owner-contract checkout/report identity
and the three fixture constants to the same successor. All other workflow
fields, original clocks, guards, unavailable report plan and publication paths
remain unchanged. Frozen recovery identities, verifier bytes and the original
PR #125 source-comparison JSON remain byte-identical. Its `current_relay_revision`
field describes the original comparison, not this later source selection.

Only source, syntax, hash/tree and schema-metadata checks were performed for this
update. No generation, helper/native consumer, tests, lint, build, CI or actual
artifact/publication/recovery qualification was run. Existing acceptance and
human-source holds remain separate from this source reconciliation.
