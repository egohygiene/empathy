# Universal UI source audit

Date: 2026-08-16
Source commit: `4815192f9e0cd70ddb870992a493f379d5f76d8e`
Source path: `.staging/react-template/universal`

## Snapshot identity

- files: 108
- bytes: 2,750,672
- ordered path-list SHA-256:
  `bd837eabf04e247dea25533fc090e9e9222ce86f8d1ff744295760c44785c492`
- largest source asset: `public/universal.png` (1,715,879 bytes)

Git preserves the complete source tree at the commit above. This report keeps
its identity and the migration decisions in the active template without
copying an incomplete application into a second archive directory.

## Readiness findings

The source was useful as a design and capability corpus, but it was not a
runnable universal application:

- `package.json` has no package name, while its README filters by
  `universal-ui`;
- declared scripts reference absent `tsconfig.typecheck.json` and
  `eslint.config.mjs` files;
- the cloud-provider barrel imports absent Dropbox, Carto, and Foursquare
  provider implementations;
- `useGroupDrowdown.ts` imports an absent `useMaps` hook and retains an inline
  replacement instruction;
- `HomePage.tsx` imports absent Announcement, Banner, and Map components;
- the About route imports an absent animation JSON file;
- the Kepler component imports undeclared AI assistant, DuckDB,
  styled-components, and resizable-panel packages;
- the code mixes TanStack Router, React Router, Redux Toolkit, legacy
  `react-query`, modern TanStack Query, Axios, direct local storage, and direct
  environment reads without a coherent application boundary;
- app pages contain Universal/Kepler demonstration copy and authorization
  assumptions, so they are not reusable component-library content.

These are source facts, not criticisms of the intended capabilities. They are
why the promotion synthesizes stable contracts and records deferred profiles
instead of moving files wholesale.

## Asset evidence

The staged icon set contains valid PNGs at 16, 32, 48, 64, 128, 192, 256, 384,
and 512 pixels plus a multi-resolution ICO. It is branded “Universal,” has no
source design specification or ownership metadata, and does not cover the
canonical identity asset contract.

Representative SHA-256 values:

| Asset              | SHA-256                                                            |
| ------------------ | ------------------------------------------------------------------ |
| `favicon.ico`      | `1c34f65c134ab58283ea6999ed90360844fc4ab2b5f3f55c44ff4a2fd15e5475` |
| `universal.png`    | `2315827268e711de7cb5c391a6573b3ff1a8c1a4eebb0310b7177b53d89ddcf1` |
| `icon-192x192.png` | `9241ac04d9009b1c933c1bc488f0ed00c43fc10d190b15b5896d8675b69957e8` |
| `icon-512x512.png` | `f3f61719278c3dbfb94df7fa361a2af0c0b90c0cc385bcda89cb0f250e79ddfb` |

The files are retired from the active template rather than relabeled as Ego
Hygiene assets. The `identity` system remains the owner of future favicon, PWA,
maskable, Apple touch, social-preview, and related branded variants.

## Complete disposition map

Every one of the 108 source files is covered below. Mixed directories name the
exception explicitly.

| Source group                                              |   Files | Final disposition         | Canonical result                                                                             |
| --------------------------------------------------------- | ------: | ------------------------- | -------------------------------------------------------------------------------------------- |
| `apps/README.md`                                          |       1 | Retired                   | superseded by the template README and app catalog                                            |
| `apps/ui/*` top-level files                               |       7 | Superseded                | canonical root Vite, Tailwind, PostCSS, Vitest, package, and Task configuration              |
| `public/assets/icons/*`                                   |       9 | Retired                   | identity-generated application assets; evidence retained above and in Git                    |
| `public/{favicon.ico,manifest.webmanifest,universal.png}` |       3 | Retired                   | canonical PWA factory plus future identity output                                            |
| `public/vendor/css/*`                                     |       3 | Superseded                | provider package CSS imports; no committed minified vendor copies                            |
| `scripts/tools/copy-models.sh`                            |       1 | Retired                   | app-local model copying conflicts with workspace package ownership                           |
| `src/{App.tsx,main.tsx}`                                  |       2 | Retired                   | incomplete application shell; apps remain explicit consumers                                 |
| `src/api/*`                                               |       6 | Superseded / Deferred     | generic client concepts owned by `api-client`; `maps.ts` deferred to geospatial profile      |
| `src/auth/*`                                              |       9 | Superseded / Deferred     | provider-neutral behavior owned by `auth`; OIDC adapter contract recorded separately         |
| `src/cloud-providers/index.ts`                            |       1 | Deferred                  | geospatial provider-adapter roadmap                                                          |
| generic `src/components/*`                                |      16 | Materialized / Superseded | rewritten into canonical UI actions, feedback, loading, empty, content, and layout patterns  |
| map-specific `src/components/*`                           |       8 | Deferred                  | geospatial profile; broken prototype not presented as a package                              |
| `src/config/*`                                            |       3 | Superseded                | browser-safe `config` package and app-owned configuration                                    |
| `src/data/blogCategories.ts`                              |       1 | Retired                   | product content belongs to consuming apps/content packages                                   |
| `src/hooks/*`                                             |       7 | Superseded / Deferred     | auth and health concepts use canonical packages; three map hooks defer to geospatial profile |
| `src/models/*`                                            |       6 | Superseded / Deferred     | auth/API models use canonical contracts; map models defer to geospatial profile              |
| `src/pages/**/*`                                          |      13 | Retired                   | incomplete product/demo routes are not library source                                        |
| `src/routes/*`                                            |       9 | Retired                   | routing is app-owned; auth exposes provider-neutral guards                                   |
| `src/styles/app.css`                                      |       1 | Superseded                | canonical theme, Tailwind, and `@egohygiene/ui` CSS layers                                   |
| `src/utils/*`                                             |       2 | Superseded                | typed API client and utilities packages                                                      |
| **Total**                                                 | **108** |                           |                                                                                              |

The generic component count covers Button (5), CategoryCard (2),
CategoryCarousel (1), ErrorMessage (1), LoadingSpinner (1), MockBanner (3),
PageLoader (2), and the component barrel (1). The map-specific count covers
MapStateManager (1), TestCreateMapButton (1), and the Kepler Map subtree (6).

## Materialized design ideas

| Source concept                | Canonical component or contract                                |
| ----------------------------- | -------------------------------------------------------------- |
| Button                        | existing `Button`/`LinkButton`, strengthened loading semantics |
| ErrorMessage                  | `Alert` with semantic tones and consumer-owned content         |
| LoadingSpinner and PageLoader | `Spinner` and size-aware `LoadingState`                        |
| MockBanner                    | prop-driven `EnvironmentBanner`, with no environment read      |
| CategoryCard                  | content-neutral `MediaCard`                                    |
| CategoryCarousel              | keyboard-focusable, named `HorizontalScroller`                 |
| route placeholder behavior    | `Skeleton` and `EmptyState` primitives                         |
| component stories/tests       | canonical Storybook CSF stories and semantic unit tests        |

No staged source path remains after this promotion. Deferred means the
capability has an explicit future profile and recovery point, not that broken
implementation code is silently shipped.
