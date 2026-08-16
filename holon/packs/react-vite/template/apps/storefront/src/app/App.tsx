import { Route, Routes } from "react-router-dom";
import { RootLayout } from "../layouts/RootLayout";
import { AboutPage } from "../pages/AboutPage";
import { CheckoutReturnPage } from "../pages/CheckoutReturnPage";
import { HomePage } from "../pages/HomePage";
import { NotFoundPage } from "../pages/NotFoundPage";
import { ProductPage } from "../pages/ProductPage";
import { ShopPage } from "../pages/ShopPage";

export function App() {
  return (
    <Routes>
      <Route element={<RootLayout />}>
        <Route index element={<HomePage />} />
        <Route path="shop" element={<ShopPage />} />
        <Route path="products/:productSlug" element={<ProductPage />} />
        <Route path="about" element={<AboutPage />} />
        <Route path="checkout-return" element={<CheckoutReturnPage />} />
        <Route path="*" element={<NotFoundPage />} />
      </Route>
    </Routes>
  );
}
