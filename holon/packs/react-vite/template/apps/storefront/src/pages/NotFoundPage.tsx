import { Container } from "@egohygiene/store-ui";
import { Link } from "react-router-dom";

export function NotFoundPage() {
  return (
    <section className="section page-intro">
      <Container>
        <p className="eyebrow">404</p>
        <h1>this path dissolved.</h1>
        <p>The page is not part of the current storefront transmission.</p>
        <Link className="button button--primary" to="/">
          return home
        </Link>
      </Container>
    </section>
  );
}
