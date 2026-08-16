import { render } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { HorizontalScroller } from "./HorizontalScroller";
import { MediaCard } from "./MediaCard";

describe("content patterns", () => {
  it("exposes the scroller as a named region", () => {
    const { getByRole } = render(
      <HorizontalScroller label="Featured resources">Content</HorizontalScroller>,
    );
    expect(getByRole("region", { name: "Featured resources" })).toHaveAttribute("tabindex", "0");
  });

  it("keeps media text and image alternatives product-owned", () => {
    const { getByAltText, getByRole } = render(
      <MediaCard
        href="/resource"
        imageAlt="Example resource preview"
        imageSrc="/preview.png"
        title="Example resource"
      />,
    );
    expect(getByAltText("Example resource preview")).toHaveAttribute("loading", "lazy");
    expect(getByRole("link", { name: "Example resource" })).toHaveAttribute("href", "/resource");
  });
});
