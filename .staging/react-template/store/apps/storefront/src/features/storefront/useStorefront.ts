import { useContext } from "react";
import { StorefrontContext } from "./StorefrontContext";

export function useStorefront() {
  const value = useContext(StorefrontContext);
  if (!value) {
    throw new Error("useStorefront must be used within StorefrontProvider.");
  }
  return value;
}
