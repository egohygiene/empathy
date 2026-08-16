# Ego Hygiene React + Vite template

A batteries-included TypeScript monorepo for product websites, documentation,
component playgrounds, and optional commerce surfaces. This is an incubating
template: breadth is intentional, capabilities are made explicit, and later
passes can polish the defaults after real product usage proves them.

## Included applications

| Application       | Package                    | Default path   | Purpose                                    |
| ----------------- | -------------------------- | -------------- | ------------------------------------------ |
| `apps/web`        | `@egohygiene/template-web` | `/`            | Generic product/organization website       |
| `apps/docs`       | `@egohygiene/docs`         | `/docs/`       | Repository and product documentation       |
| `apps/playground` | `@egohygiene/playground`   | `/playground/` | Design-system and package integration lab  |
| `apps/storefront` | `@egohygiene/storefront`   | `/store/`      | Optional provider-neutral commerce profile |

## Included platform packages

- API client, runtime configuration, schemas, content, and internationalization
- design tokens, themes, icons, UI primitives, utilities, and visualizations
- provider-neutral authentication with a safe development adapter
- provider-neutral commerce, store configuration, and storefront UI
- canonical Vite and Tailwind CSS configuration packages

The template also includes Turborepo, pnpm workspaces, Biome, Prettier,
TypeScript strict mode, Vitest, Playwright, Storybook, Changesets, dependency
and secret scanning configuration, release tooling, workspace generators, and
deployment examples.

## Requirements

- Node.js 24.19 or newer
- Corepack
- pnpm 11.19 or newer
- Task 3 (optional command facade)

## Install and run

```bash
corepack enable
pnpm install --no-frozen-lockfile
pnpm dev
```

Run one surface:

```bash
pnpm --filter @egohygiene/template-web run dev
pnpm --filter @egohygiene/docs run dev
pnpm --filter @egohygiene/playground run dev
pnpm --filter @egohygiene/storefront run dev
```

Copy `.env.example` to `.env.local` only when you need overrides. Every
`VITE_*` variable is public browser data.

## Deterministic checks

```bash
pnpm format:check
pnpm lint
pnpm typecheck
pnpm test
pnpm build
pnpm test:e2e
pnpm check
```

Generate per-app bundle treemaps:

```bash
pnpm build:analyze
```

## Configuration

- [`docs/tooling/vite.md`](docs/tooling/vite.md) explains the shared Vite
  factory, secure defaults, feature switches, and per-app composition.
- [`docs/tooling/tailwind.md`](docs/tooling/tailwind.md) explains the Tailwind
  CSS v3 preset, token contract, content scanning, and customization boundary.
- [`docs/profiles/commerce/`](docs/profiles/commerce/) documents the optional
  storefront and its provider adapter.
- [`docs/architecture/component-library.md`](docs/architecture/component-library.md)
  defines the reusable React component contract and publication boundary.
- [`docs/profiles/geospatial/roadmap.md`](docs/profiles/geospatial/roadmap.md)
  and [`docs/profiles/auth/oidc-roadmap.md`](docs/profiles/auth/oidc-roadmap.md)
  preserve optional profile intent without coupling it to the core UI package.
- [`docs/migration/staging-promotion-ledger.md`](docs/migration/staging-promotion-ledger.md)
  records exactly what was promoted, retained, or removed from `.staging`.
- [`docs/migration/first-pass-readiness.md`](docs/migration/first-pass-readiness.md)
  distinguishes validated structure from the dependency/runtime gates still due.

## Incubation boundary

This directory is the materialized template. `holon/packs/react-vite` owns the
incubation metadata and migration decisions. Individual product repositories
remain independent: they consume the baseline and own their branding, content,
routes, secrets, infrastructure, and deployment policy.

The staged website did not include a workspace lockfile. During incubation,
setup uses `--no-frozen-lockfile`; the first dependency-hardening pass must
generate and commit the combined `pnpm-lock.yaml`, then restore frozen installs
for CI, Task, container, and deployment commands.
