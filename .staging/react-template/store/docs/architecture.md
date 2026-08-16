# Store Architecture

## System boundary

The repository owns the customer-facing shopping experience. Fourthwall owns
commerce operations after the application hands off to hosted checkout.

```text
apps/storefront
  presentation, routing, interaction, browser persistence

packages/store-ui
  reusable visual primitives

packages/store-config
  typed environment parsing and validation

packages/commerce
  provider-neutral models and commerce port
  mock adapter
  Fourthwall Storefront API adapter

Fourthwall
  product system of record
  carts
  hosted checkout
  payment processing
  manufacturing
  fulfillment
  shipping
  customer-order support
```

## Provider boundary

The application imports only normalized models and `CommerceClient`.
Fourthwall payload parsing and endpoint knowledge stay inside the adapter.

## Runtime modes

### Mock

The default. Uses a local catalog and in-memory cart. This mode powers local
onboarding, automated tests, and visual development.

### Fourthwall

Fetches the public product catalog through the Storefront API and redirects a
real cart to hosted checkout.

## Future proxy

A server-side proxy can be introduced later without changing page components:
implement another `CommerceClient` adapter that calls `/api/storefront/*`.
