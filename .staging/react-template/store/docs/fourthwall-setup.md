# Fourthwall Setup

## 1. Create the shop

Create the products and collections in Fourthwall first. The storefront only
renders products that Fourthwall reports as public.

## 2. Create a Storefront token

In the Fourthwall dashboard, open the developer settings and create a
Storefront token.

Storefront tokens are used by the customer-facing Storefront API. Do not use a
Fourthwall Platform API key in this Vite application.

## 3. Configure local environment

```bash
cp .env.example .env.local
```

Set:

```dotenv
VITE_COMMERCE_PROVIDER=fourthwall
VITE_FOURTHWALL_STOREFRONT_TOKEN=ptkn_replace_me
VITE_FOURTHWALL_CHECKOUT_DOMAIN=your-shop.fourthwall.com
VITE_STORE_CURRENCY=USD
```

## 4. Run

```bash
pnpm dev:store
```

## 5. Verify

- Catalog products render.
- Product variants are selectable.
- Add to cart returns a Fourthwall cart.
- Refreshing the page restores the cart identifier.
- Checkout redirects to the configured Fourthwall domain.

## Security distinction

The Storefront token is used by the browser-facing Storefront API. A Platform
API key can manage the shop and must never be placed in `VITE_*` variables,
client bundles, or repository files.

## Integration notes

The adapter currently uses:

- `GET /v1/collections/all/products`
- `GET /v1/products/{slug}`
- `GET /v1/carts/{cartId}`
- `POST /v1/carts`
- `POST /v1/carts/{cartId}/add`
- `POST /v1/carts/{cartId}/change`
- hosted `/cart/checkout`

Run a private smoke test after connecting the live shop because provider
contracts may evolve.
