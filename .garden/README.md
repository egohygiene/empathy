# Empathy Garden

This directory is Empathy's first Mindgarden consumer instance. Its committed
Markdown and YAML are canonical repository knowledge that may later be viewed
through Obsidian, published through GitHub Pages, or retrieved by agent tools.

The initial pass intentionally contains only the portable v0 contract and a
home map. Obsidian configuration, agent adapters, ingestion, indexing, and Pages
publishing will arrive through separately reviewable changes.

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
