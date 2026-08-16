import type { Product } from "@egohygiene/commerce";
import { StatusBadge } from "@egohygiene/store-ui";
import { Link } from "react-router-dom";
import { formatMoney, minimumProductPrice } from "../lib/money";

export interface ProductCardProps {
  readonly product: Product;
}

export function ProductCard({ product }: ProductCardProps) {
  const image = product.images.at(0);
  const price = minimumProductPrice(product);

  return (
    <article className="product-card">
      <Link className="product-card__image-link" to={`/products/${product.slug}`}>
        {image ? (
          <img className="product-card__image" src={image.url} alt={image.alt} loading="lazy" />
        ) : (
          <div className="product-card__placeholder">image arriving soon</div>
        )}
      </Link>
      <div className="product-card__body">
        <div className="product-card__meta">
          <StatusBadge tone="accent">{product.status}</StatusBadge>
          <span>{price ? `from ${formatMoney(price)}` : "price unavailable"}</span>
        </div>
        <h3>
          <Link to={`/products/${product.slug}`}>{product.name}</Link>
        </h3>
        <p>{product.description}</p>
      </div>
    </article>
  );
}
