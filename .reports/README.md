# Quality reports

This directory is the only repository namespace for generated quality, security,
compliance, and architecture reports.

Generated contents are ignored by default. Pull-request runs remain read-only and
upload their complete output as workflow artifacts. Trusted default-branch pushes,
schedules, and manual runs may commit curated stable snapshots through
`.github/actions/publish-report-snapshot`.

Artifacts and Git history preserve historical results. Report generators must not
accumulate timestamped history trees in this directory.

Human-authored findings and architectural analysis generally belong in
`.audits/`. Stable remediation summaries may live beside their generated tool
output when they are part of that report namespace's lifecycle contract.

The source contracts currently reserve this hierarchy:

```text
.reports/
├── complementary/<tool>/latest.json
├── egolint/architecture/
│   ├── README.md
│   └── lint-architecture.svg
├── megalinter/
│   ├── summary.json
│   ├── remediation.md
│   ├── grype/
│   ├── syft/
│   │   ├── sbom.cyclonedx.json
│   │   └── sbom.spdx.json
│   └── trivy/
├── osv/
│   └── summary.json
├── scorecard/
│   └── summary.json
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

OSV, MegaLinter, and OpenSSF Scorecard each publish a compact `summary.json`
using `egohygiene.repository-report-summary/v1`. The JSON Schema and producer
normalizer live in `.github/actions/normalize-repository-report/`. These
summaries keep execution, findings, freshness, provenance, and links separate;
producer-native JSON and SARIF remain authoritative and continue through their
existing artifact and Security-tab paths.

Scorecard's aggregate is copied from the official API only when the API result
names the exact commit evaluated by the workflow. A late, stale, or unavailable
API response produces a `null` aggregate rather than a locally invented score.

`.reports/megalinter/remediation.md` is the stable, human-readable assessment
of the latest cleanup pass. Unlike generated scanner payloads, it is curated and
versioned so future runs can distinguish acknowledged debt from regressions.

Only report-publication jobs receive `contents: write`. Every scanner and
generator job runs with read-only repository access, and no pull-request job can
invoke the guarded publisher.
