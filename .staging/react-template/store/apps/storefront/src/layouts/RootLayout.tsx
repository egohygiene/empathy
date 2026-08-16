import { Outlet } from "react-router-dom";
import { CartDrawer } from "../components/CartDrawer";
import { Footer } from "../components/Footer";
import { Header } from "../components/Header";

export function RootLayout() {
  return (
    <div className="site-shell">
      <Header />
      <main id="main-content">
        <Outlet />
      </main>
      <Footer />
      <CartDrawer />
    </div>
  );
}
