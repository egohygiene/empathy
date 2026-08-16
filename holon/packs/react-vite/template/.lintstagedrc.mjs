export default {
  "*.{cjs,css,html,js,json,jsonc,jsx,md,mdx,mjs,scss,ts,tsx,yaml,yml}": [
    "prettier --write --ignore-unknown",
  ],
  "*.{cjs,js,jsx,mjs,ts,tsx,json,jsonc,css}": ["biome check --write --no-errors-on-unmatched"],
};
