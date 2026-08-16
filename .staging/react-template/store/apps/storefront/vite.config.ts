import react from "@vitejs/plugin-react";
import { defineConfig, loadEnv } from "vite";

function normalizeBasePath(value: string): string {
  const withLeadingSlash = value.startsWith("/") ? value : `/${value}`;
  return withLeadingSlash.endsWith("/") ? withLeadingSlash : `${withLeadingSlash}/`;
}

export default defineConfig(({ mode }) => {
  const environment = loadEnv(mode, "../../", "");
  const basePath = normalizeBasePath(environment.VITE_STORE_BASE_PATH ?? "/store/");

  return {
    base: basePath,
    envDir: "../../",
    plugins: [react()],
    server: {
      open: basePath,
      port: 5173,
    },
    preview: {
      port: 4173,
    },
    build: {
      sourcemap: true,
      target: "es2022",
    },
  };
});
