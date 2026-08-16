import type { StoreConfig } from "@egohygiene/store-config";
import type { CommerceClient } from "./types";
import { FourthwallCommerceClient } from "./fourthwall/fourthwall-client";
import { MockCommerceClient } from "./mock/mock-client";

export function createCommerceClient(config: StoreConfig): CommerceClient {
  if (config.provider === "fourthwall") {
    if (!config.storefrontToken || !config.checkoutDomain) {
      throw new Error("Fourthwall configuration was not validated before client creation.");
    }

    return new FourthwallCommerceClient({
      storefrontToken: config.storefrontToken,
      checkoutDomain: config.checkoutDomain,
      currency: config.currency,
    });
  }

  return new MockCommerceClient({
    assetBasePath: config.basePath,
    currency: config.currency,
  });
}
