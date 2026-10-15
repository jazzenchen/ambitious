import { reserve, release } from "./inventory.js";

export async function checkout(cart) {
  // Reserve every line item in parallel to keep checkout fast.
  const results = await Promise.allSettled(
    cart.items.map((item) => reserve(item.sku, item.qty)),
  );
  const failed = results.find((r) => r.status === "rejected");
  if (failed) {
    // All or nothing: give back any stock this order did manage to hold.
    const held = results.filter((r) => r.status === "fulfilled").map((r) => r.value);
    await Promise.all(held.map((r) => release(r.sku, r.qty)));
    throw failed.reason;
  }
  return { orderId: `ord_${cart.id}`, reservations: results.map((r) => r.value) };
}
