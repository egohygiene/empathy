import { createCommerceClient, type Cart } from "@egohygiene/commerce";
import type { StoreConfig } from "@egohygiene/store-config";
import { type ReactNode, useCallback, useEffect, useMemo, useState } from "react";
import { StorefrontContext } from "./StorefrontContext";

const cartStorageKey = "egohygiene.store.cart-id";

export interface StorefrontProviderProps {
  readonly children: ReactNode;
  readonly config: StoreConfig;
}

export function StorefrontProvider({ children, config }: StorefrontProviderProps) {
  const client = useMemo(() => createCommerceClient(config), [config]);
  const [products, setProducts] = useState<Awaited<ReturnType<typeof client.listProducts>>>([]);
  const [productsLoading, setProductsLoading] = useState(true);
  const [productsError, setProductsError] = useState<string | null>(null);
  const [cart, setCart] = useState<Cart | null>(null);
  const [cartBusy, setCartBusy] = useState(false);
  const [cartOpen, setCartOpen] = useState(false);

  useEffect(() => {
    let active = true;
    setProductsLoading(true);

    client
      .listProducts()
      .then((nextProducts) => {
        if (active) {
          setProducts(nextProducts);
          setProductsError(null);
        }
      })
      .catch((error: unknown) => {
        if (active) {
          setProductsError(error instanceof Error ? error.message : "Unable to load products.");
        }
      })
      .finally(() => {
        if (active) {
          setProductsLoading(false);
        }
      });

    return () => {
      active = false;
    };
  }, [client]);

  useEffect(() => {
    const storedCartId = window.localStorage.getItem(cartStorageKey);
    if (!storedCartId) {
      return;
    }

    client
      .getCart(storedCartId)
      .then((storedCart) => {
        if (storedCart) {
          setCart(storedCart);
        } else {
          window.localStorage.removeItem(cartStorageKey);
        }
      })
      .catch(() => {
        window.localStorage.removeItem(cartStorageKey);
      });
  }, [client]);

  const storeCart = useCallback((nextCart: Cart) => {
    setCart(nextCart);
    window.localStorage.setItem(cartStorageKey, nextCart.id);
  }, []);

  const addToCart = useCallback(
    async (variantId: string, quantity = 1) => {
      setCartBusy(true);
      try {
        const nextCart = await client.addItem(cart?.id ?? null, variantId, quantity);
        storeCart(nextCart);
        setCartOpen(true);
      } finally {
        setCartBusy(false);
      }
    },
    [cart?.id, client, storeCart],
  );

  const changeQuantity = useCallback(
    async (variantId: string, quantity: number) => {
      if (!cart) {
        return;
      }

      setCartBusy(true);
      try {
        storeCart(await client.changeItemQuantity(cart.id, variantId, Math.max(0, quantity)));
      } finally {
        setCartBusy(false);
      }
    },
    [cart, client, storeCart],
  );

  const removeItem = useCallback(
    async (variantId: string) => changeQuantity(variantId, 0),
    [changeQuantity],
  );

  const checkout = useCallback(() => {
    if (!cart || cart.items.length === 0) {
      return;
    }

    const checkoutUrl = client.buildCheckoutUrl(cart.id);
    if (client.providerName === "mock") {
      window.location.assign(`${config.basePath}${checkoutUrl}`);
      return;
    }

    window.location.assign(checkoutUrl);
  }, [cart, client, config.basePath]);

  const cartItemCount = cart?.items.reduce((total, item) => total + item.quantity, 0) ?? 0;

  const contextValue = useMemo(
    () => ({
      config,
      providerName: client.providerName,
      products,
      productsLoading,
      productsError,
      cart,
      cartBusy,
      cartOpen,
      cartItemCount,
      openCart: () => setCartOpen(true),
      closeCart: () => setCartOpen(false),
      addToCart,
      changeQuantity,
      removeItem,
      checkout,
    }),
    [
      addToCart,
      cart,
      cartBusy,
      cartItemCount,
      cartOpen,
      changeQuantity,
      checkout,
      client.providerName,
      config,
      products,
      productsError,
      productsLoading,
      removeItem,
    ],
  );

  return <StorefrontContext.Provider value={contextValue}>{children}</StorefrontContext.Provider>;
}
