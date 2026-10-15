import { test } from "node:test";
import assert from "node:assert/strict";
import { readdirSync, readFileSync } from "node:fs";
import path from "node:path";

// forEach ignores the promises an async callback returns, so the caller moves on
// before the work finishes and any rejection goes unhandled (see SHOP-412).
const ASYNC_FOREACH = /\.forEach\(\s*async\b/;

function sourceFiles(dir) {
  return readdirSync(dir, { withFileTypes: true }).flatMap((e) => {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) return sourceFiles(p);
    return /\.[cm]?js$/.test(e.name) ? [p] : [];
  });
}

test("src/ never passes an async callback to forEach", () => {
  const hits = sourceFiles(process.env.ASYNC_CHECK_DIR ?? "src").flatMap((file) =>
    readFileSync(file, "utf8").split("\n").flatMap((line, i) =>
      ASYNC_FOREACH.test(line) ? [`${file}:${i + 1}`] : []),
  );
  assert.deepEqual(hits, [], "use `await Promise.all(items.map(...))` instead");
});
