import { MOCK_ORDERS } from "../mocks/orders";

export default function Orders() {
  return (
    <div className="max-w-5xl mx-auto p-6">
      <h1 className="text-2xl font-bold text-indigo-900 mb-4">Meus pedidos</h1>
      <div className="space-y-4">
        {MOCK_ORDERS.map((o) => (
          <div key={o.id} className="rounded-xl border p-4">
            <div className="flex justify-between">
              <div>
                <div className="font-semibold">{o.id}</div>
                <div className="text-sm text-slate-500">
                  {new Date(o.createdAt).toLocaleString()}
                </div>
              </div>
              <div className="text-sm">
                <span className="px-2 py-1 rounded bg-indigo-50 text-indigo-700">
                  {o.status}
                </span>
              </div>
            </div>
            <ul className="mt-3 text-sm text-slate-700 list-disc ml-5">
              {o.items.map((it) => (
                <li key={it.book.id}>
                  {it.qty} × {it.book.title} — R${" "}
                  {(it.book.price * it.qty).toFixed(2)}
                </li>
              ))}
            </ul>
            <div className="mt-3 text-right">
              <span className="font-semibold">
                Total: R$ {o.total.toFixed(2)}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
