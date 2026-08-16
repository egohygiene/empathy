/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_COMMERCE_PROVIDER?: "mock" | "fourthwall";
  readonly VITE_FOURTHWALL_STOREFRONT_TOKEN?: string;
  readonly VITE_FOURTHWALL_CHECKOUT_DOMAIN?: string;
  readonly VITE_STORE_CURRENCY?: string;
  readonly VITE_STORE_BASE_PATH?: string;
  readonly VITE_STORE_NAME?: string;
  readonly VITE_STORE_HOME_URL?: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
