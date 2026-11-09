# Public GitHub source feeds

This implementation checkpoint starts from Empathy main
`322f8d0a6657ea8584c80fb688aeaf6ac2184ca7`, which merged the native
Journey/attributed Search selection in #123. The current Relay source is
`94e3a3a4a18f9ced7b3694fe258ae397eed55953`; final review must retain one exact
reviewed immutable pin across the source producer, generators and provenance
helpers. Refs [Empathy #105](https://github.com/egohygiene/empathy/issues/105),
[Relay #146](https://github.com/egohygiene/relay/issues/146),
[#149](https://github.com/egohygiene/relay/issues/149),
[#150](https://github.com/egohygiene/relay/issues/150), and
[organization #41](https://github.com/egohygiene/.github/issues/41).

## Selected production path

The existing current Mindgarden build acquires public Work, Health and Releases
captures on `push` and `workflow_dispatch`. Those successfully uploaded capture
paths also select `collect-dependencies`, using the same actual post-capture
evaluation boundary for Hygiene
`49639c1845cdfd08fbd5a768261a8b3cf515f80f` public catalog admission. The earlier
commit-time clock on PR/workflow-run paths cannot bind that later catalog, so
those paths leave the dependency source off. Declared `depends-on` edges are
authored owner evidence, without runtime adoption or a new inventory coverage
domain. The standalone artifact workflow
does the same on manual dispatch. The pinned Relay source producer checks
unauthenticated public repository identity before and after its bounded reads,
verifies the exact represented Git/API commit, and writes only allowlisted JSON
transport captures. The next existing ordinary artifact upload retains the
closed same-run/head/attempt bundle for seven days. Both composed generator
calls receive the same exact immutable artifact ID/digest and actual `as-of`
boundary, so duplicate verification replays the original captures and does not
query GitHub twice.

The build jobs add only `actions: read`, `issues: read`, `pull-requests: read`
and `checks: read`. The existing `contents: read` and Pages read boundaries
remain. No source-provider write, secret inheritance, consumer-code execution
or new deployment authority is added. The separately pinned producer receives
the existing job token only for selected public issue/PR/check reads; release,
asset and visibility reads remain unauthenticated and cannot expose drafts.
Public provider titles/check names are explicitly selected; their bounded
sanitization and escaping remain owned by Relay and the downstream renderer.
Bodies, comments, actors, emails, labels, app objects and logs are excluded.

The capture seam currently supports `push` and `workflow_dispatch` events.
PRs, trusted producer `workflow_run` refreshes and frozen rollback rebuilds
retain their existing no-capture source path. Trusted failed-producer refresh
remains admitted by its original allowlist and status policy. Extending exact
capture transport to `workflow_run` requires separately reviewed provider-head
binding; this checkpoint does not relabel another run or event as the current
capture producer. No event, job dependency, publication guard, skip/failure gate,
timeout or existing artifact retention is weakened.

## Evidence meaning

Work keeps separate issue and PR records, original states/closure reasons and
pagination. It infers no relationships or completion from bodies or merges.
Health captures check runs only at the exact consumer SHA; matching execution
states and conclusions remain independent of source completeness. The
applicable producer inventory stays partial. Releases resolves public tag refs
to actual Git commits and retains public asset metadata and supplied digests;
unavailable historical Git objects or incomplete asset inventories remain
partial. Deployments and install verification remain uncollected.

Existing `.reports` summaries retain their literal original scanner revisions,
execution/findings and freshness. This checkpoint does not feed unbound or
mismatched scanner results into a supposedly current Health source. The OSV/
MegaLinter mismatch and missing Scorecard remain owned by Empathy #98. Source
coverage, check outcomes, actual release publication, Pages deployment and human
acceptance remain separate claims.

The producer receipt is retained outside the public site in the existing
provenance artifact (or beside the standalone sanitized run report). It contains
fixed collection outcomes, original clocks, source/implementation/file hashes
and bounded pagination. The public bundle contains only owner-normalized
evidence, not raw captures, provider responses or transport credentials.

## Review boundary

ADR-0001 governs pinned specialist consumption; no new ownership decision is
introduced. Current helpers and fixture pin constants follow the reviewed
source; test assertions remain unchanged. The frozen rollback generator,
consumer revision, site digest, verifier bytes and recovery sequence remain
fixed. Native Journey and attributed Search stay enabled on current paths;
no ADR/Roadmap or retained Compare baseline is selected.

Static YAML/shell/Python parsing, pin/input inspection, and comparison of the
unchanged publication/rollback gates are the scoped review evidence. Tests,
holistic lint, native acquisition/collection/builds, provider/artifact canaries,
browser checks, actual duplicate payload equality, publication and recovery
qualification remain deferred at the maintainer's request. Empathy #105 stays
open; no deployment or completed acceptance is claimed. There is no root
`CONTINUITY.md` in the starting repository; this bounded integration document
records the handoff without inventing a prior checkpoint.
