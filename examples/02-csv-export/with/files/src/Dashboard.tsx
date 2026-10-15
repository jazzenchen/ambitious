import { useOrders } from "./useOrders";
import { toCsv, downloadCsv } from "./toCsv";

export function Dashboard() {
  const { orders } = useOrders();
  const exportCsv = () =>
    downloadCsv(
      "orders.csv",
      toCsv(orders, [
        { header: "ID", value: (o) => o.id },
        { header: "Customer", value: (o) => o.customer },
        { header: "Total", value: (o) => o.total },
        { header: "Status", value: (o) => o.status },
      ]),
    );
  return (
    <section>
      <h1>Orders</h1>
      <button type="button" onClick={exportCsv} disabled={orders.length === 0}>
        Download CSV
      </button>
      <table>
        <thead><tr><th>ID</th><th>Customer</th><th>Total</th><th>Status</th></tr></thead>
        <tbody>
          {orders.map((o) => (
            <tr key={o.id}><td>{o.id}</td><td>{o.customer}</td><td>{o.total}</td><td>{o.status}</td></tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}
