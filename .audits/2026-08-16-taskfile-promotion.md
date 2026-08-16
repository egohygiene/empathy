# Staged Taskfile promotion audit

## Decision

The staged Task corpus was assimilated into an explicit repository command
architecture on 2026-08-16. Universal lifecycle and Git inspection tasks were
promoted, existing root commands were split into owned modules, degraded copies
were removed as duplicates, and unavailable product/tool-specific definitions
were consolidated into one inert review queue.

The root `Taskfile.yml` now contains composition only. Public root commands are
implemented under `.tasks/`, while Beacon, Egolint, Mantle, the React + Vite
pack, and complementary tools retain subsystem-owned Taskfiles and namespaces.

## Source evidence

- Source tree: `.staging/tasks/`
- Recoverable source commit: `be89125`
- Source files: 9
- Source bytes: 16,017
- Manifest SHA-256: `265d1f9d874d1f4b82ab30011ce76b9937439c5bc546352ce28a6e75399c7dfb`

The manifest digest is the SHA-256 of the sorted `sha256sum` output for every
direct file in the source directory. Individual source checksums follow.

| Source              | SHA-256                                                            |
| ------------------- | ------------------------------------------------------------------ |
| `agents copy.yml`   | `0bfd7db340eab738c900319d0762e32011201c95d3aadc5416e96695edf21af9` |
| `agents.yml`        | `0a16efacdef7b0aae433dc49e0bf623fef5fe0d55b875bab74ae023d471aebf3` |
| `app.yml`           | `e40f55389b4b414a39cf15b6bf90913ba9f8b9fcf76ccea6d464cb2020ba99cc` |
| `copilot.yml`       | `1bbbb477a58c4e5e823a18adfb6aac845789741a640585050a385c922ed8b85a` |
| `git.yml`           | `acd35c08cd45c92ffd836ff0696007a46ee73ff3a71043423c1bcc0d660dda21` |
| `project.yml`       | `aad14444da85275a61d96aab636cc1e7351f0b0596d097dd329c231adbf7b613` |
| `security copy.yml` | `95034634e4408707960b07f94e03e6309da8cfc8e48edcd1dd792a4b662940b8` |
| `security.yml`      | `751635e00ce0469ae7cb34b612efc4283292dd362537b391dbe9ddda64114ff0` |
| `tests.yml`         | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

## Disposition

| Source              | Classification                     | Destination and rationale                                                                                                                                                          |
| ------------------- | ---------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `git.yml`           | Promoted and upgraded              | `.tasks/git.yml`; retained all read-only helpers and added changes/remotes inspection.                                                                                             |
| `project.yml`       | Promoted and generalized           | `.tasks/project.yml`; retained platform/version concepts and completed the stable lifecycle contract. Flutter/Java diagnostics moved to the deferred application queue.            |
| Existing root tasks | Refactored without behavioral loss | `.tasks/quality.yml`, `.tasks/mindgarden.yml`, and `.tasks/identity.yml`.                                                                                                          |
| `app.yml`           | Deferred, product-specific         | `.staging/tasks-todo.yml`; all 27 public Flutter application tasks plus the internal guard remain reviewable. Empathy has no `apps/egohygiene/pubspec.yaml` or integration runner. |
| `agents.yml`        | Deferred, unavailable capability   | `.staging/tasks-todo.yml`; all seven tasks remain reviewable. Empathy has no agent doctor, Mindcap Taskfile, or declared OpenCode/Ollama contract.                                 |
| `copilot.yml`       | Deferred, unavailable capability   | `.staging/tasks-todo.yml`; both tasks remain reviewable. The referenced hook config and fixture script are absent.                                                                 |
| `security.yml`      | Deferred, host-specific capability | `.staging/tasks-todo.yml`; Lynis remains explicit and nonprivileged, but the referenced profile is absent and host auditing is not a universal repository check.                   |
| `agents copy.yml`   | Superseded duplicate               | Removed; it is a less guarded subset of `agents.yml`.                                                                                                                              |
| `security copy.yml` | Superseded duplicate               | Removed; it is a malformed, less complete predecessor of `security.yml`.                                                                                                           |
| `tests.yml`         | Empty duplicate                    | Removed; zero-byte file with no task definition.                                                                                                                                   |

No task from the staged source was silently discarded. Deferred definitions are
not imported and therefore cannot appear as supported repository capabilities.

## Added controls

- `TASKS.md` separates command documentation from the root README.
- `tools/task_catalog.py` renders the live public command graph into
  `TASKS.md`, preventing hand-maintained command lists from drifting.
- `task taskfile:check` verifies Task can resolve the complete include graph and
  that the committed catalog is current.
- `task taskfile:catalog:write` intentionally updates the generated catalog.
- `.tasks/README.md` records ownership and universalization rules.

## Recovery

To inspect an original source without restoring the staging directory, use:

```bash
git show be89125:.staging/tasks/git.yml
```

Replace `git.yml` with any source path listed above.
