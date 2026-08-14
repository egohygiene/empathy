# Staged GitHub automation

This directory preserves imported workflows that are not part of Empathy's
active universal baseline. GitHub does not execute workflows outside
`.github/workflows/`.

Staging is a migration boundary, not an alternate production workflow folder.
Files here may contain stale action versions, source-repository paths, missing
secrets, mutually exclusive release strategies, or assumptions that only make
sense for one future profile.

## Categories

| Directory | Preserved capability | Promotion destination |
| --- | --- | --- |
| `scripts/` | Helpers required by staged workflows | Move with the owning workflow |
| `agent-environment/` | Copilot and agent workstation validation | Agent/environment profile |
| `application-flutter/` | Flutter generation, autofix, and release artifacts | Flutter application profile |
| `container-platform/` | Dev-container builds, benchmarks, publishing, and image scans | Realm/container profile |
| `content-and-docs/` | Bookmarks, Pages, Quartz, images, and generated docs | Content/garden profiles |
| `release-strategies/` | Changesets, Release Please, and semantic-release alternatives | One selected release profile |
| `security-optional/` | Higher-cost or policy-dependent security checks | Security capability profiles |
| `source-specific/` | Aether and other source-repository automation | Owning repository or profile |

## Promotion gate

A staged workflow may become canonical only after it:

- has one owning capability and no embedded product identity;
- declares explicit inputs, permissions, concurrency, and job timeouts;
- pins every external action to a reviewed full commit SHA;
- handles forks, missing secrets, and absent technology files safely;
- verifies required repository features such as Dependency Graph are enabled;
- passes actionlint, MegaLinter, and a representative end-to-end run;
- documents whether it belongs in Empathy, Relay, Realm, Aether, or a technology
  profile.

Do not copy staged workflows into a generated repository unchanged.

## Promotion ledger

| Capability | Status | Reason / owner |
| --- | --- | --- |
| Dependency review | Promoted in Empathy | A least-privilege pull-request gate with no product assumptions. It is a thin caller around GitHub's maintained action. |
| OpenSSF Scorecard | Already active | Empathy's canonical workflow is newer than the staged copy and will gain a stable dashboard summary in a later slice. |
| OSV, SBOM, and Trivy | Already owned by current reports | Do not duplicate scanners. The repository dashboard will consume compact published summaries from the canonical scanners. |
| Gitleaks | Not promoted | MegaLinter already runs secret-scanning coverage; adding another default scanner would duplicate alerts until an explicit policy selects it. |
| DCO and REUSE | Optional governance profiles | Both are valuable but change contributor/release policy and belong behind opt-in organization profiles. |
| Devcontainer, image, Flutter, release, and Quartz workflows | Profile-specific | Realm, application, release, and Mindgarden owners should promote them through their own contracts. |
| Vitality audit | Redesign as dashboard collector | The staged Ruby script is a useful signal source, but the canonical implementation should emit the dashboard's versioned JSON contract. |
