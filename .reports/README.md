# Quality reports

This directory is the only repository namespace for generated quality, security,
compliance, and architecture reports.

Generated contents are ignored by default. Pull-request runs remain read-only and
upload their complete output as workflow artifacts. Trusted default-branch pushes,
schedules, and manual runs may commit curated stable snapshots through
`.github/actions/publish-report-snapshot`.

Artifacts and Git history preserve historical results. Report generators must not
accumulate timestamped history trees in this directory.

Human-authored findings and architectural analysis belong in `.audits/`, not here.

The source contracts currently reserve this hierarchy:

```text
.reports/
├── complementary/<tool>/latest.json
├── egolint/architecture/
│   ├── README.md
│   └── lint-architecture.svg
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
collapsed into one ambiguous signal. The architecture snapshot is generated
from both canonical tool matrices rather than maintained manually.

Only report-publication jobs receive `contents: write`. Every scanner and
generator job runs with read-only repository access, and no pull-request job can
invoke the guarded publisher.
