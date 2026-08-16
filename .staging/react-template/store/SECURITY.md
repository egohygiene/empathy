# Security Policy

Report security concerns privately to the repository owner.

Never commit:

- Fourthwall Platform API keys
- payment information
- customer records
- order exports
- webhook signing secrets
- `.env` files

The browser application may use a Fourthwall Storefront token, but privileged
Platform API credentials must remain server-side.
