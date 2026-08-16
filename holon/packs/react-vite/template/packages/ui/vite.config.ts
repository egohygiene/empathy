import { createReactLibraryConfig } from "@egohygiene/vite-config";

export default createReactLibraryConfig({
  packageDirectory: new URL(".", import.meta.url),
  entry: "src/library.ts",
  external: ["@egohygiene/icons", "@egohygiene/themes", "@egohygiene/utilities"],
});
