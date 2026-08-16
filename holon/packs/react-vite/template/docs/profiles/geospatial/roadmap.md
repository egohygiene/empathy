# Geospatial UI profile roadmap

The former universal application mixed Kepler.gl rendering, map persistence,
cloud providers, route state, and test controls into its general UI surface.
That code is not part of `@egohygiene/ui`.

## Intended future boundary

A geospatial profile may be introduced only when a real consumer validates it:

```text
apps/map-workbench
  -> @egohygiene/geospatial-ui
      -> @egohygiene/geospatial-core
          -> provider adapters (Kepler, MapLibre, Mapbox, cloud persistence)
```

The core package should own normalized viewport, layer, selection, persistence,
and error contracts. Provider packages should own SDK imports and credentials.
The UI package should accept capabilities through props or context rather than
reading environment variables or calling map APIs directly.

## Admission gates

- identify an active product consumer and supported provider versions;
- replace the legacy missing imports and prototype-only controls;
- define browser-safe configuration and server-side credential boundaries;
- use package-provided map CSS instead of committing minified vendor copies;
- test map loading, resize behavior, keyboard access, reduced motion, failure
  states, and persistence normalization;
- isolate large SDKs behind lazy imports and publish bundle budgets;
- document data licensing, privacy, telemetry, and geolocation behavior.

The historical prototype remains recoverable from Git at commit
`4815192f9e0cd70ddb870992a493f379d5f76d8e` under
`.staging/react-template/universal`. It was intentionally deferred rather than
represented as a working package.
