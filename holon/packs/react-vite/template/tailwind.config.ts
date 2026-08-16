import preset from "@egohygiene/tailwind-config";
import type { Config } from "tailwindcss";

const config = {
  presets: [preset],
  content: [
    "./index.html",
    "./apps/**/*.{html,js,jsx,md,mdx,ts,tsx}",
    "./packages/**/*.{html,js,jsx,md,mdx,ts,tsx}",
    "./stories/**/*.{js,jsx,mdx,ts,tsx}",
    "./.storybook/**/*.{js,jsx,mdx,ts,tsx}",
  ],
  safelist: [
    "sr-only",
    "not-sr-only",
    "motion-reduce:transition-none",
    {
      pattern: /^(bg|border|text)-(success|warning|danger|info)$/,
      variants: ["dark", "hover", "focus-visible"],
    },
  ],
} satisfies Config;

export default config;
