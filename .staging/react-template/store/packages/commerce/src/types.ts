import type { StoreCurrency } from "@egohygiene/store-config";

export interface Money {
  readonly value: number;
  readonly currency: StoreCurrency | string;
}

export interface ProductImage {
  readonly id: string;
  readonly url: string;
  readonly width?: number;
  readonly height?: number;
  readonly alt: string;
}

export interface ProductVariant {
  readonly id: string;
  readonly name: string;
  readonly sku?: string;
  readonly price: Money;
  readonly compareAtPrice?: Money;
  readonly description?: string;
  readonly colorName?: string;
  readonly colorSwatch?: string;
  readonly sizeName?: string;
  readonly available: boolean;
  readonly images: readonly ProductImage[];
}

export interface Product {
  readonly id: string;
  readonly slug: string;
  readonly name: string;
  readonly description: string;
  readonly images: readonly ProductImage[];
  readonly variants: readonly ProductVariant[];
  readonly status: string;
  readonly additionalInformation: readonly {
    readonly title: string;
    readonly bodyHtml: string;
  }[];
}

export interface ProductPage {
  readonly products: readonly Product[];
  readonly pageNumber: number;
  readonly hasNextPage: boolean;
  readonly totalProducts: number;
}

export interface CartItem {
  readonly variantId: string;
  readonly productId: string;
  readonly productSlug: string;
  readonly productName: string;
  readonly variantName: string;
  readonly quantity: number;
  readonly price: Money;
  readonly image?: ProductImage;
}

export interface Cart {
  readonly id: string;
  readonly items: readonly CartItem[];
  readonly subtotal: Money;
}

export interface CommerceClient {
  readonly providerName: string;
  listProducts(): Promise<readonly Product[]>;
  getProduct(productSlug: string): Promise<Product | null>;
  getCart(cartId: string): Promise<Cart | null>;
  addItem(cartId: string | null, variantId: string, quantity: number): Promise<Cart>;
  changeItemQuantity(cartId: string, variantId: string, quantity: number): Promise<Cart>;
  buildCheckoutUrl(cartId: string): string;
}
