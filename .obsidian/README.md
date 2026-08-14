# Empathy Obsidian Profile

Open the **repository root** as the Obsidian vault. Do not open `.garden/` as a
nested vault: repository links are intentionally part of the same knowledge
space, and nested vault boundaries can break link maintenance.

## Safe baseline

The committed profile configures:

- `.garden/inbox/` as the default new-note location;
- `.garden/attachments/` as the attachment location;
- `.garden/templates/` as the template folder;
- automatic link updates and relative Markdown paths;
- a first-party `mindgarden.css` dashboard snippet.

Enable the **Bases** core plugin if it is not already enabled, then open
`.garden/dashboard.md`. Bases reads note properties directly from Markdown and
does not create a separate database.

## Local state

Workspace layouts, caches, installed plugin binaries, and plugin data are
machine-local and ignored by Git. The shareable profile never commits secrets,
API keys, or a developer's open tabs.

## Community plugins

No community plugin is required or automatically enabled. Community plugins run
third-party code, so Restricted Mode and installation remain human decisions.

The machine-readable profile at
[`mindgarden/profiles/obsidian/profile.json`](../mindgarden/profiles/obsidian/profile.json)
declares Project Manager as an optional enhancement. Review its repository and
permissions, turn off Restricted Mode deliberately, install `project-manager`
from Obsidian's community directory, and enable it only if its table, Gantt, and
Kanban views are useful.

Dataview is not part of the baseline. Its upstream repository was archived on
2026-08-13, and native Bases now covers the dashboard's foundational query and
view requirements without JavaScript execution.
