# Security Policy

Report security concerns privately to the repository owner. Do not open a
public issue containing exploit details, credentials, or personal data.

Never commit:

- payment information, customer records, order exports, or health data
- private API keys, database credentials, or webhook signing secrets
- identity-provider client secrets or privileged commerce Platform API keys
- `.env` and `.env.*` files other than reviewed examples

Every `VITE_*` value is public browser data. A provider may expose a deliberately
public storefront token, but privileged provider credentials must remain behind
a server-side boundary.
