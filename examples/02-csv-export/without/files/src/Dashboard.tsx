import { useOrders } from "./useOrders";

const COLUMNS = [
  { header: "ID", key: "id" },
  { header: "Customer", key: "customer" },
  { header: "Total", key: "total" },
  { header: "Status", key: "status" },
] as const;

// Quote fields per RFC 4180, and neutralize leading =+-@ so Excel/Sheets
// don't evaluate customer-supplied text as a formula.
function csvField(value: unknown): string {
  let s = value == null ? "" : String(value);
  if (/^[=+\-@\t\r]/.test(s) && typeof value !== "number") s = "'" + s;
  return /[",\r\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
}

type ExportRow = Record<(typeof COLUMNS)[number]["key"], unknown>;

function exportCsv(orders: ExportRow[]) {
  const lines = [
    COLUMNS.map((c) => csvField(c.header)).join(","),
    ...orders.map((o) => COLUMNS.map((c) => csvField(o[c.key])).join(",")),
  ];
  // BOM so Excel opens UTF-8 customer names correctly.
  const blob = new Blob(["﻿" + lines.join("\r\n")], { type: "text/csv;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `orders-${new Date().toISOString().slice(0, 10)}.csv`;
  a.click();
  URL.revokeObjectURL(url);
}

export function Dashboard() {
  const { orders } = useOrders();
  return (
    <section>
      <h1>Orders</h1>
      <button type="button" onClick={() => exportCsv(orders)} disabled={orders.length === 0}>
        Export CSV
      </button>
      <table>
        <thead><tr>{COLUMNS.map((c) => <th key={c.key}>{c.header}</th>)}</tr></thead>
        <tbody>
          {orders.map((o) => (
            <tr key={o.id}><td>{o.id}</td><td>{o.customer}</td><td>{o.total}</td><td>{o.status}</td></tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}
