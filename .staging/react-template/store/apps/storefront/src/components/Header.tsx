import { Container } from "@egohygiene/store-ui";
import { Link, NavLink } from "react-router-dom";
import { useStorefront } from "../features/storefront/useStorefront";

export function Header() {
  const { cartItemCount, openCart, config } = useStorefront();

  return (
    <header className="site-header">
      <Container className="site-header__inner">
        <a className="skip-link" href="#main-content">
          Skip to content
        </a>
        <Link className="brand" to="/" aria-label="Ego Hygiene store home">
          <span className="brand__mark" aria-hidden="true">
            ◉
          </span>
          <span>
            <strong>ego hygiene</strong>
            <small>store</small>
          </span>
        </Link>

        <nav className="primary-navigation" aria-label="Store navigation">
          <NavLink className={({ isActive }) => (isActive ? "active" : undefined)} to="/shop">
            shop
          </NavLink>
          <NavLink className={({ isActive }) => (isActive ? "active" : undefined)} to="/about">
            about
          </NavLink>
          <a href={config.homeUrl}>ecosystem</a>
        </nav>

        <button
          className="cart-trigger"
          type="button"
          onClick={openCart}
          aria-label={`Open cart with ${cartItemCount} ${cartItemCount === 1 ? "item" : "items"}`}
        >
          cart <span aria-hidden="true">{cartItemCount}</span>
        </button>
      </Container>
    </header>
  );
}
