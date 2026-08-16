import type { Meta, StoryObj } from "@storybook/react-vite";

import { HorizontalScroller } from "./HorizontalScroller";
import { MediaCard } from "./MediaCard";

const previewImage =
  "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='640' height='360' viewBox='0 0 640 360'%3E%3Cdefs%3E%3ClinearGradient id='g' x1='0' y1='0' x2='1' y2='1'%3E%3Cstop stop-color='%237c3aed'/%3E%3Cstop offset='1' stop-color='%23f472b6'/%3E%3C/linearGradient%3E%3C/defs%3E%3Crect width='640' height='360' fill='url(%23g)'/%3E%3C/svg%3E";
const resourceNames = ["Foundations", "Components", "Patterns", "Profiles", "Examples"];

const meta = {
  title: "Patterns/Content",
  component: MediaCard,
} satisfies Meta<typeof MediaCard>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Card: Story = {
  args: {
    description: "A data-neutral card that products can fill with their own content.",
    href: "#",
    imageAlt: "Purple and pink gradient placeholder",
    imageSrc: previewImage,
    title: "Reusable content card",
  },
};

export const Scroller: Story = {
  render: () => (
    <HorizontalScroller label="Featured resources">
      {resourceNames.map((resourceName) => (
        <MediaCard
          description="Use arrow keys or a pointer to explore the horizontal collection."
          href="#"
          imageAlt="Purple and pink gradient placeholder"
          imageSrc={previewImage}
          key={resourceName}
          title={resourceName}
        />
      ))}
    </HorizontalScroller>
  ),
};
