import { useOrders } from "./useOrders";
import { downloadCsv, toCsv } from "./exportCsv";

export function Dashboard() {
  const { orders } = useOrders();
  const exportCsv = () => {
    const csv = toCsv(orders, [
      { key: "id", header: "ID" },
      { key: "customer", header: "Customer" },
      { key: "total", header: "Total" },
      { key: "status", header: "Status" },
    ]);
    downloadCsv(`orders-${new Date().toISOString().slice(0, 10)}.csv`, csv);
  };
  return (
    <section>
      <h1>Orders</h1>
      <button type="button" onClick={exportCsv} disabled={orders.length === 0}>
        Export CSV
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
