# Contributing

## Local setup

```bash
corepack enable
pnpm install --no-frozen-lockfile
cp .env.example .env.local
pnpm run dev:web
```

## Before committing

```bash
pnpm run check
pnpm run test:e2e
```

Use conventional commits and keep pull requests focused. Update the migration
ledger whenever staged material is promoted or removed.

Provider integrations must normalize data behind an adapter contract rather
than leaking provider response types into pages or shared UI components.
