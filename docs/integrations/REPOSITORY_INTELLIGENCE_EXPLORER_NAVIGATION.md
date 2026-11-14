# Dashboard explorer navigation source checkpoint

Current consumer paths select immutable Relay
`41fe97bc69e44fdaff6b6c34ae28e4d2af22e41b`, ordinarily merged through
[Relay #191](https://github.com/egohygiene/relay/pull/191) for
[owner issue #189](https://github.com/egohygiene/relay/issues/189).
This successor starts from Empathy
`88667126133cdec5843bf22a09b1ef40b493f5f9`.

## Observed behavior and owner correction

The preceding source passed producer, publication and HTTP byte checks, but
actual browser inspection found a separate dashboard exception. That page loads
`explorer.js` instead of `site.js`; two duplicated context-link writes still
assigned the getter-only SVG `href` property. Initial link context could remain
absent even though the earlier graph repair enabled later focus/navigation.
The optional tree controls were unselected and do not explain that finding.

The owner changes those two writes to `setAttribute` using the existing
validated destination. Accepted site/graph assets and URL/context allowlists
remain unchanged. Empathy consumes the repair without copying implementation.
The [owner checkpoint](https://github.com/egohygiene/relay/blob/41fe97bc69e44fdaff6b6c34ae28e4d2af22e41b/docs/dashboard-svg-context-2026-11-14.md)
records the complete existing-asset audit and derived retained-consumer checks.

At this exact merged owner pin, the checked-in real Chromium driver passes all
18 generated Intelligence pages and 23 assertions with zero page errors. It
checks served script bytes, initial dashboard query/entity context before focus,
native SVG focus, pointer and Enter navigation, shared filters/hash handling
and HTML/SVG parity. These local fixtures remain separate from canonical Pages
acceptance and make no claim about future markup or unselected optional views.

## Preserved boundaries and remaining acceptance

Current standalone, composed, duplicate, capture, typed-feed, provenance,
failure, normalizer and fixture selections use the same full owner revision.
Workflow events, permissions, guards and native-domain selections are unchanged.
All four snapshot publisher calls remain at
`1eada5142f7fc7da7862f335589e3b8f5884ffaf`.

Historical rollback remains consumer
`254185272ab27b6858b8b0393af6549c205c9a8d`, Relay
`b71b090406a3a9e4cd9f107e9d14a623bbecb127`, and original composed digest
`sha256:1e92a0a74c154bbc3c339a6ef1764852bfcceba1a58b294e238b4a0331f94498`.
Its verifier, protected adoption/configuration bytes, staging/migration trees
and accepted local-CI/foundation integration are preserved. The earlier
[SVG source checkpoint](REPOSITORY_INTELLIGENCE_SVG_NAVIGATION.md) and
[dated batch evidence](REPOSITORY_INTELLIGENCE_BATCH10.json) retain their
original pins, subjects, clocks and outcomes.

Record equipped consumer contracts, exact review-head holistic diagnostics and
actual read-only PR compositions separately. After ordinary integration, freeze
the real new main and obtain fresh source-matching producer artifacts, current
publication/live bytes, declared-input portability and canonical browser proof.
Earlier successful HTTP verification does not override a browser failure or
become execution evidence for a later source. Existing failed scans and native
partial/unavailable states remain literal.

Acceptance belongs to [#98](https://github.com/egohygiene/empathy/issues/98)
and [#105](https://github.com/egohygiene/empathy/issues/105), tracked by
[#118](https://github.com/egohygiene/empathy/issues/118). The completed #94,
specialist #110 and wider #79 scopes remain separate. UI redesign, whole-fleet
qualification and human ratification are outside this source correction.

Decision impact: no new ADR; existing
[ADR-0001](../decisions/ADR-0001-foundation-ownership.md) retains specialist ownership.
