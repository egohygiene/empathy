import type { Cart, Product } from "@egohygiene/commerce";
import type { StoreConfig } from "@egohygiene/store-config";
import { createContext } from "react";

export interface StorefrontContextValue {
  readonly config: StoreConfig;
  readonly providerName: string;
  readonly products: readonly Product[];
  readonly productsLoading: boolean;
  readonly productsError: string | null;
  readonly cart: Cart | null;
  readonly cartBusy: boolean;
  readonly cartOpen: boolean;
  readonly cartItemCount: number;
  readonly openCart: () => void;
  readonly closeCart: () => void;
  readonly addToCart: (variantId: string, quantity?: number) => Promise<void>;
  readonly changeQuantity: (variantId: string, quantity: number) => Promise<void>;
  readonly removeItem: (variantId: string) => Promise<void>;
  readonly checkout: () => void;
}

export const StorefrontContext = createContext<StorefrontContextValue | null>(null);
