# GitHub Copilot Instructions

## Purpose

This repository follows a structured, reusable, and automation-focused
engineering workflow.

When making changes:
- prioritize maintainability and clarity
- prefer explicit behavior over implicit behavior
- optimize for long-term readability and reproducibility
- avoid introducing unnecessary complexity

---

# Engineering Principles

## Prefer Simplicity

- Prefer small, focused changes.
- Avoid premature abstraction.
- Favor readable and predictable implementations.

---

## Preserve Existing Structure

- Follow established repository patterns and conventions.
- Reuse existing utilities and abstractions where appropriate.
- Avoid introducing parallel systems that duplicate functionality.

---

## Make Incremental Changes

- Prefer incremental refactors over large rewrites.
- Avoid unrelated modifications in the same change set.
- Keep pull requests scoped to a single responsibility.

---

# Validation Expectations

Before finalizing changes:

- ensure linting passes
- ensure tests pass where applicable
- ensure generated artifacts are not unintentionally committed
- ensure formatting is consistent with repository configuration

Do not assume changes work without validation.

---

# Repository Conventions

## Formatting

This repository uses:
- EditorConfig
- Prettier
- ESLint
- additional repository-specific linting tools where configured

Respect existing formatting and linting rules.

---

## Documentation

When introducing new systems or workflows:
- update relevant documentation
- include concise comments where helpful
- avoid redundant comments that restate obvious behavior

---

## Configuration Changes

When modifying configuration:
- prefer conservative defaults
- avoid tool-specific hacks unless necessary
- preserve cross-platform compatibility where possible

---

# Automation & CI

Treat CI failures as important signals.

When changing:
- workflows
- scripts
- tooling
- dependency management
- build systems

consider how changes affect:
- reproducibility
- local development
- automation pipelines
- caching behavior
- cross-platform execution

---

# AI-Assisted Development Expectations

AI-generated code must still be:
- reviewed
- validated
- maintainable
- understandable

Do not introduce code that cannot be confidently explained or maintained.

Prefer:
- explicit naming
- structured organization
- minimal surprise

over:
- cleverness
- unnecessary abstraction
- opaque generated code

---

# Repository Exploration

Before introducing new dependencies, utilities, or patterns:
- search for existing implementations
- reuse established conventions when appropriate

Avoid unnecessary duplication.

---

# Final Guidance

Prioritize:
1. clarity
2. maintainability
3. reproducibility
4. developer experience
5. long-term project health
