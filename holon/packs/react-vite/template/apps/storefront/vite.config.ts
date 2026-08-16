import { createReactViteConfig } from "@egohygiene/vite-config";

export default createReactViteConfig({
  appDirectory: new URL(".", import.meta.url),
  workspaceDirectory: new URL("../../", import.meta.url),
  appName: "storefront",
  tsconfigFile: "tsconfig.json",
  basePath: "/store/",
  basePathEnvironmentVariable: "VITE_STORE_BASE_PATH",
  serverPort: 5176,
  previewPort: 4176,
});
