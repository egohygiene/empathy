# Contributing

## Local setup

```bash
corepack enable
pnpm install
cp .env.example .env.local
pnpm dev:store
```

## Before committing

```bash
pnpm check
pnpm test:e2e
```

Use conventional commits and keep pull requests focused.

Provider integrations must normalize data behind the commerce contract rather
than leaking provider response types into page components.
