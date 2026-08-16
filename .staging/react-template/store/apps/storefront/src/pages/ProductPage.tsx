import { Button, Container, StatusBadge } from "@egohygiene/store-ui";
import { useEffect, useMemo, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { useStorefront } from "../features/storefront/useStorefront";
import { formatMoney } from "../lib/money";

function providerInformationText(bodyHtml: string): string {
  const providerDocument = new DOMParser().parseFromString(bodyHtml, "text/html");
  return providerDocument.body.textContent?.trim() ?? "";
}

export function ProductPage() {
  const { productSlug } = useParams();
  const { products, productsLoading, addToCart, cartBusy } = useStorefront();
  const product = useMemo(
    () => products.find((candidate) => candidate.slug === productSlug),
    [productSlug, products],
  );
  const [selectedVariantId, setSelectedVariantId] = useState<string>("");

  useEffect(() => {
    const firstAvailableVariant = product?.variants.find((variant) => variant.available);
    setSelectedVariantId(firstAvailableVariant?.id ?? "");
  }, [product]);

  if (productsLoading) {
    return (
      <Container className="section">
        <p className="loading-message">Resolving product…</p>
      </Container>
    );
  }

  if (!product) {
    return (
      <Container className="section page-intro">
        <p className="eyebrow">404</p>
        <h1>That object drifted out of range.</h1>
        <Link to="/shop">return to the collection</Link>
      </Container>
    );
  }

  const selectedVariant = product.variants.find((variant) => variant.id === selectedVariantId);
  const primaryImage = selectedVariant?.images.at(0) ?? product.images.at(0);

  return (
    <section className="section">
      <Container className="product-detail">
        <div className="product-detail__media">
          {primaryImage ? <img src={primaryImage.url} alt={primaryImage.alt} /> : null}
        </div>
        <div className="product-detail__content">
          <StatusBadge tone="accent">{product.status}</StatusBadge>
          <p className="eyebrow">ego hygiene object</p>
          <h1>{product.name}</h1>
          <p className="product-detail__description">{product.description}</p>

          <label className="field" htmlFor="variant">
            <span>choose a version</span>
            <select
              id="variant"
              value={selectedVariantId}
              onChange={(event) => setSelectedVariantId(event.target.value)}
            >
              {product.variants.map((variant) => (
                <option key={variant.id} value={variant.id} disabled={!variant.available}>
                  {variant.name} — {formatMoney(variant.price)}
                  {!variant.available ? " — unavailable" : ""}
                </option>
              ))}
            </select>
          </label>

          {selectedVariant ? (
            <div className="product-detail__purchase">
              <strong>{formatMoney(selectedVariant.price)}</strong>
              <Button
                busy={cartBusy}
                disabled={!selectedVariant.available}
                onClick={() => addToCart(selectedVariant.id)}
              >
                add to cart
              </Button>
            </div>
          ) : (
            <p>This product has no purchasable variants yet.</p>
          )}

          {product.additionalInformation.map((information) => (
            <details key={information.title} className="product-information">
              <summary>{information.title}</summary>
              <p>{providerInformationText(information.bodyHtml)}</p>
            </details>
          ))}
        </div>
      </Container>
    </section>
  );
}
