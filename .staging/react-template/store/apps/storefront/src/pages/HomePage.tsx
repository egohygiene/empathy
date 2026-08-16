import { Container, StatusBadge } from "@egohygiene/store-ui";
import { Link } from "react-router-dom";
import { ProductGrid } from "../components/ProductGrid";
import { useStorefront } from "../features/storefront/useStorefront";

export function HomePage() {
  const { products, productsLoading, productsError, providerName } = useStorefront();

  return (
    <>
      <section className="hero-section">
        <Container className="hero-section__inner">
          <div className="hero-copy">
            <StatusBadge tone="accent">
              {providerName === "mock" ? "concept storefront" : "live collection"}
            </StatusBadge>
            <p className="eyebrow">physical artifacts from a living ecosystem</p>
            <h1>carry the signal.</h1>
            <p className="hero-copy__lede">
              Clothing, objects, prints, and strange little reminders to notice yourself, make room
              for complexity, and move toward balance.
            </p>
            <div className="hero-actions">
              <Link className="button button--primary" to="/shop">
                enter the collection
              </Link>
              <Link className="button button--secondary" to="/about">
                what is this?
              </Link>
            </div>
          </div>
          <div className="hero-orbit" aria-hidden="true">
            <div className="hero-orbit__ring hero-orbit__ring--one" />
            <div className="hero-orbit__ring hero-orbit__ring--two" />
            <div className="hero-orbit__core">
              <span>☯</span>
            </div>
          </div>
        </Container>
      </section>

      <section className="section">
        <Container>
          <div className="section-heading">
            <div>
              <p className="eyebrow">first transmission</p>
              <h2>featured objects</h2>
            </div>
            <Link to="/shop">view everything →</Link>
          </div>

          {productsLoading ? <p className="loading-message">Loading the collection…</p> : null}
          {productsError ? <p className="error-message">{productsError}</p> : null}
          {!productsLoading && !productsError ? (
            <ProductGrid products={products.slice(0, 3)} />
          ) : null}
        </Container>
      </section>

      <section className="manifesto-section">
        <Container className="manifesto-grid">
          <div>
            <p className="eyebrow">not just logo merch</p>
            <h2>small portals into the ideas.</h2>
          </div>
          <div className="manifesto-copy">
            <p>
              Every object can become a fragment of the larger Ego Hygiene universe: awareness,
              empathy, creative expression, nervous-system gentleness, engineering, play, and the
              ongoing work of returning to equilibrium.
            </p>
            <p>
              Fourthwall can eventually manufacture and fulfill the products. This repository owns
              the world wrapped around them.
            </p>
          </div>
        </Container>
      </section>
    </>
  );
}
