# Domain Routing

The storefront deploys independently but is presented beneath the main domain:

```text
https://egohygiene.io/store/
```

## Store project

The Vite build uses `/store/` as its public base. The store deployment includes
SPA and asset rewrites so its preview URL can resolve the prefixed paths.

## Main website gateway

The main `egohygiene/website` deployment should proxy the path while stripping
the prefix before forwarding to the independent store deployment.

Conceptual rule:

```json
{
  "source": "/store/:path*",
  "destination": "https://egohygiene-store.vercel.app/:path*"
}
```

Add an additional exact `/store` rule when the gateway platform requires it.

## Local development

The local URL is:

```text
http://localhost:5173/store/
```

React Router derives its basename from Vite's configured base path.
