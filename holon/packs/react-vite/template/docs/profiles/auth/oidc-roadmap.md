# OIDC adapter roadmap

`@egohygiene/auth` owns provider-neutral session and authorization contracts.
The former universal app's direct `react-oidc-context` and Keycloak environment
reads are not copied into the UI package.

A future `@egohygiene/auth-oidc` adapter should:

- implement the existing auth contract without changing UI components;
- accept authority, client ID, redirect URI, scopes, and audience through a
  validated browser-safe configuration object;
- keep client secrets and token exchange policy out of the browser bundle;
- support callback, refresh, logout, expiry, clock-skew, offline, and denied
  states;
- normalize claims and roles without assuming one provider's claim names;
- provide mock and deterministic test fixtures;
- document CSP, redirect allowlists, storage choice, cross-tab behavior, and
  threat-model assumptions.

The historical comparison source remains recoverable from Git at commit
`4815192f9e0cd70ddb870992a493f379d5f76d8e` under
`.staging/react-template/universal/apps/ui/src/auth`.
