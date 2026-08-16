import type { Product } from "../types";

export function createMockProducts(assetBasePath: string): readonly Product[] {
  const imageUrl = (fileName: string) => `${assetBasePath}mock-products/${fileName}`;

  return [
    {
      id: "mock-cosmic-balance-hoodie",
      slug: "cosmic-balance-hoodie",
      name: "cosmic balance hoodie",
      description:
        "A soft heavyweight hoodie carrying the Ego Hygiene galaxy balance mark across the chest.",
      status: "available",
      images: [
        {
          id: "hoodie-image",
          url: imageUrl("cosmic-balance-hoodie.svg"),
          alt: "Cosmic balance hoodie concept",
          width: 1200,
          height: 1200,
        },
      ],
      variants: [
        {
          id: "mock-hoodie-black-small",
          name: "Black / Small",
          price: { value: 64, currency: "USD" },
          colorName: "Black",
          colorSwatch: "#111019",
          sizeName: "S",
          available: true,
          images: [],
        },
        {
          id: "mock-hoodie-black-medium",
          name: "Black / Medium",
          price: { value: 64, currency: "USD" },
          colorName: "Black",
          colorSwatch: "#111019",
          sizeName: "M",
          available: true,
          images: [],
        },
        {
          id: "mock-hoodie-black-large",
          name: "Black / Large",
          price: { value: 64, currency: "USD" },
          colorName: "Black",
          colorSwatch: "#111019",
          sizeName: "L",
          available: true,
          images: [],
        },
      ],
      additionalInformation: [
        {
          title: "Concept drop",
          bodyHtml: "<p>This mock item demonstrates the product-detail experience.</p>",
        },
      ],
    },
    {
      id: "mock-awareness-shirt",
      slug: "awareness-signal-shirt",
      name: "awareness signal shirt",
      description:
        "A minimal signal tee built around awareness, reflection, and the space between reactions.",
      status: "available",
      images: [
        {
          id: "shirt-image",
          url: imageUrl("awareness-signal-shirt.svg"),
          alt: "Awareness signal shirt concept",
          width: 1200,
          height: 1200,
        },
      ],
      variants: [
        {
          id: "mock-shirt-small",
          name: "Midnight / Small",
          price: { value: 34, currency: "USD" },
          sizeName: "S",
          available: true,
          images: [],
        },
        {
          id: "mock-shirt-medium",
          name: "Midnight / Medium",
          price: { value: 34, currency: "USD" },
          sizeName: "M",
          available: true,
          images: [],
        },
        {
          id: "mock-shirt-large",
          name: "Midnight / Large",
          price: { value: 34, currency: "USD" },
          sizeName: "L",
          available: true,
          images: [],
        },
      ],
      additionalInformation: [],
    },
    {
      id: "mock-reflection-journal",
      slug: "reflection-field-journal",
      name: "reflection field journal",
      description:
        "A compact notebook for fragments, patterns, observations, and whatever needs somewhere to land.",
      status: "available",
      images: [
        {
          id: "journal-image",
          url: imageUrl("reflection-field-journal.svg"),
          alt: "Reflection field journal concept",
          width: 1200,
          height: 1200,
        },
      ],
      variants: [
        {
          id: "mock-journal-default",
          name: "Softcover",
          price: { value: 24, currency: "USD" },
          available: true,
          images: [],
        },
      ],
      additionalInformation: [],
    },
    {
      id: "mock-harmony-print",
      slug: "harmony-field-print",
      name: "harmony field print",
      description:
        "A saturated cosmic print mapping tension, softness, movement, and return toward equilibrium.",
      status: "available",
      images: [
        {
          id: "print-image",
          url: imageUrl("harmony-field-print.svg"),
          alt: "Harmony field art print concept",
          width: 1200,
          height: 1200,
        },
      ],
      variants: [
        {
          id: "mock-print-small",
          name: "12 × 12 inches",
          price: { value: 28, currency: "USD" },
          sizeName: "12 × 12",
          available: true,
          images: [],
        },
        {
          id: "mock-print-large",
          name: "20 × 20 inches",
          price: { value: 48, currency: "USD" },
          sizeName: "20 × 20",
          available: true,
          images: [],
        },
      ],
      additionalInformation: [],
    },
  ];
}
