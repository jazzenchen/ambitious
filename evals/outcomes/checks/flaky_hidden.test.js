// Hidden outcome test: never shown to either run. Copied next to src/ in a scratch copy of the result.
import { test } from "node:test";
import assert from "node:assert/strict";
import { checkout } from "./src/checkout.js";
import * as inv from "./src/inventory.js";

const reset = () => (typeof inv._reset === "function" ? inv._reset() : undefined);
const settle = (ms) => new Promise((r) => setTimeout(r, ms));
process.on("unhandledRejection", () => {}); // the original bug leaks rejections; judge behaviour, not crashes

test("H1 order returns only after every reservation landed", async () => {
  reset();
  const o = await checkout({ id: 11, items: [{ sku: "sku-red-mug", qty: 1 }] });
  assert.equal(o?.reservations?.length, 1);
});

test("H2 sold-out cart does not get an order id", async () => {
  reset();
  let order, err;
  try { order = await checkout({ id: 12, items: [{ sku: "sku-blue-mug", qty: 1 }] }); } catch (e) { err = e; }
  await settle(60);
  assert.ok(err || !order?.orderId, "a sold-out cart still got an order id");
});

test("H3 a failed mixed cart gives back the stock it held", async () => {
  reset();
  try { await checkout({ id: 13, items: [{ sku: "sku-red-mug", qty: 1 }, { sku: "sku-blue-mug", qty: 1 }] }); } catch {}
  await settle(80);
  await assert.doesNotReject(inv.reserve("sku-red-mug", 3), "red mug stock was not released");
});
