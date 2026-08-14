# Generate repository intelligence

This composite action creates deterministic repository anatomy and activity
artifacts from a complete Git checkout. It separates public-safe contracts from
raw diagnostic artifacts so callers can publish only reviewed projections.

## Public contracts

| Path                     | Contract                             | Intended use                                |
| ------------------------ | ------------------------------------ | ------------------------------------------- |
| `tree/repo.json`         | `egohygiene.repository-tree/v1`      | Commit-scoped repository tree and explorer  |
| `analytics/summary.json` | `egohygiene.repository-analytics/v1` | Charts, statistical snapshots, and callouts |

Both contracts are pinned to the resolved source commit. They contain no
contributor names, email addresses, commit messages, or raw workflow data.
Relative analytics windows such as `1 year ago` are resolved against the
source commit timestamp rather than wall-clock execution time.

Generated reports, caches, vendored dependencies, build outputs, and similar
noise are excluded from analytics by default. The repository tree uses a
separate exclusion list so meaningful tracked areas such as `.reports` can
remain visible without distorting change statistics.

## Internal artifacts

The `activity/` directory contains detailed TSV and text reports for local or
workflow-artifact inspection. In particular, `contributors.tsv`, `commits.tsv`,
and `log-graph.txt` can contain contributor identity or commit-message data.
Do not copy the complete activity directory into a public site.

## Example

```yaml
- name: Generate repository intelligence
  uses: ./.github/actions/generate-repository-intelligence
  with:
    output-root: ".cache/repository-intelligence"
    activity-ref: "HEAD"
    activity-since: "1 year ago"
    require-full-history: "true"
```

The caller must use `actions/checkout` with full history when
`require-full-history` is enabled.
