import { fileURLToPath } from "node:url";

import autoprefixer from "autoprefixer";
import postcssImport from "postcss-import";
import tailwindcss from "tailwindcss";

const tailwindConfig = fileURLToPath(new URL("./tailwind.config.ts", import.meta.url));

export default {
  plugins: [postcssImport(), tailwindcss({ config: tailwindConfig }), autoprefixer()],
};
