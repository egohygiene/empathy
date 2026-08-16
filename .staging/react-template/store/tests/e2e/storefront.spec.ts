import { expect, test } from "@playwright/test";

test("loads the mock storefront and navigates to a product", async ({ page }) => {
  await page.goto("./");

  await expect(page.getByRole("heading", { name: "carry the signal." })).toBeVisible();
  await expect(page.getByText("concept storefront")).toBeVisible();

  await page.getByRole("link", { name: "cosmic balance hoodie" }).first().click();
  await expect(page.getByRole("heading", { name: "cosmic balance hoodie" })).toBeVisible();

  await page.getByRole("button", { name: "add to cart" }).click();
  await expect(page.getByRole("dialog", { name: "cart" })).toBeVisible();
  await expect(page.getByText("Black / Small")).toBeVisible();
});
