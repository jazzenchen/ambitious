// Simulated inventory service with variable network latency.
const stock = new Map([["sku-red-mug", 3], ["sku-blue-mug", 0]]);

export async function reserve(sku, qty) {
  await new Promise((r) => setTimeout(r, Math.random() * 40));
  const available = stock.get(sku) ?? 0;
  if (available < qty) throw new Error(`out of stock: ${sku}`);
  stock.set(sku, available - qty);
  return { sku, qty, reservedAt: Date.now() };
}

export function _reset() {
  stock.set("sku-red-mug", 3);
  stock.set("sku-blue-mug", 0);
}
