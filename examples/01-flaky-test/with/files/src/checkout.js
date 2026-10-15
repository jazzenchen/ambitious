import { reserve, release } from "./inventory.js";

export async function checkout(cart) {
  // Reserve every line item in parallel to keep checkout fast.
  const results = await Promise.allSettled(
    cart.items.map((item) => reserve(item.sku, item.qty)),
  );
  const failed = results.find((r) => r.status === "rejected");
  if (failed) {
    // Give back whatever we did manage to hold before failing the order.
    for (const r of results) {
      if (r.status === "fulfilled") release(r.value.sku, r.value.qty);
    }
    throw failed.reason;
  }
  return { orderId: `ord_${cart.id}`, reservations: results.map((r) => r.value) };
}
