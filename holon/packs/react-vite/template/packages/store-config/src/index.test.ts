import { describe, expect, it } from "vitest";
import { createStoreConfig } from "./index";

describe("createStoreConfig", () => {
  it("creates a runnable mock configuration by default", () => {
    const config = createStoreConfig({});

    expect(config.provider).toBe("mock");
    expect(config.basePath).toBe("/store/");
    expect(config.currency).toBe("USD");
  });

  it("requires Fourthwall connection values in live mode", () => {
    expect(() => createStoreConfig({ VITE_COMMERCE_PROVIDER: "fourthwall" })).toThrow(
      /STOREFRONT_TOKEN/u,
    );
  });

  it("normalizes paths and checkout domains", () => {
    const config = createStoreConfig({
      VITE_COMMERCE_PROVIDER: "fourthwall",
      VITE_FOURTHWALL_STOREFRONT_TOKEN: "ptkn_demo",
      VITE_FOURTHWALL_CHECKOUT_DOMAIN: "https://shop.example.com/",
      VITE_STORE_BASE_PATH: "store",
    });

    expect(config.checkoutDomain).toBe("shop.example.com");
    expect(config.basePath).toBe("/store/");
  });
});
