# Ego Hygiene Store

A modular React + Vite storefront for `egohygiene.io/store`, designed to use
Fourthwall for products, carts, hosted checkout, manufacturing, fulfillment,
shipping, and order operations.

The repository boots in **mock commerce mode**, so it runs immediately without
credentials. Switch one environment variable to connect a real Fourthwall shop.

## Architecture

```text
Browser
  -> storefront application
      -> commerce port
          -> mock adapter (default)
          -> Fourthwall Storefront API adapter
              -> Fourthwall hosted checkout
```

The UI never imports Fourthwall-specific response shapes. Provider data is
normalized behind `@egohygiene/commerce`, which keeps the application ready for
another provider or a server-side proxy later.

## Requirements

- Node.js 22 or newer
- Corepack
- pnpm 10

## Run locally

```bash
corepack enable
pnpm install
cp .env.example .env.local
pnpm dev:store
```

Open:

```text
http://localhost:5173/store/
```

## Connect Fourthwall

Edit `.env.local`:

```dotenv
VITE_COMMERCE_PROVIDER=fourthwall
VITE_FOURTHWALL_STOREFRONT_TOKEN=ptkn_replace_me
VITE_FOURTHWALL_CHECKOUT_DOMAIN=your-shop.fourthwall.com
```

Then restart the development server.

See [`docs/fourthwall-setup.md`](docs/fourthwall-setup.md).

## Commands

```bash
pnpm dev:store
pnpm build
pnpm preview:store
pnpm format
pnpm lint
pnpm typecheck
pnpm test
pnpm test:e2e
pnpm check
```

## Deployment model

The application builds with `/store/` as its public base path. The main
`egohygiene.io` gateway can proxy `/store/*` to this project's independent
Vercel deployment.

See [`docs/domain-routing.md`](docs/domain-routing.md).

## Current scope

Included:

- mock product catalog
- Fourthwall product collection adapter
- product listing and product-detail routes
- provider-neutral cart operations
- hosted-checkout redirect
- persistent cart identifier
- responsive accessible shell
- dark cosmic visual foundation
- unit and end-to-end test scaffolding
- Vercel and GitHub Actions configuration

Deliberately deferred:

- customer accounts
- order-history UI
- webhooks
- analytics
- search
- product reviews
- inventory administration
- custom Fourthwall Platform API operations

## License

MIT
