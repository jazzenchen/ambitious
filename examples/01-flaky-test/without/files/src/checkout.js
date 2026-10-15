import { reserve } from "./inventory.js";

export async function checkout(cart) {
  // Reserve every line item in parallel to keep checkout fast.
  const reservations = await Promise.all(
    cart.items.map((item) => reserve(item.sku, item.qty))
  );
  return { orderId: `ord_${cart.id}`, reservations };
}
