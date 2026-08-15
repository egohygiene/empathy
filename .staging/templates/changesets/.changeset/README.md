# Changesets

This repository uses Changesets for versioning and release management.

## Creating a Changeset

When a change affects a published package:

```bash
pnpm changeset
```

Follow the prompts to:

* Select affected packages.
* Choose the version bump type.
* Write release notes.

This creates a markdown file in:

```text
.changeset/
```

Example:

```md
---
"my-package": minor
---

Add support for GitHub Pages deployment.
```

## Releasing

Typical workflow:

```bash
pnpm changeset version
```

Updates:

* package versions
* changelogs

Then:

```bash
pnpm changeset publish
```

Publishes packages.

## References

* <https://github.com/changesets/changesets>
* <https://github.com/changesets/changesets/blob/main/docs/common-questions.md>
