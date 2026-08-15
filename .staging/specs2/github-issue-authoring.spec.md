# GitHub Issue Authoring Specification

## Purpose

When asked to generate a GitHub issue, always produce output that is immediately copyable into GitHub without requiring manual cleanup.

Assume the user will copy and paste directly from ChatGPT.

---

# Output Format

Always produce exactly two code blocks.

Do not output any additional code blocks unless explicitly requested.

---

## Code Block 1

Language:

```text
```

Contents:

Only the GitHub issue title.

Format:

```text
{emoji} {title}
```

Example:

```text
🏗️ Unify CI/CD workflows into reusable workflows
```

Do not include:

- "Title:"
- Markdown headings
- Quotes
- Bullets
- Explanation

Only the title text.

---

## Code Block 2

Language:

```markdown
```

Contents:

The complete GitHub issue body.

The issue should follow the repository's standard issue template.

---

# GitHub Issue Structure

Unless instructed otherwise, use the following sections.

```text
## Summary

## Goals

## Scope

## Constraints

## Expected File Changes

## Validation

## Acceptance Criteria

## References

## TODO.md
```

Additional sections may be added when they improve clarity.

---

# Markdown Rules

The markdown code block must contain only valid GitHub-flavored Markdown.

Do not nest fenced code blocks inside another fenced code block.

When code examples are required inside the issue body, prefer indented code blocks instead of nested triple backticks.

Always ensure every opened code fence is closed.

Never leave an unterminated markdown block.

---

# Writing Style

Use:

- concise engineering language
- architecture-first thinking
- specification-driven wording
- implementation guidance rather than implementation details

Avoid unnecessary filler.

Assume the issue will be implemented by GitHub Copilot.

---

# Acceptance Criteria

Acceptance criteria should:

- be implementation-focused
- be measurable
- use GitHub checklist syntax

Example:

- [ ] CI passes.
- [ ] Documentation updated.
- [ ] Tests added.
- [ ] Analyzer passes.

---

# TODO.md

Every issue should end with a `TODO.md` section instructing the implementer to:

- update the repository root `TODO.md`
- check off completed work
- add discovered follow-up tasks
- avoid checking off unfinished work
- preserve unrelated TODO items
- advance the active phase when appropriate

---

# Important

Never wrap the title and markdown body inside a single code block.

Never output the markdown issue outside the markdown code block.

Always close every code fence.

The output should be immediately copyable into GitHub with no editing required.

# Repository Context

Assume the repository follows:

- architecture-first development
- specification-driven development
- long-term maintainability
- developer experience first
- reusable systems over one-off solutions

When reasonable, prefer creating one cohesive issue over many tiny issues.
