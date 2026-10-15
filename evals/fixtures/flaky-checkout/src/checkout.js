import { reserve } from "./inventory.js";

export async function checkout(cart) {
  const reservations = [];
  // Reserve every line item in parallel to keep checkout fast.
  cart.items.forEach(async (item) => {
    reservations.push(await reserve(item.sku, item.qty));
  });
  return { orderId: `ord_${cart.id}`, reservations };
}
