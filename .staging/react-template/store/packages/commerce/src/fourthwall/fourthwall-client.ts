import type { StoreCurrency } from "@egohygiene/store-config";
import { z } from "zod";
import { CommerceError } from "../errors";
import type {
  Cart,
  CartItem,
  CommerceClient,
  Money,
  Product,
  ProductImage,
  ProductVariant,
} from "../types";

const moneySchema = z.object({
  value: z.union([z.number(), z.string()]),
  currency: z.string(),
});

const imageSchema = z
  .object({
    id: z.string(),
    url: z.string(),
    transformedUrl: z.string().optional(),
    width: z.number().optional(),
    height: z.number().optional(),
  })
  .passthrough();

const variantSchema = z
  .object({
    id: z.string(),
    name: z.string(),
    sku: z.string().nullish(),
    unitPrice: moneySchema,
    compareAtPrice: moneySchema.nullish(),
    attributes: z
      .object({
        description: z.string().nullish(),
        color: z.object({ name: z.string().nullish(), swatch: z.string().nullish() }).nullish(),
        size: z.object({ name: z.string().nullish() }).nullish(),
      })
      .nullish(),
    stock: z
      .object({
        type: z.string(),
        inStock: z.number().nullish(),
      })
      .nullish(),
    images: z.array(imageSchema).default([]),
    product: z.object({ id: z.string(), name: z.string(), slug: z.string() }).nullish(),
  })
  .passthrough();

const productSchema = z
  .object({
    id: z.string(),
    name: z.string(),
    slug: z.string(),
    description: z.string().nullish(),
    state: z.object({ type: z.string() }).nullish(),
    images: z.array(imageSchema).default([]),
    variants: z.array(variantSchema).default([]),
    additionalInformation: z
      .array(z.object({ title: z.string(), bodyHtml: z.string(), type: z.string().optional() }))
      .default([]),
  })
  .passthrough();

const productPageSchema = z.object({
  results: z.array(productSchema),
  paging: z.object({
    pageNumber: z.number().default(0),
    hasNextPage: z.boolean().default(false),
    elementsTotal: z.number().default(0),
  }),
});

const cartSchema = z.object({
  id: z.string(),
  items: z
    .array(
      z.object({
        variant: variantSchema,
        quantity: z.number(),
      }),
    )
    .default([]),
});

export interface FourthwallCommerceClientOptions {
  readonly storefrontToken: string;
  readonly checkoutDomain: string;
  readonly currency: StoreCurrency;
  readonly apiBaseUrl?: string;
  readonly fetchImplementation?: typeof fetch;
}

function toMoney(rawMoney: z.infer<typeof moneySchema>): Money {
  return {
    value: Number(rawMoney.value),
    currency: rawMoney.currency,
  };
}

function toImage(rawImage: z.infer<typeof imageSchema>, alt: string): ProductImage {
  return {
    id: rawImage.id,
    url: rawImage.transformedUrl ?? rawImage.url,
    width: rawImage.width,
    height: rawImage.height,
    alt,
  };
}

function isVariantAvailable(rawVariant: z.infer<typeof variantSchema>): boolean {
  const stockType = rawVariant.stock?.type.toLowerCase() ?? "available";
  if (stockType.includes("out") || stockType.includes("unavailable")) {
    return false;
  }

  return rawVariant.stock?.inStock === undefined || rawVariant.stock.inStock === null
    ? true
    : rawVariant.stock.inStock > 0;
}

function toVariant(rawVariant: z.infer<typeof variantSchema>, productName: string): ProductVariant {
  return {
    id: rawVariant.id,
    name: rawVariant.name,
    sku: rawVariant.sku ?? undefined,
    price: toMoney(rawVariant.unitPrice),
    compareAtPrice: rawVariant.compareAtPrice ? toMoney(rawVariant.compareAtPrice) : undefined,
    description: rawVariant.attributes?.description ?? undefined,
    colorName: rawVariant.attributes?.color?.name ?? undefined,
    colorSwatch: rawVariant.attributes?.color?.swatch ?? undefined,
    sizeName: rawVariant.attributes?.size?.name ?? undefined,
    available: isVariantAvailable(rawVariant),
    images: rawVariant.images.map((image) => toImage(image, productName)),
  };
}

function toProduct(rawProduct: z.infer<typeof productSchema>): Product {
  return {
    id: rawProduct.id,
    slug: rawProduct.slug,
    name: rawProduct.name,
    description: rawProduct.description ?? "",
    images: rawProduct.images.map((image) => toImage(image, rawProduct.name)),
    variants: rawProduct.variants.map((variant) => toVariant(variant, rawProduct.name)),
    status: rawProduct.state?.type ?? "available",
    additionalInformation: rawProduct.additionalInformation.map((information) => ({
      title: information.title,
      bodyHtml: information.bodyHtml,
    })),
  };
}

function toCart(rawCart: z.infer<typeof cartSchema>, currency: StoreCurrency): Cart {
  const items: CartItem[] = rawCart.items.map(({ variant, quantity }) => {
    const product = variant.product;
    const productName = product?.name ?? variant.name;
    const image = variant.images.at(0);

    return {
      variantId: variant.id,
      productId: product?.id ?? variant.id,
      productSlug: product?.slug ?? "",
      productName,
      variantName: variant.name,
      quantity,
      price: toMoney(variant.unitPrice),
      image: image ? toImage(image, productName) : undefined,
    };
  });

  return {
    id: rawCart.id,
    items,
    subtotal: {
      value: items.reduce((total, item) => total + item.price.value * item.quantity, 0),
      currency,
    },
  };
}

export class FourthwallCommerceClient implements CommerceClient {
  readonly providerName = "fourthwall";

  private readonly storefrontToken: string;
  private readonly checkoutDomain: string;
  private readonly currency: StoreCurrency;
  private readonly apiBaseUrl: string;
  private readonly fetchImplementation: typeof fetch;

  constructor(options: FourthwallCommerceClientOptions) {
    this.storefrontToken = options.storefrontToken;
    this.checkoutDomain = options.checkoutDomain;
    this.currency = options.currency;
    this.apiBaseUrl = options.apiBaseUrl ?? "https://storefront-api.fourthwall.com/v1";
    this.fetchImplementation = options.fetchImplementation ?? fetch;
  }

  async listProducts(): Promise<readonly Product[]> {
    const products: Product[] = [];
    let pageNumber = 0;
    let hasNextPage = true;
    const maximumPages = 100;

    while (hasNextPage && pageNumber < maximumPages) {
      const payload = await this.request(`/collections/all/products?page=${pageNumber}&size=50`, {
        method: "GET",
      });
      const parsed = productPageSchema.parse(payload);
      products.push(...parsed.results.map(toProduct));
      hasNextPage = parsed.paging.hasNextPage;
      pageNumber += 1;
    }

    if (hasNextPage) {
      throw new CommerceError("Fourthwall product pagination exceeded the safety limit.", {
        code: "pagination_limit",
      });
    }

    return products;
  }

  async getProduct(productSlug: string): Promise<Product | null> {
    try {
      const payload = await this.request(`/products/${encodeURIComponent(productSlug)}`, {
        method: "GET",
      });
      return toProduct(productSchema.parse(payload));
    } catch (error) {
      if (error instanceof CommerceError && error.status === 404) {
        return null;
      }
      throw error;
    }
  }

  async getCart(cartId: string): Promise<Cart | null> {
    try {
      const payload = await this.request(`/carts/${encodeURIComponent(cartId)}`, {
        method: "GET",
      });
      return toCart(cartSchema.parse(payload), this.currency);
    } catch (error) {
      if (error instanceof CommerceError && error.status === 404) {
        return null;
      }
      throw error;
    }
  }

  async addItem(cartId: string | null, variantId: string, quantity: number): Promise<Cart> {
    const path = cartId ? `/carts/${encodeURIComponent(cartId)}/add` : "/carts";
    const payload = await this.request(path, {
      method: "POST",
      body: JSON.stringify({
        items: [{ variantId, quantity }],
        metadata: { cart_origin: "egohygiene_store" },
      }),
    });

    return toCart(cartSchema.parse(payload), this.currency);
  }

  async changeItemQuantity(cartId: string, variantId: string, quantity: number): Promise<Cart> {
    const payload = await this.request(`/carts/${encodeURIComponent(cartId)}/change`, {
      method: "POST",
      body: JSON.stringify({ items: [{ variantId, quantity }] }),
    });

    return toCart(cartSchema.parse(payload), this.currency);
  }

  buildCheckoutUrl(cartId: string): string {
    const checkoutUrl = new URL(`https://${this.checkoutDomain}/cart/checkout`);
    checkoutUrl.searchParams.set("cartId", cartId);
    checkoutUrl.searchParams.set("currency", this.currency);
    checkoutUrl.searchParams.set("cart_origin", "egohygiene_store");
    return checkoutUrl.toString();
  }

  private async request(path: string, init: RequestInit): Promise<unknown> {
    const requestUrl = new URL(`${this.apiBaseUrl}${path}`);
    requestUrl.searchParams.set("storefront_token", this.storefrontToken);
    requestUrl.searchParams.set("currency", this.currency);

    const response = await this.fetchImplementation(requestUrl, {
      ...init,
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        ...init.headers,
      },
    });

    if (!response.ok) {
      const safeMessage = `Fourthwall request failed (${response.status} ${response.statusText}).`;
      throw new CommerceError(safeMessage, {
        status: response.status,
        code: "fourthwall_request_failed",
      });
    }

    return response.json();
  }
}
