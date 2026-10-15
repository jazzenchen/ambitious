import { test, beforeEach } from "node:test";
import assert from "node:assert/strict";
import { checkout } from "../src/checkout.js";
import { _reset } from "../src/inventory.js";

beforeEach(() => _reset());

test("checkout reserves every item", async () => {
  const order = await checkout({ id: 1, items: [{ sku: "sku-red-mug", qty: 1 }] });
  assert.equal(order.reservations.length, 1);
});

test("checkout reserves multiple items", async () => {
  const order = await checkout({
    id: 2,
    items: [{ sku: "sku-red-mug", qty: 1 }, { sku: "sku-red-mug", qty: 2 }],
  });
  assert.equal(order.reservations.length, 2);
});

test("checkout rejects when an item is out of stock", async () => {
  await assert.rejects(
    checkout({ id: 3, items: [{ sku: "sku-blue-mug", qty: 1 }] }),
    /out of stock: sku-blue-mug/
  );
});
