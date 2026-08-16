import path from "node:path";
import { fileURLToPath } from "node:url";

import react from "@vitejs/plugin-react-swc";
import { visualizer } from "rollup-plugin-visualizer";
import { defineConfig, loadEnv, type PluginOption, type ProxyOptions } from "vite";
import checker from "vite-plugin-checker";
import { VitePWA } from "vite-plugin-pwa";
import svgr from "vite-plugin-svgr";
import wasm from "vite-plugin-wasm";
import tsconfigPaths from "vite-tsconfig-paths";

export type PathInput = string | URL;

export interface ReactViteConfigOptions {
  /** App directory, normally `new URL(".", import.meta.url)`. */
  appDirectory: PathInput;
  /** Monorepo root containing the shared PostCSS configuration. */
  workspaceDirectory: PathInput;
  /** Stable cache namespace used when several apps share one workspace. */
  appName: string;
  /** App TypeScript project used by the path-alias plugin. */
  tsconfigFile?: string;
  /** Public base path. Can be overridden with VITE_BASE_PATH. */
  basePath?: string;
  /** Optional app-specific VITE_* variable that overrides the public base path. */
  basePathEnvironmentVariable?: `VITE_${string}`;
  /** Local development and preview ports. */
  serverPort?: number;
  previewPort?: number;
  /** Open the app when the dev server starts. Defaults to false in automation. */
  open?: boolean;
  /** Enable TypeScript diagnostics in the Vite development process. */
  checker?: boolean;
  /** Generate an offline-capable web app manifest and service worker. */
  pwa?: boolean;
  pwaName?: string;
  pwaShortName?: string;
  /** Enable SVG imports as React components. */
  svgr?: boolean;
  /** Enable WebAssembly imports. */
  wasm?: boolean;
  /** Additional aliases relative to the app directory unless absolute. */
  aliases?: Record<string, string>;
  /** Development proxies. Keep secrets and credentials on the server side. */
  proxy?: Record<string, string | ProxyOptions>;
}

export interface ReactLibraryConfigOptions {
  /** Package directory, normally `new URL(".", import.meta.url)`. */
  packageDirectory: PathInput;
  /** Library entry relative to the package directory. */
  entry?: string;
  /** Browser and framework packages that consumers must provide. */
  external?: string[];
  /** Stable output stem used for JavaScript and CSS artifacts. */
  fileName?: string;
}

function asDirectory(value: PathInput): string {
  return value instanceof URL ? fileURLToPath(value) : path.resolve(value);
}

function normalizeBasePath(value: string): string {
  if (value === "/") {
    return value;
  }

  const withLeadingSlash = value.startsWith("/") ? value : `/${value}`;
  return withLeadingSlash.endsWith("/") ? withLeadingSlash : `${withLeadingSlash}/`;
}

function readPort(value: string | undefined, fallback: number): number {
  const parsed = Number(value);
  return Number.isInteger(parsed) && parsed > 0 && parsed <= 65_535 ? parsed : fallback;
}

function readBoolean(value: string | undefined, fallback = false): boolean {
  if (value === undefined) {
    return fallback;
  }

  return value === "1" || value.toLowerCase() === "true";
}

function environmentValue(environment: Record<string, string>, key: string): string | undefined {
  return environment[key];
}

function manualChunks(id: string): string | undefined {
  if (!id.includes("node_modules")) {
    return undefined;
  }

  if (id.includes("react") || id.includes("scheduler")) {
    return "react";
  }

  if (id.includes("@tanstack")) {
    return "tanstack";
  }

  if (id.includes("i18next") || id.includes("intl")) {
    return "internationalization";
  }

  if (id.includes("three") || id.includes("deck.gl") || id.includes("maplibre")) {
    return "visualization";
  }

  return "vendor";
}

/**
 * Creates the canonical browser-app Vite configuration for this template.
 *
 * All `VITE_*` variables are public by definition. Configuration-only switches
 * use `TEMPLATE_*` and are never copied into the client bundle.
 */
export function createReactViteConfig(options: ReactViteConfigOptions) {
  const appDirectory = asDirectory(options.appDirectory);
  const workspaceDirectory = asDirectory(options.workspaceDirectory);

  return defineConfig(
    // biome-ignore lint/complexity/noExcessiveCognitiveComplexity: This factory explicitly composes independent opt-in build capabilities.
    ({ command, mode }) => {
      const environment = loadEnv(mode, workspaceDirectory, ["VITE_", "TEMPLATE_"]);
      const production = mode === "production";
      const configuredBasePath = environmentValue(
        environment,
        options.basePathEnvironmentVariable ?? "VITE_BASE_PATH",
      );
      const basePath = normalizeBasePath(configuredBasePath ?? options.basePath ?? "/");
      const analyze = readBoolean(environmentValue(environment, "TEMPLATE_ANALYZE"));
      const sourceMaps = readBoolean(
        environmentValue(environment, "TEMPLATE_SOURCE_MAPS"),
        !production,
      );
      const enableChecker = options.checker ?? command === "serve";
      const aliases = Object.fromEntries(
        Object.entries(options.aliases ?? {}).map(([key, value]) => [
          key,
          path.isAbsolute(value) ? value : path.resolve(appDirectory, value),
        ]),
      );

      const plugins: PluginOption[] = [
        react(),
        tsconfigPaths({
          projects: [path.join(appDirectory, options.tsconfigFile ?? "tsconfig.app.json")],
        }),
      ];

      if (options.svgr ?? true) {
        plugins.push(svgr({ include: "**/*.svg?react" }));
      }

      if (options.wasm ?? true) {
        plugins.push(wasm());
      }

      if (enableChecker) {
        plugins.push(checker({ typescript: true }));
      }

      if (options.pwa) {
        plugins.push(
          VitePWA({
            registerType: "autoUpdate",
            injectRegister: "auto",
            includeAssets: ["favicon.svg", "robots.txt"],
            manifest: {
              name: options.pwaName ?? options.appName,
              short_name: options.pwaShortName ?? options.appName,
              description: `${options.pwaName ?? options.appName} progressive web application`,
              display: "standalone",
              start_url: basePath,
              scope: basePath,
              theme_color: "#111827",
              background_color: "#111827",
              icons: [
                {
                  src: "favicon.svg",
                  sizes: "any",
                  type: "image/svg+xml",
                  purpose: "any maskable",
                },
              ],
            },
            workbox: {
              cleanupOutdatedCaches: true,
              clientsClaim: true,
              skipWaiting: true,
              navigateFallbackDenylist: [/^\/api\//],
            },
            devOptions: {
              enabled: readBoolean(environmentValue(environment, "TEMPLATE_PWA_DEV")),
            },
          }),
        );
      }

      if (analyze) {
        plugins.push(
          visualizer({
            filename: path.join(appDirectory, "dist", "bundle-analysis.html"),
            gzipSize: true,
            brotliSize: true,
            open: false,
            template: "treemap",
          }),
        );
      }

      return {
        root: appDirectory,
        base: basePath,
        envDir: workspaceDirectory,
        envPrefix: ["VITE_"],
        cacheDir: path.join(workspaceDirectory, "node_modules", ".vite", options.appName),
        publicDir: path.join(appDirectory, "public"),
        plugins,
        resolve: {
          alias: {
            "@": path.join(appDirectory, "src"),
            ...aliases,
          },
          dedupe: ["react", "react-dom"],
        },
        css: {
          devSourcemap: !production,
          postcss: path.join(workspaceDirectory, "postcss.config.mjs"),
        },
        server: {
          host: environmentValue(environment, "VITE_DEV_HOST") ?? "127.0.0.1",
          port: readPort(
            environmentValue(environment, "VITE_DEV_PORT"),
            options.serverPort ?? 5173,
          ),
          strictPort: true,
          open: options.open ?? false,
          cors: false,
          ...(options.proxy === undefined ? {} : { proxy: options.proxy }),
          headers: {
            "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "X-Content-Type-Options": "nosniff",
          },
          fs: {
            strict: true,
            allow: [workspaceDirectory],
          },
        },
        preview: {
          host: environmentValue(environment, "VITE_PREVIEW_HOST") ?? "127.0.0.1",
          port: readPort(
            environmentValue(environment, "VITE_PREVIEW_PORT"),
            options.previewPort ?? 4173,
          ),
          strictPort: true,
        },
        build: {
          target: "es2022",
          outDir: path.join(appDirectory, "dist"),
          emptyOutDir: true,
          sourcemap: sourceMaps,
          cssCodeSplit: true,
          assetsInlineLimit: 4_096,
          reportCompressedSize: true,
          chunkSizeWarningLimit: 900,
          modulePreload: {
            polyfill: true,
          },
          rollupOptions: {
            output: {
              assetFileNames: "assets/[name]-[hash][extname]",
              chunkFileNames: "assets/[name]-[hash].js",
              entryFileNames: "assets/[name]-[hash].js",
              manualChunks,
            },
          },
        },
        optimizeDeps: {
          entries: [path.join(appDirectory, "index.html")],
          include: ["react", "react-dom", "react/jsx-runtime"],
          esbuildOptions: {
            target: "es2022",
          },
        },
      };
    },
  );
}

/**
 * Creates the canonical React package build used by publishable UI libraries.
 *
 * The output is intentionally dual-format while React and workspace packages
 * stay external. TypeScript declarations are emitted by the package's
 * `tsconfig.build.json` after Vite writes the JavaScript and CSS artifacts.
 */
export function createReactLibraryConfig(options: ReactLibraryConfigOptions) {
  const packageDirectory = asDirectory(options.packageDirectory);
  const fileName = options.fileName ?? "index";

  return defineConfig({
    root: packageDirectory,
    plugins: [react()],
    resolve: {
      dedupe: ["react", "react-dom"],
    },
    build: {
      target: "es2022",
      outDir: path.join(packageDirectory, "dist"),
      emptyOutDir: true,
      sourcemap: true,
      cssCodeSplit: false,
      lib: {
        entry: path.join(packageDirectory, options.entry ?? "src/index.ts"),
        formats: ["es", "cjs"],
        fileName: (format) => (format === "cjs" ? `${fileName}.cjs` : `${fileName}.js`),
        cssFileName: "styles",
      },
      rollupOptions: {
        external: ["react", "react-dom", "react/jsx-runtime", ...(options.external ?? [])],
      },
    },
  });
}
