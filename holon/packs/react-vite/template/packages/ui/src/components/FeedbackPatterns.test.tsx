import { render } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { Alert } from "./Alert";
import { EnvironmentBanner } from "./EnvironmentBanner";
import { LoadingState } from "./LoadingState";

describe("feedback patterns", () => {
  it("announces dangerous alerts assertively", () => {
    const { getByRole } = render(<Alert tone="danger">Unable to save.</Alert>);
    expect(getByRole("alert")).toHaveTextContent("Unable to save.");
  });

  it("announces one loading status without duplicating the spinner label", () => {
    const { getAllByRole } = render(<LoadingState message="Loading resources…" />);
    expect(getAllByRole("status")).toHaveLength(1);
  });

  it("can omit an environment notice without leaving empty markup", () => {
    const { container } = render(<EnvironmentBanner hidden label="Development" />);
    expect(container).toBeEmptyDOMElement();
  });
});
