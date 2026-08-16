import { rm } from "node:fs/promises";

const generatedDirectories = [".turbo", "coverage", "playwright-report", "test-results"];

await Promise.all(
  generatedDirectories.map((generatedDirectory) =>
    rm(generatedDirectory, { force: true, recursive: true }),
  ),
);

console.log("Removed repository-level generated output.");
