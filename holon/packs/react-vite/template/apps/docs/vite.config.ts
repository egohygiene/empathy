import { createReactViteConfig } from "@egohygiene/vite-config";

export default createReactViteConfig({
  appDirectory: new URL(".", import.meta.url),
  workspaceDirectory: new URL("../../", import.meta.url),
  appName: "docs",
  basePath: "/docs/",
  serverPort: 5174,
  previewPort: 4174,
});
