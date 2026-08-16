import type { Money, Product } from "@egohygiene/commerce";

export function formatMoney(money: Money): string {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: money.currency,
  }).format(money.value);
}

export function minimumProductPrice(product: Product): Money | null {
  const prices = product.variants.map((variant) => variant.price);
  if (prices.length === 0) {
    return null;
  }

  return prices.reduce((minimum, candidate) =>
    candidate.value < minimum.value ? candidate : minimum,
  );
}
