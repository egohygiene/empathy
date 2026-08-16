import { describe, expect, it } from "vitest";
import { formatMoney } from "./money";

describe("formatMoney", () => {
  it("formats a normalized commerce value", () => {
    expect(formatMoney({ value: 24, currency: "USD" })).toBe("$24.00");
  });
});
