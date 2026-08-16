import { Container } from "@egohygiene/store-ui";

export function AboutPage() {
  return (
    <section className="section page-intro">
      <Container className="prose-page">
        <p className="eyebrow">the store as a world</p>
        <h1>merch can be more than merch.</h1>
        <p>
          Ego Hygiene is an evolving ecosystem of creative work, reflective practices, experimental
          technology, and tools for making life a little more inhabitable.
        </p>
        <p>
          The store is where those ideas can become tactile: clothing, prints, journals, digital
          artifacts, limited objects, and products that have not been invented yet.
        </p>
        <p>
          The custom storefront remains independent from manufacturing and fulfillment. That lets
          the experience stay expressive while a commerce provider handles the operational weight.
        </p>
      </Container>
    </section>
  );
}
