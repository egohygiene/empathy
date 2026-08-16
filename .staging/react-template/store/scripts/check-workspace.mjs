import { access, readFile } from "node:fs/promises";

const requiredFiles = [
  "apps/storefront/package.json",
  "packages/commerce/package.json",
  "packages/store-config/package.json",
  "packages/store-ui/package.json",
  "vercel.json",
  ".env.example",
];

for (const requiredFile of requiredFiles) {
  await access(requiredFile);
}

const rootPackage = JSON.parse(await readFile("package.json", "utf8"));
if (rootPackage.private !== true) {
  throw new Error("The repository root must remain private to prevent accidental publication.");
}

console.log(`Workspace check passed (${requiredFiles.length} required files).`);
