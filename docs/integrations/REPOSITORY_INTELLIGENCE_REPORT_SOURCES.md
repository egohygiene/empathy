# Report source boundaries and Scorecard cleanup

This is the bounded [Empathy #98](https://github.com/egohygiene/empathy/issues/98)
checkpoint selected in the current implementation batch. It fixes the concrete
Scorecard publisher failure and records actual source-bound input behavior.
It does not claim the complete issue, current scan results or Pages acceptance.
The existing [publication contract](REPOSITORY_INTELLIGENCE.md), completed #94
canary and fixed rollback remain unchanged.

The later [exact-source artifact checkpoint](REPOSITORY_INTELLIGENCE_ARTIFACT_REPORTS.md)
adds reviewed manual report selection and artifact-only scans. Its actual
producer/preview/live qualification remains distinct from the dated Scorecard
repair and historical replay below.

## Observed publisher failure and repair

Historical [run 39240875694, attempt 1](https://github.com/egohygiene/empathy/actions/runs/39240875694)
represents source `480d70bc59c989f46abf7a323e645699b11c7d4a` on the default
branch. Its scheduled Scorecard scan, SARIF upload and artifact upload succeeded.
The separate summary publisher failed in its cleanup step with exit **129**:
`unknown option recursive`. Download, aggregate selection, normalization and
snapshot publication were all skipped. A successful scanner job therefore
did not supply a compatible committed summary.

Git supports `git rm -r`; it does not support `git rm --recursive`. Functional
repair `042fccfcbb597f0c1f4eb7b42f92ec39bbfef481` changes only that flag in the
existing trusted publisher. The new regression executes the exact cleanup
shell step in a disposable Git fixture, both with a tracked Scorecard summary
and with it already absent. It preserves another producer's tracked report.
No trigger, permission, event/default-branch guard, normalizer/publisher pin,
aggregate match condition or Pages/recovery behavior is weakened.

Scorecard is already configured as an optional producer through the existing
push, weekly schedule and manual workflow. It does not need a fabricated
not-applicable disposition or a new paid service. Current missing input remains
unavailable until a subsequent actual producer/normalization/publication path
is observed; the source repair alone is not that observation.

## Actual represented inputs

The existing consumer input collector was executed against clean source
`4853a1e55808bc5104dc509199c411e798d104dc` before this change. It observed:

| Input | Original report source | Execution | Matches that consumer? |
| --- | --- | --- | --- |
| OSV | `18d22e113e87c306b76d24873841249d41358c77` | success | no |
| MegaLinter | `e313e00d311397566450fd90ec1b18df8f8f40de` | failure | no |
| Scorecard | absent | unknown | no evidence |

The actual bytes and original source identities stay unchanged. The pinned
Relay reader rejects mismatches as invalid with unknown current findings.
Execution success/failure is independent of findings, freshness and source
coverage. In particular, zero recorded findings cannot turn a failed runner
into a successful scan. These observations name the inspected source boundary;
later source merges do not retroactively refresh it.

## Native historical replay

Actual retained SARIF artifact `12181865348` from the historical run was
downloaded and matched its provider archive SHA-256:
`3b1d9c4c41608116b32078f8b51bc6dded80759f85aef6b13d883617fee00183`.
The existing normalizer at exact Relay
`1eada5142f7fc7da7862f335589e3b8f5884ffaf` processed that actual SARIF locally.
The replay explicitly freezes the original artifact-creation time,
`2026-10-19T10:56:39Z`, and original source. It creates no current scan or
published report and does not retime the evidence to November.

The exact current reader at Relay
`d7c60473626f8dcc901210a208ad01a6474e8c1d` then proves:

| Selected boundary | Native result |
| --- | --- |
| Matching historical source at captured time | available; execution success; findings attention |
| Matching historical source evaluated now | available historical evidence; freshness stale |
| Consumer `4853a1e…` with that older report | invalid; current findings unknown |
| Actually absent committed Scorecard input | unavailable; execution/findings unknown |

No official Scorecard API aggregate was supplied. The numeric aggregate remains
null/unavailable; SARIF check results do not manufacture its weighted score.
Native projection preserved the normalized replay bytes. The
[bounded receipt](evidence/scorecard-source-boundary-2026-11-13.json) retains
provider identities, source boundaries, outcomes and limitations without raw
SARIF, scanner logs, local paths or credentials.

The existing pinned report suite passes all **11** tests, including matching,
mismatch, exact expiry, absence, malformed inputs, safe links and independent
execution/findings. All **7** publication-policy tests pass, including the new
actual cleanup regression. Reproduce the report integration with the exact
owner checkout, without copying its implementation:

```bash
RELAY_CHECKOUT=/path/to/exact-relay-d7c604 \
  python3 -m unittest discover -s tests -p test_repository_intelligence_reports.py
python3 -m unittest discover -s tests -p test_report_publication.py
```

Canonical Ruff/format, Mypy, Bandit and focused Secretlint checks were applied
to the changed source/test. Fixed local Git/bash operations use owned temporary
fixtures; their explicit subprocess suppressions were reviewed. This is
focused proof, separate from the complete holistic profile. The canonical
Lychee configuration also passes all five links in this guide; only its local
cache was disabled. No broken links or timeout acceptance was added.

## Remaining acceptance and next source boundary

Committing a generated summary changes Git HEAD. A report describing scanner
source **S** must not be relabelled as the later snapshot-publication commit
**P**. The current strict reader correctly rejects that mismatch. Independently
scheduled producers can also describe different sources. Fixing cleanup cannot
make those distinct commits one current capture.

Full #98 acceptance still needs a coordinated explicit represented source and
same-source report artifact selection for the actual producer and composed
preview, followed by the separately reviewed live summary. Keep old reports
historical, preserve original clocks, and retain precise blockers when an input
is missing or incompatible. Reuse the existing normalizer and artifact/build
contracts; a second assembler or a weakened source check is not a solution.

No current scan, report snapshot commit, Empathy Pages deployment, rollback,
full holistic MegaLinter or broad CI outcome is claimed here. The current
generator's wider acceptance stays with #105, and dependency/lint/staging work
stays with its existing owners. #98 and parent #118 remain open.

Decision impact: **ADR not required**. This repairs a caller-owned Git option
and qualifies the existing pinned report contracts under
[ADR-0001](../decisions/ADR-0001-foundation-ownership.md); no ownership, schema,
source policy or publication authority changes.
