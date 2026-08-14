# Empathy Garden

This directory is Empathy's first Mindgarden consumer instance. Its committed
Markdown and YAML are canonical repository knowledge that can be viewed through
Obsidian and may later be published through GitHub Pages or retrieved by agent
tools.

Open the repository root, not this directory, as the Obsidian vault. That keeps
repository documents and `.garden/` notes in one linkable knowledge space while
the shareable vault profile under [`.obsidian/`](../.obsidian/README.md) keeps
machine-local workspace state out of Git.

The current profile uses Obsidian's native Bases feature and first-party CSS for
the garden dashboard. Agent adapters, ingestion, indexing, and Pages publishing
remain separate future changes.

## Public boundary

Empathy is a public repository. Every committed note in this directory must use
`visibility: public`. Material that is private or merely internal belongs in the
ignored `.garden.local/` overlay and must not be committed.

## Validation

From the repository root, run:

```bash
task garden:check
```

The manifest declares which paths contain validated knowledge. Templates and
generated artifacts are outside those content roots.

Start from [`dashboard.md`](dashboard.md) for the visual knowledge view or
[`home.md`](home.md) for the compact garden map.

Agents can begin at [`../llms.txt`](../llms.txt) or use the deterministic
[agent profile](../mindgarden/profiles/agent/README.md) for validated search and
bounded context packs.
