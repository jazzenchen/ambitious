import { test, beforeEach } from "node:test";
import assert from "node:assert/strict";
import { checkout } from "../src/checkout.js";
import { _reset } from "../src/inventory.js";

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

test("failed checkout releases the items it already reserved", async () => {
  await assert.rejects(
    checkout({ id: 3, items: [{ sku: "sku-red-mug", qty: 2 }, { sku: "sku-blue-mug", qty: 1 }] }),
  );
  const order = await checkout({ id: 4, items: [{ sku: "sku-red-mug", qty: 3 }] });
  assert.equal(order.reservations[0].qty, 3);
});
