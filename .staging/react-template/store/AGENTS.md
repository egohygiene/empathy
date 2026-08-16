# Agent Instructions

## Mission

Maintain a small, explicit, provider-neutral commerce frontend for Ego Hygiene.

## Dependency direction

```text
apps/storefront
  -> packages/store-ui
  -> packages/store-config
  -> packages/commerce
```

The application may depend on packages. Packages must never import application
modules.

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
