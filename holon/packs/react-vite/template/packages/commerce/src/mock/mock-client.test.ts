import { describe, expect, it } from "vitest";
import { MockCommerceClient } from "./mock-client";

describe("MockCommerceClient", () => {
  it("lists products and maintains a cart", async () => {
    const client = new MockCommerceClient({ assetBasePath: "/store/", currency: "USD" });
    const products = await client.listProducts();
    const variant = products[0]?.variants[0];

    expect(products.length).toBeGreaterThan(0);
    expect(variant).toBeDefined();

    if (!variant) {
      throw new Error("Fixture variant missing.");
    }

    const cart = await client.addItem(null, variant.id, 2);
    expect(cart.items).toHaveLength(1);
    expect(cart.items[0]?.quantity).toBe(2);

    const emptyCart = await client.changeItemQuantity(cart.id, variant.id, 0);
    expect(emptyCart.items).toHaveLength(0);
  });
});
