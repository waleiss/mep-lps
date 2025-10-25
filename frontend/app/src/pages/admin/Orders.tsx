import { useMemo, useState } from "react";
import { type Pedido, MOCK_PEDIDOS } from "../../mocks/info-admin";

export default function Orders() {
  const [orders] = useState<Pedido[]>(() => MOCK_PEDIDOS);
  const [q, setQ] = useState("");
  const [status, setStatus] = useState<"" | Pedido["status"]>("");

  const filtered = useMemo(() => {
    let list = [...orders];
    if (q.trim()) {
      const s = q.toLowerCase();
      list = list.filter(
        (p) =>
          p.id.includes(q) ||
          p.cliente.toLowerCase().includes(s) ||
          p.email.toLowerCase().includes(s)
      );
    }
    if (status) list = list.filter((p) => p.status === status);
    return list;
  }, [orders, q, status]);

  return (
    <div className="bg-white rounded-2xl p-6 shadow-sm border">
      <div className="flex flex-wrap gap-3 mb-4">
        <input
          value={q}
          onChange={(e) => setQ(e.target.value)}
          placeholder="Buscar..."
          className="px-3 py-2 border rounded-lg flex-1"
        />
        <select
          value={status}
          onChange={(e) => setStatus(e.target.value as any)}
          className="px-3 py-2 border rounded-lg"
        >
          <option value="">Todos</option>
          <option value="PENDENTE">PENDENTE</option>
          <option value="PAGO">PAGO</option>
          <option value="ENVIADO">ENVIADO</option>
          <option value="CANCELADO">CANCELADO</option>
        </select>
      </div>

      <table className="w-full text-sm">
        <thead className="text-slate-600">
          <tr>
            <th className="text-left p-2">Pedido</th>
            <th className="text-left p-2">Cliente</th>
            <th className="text-left p-2">Itens</th>
            <th className="text-left p-2">Total</th>
            <th className="text-left p-2">Status</th>
          </tr>
        </thead>
        <tbody>
          {filtered.map((p) => (
            <tr key={p.id} className="border-t hover:bg-slate-50">
              <td className="p-2 font-medium">#{p.id}</td>
              <td className="p-2">
                <div>{p.cliente}</div>
                <div className="text-xs text-slate-500">{p.email}</div>
              </td>
              <td className="p-2">
                {p.itens.map((i) => (
                  <div key={i.titulo} className="text-xs">
                    {i.qtd}× {i.titulo}
                  </div>
                ))}
              </td>
              <td className="p-2 font-semibold">R$ {p.total.toFixed(2)}</td>
              <td className="p-2">{p.status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
