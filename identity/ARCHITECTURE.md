# Architecture

## Layers

1. **Consumer intent** — `.identity/identity.toml`, `.identity/brief.md`, and
   approved references define project-owned identity intent.
2. **Reusable contracts** — schemas and versioned profiles define valid inputs
   and output targets without owning a consumer's brand.
3. **Planning and handoff** — the CLI resolves profiles into an explainable,
   deterministic asset plan and a tool-neutral creative handoff.
4. **Approved sources** — a human promotes selected candidate artwork into
   `.identity/sources/`.
5. **Generation and verification** — future renderers derive committed assets,
   metadata, previews, and reports from approved sources.
6. **Adapters** — future framework, marketplace, and Renderflow integrations
   consume the generated package without changing canonical identity intent.

## Invariants

- AI is an optional authoring collaborator, not part of deterministic builds.
- Canonical source artwork is small, reviewable, and human-approved.
- Platform targets are versioned because external requirements change.
- Output paths are repository-relative and may not escape the repository.
- Profiles explain their provenance and the date on which requirements were
  verified.
- App behavior such as PWA scope and navigation remains application-owned.
- Reusable source beneath `identity/` never imports Empathy-specific files.
