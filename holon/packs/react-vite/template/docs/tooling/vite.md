# Canonical Vite configuration

## Configuration factories

`@egohygiene/vite-config` exposes two deliberate build boundaries:

- `createReactViteConfig` for runnable browser applications;
- `createReactLibraryConfig` for reusable React packages.

The library factory uses Vite library mode, produces ESM and CommonJS bundles,
emits one stable CSS artifact, keeps React and declared workspace packages
external, deduplicates React at development time, and writes source maps. The
package TypeScript project emits declarations after Vite so both artifact sets
share one `dist/` tree.

`@egohygiene/ui` is the first consumer. Its workspace exports continue to point
to source during incubation; public publication requires conditional `dist`
exports and packed-consumer validation.

Every browser app composes `createReactViteConfig` from
`@egohygiene/vite-config`. The package is the synthesized successor to the
historical configurations in `.staging/vite.corpus.txt`; individual apps no
longer copy a drifting configuration object.

## Baseline behavior

The factory configures:

- React 19 through the SWC plugin
- TypeScript path discovery and an app-local `@` alias
- React dependency deduplication in a pnpm workspace
- SVG component imports using the `?react` suffix
- WebAssembly imports
- Tailwind CSS v3 through the workspace PostCSS configuration
- strict, loopback-only development and preview servers
- fixed ports, compressed-size reporting, CSS splitting, stable hashed assets,
  ES2022 output, and deliberate vendor chunks
- development TypeScript diagnostics
- optional progressive-web-app output
- optional bundle treemaps

Expensive features are installed but conditional. PWA is enabled only for apps
that request it. Bundle analysis is enabled only for an analysis build.

## App composition

```ts
import { createReactViteConfig } from "@egohygiene/vite-config";

export default createReactViteConfig({
  appDirectory: new URL(".", import.meta.url),
  workspaceDirectory: new URL("../../", import.meta.url),
  appName: "web",
  basePath: "/",
  serverPort: 5173,
  previewPort: 4173,
  pwa: true,
});
```

Use `aliases` for an app-specific import only when the TypeScript project has a
matching `paths` entry. Use `proxy` only for local development; production API
routing belongs to deployment infrastructure.

## Environment model

Vite exposes `VITE_*` variables to browser code. They must contain only public
configuration. Secrets, privileged commerce keys, private API keys, database
credentials, and server-only tokens must never use that prefix.

The factory loads two prefixes:

- `VITE_*`: public runtime configuration and local ports
- `TEMPLATE_*`: build-tool switches consumed by `vite.config.ts`

Supported build switches:

| Variable               | Default               | Behavior                                            |
| ---------------------- | --------------------- | --------------------------------------------------- |
| `TEMPLATE_ANALYZE`     | `false`               | Emits `dist/bundle-analysis.html`                   |
| `TEMPLATE_SOURCE_MAPS` | `false` in production | Emits production source maps                        |
| `TEMPLATE_PWA_DEV`     | `false`               | Enables the service worker during local development |

Use a server-side boundary or secret-bearing backend-for-frontend whenever a
provider requires credentials that are not intended for every site visitor.

## Security defaults

- Development binds to `127.0.0.1`, not every network interface.
- Ports are strict so automation does not silently select another endpoint.
- CORS is disabled by default.
- file serving is restricted to the template workspace.
- conservative permissions, referrer, and content-type headers are emitted.
- PWA navigation fallback excludes `/api/`.
- source maps require an explicit production opt-in.

Authentication popups and cross-origin-isolated WASM applications may require
app-specific response headers. Add those intentionally after testing the exact
provider rather than weakening every generated application.

## Corpus status

This pass covers the broadly reusable corpus capabilities: React/SWC, aliases,
env loading, deterministic servers, SVG, WASM, PWA, diagnostics, visualization,
and production chunking. Specialized Potree, Kepler, deck.gl, Nx, library-mode,
SSR, and multi-page configurations remain candidates for later opt-in profiles.
The historical corpus remains in `.staging` until that second classification is
complete.

References: [Vite configuration](https://vite.dev/config/),
[environment variables and modes](https://vite.dev/guide/env-and-mode), and
[production builds](https://vite.dev/guide/build).
