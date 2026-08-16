import { createReactViteConfig } from "@egohygiene/vite-config";

export default createReactViteConfig({
  appDirectory: new URL(".", import.meta.url),
  workspaceDirectory: new URL("../../", import.meta.url),
  appName: "playground",
  basePath: "/playground/",
  serverPort: 5175,
  previewPort: 4175,
});
