# First-pass readiness report

Date: 2026-08-16
Assessment: structurally integrated; dependency and runtime hardening remain

## Completed in this pass

- one Holon-owned pnpm/Turborepo workspace with four runnable app surfaces
- website, documentation, playground, and commerce-profile topology
- provider-neutral auth and commerce boundaries
- one canonical Vite configuration factory used by every app
- one Tailwind CSS v3 preset, PostCSS pipeline, token contract, and app import
- strict app ports/base paths and Playwright projects for all four surfaces
- root Task integration, workspace checks, release/quality configuration, and
  hardened starter CI
- source-disposition ledger covering website, store, universal, and Vite corpus
- canonical `@egohygiene/ui` component-library boundary with reusable feedback,
  loading, empty-state, media, scrolling, and skeleton patterns
- complete classification and removal of all 108 files in the universal staging
  subtree, with Git recovery pointers and deferred geospatial/OIDC profiles

## Validation completed

- every `package.json` parses as strict JSON
- all 21 workspace manifests have unique, resolvable `workspace:*` references
- all 22 TypeScript project references point to existing files
- YAML files parse successfully
- new JavaScript and erasable-TypeScript configuration files pass Node syntax
  checks
- the repository and template pass `git diff --check`
- the dependency-free workspace manifest checker passes

## Validation not yet completed

The execution environment could not reach the npm registry, so this pass could
not generate the first combined `pnpm-lock.yaml`, install the dependency graph,
or execute TypeScript, Vitest, Vite, Storybook, Playwright, Biome, and Prettier.
Those are mandatory gates for the next hardening pass; structural validation is
not a substitute for them.

## Component-library promotion validation

The universal UI follow-up used a focused temporary dependency environment so
it could validate the affected packages without generating the canonical
workspace lockfile:

- dependency-free workspace manifest validation passed;
- strict TypeScript checks passed for `ui`, `vite-config`, and
  `tailwind-config`;
- all 6 UI test files passed (11 tests);
- the Vite library build emitted ESM, CommonJS, CSS, source maps, and TypeScript
  declarations;
- the verified JavaScript artifacts were 7.63 kB ESM and 5.26 kB CommonJS;
- the verified CSS artifact was 10.29 kB (2.73 kB gzip);
- `git diff --check` and targeted Prettier formatting passed.

Generated `dist` output was inspected and removed after validation. Full
workspace installation, application builds, Storybook, accessibility-browser,
and Playwright execution remain part of dependency convergence.

## Preserved incompleteness

The promoted website skeleton contains empty feature barrels, draft docs,
package-local Vitest configurations, generator bodies, and test placeholders.
They were retained rather than silently deleted because several encode intended
future surfaces. None should be described as implemented solely because a path
exists.

The next implementation pass should classify them in this order:

1. Fill or remove imported/runtime-relevant placeholders.
2. Consolidate redundant package-local Vitest files into shared tooling.
3. Convert empty documentation into real contracts or remove it with a ledger
   entry.
4. Implement generators only after the materialized target tree stabilizes.
5. Turn empty feature barrels into explicit optional profiles or remove them.

## Recommended next PRs

1. **Dependency convergence and green build** — generate the lockfile, install,
   align version families, fix type/build/test failures, and restore frozen CI.
2. **Generic application content** — replace remaining organization/product
   copy with typed sample content while keeping Ego Hygiene as a documented
   example profile.
3. **Component package hardening** — run the library build and packed-consumer
   matrix, then switch source exports to `dist` when publication is authorized.
4. **Vite corpus parity** — add intentional viewer/WASM, maps, SSR,
   multi-page, and Nx variants or record why each is rejected.
5. **Instantiation and drift** — build a generator, golden fixtures, upgrade
   strategy, and PACE drift checks after the baseline is green.
