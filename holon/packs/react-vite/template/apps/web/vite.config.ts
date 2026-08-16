import { createReactViteConfig } from "@egohygiene/vite-config";

export default createReactViteConfig({
  appDirectory: new URL(".", import.meta.url),
  workspaceDirectory: new URL("../../", import.meta.url),
  appName: "web",
  basePath: "/",
  serverPort: 5173,
  previewPort: 4173,
  pwa: true,
  pwaName: "React Vite Template",
  pwaShortName: "Template",
});
