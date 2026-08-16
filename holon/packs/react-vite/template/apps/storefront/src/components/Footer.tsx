import { Container } from "@egohygiene/store-ui";

export function Footer() {
  return (
    <footer className="site-footer">
      <Container className="site-footer__inner">
        <div>
          <strong>ego hygiene store</strong>
          <p>objects for awareness, expression, balance, and beautiful weirdness.</p>
        </div>
        <div className="site-footer__links">
          <a href="https://egohygiene.io/privacy">privacy</a>
          <a href="https://egohygiene.io/terms">terms</a>
          <a href="https://github.com/egohygiene/store">source</a>
        </div>
        <small>© 2026 Ego Hygiene</small>
      </Container>
    </footer>
  );
}
