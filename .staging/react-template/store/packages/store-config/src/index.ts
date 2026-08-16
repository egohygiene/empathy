import { z } from "zod";

const supportedCurrencies = [
  "USD",
  "EUR",
  "CAD",
  "GBP",
  "AUD",
  "NZD",
  "SEK",
  "NOK",
  "DKK",
  "PLN",
  "INR",
  "JPY",
  "MYR",
  "SGD",
  "MXN",
  "BRL",
  "CHF",
] as const;

const rawStoreConfigSchema = z.object({
  VITE_COMMERCE_PROVIDER: z.enum(["mock", "fourthwall"]).default("mock"),
  VITE_FOURTHWALL_STOREFRONT_TOKEN: z.string().optional(),
  VITE_FOURTHWALL_CHECKOUT_DOMAIN: z.string().optional(),
  VITE_STORE_CURRENCY: z.enum(supportedCurrencies).default("USD"),
  VITE_STORE_BASE_PATH: z.string().default("/store/"),
  VITE_STORE_NAME: z.string().default("ego hygiene store"),
  VITE_STORE_HOME_URL: z.string().url().default("https://egohygiene.io/"),
});

export type CommerceProvider = "mock" | "fourthwall";
export type StoreCurrency = (typeof supportedCurrencies)[number];

export interface StoreConfig {
  readonly provider: CommerceProvider;
  readonly storefrontToken?: string;
  readonly checkoutDomain?: string;
  readonly currency: StoreCurrency;
  readonly basePath: string;
  readonly storeName: string;
  readonly homeUrl: string;
}

function normalizeBasePath(value: string): string {
  const withLeadingSlash = value.startsWith("/") ? value : `/${value}`;
  return withLeadingSlash.endsWith("/") ? withLeadingSlash : `${withLeadingSlash}/`;
}

function normalizeDomain(value: string | undefined): string | undefined {
  if (!value) {
    return undefined;
  }

  return value.replace(/^https?:\/\//u, "").replace(/\/+$/u, "");
}

export function createStoreConfig(
  rawEnvironment: Record<string, string | boolean | undefined>,
): StoreConfig {
  const parsed = rawStoreConfigSchema.parse(rawEnvironment);
  const checkoutDomain = normalizeDomain(parsed.VITE_FOURTHWALL_CHECKOUT_DOMAIN);
  const storefrontToken = parsed.VITE_FOURTHWALL_STOREFRONT_TOKEN?.trim() || undefined;

  if (parsed.VITE_COMMERCE_PROVIDER === "fourthwall") {
    if (!storefrontToken) {
      throw new Error(
        "VITE_FOURTHWALL_STOREFRONT_TOKEN is required when using Fourthwall commerce.",
      );
    }

    if (!checkoutDomain) {
      throw new Error(
        "VITE_FOURTHWALL_CHECKOUT_DOMAIN is required when using Fourthwall commerce.",
      );
    }
  }

  return {
    provider: parsed.VITE_COMMERCE_PROVIDER,
    storefrontToken,
    checkoutDomain,
    currency: parsed.VITE_STORE_CURRENCY,
    basePath: normalizeBasePath(parsed.VITE_STORE_BASE_PATH),
    storeName: parsed.VITE_STORE_NAME,
    homeUrl: parsed.VITE_STORE_HOME_URL,
  };
}
