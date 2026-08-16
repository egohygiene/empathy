# `@egohygiene/ui`

Accessible, themeable React primitives and product-neutral interface patterns
for Ego Hygiene applications. This package is the canonical owner of reusable
React UI in the React + Vite template.

## Install inside the workspace

```bash
pnpm --filter @egohygiene/template-web add "@egohygiene/ui@workspace:*"
```

Import the component API and the shared stylesheet:

```tsx
import { Alert, Button, LoadingState, Stack } from "@egohygiene/ui";
import "@egohygiene/ui/styles.css";

export function Example() {
  return (
    <Stack>
      <Alert title="Ready" tone="success">
        The shared interface layer is active.
      </Alert>
      <LoadingState message="Loading resources…" />
      <Button>Continue</Button>
    </Stack>
  );
}
```

Applications should also install the canonical theme and Tailwind CSS layers
described in the template documentation. Components use the stable `eh-*` CSS
namespace and the semantic tokens owned by `@egohygiene/themes`.

## Public component families

- actions: `Button`, `LinkButton`
- feedback: `Alert`, `EnvironmentBanner`, `StatusBadge`
- progress and placeholders: `Spinner`, `LoadingState`, `Skeleton`, `EmptyState`
- content: `Card`, `MediaCard`, `HorizontalScroller`
- layout: `Container`, `Stack`, `Cluster`, `PageSection`
- preferences and accessibility: `ThemeToggle`, `VisuallyHidden`

The package owns presentation and interaction semantics. Product copy, routes,
API requests, auth decisions, feature flags, analytics, and provider SDKs stay
with consumers or their dedicated packages.

## Development

```bash
pnpm --filter @egohygiene/ui run typecheck
pnpm --filter @egohygiene/ui run test
pnpm --filter @egohygiene/ui run build
pnpm storybook
```

The build emits ESM, CommonJS, CSS, source maps, and TypeScript declarations to
`dist/`. Workspace exports intentionally continue to target `src/` during
incubation so `pnpm dev` does not require a prebuild.

## Publication gate

The package remains `private: true` while it is incubated in Empathy. Before its
first registry release:

1. make the combined workspace green and commit the canonical lockfile;
2. run type, unit, accessibility, Storybook, package-build, and package-content
   checks in CI;
3. replace source exports with conditional `dist` exports for ESM, CommonJS,
   declarations, and `styles.css`;
4. set `private` to `false`, confirm the final package scope and license, and
   publish through Changesets with npm provenance;
5. validate a packed tarball in both a plain Vite consumer and the template
   playground before promoting a stable release.

The package manifest already declares public access, provenance, packaged
files, side effects, and broad React 19 peer ranges so that publication is an
explicit hardening pass instead of a redesign.
