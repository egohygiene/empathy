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

## Qualification checkpoint

At base `2202636a1957ee7598359465b4ae562e1c67358a`, all 27 staging tests passed
with zero skips. The exact unchanged base/head gate also passed and preserved
all historical claims. Actual PR-event execution, retained artifact inspection
and final-head canonical holistic review are pending; no hosted success is
claimed by this initial source preparation.

The baseline validation job is independent. Its failure does not suppress the
staging result and must remain visible in the overall workflow conclusion.
Report publication is forbidden on this feature branch by its existing guard.

ADR disposition: reference ADR-0001. Retaining the existing gate output is
implementation and qualification of the accepted source-preservation boundary;
it changes no ownership, migration authority or human lifecycle state.
