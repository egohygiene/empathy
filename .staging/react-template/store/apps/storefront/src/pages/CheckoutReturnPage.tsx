import { Container } from "@egohygiene/store-ui";
import { Link, useSearchParams } from "react-router-dom";

export function CheckoutReturnPage() {
  const [searchParameters] = useSearchParams();
  const mockMode = searchParameters.get("mode") === "mock";

  return (
    <section className="section page-intro">
      <Container className="prose-page">
        <p className="eyebrow">{mockMode ? "demo checkout" : "checkout return"}</p>
        <h1>{mockMode ? "the mock cart made it this far." : "welcome back."}</h1>
        <p>
          {mockMode
            ? "Connect Fourthwall to hand real carts to secure hosted checkout."
            : "Your checkout session has returned to the Ego Hygiene store."}
        </p>
        <Link className="button button--primary" to="/shop">
          continue exploring
        </Link>
      </Container>
    </section>
  );
}
