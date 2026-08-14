# Repository intelligence dashboard builder

This composite action turns normalized producer summaries into a small public
dashboard bundle without a client-side framework, remote font, analytics script,
or rendering service.

## Inputs and outputs

The builder reads these inputs when present:

```text
.reports/
├── megalinter/summary.json
├── osv/summary.json
└── scorecard/summary.json

.cache/repository-intelligence/
└── analytics/
    └── summary.json
```

It always writes:

```text
<output-root>/
├── index.html
├── styles.css
└── summary.json
```

`summary.json` uses `egohygiene.repository-intelligence-dashboard/v2`, declared
by the checked-in `repository-intelligence-dashboard.schema.json`. It is a
public projection, not another scanner report. Canonical producer JSON, SARIF,
workflow artifacts, and GitHub Security integrations remain authoritative.

## Truth-preserving states

- Missing producer summaries become `availability: unavailable`.
- Malformed or incompatible summaries become `availability: invalid` and
  `execution.state: failure`.
- Freshness is derived from each producer's `expires_at` using the explicit
  `as-of` instant.
- Execution, findings, and freshness remain separate on every card.
- The aggregate JSON exposes state counts rather than collapsing everything
  into one ambiguous green or red score.

The default `as-of` value is the represented commit's timestamp, so repeated
builds from the same checkout and inputs are byte-for-byte deterministic.

## Repository vitality

The local collector reports counts and automation posture only: recent commits,
recent contributor count, tracked files, workflows, composite actions, tests,
and whether full Git history was available. Contributor identities, raw Git
logs, tokens, and artifact URLs are not published.

## Statistical snapshots

When `analytics-summary` points to an
`egohygiene.repository-analytics/v1` document for the represented commit, the
builder renders:

- every weekly commit and merge point as an accessible line chart;
- the five largest repository areas plus `Other` as a composition donut;
- the eight most frequently changed repository areas as horizontal bars;
- blocking, advisory, clear, and unknown scanner findings by producer; and
- explicit producer evidence-window meters.

Charts are inline SVG or native HTML progress elements. Each visualization has
an accessible title, description, and expandable semantic table. No charting
runtime, CDN, JavaScript, or synthetic health score is introduced. Missing or
commit-mismatched analytics render as unavailable rather than zero.

## Workflow usage

```yaml
- name: Generate repository intelligence dashboard
  uses: ./.github/actions/generate-repository-intelligence-dashboard
  with:
    reports-root: .reports
    analytics-summary: .cache/repository-intelligence/analytics/summary.json
    output-root: .cache/mindgarden/site/intelligence
    repository: "${{ github.repository }}"
    default-branch: "${{ github.event.repository.default_branch }}"
    source-commit: "${{ github.sha }}"
```

Pages deployment is intentionally owned by the caller workflow. This action
only validates local inputs and writes static files.
