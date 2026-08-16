import { Container } from "@egohygiene/store-ui";
import { ProductGrid } from "../components/ProductGrid";
import { useStorefront } from "../features/storefront/useStorefront";

export function ShopPage() {
  const { products, productsLoading, productsError, providerName } = useStorefront();

  return (
    <section className="section page-intro">
      <Container>
        <p className="eyebrow">{providerName === "mock" ? "mock collection" : "live collection"}</p>
        <h1>shop the universe.</h1>
        <p>Products are made after ordering whenever the selected fulfillment path supports it.</p>

        {productsLoading ? <p className="loading-message">Loading products…</p> : null}
        {productsError ? <p className="error-message">{productsError}</p> : null}
        {!productsLoading && !productsError ? <ProductGrid products={products} /> : null}
      </Container>
    </section>
  );
}
