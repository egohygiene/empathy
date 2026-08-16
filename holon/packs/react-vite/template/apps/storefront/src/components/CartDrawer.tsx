import { Button } from "@egohygiene/store-ui";
import { useEffect } from "react";
import { formatMoney } from "../lib/money";
import { useStorefront } from "../features/storefront/useStorefront";

export function CartDrawer() {
  const { cart, cartOpen, closeCart, checkout, cartBusy, changeQuantity, removeItem } =
    useStorefront();

  useEffect(() => {
    if (!cartOpen) {
      return undefined;
    }

    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        closeCart();
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [cartOpen, closeCart]);

  if (!cartOpen) {
    return null;
  }

  return (
    <div className="cart-layer">
      <button
        className="cart-layer__backdrop"
        type="button"
        aria-label="Close cart"
        onClick={closeCart}
      />
      <aside className="cart-drawer" role="dialog" aria-modal="true" aria-labelledby="cart-title">
        <header className="cart-drawer__header">
          <div>
            <p className="eyebrow">your collection</p>
            <h2 id="cart-title">cart</h2>
          </div>
          <button className="icon-button" type="button" onClick={closeCart} aria-label="Close cart">
            ×
          </button>
        </header>

        {!cart || cart.items.length === 0 ? (
          <div className="cart-empty">
            <p>Your cart is still floating in empty space.</p>
            <Button variant="secondary" onClick={closeCart}>
              keep exploring
            </Button>
          </div>
        ) : (
          <>
            <ul className="cart-items">
              {cart.items.map((item) => (
                <li key={item.variantId} className="cart-item">
                  {item.image ? <img src={item.image.url} alt="" /> : null}
                  <div className="cart-item__details">
                    <strong>{item.productName}</strong>
                    <span>{item.variantName}</span>
                    <span>{formatMoney(item.price)}</span>
                    <fieldset className="quantity-control">
                      <legend className="visually-hidden">Quantity for {item.productName}</legend>
                      <button
                        type="button"
                        onClick={() => changeQuantity(item.variantId, item.quantity - 1)}
                        aria-label={`Decrease ${item.productName} quantity`}
                      >
                        −
                      </button>
                      <span>{item.quantity}</span>
                      <button
                        type="button"
                        onClick={() => changeQuantity(item.variantId, item.quantity + 1)}
                        aria-label={`Increase ${item.productName} quantity`}
                      >
                        +
                      </button>
                    </fieldset>
                    <button
                      className="text-button"
                      type="button"
                      onClick={() => removeItem(item.variantId)}
                    >
                      remove
                    </button>
                  </div>
                </li>
              ))}
            </ul>

            <footer className="cart-drawer__footer">
              <div className="cart-total">
                <span>subtotal</span>
                <strong>{formatMoney(cart.subtotal)}</strong>
              </div>
              <p>Shipping and taxes are calculated during secure checkout.</p>
              <Button onClick={checkout} busy={cartBusy}>
                continue to checkout
              </Button>
            </footer>
          </>
        )}
      </aside>
    </div>
  );
}
