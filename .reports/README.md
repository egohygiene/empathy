# Quality reports

This directory is the only repository namespace for generated quality, security,
compliance, and architecture reports.

Generated contents are intentionally ignored during the policy phase. A later CI
orchestration change will define which trusted scheduled, manual, and default-branch
runs may publish a curated `latest` snapshot here. Pull-request runs remain read-only
and publish their complete output as workflow artifacts.

Human-authored findings and architectural analysis belong in `.audits/`, not here.

The source contracts currently reserve this hierarchy:

```text
.reports/
├── complementary/<tool>/latest.json
├── megalinter/
│   ├── grype/
│   ├── syft/
│   │   ├── sbom.cyclonedx.json
│   │   └── sbom.spdx.json
│   └── trivy/
├── osv/
└── supply-chain/
    ├── licenses/
    ├── sbom/
    └── vulnerabilities/
```

The complementary runner writes normalized local `latest.json` results. Syft,
Grype, Trivy, and OSV retain separate native outputs so source licensing,
dependency licensing, inventories, and vulnerability findings are never
collapsed into one ambiguous signal. PR 4 will define artifact upload and the
trusted-run publication policy without changing these ownership boundaries.
