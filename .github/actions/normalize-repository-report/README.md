# Normalized repository reports

This action converts canonical scanner output into the compact contract consumed
by repository-intelligence projections. It does not replace native JSON, SARIF,
workflow artifacts, or GitHub Security-tab uploads.

The contract is defined by
[`repository-report-summary.schema.json`](repository-report-summary.schema.json)
and identified as `egohygiene.repository-report-summary/v1`.

## Status model

Each summary keeps three independent ideas separate:

- `execution.state` says whether the producer emitted usable output.
- `findings.state` says whether that output is clear, advisory, or blocked by
  repository policy.
- `freshness.expires_at` gives consumers a deterministic deadline from which to
  derive `fresh` or `stale` at read time.

Unavailable and malformed inputs never become green. An unavailable input emits
`execution.state: unknown`; malformed producer data emits
`execution.state: failure`; both emit `findings.state: unknown`.

## Producers

| Producer   | Canonical input                              | Policy behavior                                                                    |
| ---------- | -------------------------------------------- | ---------------------------------------------------------------------------------- |
| OSV        | Workflow-generated OSV summary               | Counts at or above `severity_threshold` are blocking; lower findings are advisory. |
| MegaLinter | `mega-linter-report.json` and tool matrix    | Each finding-bearing tool inherits `blocking` or `advisory` from the matrix.       |
| Scorecard  | OpenSSF SARIF and optional official API JSON | Checks below ten are advisory; no aggregate is invented from SARIF check scores.   |

The Scorecard aggregate is accepted only when the official API repository and
commit match the evaluated workflow commit exactly. Stale, unavailable, and
invalid API data leave `scorecard.aggregate_score` as `null` while preserving
the SARIF-derived check signals.

## Workflow usage

```yaml
- name: Normalize MegaLinter summary
  if: always()
  uses: ./.github/actions/normalize-repository-report
  with:
    producer: megalinter
    input: .reports/megalinter/mega-linter-report.json
    output: .reports/megalinter/summary.json
    policy-input: egolint/.config/megalinter/tool-matrix.json
```

Run the normalizer after the canonical producer and before report artifact
upload. Stable publication remains the responsibility of the guarded
`publish-report-snapshot` action in a trusted default-branch job.
