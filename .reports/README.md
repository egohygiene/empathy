# Quality reports

This directory is the only repository namespace for generated quality, security,
compliance, and architecture reports.

Generated contents are intentionally ignored during the policy phase. A later CI
orchestration change will define which trusted scheduled, manual, and default-branch
runs may publish a curated `latest` snapshot here. Pull-request runs remain read-only
and publish their complete output as workflow artifacts.

Human-authored findings and architectural analysis belong in `.audits/`, not here.
