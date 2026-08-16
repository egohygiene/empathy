import type { StoreCurrency } from "@egohygiene/store-config";
import { CommerceError } from "../errors";
import type { Cart, CartItem, CommerceClient, Product, ProductVariant } from "../types";
import { createMockProducts } from "./mock-products";

export interface MockCommerceClientOptions {
  readonly assetBasePath: string;
  readonly currency: StoreCurrency;
}

function findVariant(
  products: readonly Product[],
  variantId: string,
): {
  product: Product;
  variant: ProductVariant;
} {
  for (const product of products) {
    const variant = product.variants.find((candidate) => candidate.id === variantId);
    if (variant) {
      return { product, variant };
    }
  }

  throw new CommerceError(`Unknown mock variant: ${variantId}`, {
    code: "variant_not_found",
  });
}

export class MockCommerceClient implements CommerceClient {
  readonly providerName = "mock";

  private readonly products: readonly Product[];
  private readonly currency: StoreCurrency;
  private cartItems: CartItem[] = [];

  constructor(options: MockCommerceClientOptions) {
    this.products = createMockProducts(options.assetBasePath);
    this.currency = options.currency;
  }

  async listProducts(): Promise<readonly Product[]> {
    return this.products;
  }

  async getProduct(productSlug: string): Promise<Product | null> {
    return this.products.find((product) => product.slug === productSlug) ?? null;
  }

  async getCart(cartId: string): Promise<Cart | null> {
    return cartId === "mock-cart" ? this.createCartResult() : null;
  }

  async addItem(_cartId: string | null, variantId: string, quantity: number): Promise<Cart> {
    const { product, variant } = findVariant(this.products, variantId);
    const currentItem = this.cartItems.find((item) => item.variantId === variantId);

    if (currentItem) {
      this.cartItems = this.cartItems.map((item) =>
        item.variantId === variantId ? { ...item, quantity: item.quantity + quantity } : item,
      );
    } else {
      this.cartItems = [
        ...this.cartItems,
        {
          variantId,
          productId: product.id,
          productSlug: product.slug,
          productName: product.name,
          variantName: variant.name,
          quantity,
          price: variant.price,
          image: variant.images.at(0) ?? product.images.at(0),
        },
      ];
    }

    return this.createCartResult();
  }

  async changeItemQuantity(_cartId: string, variantId: string, quantity: number): Promise<Cart> {
    this.cartItems =
      quantity <= 0
        ? this.cartItems.filter((item) => item.variantId !== variantId)
        : this.cartItems.map((item) =>
            item.variantId === variantId ? { ...item, quantity } : item,
          );

    return this.createCartResult();
  }

  buildCheckoutUrl(_cartId: string): string {
    return "checkout-return?mode=mock";
  }

  private createCartResult(): Cart {
    return {
      id: "mock-cart",
      items: this.cartItems,
      subtotal: {
        value: this.cartItems.reduce((total, item) => total + item.price.value * item.quantity, 0),
        currency: this.currency,
      },
    };
  }
}
