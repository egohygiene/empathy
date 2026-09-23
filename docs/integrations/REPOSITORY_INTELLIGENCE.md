# Repository Intelligence publication

Empathy consumes Relay's Repository Intelligence builder and owns the complete
Mindgarden/Quartz site, its Pages deployment, and publication evidence. This is
the consumer checkpoint for [Empathy #94](https://github.com/egohygiene/empathy/issues/94)
and [Relay #33](https://github.com/egohygiene/relay/issues/33).
Implementation and PR evidence precede the default-branch deployment proof;
Empathy #94 remains open until the post-merge acceptance sequence below is recorded.
Relay #33 and [Relay #106](https://github.com/egohygiene/relay/issues/106) remain
open for their broader acceptance and final reconciliation.

## Immutable inputs and ownership

| Input | Reviewed revision | Role |
| --- | --- | --- |
| Relay v1.6.0 | `9a6315978766c336566b9fa7139b800fa8789ba5` | Current builder in both integrations; composition and receipt validation |
| Relay v1.4.0 | `b71b090406a3a9e4cd9f107e9d14a623bbecb127` | Previous Repository Intelligence builder pin, frozen for historical replay |
| Quartz | `075afd3f712da0088a07f5284a7b3aba37dd61b6` | Existing external site engine; Node.js 24 and profile behavior preserved |

The two current integrations are
[`mindgarden-pages.yml`](../../.github/workflows/mindgarden-pages.yml) and
[`repository-intelligence.yml`](../../.github/workflows/repository-intelligence.yml).
All remote actions remain pinned to full commit SHAs. The normalized-report
producers and guarded snapshot publishers retain their existing pins and policy.

Mindgarden's [reviewed-public projection](../../mindgarden/profiles/quartz/README.md)
remains the admission boundary. Private overlays, provenance sidecars, context
packs, draft notes, and unreviewed material do not enter Quartz. The existing
profile and Quartz engine remain unchanged. Relay writes only
`.cache/mindgarden/site/intelligence/`, after Quartz builds the rest of the site.
The workflow captures the pre-composition file inventory and verifies that every
consumer file outside `intelligence/` keeps its exact bytes.

Empathy is the only Pages composition and deployment authority. Relay generates
and validates evidence; it receives no Pages deployment authority. Observatory
views without a supplied commit-matched read model intentionally say evidence
is unavailable. This checkpoint does not introduce that read model or expand
into Observatory #24, Relay #102, #101 polish, or fleet adoption.

## Events and trust boundaries

| Entry point | Build and retained evidence | Publication authority |
| --- | --- | --- |
| Pull request | Complete current composition and fixed `rollback-v1.4` replay; 30-day review artifacts | No Pages configuration, Pages artifact, deployment, receipt, or privileged refresh |
| Default-branch push | Current composition, duplicate Relay build, provenance, and run report | Empathy's existing `deploy` job |
| Manual `current` on `main` | Same current build and evidence | Empathy's existing `deploy` job |
| Manual `rollback-v1.4` on `main` | Fixed historical source and verified rollback evidence | Empathy's existing `deploy` job |
| Trusted producer `workflow_run` | Current default-branch checkout, committed summaries, and producer identifiers | Empathy's existing `deploy` job |
| Standalone Repository Intelligence workflow | Public bundle and sanitized run evidence | Artifact-only; no deployment |

A manual run on another branch may build but cannot publish. The producer refresh
accepts only completed `MegaLinter`, `OpenSSF Scorecard`, or
`🔍 OSV Vulnerability Scan` runs originating from `push`, `schedule`, or
`workflow_dispatch`. Both producer repository identities must equal the consumer
repository, and the producer head branch must equal the default branch.
Pull-request and `pull_request_target` origins cannot enter this path. The
predicate deliberately has no successful-conclusion requirement: failed scans
can publish useful failure or blocking-findings evidence before the refresh.
The refresh uses the default-branch workflow checkout, not producer-supplied code
or a producer artifact as an executable input.

This behavior was already demonstrated by the failed scheduled
[OSV run 35839887136](https://github.com/egohygiene/empathy/actions/runs/35839887136):
its severity gate failed after normalization and artifact upload, its snapshot
publication succeeded, and
[Pages run 35840040112](https://github.com/egohygiene/empathy/actions/runs/35840040112)
built and deployed the refresh. The upgrade preserves this trigger behavior.

Build jobs use read permissions and disable persisted checkout credentials. Only
the separate `deploy` job receives `pages: write` and `id-token: write`; it executes
the pinned Pages deployment action without checking out consumer code. Receipt
finalization and live verification use read permissions. The separate scanner
publication jobs retain their existing trusted-default-branch `contents: write`
boundary; PR jobs cannot invoke their publisher. No secret inheritance is added.

Deployment and live-verification guards use explicit status predicates and
`needs` results. Finalization uses `always()` so a real deployment failure still
records its outcome; it reasserts that failure after retaining the receipt.
[`repository-intelligence-gates.yml`](../../.github/workflows/repository-intelligence-gates.yml)
exercises GitHub's actual skipped-ancestor scheduling and forbidden lanes with
read-only jobs. It cannot deploy, access an environment, or obtain deployment
permissions. Inspect the expected jobs and steps, not just a green workflow badge.

## Report snapshots remain truthful

The consumer still reads `.reports/{osv,megalinter,scorecard}/summary.json` using
`egohygiene.repository-report-summary/v1`. Execution, findings, freshness, and
source identity remain separate. A successful OSV scan can have blocking findings;
a failed MegaLinter execution can have zero recorded findings. Missing evidence
is unknown, and malformed or incompatible evidence is invalid. Expired accepted
evidence is stale at its declared expiry. Freshness evaluation is anchored to
the declared build instant, normally the represented commit timestamp.

The hardened Relay contract requires a report's original scanner commit to match
the represented consumer commit. A subsequent snapshot-publication commit does
not make the earlier scan evidence current. Existing OSV and MegaLinter snapshots
can therefore render invalid with unknown findings after the upgrade. Their
original commit IDs and payloads are preserved; neither timestamps nor commit
IDs are rewritten to manufacture a match. A later matching report is accepted
with its actual execution and finding state.

[`repository_intelligence_publication.py`](../../tools/repository_intelligence_publication.py)
records the exact consumer SHA/tree, Quartz pin and configuration hashes, and
each normalized summary's byte digest, recognized schema, original source SHA,
execution state, and source-match flag in `inputs.json`. It also records allowlisted
triggering producer run, attempt, event, conclusion, and source identifiers.
Duplicate JSON keys are rejected before either integration invokes Relay.
Unrecognized or malformed summaries remain explicitly incompatible or invalid;
their raw values, logs, private context, and signed artifact URLs are not copied
into diagnostics. Relay retains ownership of report schema validation and public
projection; the consumer adapter does not reinterpret scanner policy.

## Determinism, composition, and receipts

The current Pages build runs Relay twice with identical declared inputs on the
same already-built Quartz site. `determinism.json` proves equality of the complete
two composed inventories, their manifest bytes, and their digest. Composition
validation also proves that Relay preserved the Quartz baseline. This establishes
repeatability of Repository Intelligence within that build context; it does not
claim two fresh Quartz builds are byte-identical. Quartz's synthetic tag entries
use runtime dates in `index.xml` and `sitemap.xml`.

The pinned Relay versions also incorporate the checkout basename. The rollback
lane requires the provider checkout basename `empathy` and `TZ=UTC`. Arbitrary
checkout-directory portability is tracked separately in
[Relay #109](https://github.com/egohygiene/relay/issues/109); do not generalize the
same-context duplicate-build proof into a portability claim.

Current builds retain these distinct pieces of evidence for 30 days:

| Artifact family | Evidence |
| --- | --- |
| `empathy-composed-current-*` | Complete public composition for PR review, including hidden files |
| `empathy-provenance-current-*` | Exact site bytes, normalized input identities, Quartz baseline, composition report, and repeatability report |
| `empathy-publication-report-current-*` | Allowlisted stage, rule, outcomes, and remediation link |
| `empathy-deployment-receipt-*` | Exact current consumer/Relay identities, manifest and bundle digests, composed digest, workflow run/attempt, environment, deployment outcome and URL, routes, and rollback point |
| `empathy-live-*` | Verified public identity and exact route-byte digests |

The deterministic `intelligence/build-manifest.json` identifies the source and
generator, input contract versions, and bundle inventory. Deployment-specific
receipts remain in `.cache/mindgarden/publication/`, outside the public site.
They cannot alter the deterministic bundle. Artifact ZIP digests and logical
bundle/composition digests describe different objects and must be recorded
separately.

Live verification uses only `https://egohygiene.github.io/empathy/`. It requires
HTTP 200 without following redirects, exact manifest bytes for current builds
(historical provenance bytes for rollback), and exact retained HTML bytes for
all five Mindgarden entry points and all twelve Repository Intelligence routes.
It checks identity again after route probes to detect a deployment changing
during verification. Route availability alone is insufficient proof of revision.

## Fixed historical rollback

`rollback-v1.4` rebuilds this reviewed historical point:

| Identity | Value |
| --- | --- |
| Consumer revision | `254185272ab27b6858b8b0393af6549c205c9a8d` |
| Consumer tree | `a5cdaba679c8c0b9d677730273c9779569649929` |
| Relay revision | `b71b090406a3a9e4cd9f107e9d14a623bbecb127` |
| Quartz revision | `075afd3f712da0088a07f5284a7b3aba37dd61b6` |
| Known-good workflow | [35840040112, attempt 1](https://github.com/egohygiene/empathy/actions/runs/35840040112) |
| Historical Pages archive | [10741177073](https://github.com/egohygiene/empathy/actions/runs/35840040112/artifacts/10741177073) |
| Archive SHA-256 | `3175c601487b61ecf4e87fc820a33ce8d3a137fa34bf21b2256d9868aa04257b` |
| Original complete-site digest | `sha256:1e92a0a74c154bbc3c339a6ef1764852bfcceba1a58b294e238b4a0331f94498` |

[`verify_repository_intelligence_rollback.py`](../../tools/verify_repository_intelligence_rollback.py)
requires the historical path inventory, exact old Relay provenance, and exact
Repository Intelligence and stable Quartz bytes. Of the 81 historical files,
79 must remain byte-identical. In the remaining two feeds, only synthetic tag
dates may vary; all other parsed feed content is checked against the reviewed
baseline. The verifier changes no output bytes. It records the actual newly
composed digest separately from the original deployment digest and explicitly
declines full-site equality. The baseline has no workflow or CLI override.

The historical bundle predates v1.6 build manifests and deployment receipts.
Rollback evidence consists of its verified replay report, complete composed
artifact, real Pages deployment outcome, successful finalization reassertion,
and exact live historical provenance/routes. A current-format receipt must not
be invented for that old bundle.

For an operational rollback, dispatch **Publish Mindgarden** on `main` with
`mode=rollback-v1.4`. Inspect build, actual deployment, finalization, and live
verification. For a rehearsal, immediately dispatch the same workflow on `main`
with `mode=current` after capturing old live identity, then verify the restored
current deployment. Publication runs are serialized; the old site must not be
left live at the end of the rehearsal. The workflow's fixed historical checkout
is the exact revert procedure; it does not rewrite `main` or substitute a mutable
old branch.

## Validation and post-merge acceptance

Run the existing repository suite and the focused consumer tests. Set
`RELAY_CHECKOUT` to an external checkout at the exact current Relay pin; the
report tests verify its Git HEAD and otherwise skip only when the variable is
absent. The provider fixture must supply it explicitly.

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 -m unittest discover -s mindgarden/tests -p 'test_*.py' -v
python3 -m unittest discover -s egolint/tests -p 'test_*.py' -v
RELAY_CHECKOUT=/absolute/path/to/reviewed-relay \
  python3 -m unittest discover -s tests -p 'test_repository_intelligence*.py' -v
python3 mindgarden/scripts/validate_garden.py --repository-root .
python3 mindgarden/scripts/garden_agent.py --repository-root . verify
python3 mindgarden/scripts/publish_garden.py --repository-root . verify
task architecture:check
task taskfile:check
uvx --from ruff==0.16.5 ruff check --config egolint/.config/lint/python/ruff.toml \
  tools/repository_intelligence_publication.py tools/verify_repository_intelligence_rollback.py \
  tests/test_repository_intelligence*.py tests/test_mindgarden_publishing_integration.py
git diff --check
```

The focused tests cover trusted and rejected producer events, PR permissions,
real provider job guards, strict JSON intake, report states and freshness,
public-safe diagnostics, matching and failing live bytes, composition, receipt
separation, and historical rollback failures. Retain YAML/JSON parsing and
duplicate-key checks plus applicable Python, Bash, and JavaScript syntax checks.
Record pre-existing MegaLinter catalog-SHA and task-catalog drift as baseline
validation findings. The root Cargo workspace also references a missing
`tests/fixtures/clippy/Cargo.toml`, which blocks the normal Beacon Rust gates.
This checkpoint does not change those unrelated catalogs or workspace paths.

After review and merge, record the following on #94 before changing its state:

1. Exact merged SHA/tree and successful default-branch build, deployment,
   receipt finalization, and exact live identity/routes.
2. A successful manual `current` rebuild, including its separate receipt and
   exact public bytes; and a trusted producer refresh that preserves useful
   non-success conclusion evidence and the original summary identities.
3. Dispatch **Repository Intelligence intentional failure**. Its bounded
   `max-depth=21` fixture must fail with `RIW-002`, retain a sanitized 30-day
   report with stage/rule/remediation, upload no Pages artifact, perform no
   deployment, and leave the last known-good site unchanged.
4. Exercise `rollback-v1.4`, capture its actual deployment and live historical
   identity, immediately dispatch `current`, and verify the restored current
   deployment through every job.
5. Record exact run attempts, artifact URLs and archive hashes, input hashes,
   manifest/bundle/composition digests, receipt, route evidence, negative-path
   report, rollback proof, and restored-current proof. Distinguish implemented
   behavior, PR validation, and consumer-side execution still pending.

Use reference-only issue links in PR text, for example `Refs #94` and
`Refs egohygiene/Relay#33`. Issue completion requires the durable post-merge proof
above, independently of whether the implementation PR is merged.
