---
name: repository-audit
description: Perform an evidence-based, non-destructive repository audit and write a structured report. Use for holistic or focused reviews of architecture, code quality, testing, security, CI/CD, dependencies, documentation, developer experience, maintainability, accessibility, performance, or repository hygiene.
---

# Repository Audit

## Resolve the request

Read `../../../.github/specs/auditor.spec.md` when present. Resolve the audit strategy, included and excluded scope, focus areas, depth, and constraints. Apply specification defaults and record every inferred value in the report.

## Inspect systematically

1. Read repository overview, architecture, decisions, and applicable specifications.
2. Review existing audits before recording new findings.
3. Inspect automation, manifests, workflows, source, tests, and documentation relevant to scope.
4. Run read-only diagnostics when they provide reproducible evidence.
5. Record material files or commands that were unavailable.

## Maintain evidence integrity

- Label statements as observed, inferred, recommended, or unverified.
- Cite repository-relative paths, symbols, configuration keys, or command results precisely.
- Assign lower confidence when evidence is incomplete.
- Separate the observation from why it matters and from the recommendation.
- Record strengths and effective practices, not only defects.
- Avoid repeating a prior finding without checking its current state.

## Write the report

Use the specification's filename, frontmatter, finding schema, severity, confidence, effort, impact, and status vocabularies. Create a new file under `audits/`; never overwrite an existing report.

During a normal audit, modify only the new report. Do not apply fixes, update dependencies, reformat files, open issues, or create commits.

## Validate

Confirm that the report documents scope, exclusions, evidence, positive observations, findings, uncertainties, blocked checks, and a prioritized follow-up backlog. If the audit is incomplete, produce a truthful partial or blocked report with the next evidence needed.
