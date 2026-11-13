# Actual pull-request staging qualification

Refs [Empathy #112](https://github.com/egohygiene/empathy/issues/112), parent
[#118](https://github.com/egohygiene/empathy/issues/118), graduation
[#79](https://github.com/egohygiene/empathy/issues/79).

This checkpoint qualifies the existing immutable staging gate on a real
`pull_request` event. It preserves the [migration contract](STAGING.md),
[durable source receipts](STAGING_RECEIPTS.md), frozen staged source and
historical approval bytes. It adds no removal or owner approval.

## Reviewable event evidence

The independent read-only `staging` job now writes its existing JSON report
outside the checkout and retains it for 30 days. The report identifies the exact
reviewed base and PR head, changes and retained receipt claims. A failed gate
does not create a successful report; a missing artifact is not a passing result.
Human authority remains `not-authenticated` even when all data bindings pass.

The declaration still covers staging, tools, schemas, receipt/approval files,
ledger and migration documentation. Both event path-filter lists have disposable
source regressions. This proposed qualification PR changes existing `.github/**` and
`docs/migration/**` trigger paths on the real provider; one actual event must not
be misrepresented as three separately executed path-class canaries.

## Actual PR-event checkpoint

At base `2202636a1957ee7598359465b4ae562e1c67358a`, all 27 staging tests passed
with zero skips, as did the exact unchanged base/head gate. Actual
[PR #141](https://github.com/egohygiene/empathy/pull/141) then scheduled
[run 43528478023/1](https://github.com/egohygiene/empathy/actions/runs/43528478023)
from a real `pull_request` event at head `4eaedc284ed7d7025c23ec7a93a2e08731f9435e`.

Staging job `132239988245` passed every step and retained artifact `14085398870`.
Its downloaded report exactly binds the PR base/head, contains no staged changes,
preserves three legacy claims and keeps authority `not-authenticated`. The ZIP
matches the provider SHA-256. The [bounded proof](STAGING_PR_EVENT_QUALIFICATION.json)
retains the actual event, job, artifact and report identities. A historical run's
PR association may reflect a newer head; its immutable `head_sha` and the exact
report supply the event binding.

The independent baseline job failed and retained artifact `14086436736`:
repository tests pass, the separate EgoLint command fails, and overall acceptance
remains unqualified. The original manual proof is not retimed or overwritten.

The first event also caught an incorrectly formatted author commit subject.
Only that owned-branch header was corrected with an explicit remote-head lease;
the source tree is identical. The initial event remains historical evidence.
After this evidence commit freezes, inspect its actual PR-event artifact, commit
policy and manual canonical holistic results separately on the PR. This document
cannot contain its own eventual commit identifier. Report publication remains
forbidden on this feature branch by the existing guard.

ADR disposition: reference ADR-0001. Retaining the existing gate output is
implementation and qualification of the accepted source-preservation boundary;
it changes no ownership, migration authority or human lifecycle state.
