import type { Product } from "@egohygiene/commerce";
import { ProductCard } from "./ProductCard";

export interface ProductGridProps {
  readonly products: readonly Product[];
}

export function ProductGrid({ products }: ProductGridProps) {
  return (
    <div className="product-grid">
      {products.map((product) => (
        <ProductCard key={product.id} product={product} />
      ))}
    </div>
  );
}
