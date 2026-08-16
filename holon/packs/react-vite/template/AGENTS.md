# React + Vite template agent instructions

## Mission and ownership

Maintain a comprehensive but coherent React + Vite baseline for Ego Hygiene.
The template is incubated by the `holon` surface. Applications demonstrate
composition; packages own reusable behavior; product repositories own their
content and deployments.

Do not silently remove optional capabilities. Prefer an opt-in profile, adapter,
or documented disposition over deletion while the template is incubating.

## Dependency direction

```text
apps/*
  -> packages/*

apps/storefront
  -> packages/store-ui
  -> packages/store-config
  -> packages/commerce
```

The application may depend on packages. Packages must never import application
modules.

## Template rules

- Keep runnable applications under `apps/`.
- Keep reusable, product-neutral behavior under `packages/`.
- Configure browser applications through `@egohygiene/vite-config`.
- Configure Tailwind CSS through `@egohygiene/tailwind-config` and the root
  `tailwind.config.ts`.
- Treat every `VITE_*` value as public browser data. Never put secrets in it.
- Keep provider-specific auth and commerce logic behind adapter contracts.
- Preinstall useful integrations, but make expensive or environment-specific
  capabilities opt-in.
- Preserve a source-to-target decision in `docs/migration/` when promoting or
  deleting staged material.

## Commerce rules

- Keep Fourthwall details inside `packages/commerce/src/fourthwall`.
- UI components consume normalized commerce models only.
- Preserve mock mode so a clean clone can run without credentials.
- Never expose Fourthwall Platform API keys in browser code.
- The Storefront token is configured through Vite environment variables.
- Checkout remains hosted by Fourthwall.

## Engineering standards

- TypeScript strict mode.
- Descriptive names over abbreviations.
- No hidden global state beyond documented browser cart persistence.
- No direct user-facing output from package internals.
- Accessible semantics and keyboard support are required.
- Respect reduced-motion preferences.
- Add tests for provider normalization and business-state changes.
- Use conventional commits.
- Use long-form CLI flags in documentation and scripts.
- Shell functions must have shdoc-compatible docstrings.
- Prefer `printf` over `echo`.
