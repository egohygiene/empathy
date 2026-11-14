# SVG navigation source checkpoint

The current consumer selects immutable Relay
`2d0d88bdcfa1c9614a9a6bf7f66b26a397dfec2a`, ordinarily merged through
[Relay #190](https://github.com/egohygiene/relay/pull/190) for
[owner issue #189](https://github.com/egohygiene/relay/issues/189).
This is a new consumer source cycle from Empathy
`498aef8e64d876118d63db81823552e205e0b0b4`; earlier source, scanner,
publication and recovery receipts retain their original identities.

## Behavior and ownership

Actual browser inspection found that assigning a native SVG anchor's `href`
property throws. The shared page initializer then stops before registering
later filter and entity listeners, and graph focus/pointer inspection can fail
at the same boundary. Relay changes three writes to `setAttribute` using the
existing validated destination. HTML and SVG links keep the same URL policy,
query and entity context; Empathy copies no renderer implementation.

The [owner guide](https://github.com/egohygiene/relay/blob/2d0d88bdcfa1c9614a9a6bf7f66b26a397dfec2a/docs/svg-context-navigation-2026-11-14.md)
and [bounded evidence](https://github.com/egohygiene/relay/blob/2d0d88bdcfa1c9614a9a6bf7f66b26a397dfec2a/docs/evidence/2026-11-14-svg-context-navigation.json)
retain 18 real Chromium fixture assertions and independent old/new controls.
Separate retained-consumer DOM checks include actual Enter navigation and
pointer clicks. Those derived local fixtures do not establish canonical live
acceptance for this consumer source.

## Current and historical boundaries

Current standalone, composed, duplicate, capture, typed-feed, provenance,
failure and contract-check selections use the same full owner revision.
The three current normalizer calls select it too; normalizer behavior and
report/source admission remain unchanged. No workflow event, permission,
guard, capture plan or native-domain selection changes in this consumer slice.

All four snapshot publisher selections remain at
`1eada5142f7fc7da7862f335589e3b8f5884ffaf`: the three report producers and the
independent architecture producer. Historical rollback remains at consumer
`254185272ab27b6858b8b0393af6549c205c9a8d` and Relay
`b71b090406a3a9e4cd9f107e9d14a623bbecb127`, with original composed digest
`sha256:1e92a0a74c154bbc3c339a6ef1764852bfcceba1a58b294e238b4a0331f94498`.
The fixed verifier, protected adoption/configuration bytes, staging/migration
trees and accepted local-CI/foundation 2.1 integration remain unchanged.
The [dated batch checkpoint](REPOSITORY_INTELLIGENCE_BATCH10.json) remains
bound to its original source and Relay pin.

## Qualification and acceptance

The local consumer candidate passed all 95 equipped contract tests with zero
skips against this exact owner checkout. Its checked-in Chromium fixture passed
all 18 assertions with zero page errors on Chromium `151.0.7922.173`. These are
local fixture results, separate from provider and canonical live evidence.
Canonical Ruff `0.16.5`, Mypy `1.19.1` and Bandit `1.9.4` checks passed on the
three changed Python fixture files; existing redundant suppression notices
remain diagnostic output. Reversing only the declared workflow pins reproduces
the base definitions, and the protected source bytes remain identical.

Record the exact review-head holistic profile and actual read-only PR
compositions separately. Inherited lint findings remain
separate from introduced diagnostics; owner unit-suite baseline failures are
not converted into passing checks.

After ordinary consumer integration, freeze the actual new main revision and
produce fresh matching report artifacts. Qualify current publication, native
receipts, declared-input portability and canonical browser behavior at that
source. Exercise native SVG focus, pointer interaction and Enter navigation,
alongside HTML parity, filter/hash listeners, logos, visible focus and favicon.
Record actual source/run/artifact/receipt/live outcomes on
[Empathy #98](https://github.com/egohygiene/empathy/issues/98) and
[#105](https://github.com/egohygiene/empathy/issues/105), tracked by
[#118](https://github.com/egohygiene/empathy/issues/118). The completed #94
canary, unrelated #110 runtime/catalog work and #79 graduation keep their scopes.
No S2 report or publication is relabelled as evidence for this successor.

Decision impact: no new ADR. Empathy consumes the existing specialist repair
under [ADR-0001](../decisions/ADR-0001-foundation-ownership.md).
