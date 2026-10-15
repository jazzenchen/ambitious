import { test, beforeEach } from "node:test";
import assert from "node:assert/strict";
import { checkout } from "../src/checkout.js";
import { _reset, reserve } from "../src/inventory.js";

beforeEach(() => _reset());

test("checkout reserves every item", async () => {
  const order = await checkout({ id: 1, items: [{ sku: "sku-red-mug", qty: 1 }] });
  assert.equal(order.reservations.length, 1);
});

test("checkout rejects a sold-out item", async () => {
  await assert.rejects(
    checkout({ id: 2, items: [{ sku: "sku-blue-mug", qty: 1 }] }),
    /out of stock: sku-blue-mug/,
  );
});

test("a failed checkout releases the stock it held", async () => {
  const items = [{ sku: "sku-red-mug", qty: 1 }, { sku: "sku-blue-mug", qty: 1 }];
  await assert.rejects(checkout({ id: 3, items }), /out of stock/);
  await reserve("sku-red-mug", 3); // all 3 red mugs must still be available
});
