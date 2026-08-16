# React template staging-promotion ledger

Date: 2026-08-16
Scope: first React + Vite template incubation pass

This ledger records source disposition so `.staging` is cleared intentionally.
“Removed” below means a staged duplicate was deleted only after a promoted
canonical equivalent or explicit preservation target was identified.

## Target boundary

The materialized workspace is `holon/packs/react-vite/template`. It remains an
Empathy-incubated Holon pack. Product websites and stores are independent
consumers; they are not collapsed into one deployment or product repository.

## Website source

Source: `.staging/react-template/website`

Disposition: promoted in full as the structural foundation. The application
`apps/egohygiene.io` became `apps/web`, and the workspace was renamed
`@egohygiene/react-vite-template`. Existing packages, documentation, scripts,
tests, Storybook, CI examples, and infrastructure examples were preserved for
subsequent hardening passes.

## Store source

Source: `.staging/react-template/store`

Promoted:

- `apps/storefront` to the optional commerce application
- `packages/commerce`, `packages/store-config`, and `packages/store-ui`
- commerce architecture, routing, provider setup, and roadmap documentation
- storefront Playwright coverage and Vercel example
- source README and environment example under `docs/provenance`
- the source CNAME under `docs/provenance` so the generic template cannot
  accidentally claim a live product domain
- zero-byte website icon placeholders were replaced with a valid neutral SVG;
  full PNG, Apple touch, maskable, and social variants are deferred to the
  `identity` asset-generation pass
- store agent rules, expanded into the template-level `AGENTS.md`
- Taskfile command facade and deterministic cleanup script

Merged into canonical root files:

- package scripts and development dependencies
- environment variables
- workspace, TypeScript, Turborepo, Playwright, Biome, Changesets, editor, and
  package-manager configuration
- contribution, conduct, security, license, CI, and dependency-update metadata

Removed after merge:

- the store-only lockfile, because the combined workspace generates one new
  canonical lockfile
- duplicate root configuration and repository metadata
- the narrower JavaScript workspace checker, superseded by the typed workspace
  checker from the website foundation

## Universal source

Source: `.staging/react-template/universal`

Promoted by synthesis:

- authentication became the provider-neutral `@egohygiene/auth` adapter,
  context, authorization helpers, protected-render component, and safe in-memory
  adapter
- Tailwind forms, typography, aspect ratio, font, and content-discovery ideas
  informed `@egohygiene/tailwind-config`
- PWA, SVG, and WASM requirements informed the shared Vite factory

Retained in staging:

- Kepler/map UI, map state, cloud-provider, and map API code
- universal-specific pages, routes, category content, and runtime API models
- the original auth implementation for comparison until an OIDC adapter profile
  is implemented and tested
- icon corpus and map vendor assets pending identity/asset deduplication

The retained material is not considered production-ready. It will be reviewed
as maps, cloud, OIDC, and asset profiles rather than copied into the core.

## Vite corpus

Source: `.staging/vite.corpus.txt`

Promoted by synthesis into `@egohygiene/vite-config`: React SWC, strict servers,
aliases, environment loading, SVG, WASM, PWA, diagnostics, bundle visualization,
production chunking, source-map policy, and multi-app port/base-path support.

The corpus remains staged for a later parity pass covering specialized viewer,
map, library-mode, SSR, multi-page, and Nx variants. It must not be removed until
those variants have explicit promote/defer/reject decisions.

## Follow-up passes

1. Make the combined workspace fully green and reduce dependency-version drift.
   Generate and commit the first combined `pnpm-lock.yaml`, then restore frozen
   installation flags across CI, Task, container, and deployment examples.
2. Genericize remaining Ego Hygiene website content into replaceable sample data.
3. Classify the retained universal map/cloud assets into optional profiles.
4. Review every Vite corpus variant against the canonical factory.
5. Add a generator/instantiator and drift policy once the target shape stabilizes.
