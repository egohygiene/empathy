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
```

It always writes:

```text
<output-root>/
├── index.html
├── styles.css
└── summary.json
```

`summary.json` uses `egohygiene.repository-intelligence-dashboard/v1`, declared
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

## Workflow usage

```yaml
- name: Generate repository intelligence dashboard
  uses: ./.github/actions/generate-repository-intelligence-dashboard
  with:
    reports-root: .reports
    output-root: .cache/mindgarden/site/intelligence
    repository: "${{ github.repository }}"
    default-branch: "${{ github.event.repository.default_branch }}"
    source-commit: "${{ github.sha }}"
```

Pages deployment is intentionally owned by the caller workflow. This action
only validates local inputs and writes static files.
