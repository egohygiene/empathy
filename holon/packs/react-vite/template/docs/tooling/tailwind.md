# Tailwind CSS v3 configuration

The template deliberately standardizes on Tailwind CSS `3.4.19`. The reusable
design contract lives in `@egohygiene/tailwind-config`; the workspace root owns
content discovery and app composition in `tailwind.config.ts`.

## Included configuration

- class/data-attribute dark mode
- responsive screens from `xs` through `2xl`
- centered, responsive containers
- CSS-variable semantic colors and compatibility aliases
- accessible display, body, and mono font stacks
- display type, radii, shadows, spacing, reading widths, motion curves, and
  reusable animations
- typography, forms, and aspect-ratio plugins
- accessible focus and selection styles
- balanced/prettified text and content-visibility utilities
- app, package, Storybook, Markdown, and MDX content discovery
- a narrow safelist for runtime status colors and accessibility helpers

Apps import one stylesheet:

```ts
import "@egohygiene/tailwind-config/styles.css";
```

That stylesheet contains the Tailwind layers plus the default semantic tokens.
Products may replace token values without forking the utility configuration.

## Token contract

Colors are stored as space-separated RGB channels so Tailwind opacity modifiers
continue to work:

```css
:root {
  --color-primary-500: 139 92 246;
}
```

Use a utility such as `bg-primary/80`; do not wrap the variable in a second
`rgb()` call in product code. Brand packages should override variables at the
root or theme selector and retain the semantic names.

## Content and dynamic classes

Tailwind extracts complete class names from source text. Do not construct class
fragments such as `` `text-${status}` ``. Map runtime state to complete strings:

```ts
const statusClass = {
  error: "text-danger",
  ready: "text-success",
} as const;
```

Extend the safelist only when content genuinely arrives from a trusted external
source. Broad regular expressions increase CSS size and hide missing ownership.

## PostCSS boundary

Tailwind v3 uses the `tailwindcss` PostCSS plugin followed by `autoprefixer`.
The v4-only `@tailwindcss/postcss` and `@tailwindcss/vite` packages are not part
of this configuration. `postcss-import` runs first so layered stylesheets can be
composed deterministically.

Reference: [Tailwind CSS v3 configuration](https://v3.tailwindcss.com/docs/configuration).
