# React component-library architecture

## Decision

`packages/ui` (`@egohygiene/ui`) is the one canonical owner of reusable React
components in this template. A second “universal UI” application or parallel
component package would create competing ownership and is not retained.

Applications compose the library. They do not donate their routes, content,
provider clients, or environment reads back into it.

```text
apps/*
  -> @egohygiene/ui
      -> @egohygiene/icons
      -> @egohygiene/themes
      -> @egohygiene/utilities

@egohygiene/ui -/-> apps/*
@egohygiene/ui -/-> auth, routing, API clients, analytics, maps, commerce SDKs
```

## Component taxonomy

| Family        | Current components                             | Boundary                                                |
| ------------- | ---------------------------------------------- | ------------------------------------------------------- |
| actions       | `Button`, `LinkButton`                         | user-initiated navigation and commands                  |
| feedback      | `Alert`, `EnvironmentBanner`, `StatusBadge`    | state communication without feature policy              |
| progress      | `Spinner`, `LoadingState`, `Skeleton`          | loading and placeholder semantics                       |
| empty results | `EmptyState`                                   | consumer-provided title, description, icon, and actions |
| content       | `Card`, `MediaCard`, `HorizontalScroller`      | data-neutral content composition                        |
| layout        | `Container`, `Stack`, `Cluster`, `PageSection` | responsive spatial primitives                           |
| preferences   | `ThemeToggle`                                  | shared theme selection only                             |
| accessibility | `VisuallyHidden`                               | assistive-technology utility                            |

## API rules

- Prefer native HTML attributes and semantic elements over custom event APIs.
- Accept product content through typed props; never embed Ego Hygiene product
  copy, image paths, route names, or API response shapes in the package.
- Do not read `import.meta.env`, browser storage, URL state, or global stores in
  a presentational component.
- Keep provider-specific behavior in an adapter package or optional profile.
- Use named exports and colocate component source, types, stories, and tests.
- Use the `eh-*` class namespace and semantic theme variables; consumers may
  add classes but should not depend on internal DOM depth.
- Add a release note for public prop, export, semantic, or token changes.

## Accessibility baseline

Every interactive component must support keyboard operation, visible focus,
appropriate names and roles, disabled/busy state where relevant, reduced
motion, high contrast, and zoom/reflow. Loading patterns use one live region,
decorative spinners stay hidden from assistive technology, images require alt
text, and horizontal overflow regions are named and focusable.

Stories are component documentation and accessibility fixtures. Unit tests own
critical semantics; Storybook accessibility checks own rendered violations;
consumer end-to-end tests own feature behavior.

## Styling and theming

The package ships one explicit `styles.css` entry. It consumes tokens from
`@egohygiene/themes` and does not require a particular product palette. CSS is
kept separate from the JavaScript entry during workspace development so apps
control cascade order. Motion must have a reduced-motion alternative.

Tailwind CSS remains an application authoring tool, not the public component
contract. This prevents compiled components from requiring consumer Tailwind
content scanning and keeps the package usable in plain React/Vite consumers.

## Build and publication boundary

`createReactLibraryConfig` in `@egohygiene/vite-config` externalizes React and
workspace dependencies and emits ESM, CommonJS, CSS, and source maps. TypeScript
then emits declarations into the same `dist/` tree. The source export map stays
active during incubation; the first public release must switch it to `dist`
only after packed-consumer validation.

See [`packages/ui/README.md`](../../packages/ui/README.md) for commands and the
publication checklist.
