import assert from "node:assert/strict";
import { mkdirSync, mkdtempSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { spawnSync } from "node:child_process";
import { test } from "node:test";
import emojiRegex from "emoji-regex";

test("emoji-regex keeps joined emoji sequences together", () => {
  const input = "realm 🚀 and family 👨‍👩‍👧‍👦";
  const matches = [...input.matchAll(emojiRegex())].map((match) => match[0]);

  assert.deepEqual(matches, ["🚀", "👨‍👩‍👧‍👦"]);
});

test("Pandoc filter replaces a cached emoji in LaTeX output", () => {
  const cacheDirectory = mkdtempSync(join(tmpdir(), "realm-emoji-filter-"));
  mkdirSync(cacheDirectory, { recursive: true });
  writeFileSync(join(cacheDirectory, "1f680.pdf"), "");

  const pandocDocument = {
    "pandoc-api-version": [1, 23, 1],
    meta: {},
    blocks: [
      {
        t: "Para",
        c: [{ t: "Str", c: "🚀" }],
      },
    ],
  };

  const filterPath = resolve("bin", "pandoc-emoji-filter.mjs");
  const result = spawnSync(process.execPath, [filterPath, "latex"], {
    cwd: resolve("."),
    encoding: "utf8",
    env: {
      ...process.env,
      REALM_EMOJI_CACHE: cacheDirectory,
    },
    input: JSON.stringify(pandocDocument),
  });

  assert.equal(result.status, 0, result.stderr);
  const output = JSON.parse(result.stdout);
  assert.equal(output.blocks[0].c[0].t, "RawInline");
  assert.match(output.blocks[0].c[0].c[1], /1f680\.pdf/);
});
