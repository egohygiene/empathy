# Empathy current work

The [live GitHub roadmap (#118)](https://github.com/egohygiene/empathy/issues/118)
tracks issue order, prerequisites, and acceptance. Open its current focus and
review any linked draft PRs before selecting work. The
[2026-10-19 completeness audit](../audits/empathy-completeness-20261019T132001Z.md)
and its [validation receipt](../audits/data/empathy-completeness-20261019T132001Z.validation.json)
record the dated findings behind the roadmap.

The [strategic roadmap](../ROADMAP.md) describes the intended architecture.
[Repository agent instructions](../AGENTS.md) document review and acceptance
requirements. The [ownership decision](decisions/ADR-0001-foundation-ownership.md)
identifies the durable owner for each capability.

## Start from a clean checkout

| Area                   | Owner and prerequisites                                                                                                                            | Inspect and check                                                                                                                                                 |
| ---------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Foundation composition | Empathy; Python 3.11+                                                                                                                              | Read the [foundation contract](foundation/README.md), then run `python3 tools/foundation.py validate-manifest --manifest foundation/empathy.manifest.json`.       |
| Selected local CI      | Empathy composition; immutable Realm checkout, act and eligible Linux Docker for workflow execution                                                | Follow the [local CI consumer guide](integrations/LOCAL_CI.md); `plan` reads the explicit selection, while `run` retains scoped results and unsupported coverage. |
| Visual identity        | Identity owns the compiler; Empathy owns its inputs. Initialize the pinned submodule, and use Task, Python 3, and Cargo as described in the guide. | Follow the [Identity v1 guide](integrations/IDENTITY_V1.md) from source validation through generation and snapshot verification.                                  |
| Staging                | Empathy owns intake evidence and its file ledger. Capability owners supply migration evidence.                                                     | Read the [staging contract](migration/STAGING.md) before proposing any change to preserved intake.                                                                |

Foundation resolution and checked-in projections are active. Some specialist
capabilities are pinned consumers, some sources remain in incubation or frozen
intake, and generated outputs have their own source and verification contracts.
Release and installation evidence belongs to the owning issue and consumer
workflow. Use the [task catalog](../TASKS.md) to choose an applicable check,
then record the reviewed revision, results, and remaining evidence in the
implementation PR.
