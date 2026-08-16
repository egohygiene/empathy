import { createStoreConfig } from "@egohygiene/store-config";
import { BrowserRouter } from "react-router-dom";
import { App } from "./App";
import { ErrorBoundary } from "../components/ErrorBoundary";
import { StorefrontProvider } from "../features/storefront/StorefrontProvider";

function routerBasename(basePath: string): string {
  return basePath === "/" ? "/" : basePath.replace(/\/$/u, "");
}

export function AppProviders() {
  const config = createStoreConfig(import.meta.env as Record<string, string | boolean | undefined>);

  return (
    <ErrorBoundary>
      <StorefrontProvider config={config}>
        <BrowserRouter basename={routerBasename(config.basePath)}>
          <App />
        </BrowserRouter>
      </StorefrontProvider>
    </ErrorBoundary>
  );
}
