import { useOrders } from "./useOrders";

export function Dashboard() {
  const { orders } = useOrders();
  return (
    <section>
      <h1>Orders</h1>
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
