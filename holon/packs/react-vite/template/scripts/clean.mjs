import { readdir, rm } from "node:fs/promises";
import path from "node:path";

const generatedDirectories = [
  ".turbo",
  "coverage",
  "dist-node",
  "playwright-report",
  "storybook-static",
  "test-results",
];

for (const workspaceGroup of ["apps", "packages"]) {
  const workspaces = await readdir(workspaceGroup, { withFileTypes: true });
  for (const workspace of workspaces) {
    if (!workspace.isDirectory()) {
      continue;
    }

    generatedDirectories.push(
      path.join(workspaceGroup, workspace.name, "coverage"),
      path.join(workspaceGroup, workspace.name, "dist"),
    );
  }
}

await Promise.all(
  generatedDirectories.map((generatedDirectory) =>
    rm(generatedDirectory, { force: true, recursive: true }),
  ),
);

console.log("Removed repository-level generated output.");
