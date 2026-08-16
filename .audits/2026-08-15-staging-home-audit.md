<!-- SPDX-FileCopyrightText: 2026 Ego Hygiene -->
<!-- SPDX-License-Identifier: MIT -->

# Staging ownership and destination audit

> **Living-ledger note (2026-08-16):** The narrative and owner table below
> preserve the original `41d1da3` snapshot. The deterministic CSV is refreshed
> as approved promotion PRs land and currently covers 2,222 tracked files and
> 161,784,921 bytes. See
> [`2026-08-16-taskfile-promotion.md`](2026-08-16-taskfile-promotion.md) and
> [`2026-08-16-misc-promotion.md`](2026-08-16-misc-promotion.md) for the latest
> approved dispositions.

## Decision

`.staging/` is an intake reservoir, not a future source tree. Its 2,340 tracked
files have been assigned an owner, a safe incubation location, a proposed
canonical home, and a disposition in the accompanying
[`data/2026-08-15-staging-file-disposition.csv`](data/2026-08-15-staging-file-disposition.csv).
No file is left with an unassigned owner or `TBD` destination.

The audit recommends a preserve-first migration. Files should move into each
owner's `.staging/` area before semantic merging. Nothing classified as an
instruction bundle, executable, workflow, privileged configuration, or
third-party asset should become active merely because it has been relocated.

## Snapshot and method

- Base commit: `41d1da3`
- Inventory: 2,340 files, 164,552,938 bytes (156.93 MiB)
- Inputs: tracked regular files beneath `.staging/`
- Evidence: path and content inspection, Git mode and blob identity, targeted
  visual/OCR review of 73 creative images, active-tree comparison, and known
  capability boundaries
- Outputs: this architectural summary, the per-file CSV ledger, and the
  deterministic `tools/staging_home_audit.py` generator

The ledger records both `incubation_home` and `canonical_home`. The former is
where raw material can be moved without activating it; the latter is the
proposed result after its merge group passes review. A canonical path is a
design target, not approval to publish or execute the file.

## Capability ownership

| Owner                | Files |      Size | Responsibility in this intake                                                                         |
| -------------------- | ----: | --------: | ----------------------------------------------------------------------------------------------------- |
| Aether               | 1,584 | 24.23 MiB | Specifications, agents, skills, prompts, schemas, context adapters, and generated agent distributions |
| Realm                |   357 |  7.26 MiB | Development images, devcontainers, service modules, orchestration, and opt-in workstation profiles    |
| Holon                |   256 | 10.07 MiB | Universal application/API fixtures and parameterized project templates                                |
| Empathy              |    26 | 34.76 MiB | Universal governance/task contracts and Ego Hygiene identity references                               |
| Awesome              |    25 |  0.62 MiB | Product-specific website, contributor, catalog, RSS, and agentic automation                           |
| Beacon               |    19 |  3.59 MiB | Research-paper templates and Beacon visual references                                                 |
| Relay                |    15 |  0.15 MiB | Reusable CI mechanics, risk automation, and generated workflow delivery                               |
| Dreamscape           |    14 | 25.62 MiB | Creative-pipeline references and research                                                             |
| Egolint              |    10 |  5.22 MiB | Lint/security policy, hooks, remediation material, and formatting tools                               |
| Mindgarden           |     8 | 10.08 MiB | Knowledge-source provenance and optional publishing profiles                                          |
| Identity             |     7 | 13.78 MiB | Identity-generation references and external/personal visual archive material                          |
| Renderflow           |     7 |  9.64 MiB | Renderflow branding candidates                                                                        |
| Mantle               |     5 |  0.01 MiB | Portable shell, Git, Fastfetch, and host-runtime behavior                                             |
| Other product owners |     7 | 11.89 MiB | Aniflow, Mindcap, Reflector, Research, and project-specific visual references                         |

This follows the current architectural split: Empathy composes the universal
baseline; Realm owns environments; Mantle owns shell/runtime behavior; Egolint
owns quality policy; Relay owns reusable automation; and Aether owns agent
knowledge sources and their non-authoritative distributions.

## What remains universal to Empathy

Only a small source-level subset should eventually land in the Empathy root:

| Staged source                             | Proposed outcome            | Required treatment                                                                                  |
| ----------------------------------------- | --------------------------- | --------------------------------------------------------------------------------------------------- |
| `.specify/memory/constitution.md`         | `AI_CONSTITUTION.md`        | Merge useful privacy/provenance clauses; never overwrite the active constitution                    |
| `templates/community/GOVERNANCE.md`       | `GOVERNANCE.md`             | Normalize as the universal baseline; later distribute through the organization `.github` repository |
| `tasks/project.yml` and `tasks/tests.yml` | `tasks/`                    | Merge only generic orchestration aliases; remove the empty placeholder after approval               |
| `misc/ROADMAP.md`                         | existing `tools/ROADMAP.md` | Delete after ledger approval because the content is byte-identical                                  |

The remaining Empathy-owned rows are Ego Hygiene visual references. They should
move to `.identity/references/ego-hygiene/`, be renamed from opaque upload IDs,
and receive generation/source provenance before use.

## Realm: proposed development-environment shape

Most of `.staging/devenvironment/` belongs in `realm/.staging/` first. Realm's
eventual tree should separate the baseline image, devcontainer integration,
optional services, and host presentation:

```text
realm/
├── images/baseline/Dockerfile
├── devcontainers/baseline/
│   ├── .devcontainer/devcontainer.json
│   └── compose.yaml
├── devcontainer-features/
├── services/<service>/
└── workstation/
    ├── shared/
    └── linux/
```

The important merge groups are:

| Raw variants                                             | Incubation                         | Final target                                                   | Merge decision                                                                                                           |
| -------------------------------------------------------- | ---------------------------------- | -------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| `devcontainer.json`, `devcontainer2.json`                | `realm/.staging/.devcontainer/`    | `realm/devcontainers/baseline/.devcontainer/devcontainer.json` | Produce one portable config; remove personal editor settings, host credential mounts, and disabled SSH host verification |
| `docker-compose.yml`, `docker-compose2.yml`              | `realm/.staging/compose/`          | `realm/devcontainers/baseline/compose.yaml`                    | Split the minimal development service from opt-in service profiles; replace weak credential defaults                     |
| `base.Dockerfile`, `todo.Dockerfile`, `todo2.Dockerfile` | `realm/.staging/dockerfiles/`      | `realm/images/baseline/Dockerfile`                             | Rebuild as a pinned, documented baseline with non-root defaults and an explicit support matrix                           |
| `caddy.yml`, `caddy copy.yml`                            | `realm/.staging/containers/caddy/` | `realm/services/caddy/compose.yaml`                            | Keep one canonical variant; the two current files are exact duplicates                                                   |
| `redis.Dockerfile`, `redis2.Dockerfile`                  | `realm/.staging/containers/redis/` | `realm/services/redis/Dockerfile`                              | Compare features and merge under a service contract                                                                      |
| Apache certificate files                                 | `realm/.staging/security-review/`  | generated test fixtures                                        | Replace tracked certificates with deterministic fixture generation                                                       |

Two large apparent environment areas do **not** belong to Realm:

- `devenvironment/containers/services/api/**` is application code and belongs
  in `holon/.staging/templates/universal-app/apps/api/`.
- `react-template/universal/**` belongs beside it as the Holon universal UI
  template. Realm should expose a consumer dev profile for the template rather
  than owning its source.

Portable shell defaults under `workstation/shared/shell/` belong to Mantle.
OpenCode theme/TUI preferences remain an opt-in Realm workstation profile;
OpenCode commands belong to Aether as generated agent distributions.

## Aether: source, distribution, and community quarantine

The Aether intake has three different trust levels and must not be flattened:

1. Organization source candidates: 53 specifications, 28 skill sources, and 13
   agents should be compared with the evolved canonical library before an
   explicit supersession decision.
2. Distribution adapters: `.opencode/commands/**` and Spec Kit adapters are
   non-authoritative projections that must reverse-map to Aether source
   contracts.
3. Community material: 1,447 files from community agents, skills, and
   instructions remain under `aether/.staging/community/awesome-copilot/`.

The community corpus is useful but not activation-ready. Of 383 `SKILL.md`
files, only 39 declare a frontmatter license and only six packages include a
license file. The scan also found prompt-override language in four files and 77
files classified as quarantined executables. Every package needs recorded
upstream URL/revision, license disposition, content digest, prompt-safety
review, executable review, and an allow/deny decision before it can appear in
an active distribution.

`create-skill.mjs`, `validate-skills.mjs`, `generate-open-pr-report.mjs`, and
`update-readme.mjs` also import an absent `constants.mjs`; they require repair
and tests rather than direct promotion.

## Automation split

The 37 imported GitHub workflows mix three owners:

- Relay receives 12 reusable mechanics such as Flutter CI, line-ending checks,
  publishing, label setup, webhook calling, and PR-risk scanning. Convert them
  to pinned, least-privilege reusable workflows or composite actions.
- Aether receives five thin consumer workflows for skill/plugin and agentic
  validation; reusable mechanics still move to Relay.
- Awesome receives eight product-specific website, catalog, contributor, RSS,
  and traffic workflows plus five source/lock agentic workflow pairs.

The `codeowner-update.md` instruction source belongs to Aether, while its
generated lock workflow and lock metadata belong to Relay. Generated workflow
artifacts are never the authoritative edit surface.

## Other destination decisions

- Merge `templates/paper/**` into Beacon's existing manifest-driven
  research-paper template.
- Merge `.pre-commit-config.yaml` into Egolint only after splitting its multiple
  concatenated YAML documents. Do not promote it as-is.
- Compare the disabled `.husky/commit-msg` hook with Egolint's active hook and
  discard it if it adds no behavior.
- Treat `mkdocs.yml` as an optional Mindgarden publishing profile after removing
  stale Sanctuary metadata; Quartz remains Empathy's current public projection.
- Keep `vite.corpus.txt` as Holon research evidence, not executable
  configuration.
- Route project images by visual owner. Opaque filenames must be renamed and
  paired with provenance. Incompris and personal “Alan ecosystem” references
  stay in Identity's external archive and must not be published as Ego Hygiene
  assets.

## Safety and cleanup gates

Relocation must preserve quarantine. Before activation:

- replace weak/default development credentials and avoid committing secrets;
- remove `StrictHostKeyChecking=no`, unnecessary privileged mode, host
  `.ssh`/`.aws` mounts, and passwordless sudo defaults;
- replace tracked certificates with generated fixtures;
- normalize 65 PNG files incorrectly marked executable and review the 30 actual
  executable/script entries;
- verify third-party asset licenses, particularly the GRUB theme tree;
- review 48 rows with an exact-content peer. Preserve package-local licenses,
  references, initializers, and layout-significant assets; delete only approved
  redundant copies; and
- treat all imported workflows, scripts, prompt files, and agent instructions
  as untrusted until reviewed.

## Recommended migration PR sequence

1. **Create intake boundaries.** Add owner-local `.staging/` contracts and move
   files according to the ledger without activating them.
2. **Build Realm's minimal baseline.** Merge the baseline Dockerfile,
   devcontainer, and minimal compose configuration with security gates and
   integration tests.
3. **Modularize Realm services.** Normalize optional service profiles, health
   checks, fixtures, and local-secret handling.
4. **Separate workstation behavior.** Keep Realm host profiles opt-in and move
   portable shell/Git behavior to Mantle.
5. **Assemble the Holon universal app template.** Merge the API and React
   fixtures, then add a thin Realm consumer profile.
6. **Reconcile Aether organization sources.** Compare specs, agents, and skills
   against the canonical library with explicit provenance/supersession records.
7. **Curate community agent material.** Establish the provenance/license/safety
   catalog before enabling any package.
8. **Split automation by owner.** Extract Relay mechanics and retain only thin
   Aether/Awesome callers.
9. **Merge bounded specialist material.** Handle Beacon, Egolint, Mindgarden,
   Identity, Renderflow, and remaining product assets in owner-scoped PRs.
10. **Drain and close intake.** Re-run the ledger, resolve approved duplicates,
    document archives, and remove `.staging/` only when it reaches zero tracked
    files.

## Reproducing the ledger

Generate or refresh it with:

```bash
python3 tools/staging_home_audit.py --repository-root "."
```

CI or a reviewer can verify that the checked-in ledger matches the current
tracked intake with:

```bash
python3 tools/staging_home_audit.py --repository-root "." --check
```

The CSV is the file-level disposition authority for this snapshot. If new files
arrive in `.staging/`, extend the classifier deliberately; its contract test
fails whenever a tracked staging file lacks a concrete owner or destination.
