import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "@egohygiene/tailwind-config/styles.css";

import { AppProviders } from "./app/AppProviders";
import "./styles/reset.css";
import "./styles/tokens.css";
import "./styles/app.css";

const rootElement = document.getElementById("root");
if (!rootElement) {
  throw new Error("Unable to find the application root element.");
}

createRoot(rootElement).render(
  <StrictMode>
    <AppProviders />
  </StrictMode>,
);
