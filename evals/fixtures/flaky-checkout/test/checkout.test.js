import { test, beforeEach } from "node:test";
import assert from "node:assert/strict";
import { checkout } from "../src/checkout.js";
import { _reset } from "../src/inventory.js";

beforeEach(() => _reset());

test("checkout reserves every item", async () => {
  const order = await checkout({ id: 1, items: [{ sku: "sku-red-mug", qty: 1 }] });
  await new Promise((r) => setTimeout(r, 25)); // give reservations time to land
  assert.equal(order.reservations.length, 1);
});
