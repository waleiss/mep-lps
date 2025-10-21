import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";

// TODO: Criar API de pedidos quando o order service estiver pronto
type Order = {
  id: string;
  createdAt: string;
  status: string;
  items: Array<{
    book: { id: string; title: string; price: number };
    qty: number;
  }>;
  total: number;
};

export default function Orders() {
  const { user } = useAuth();
  const [orders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // TODO: Buscar pedidos do backend quando order service estiver integrado
    // Exemplo de como buscar: 
    // const fetchOrders = async () => {
    //   const data = await ordersApi.getOrders(user.id);
    //   setOrders(data);
    //   setLoading(false);
    // };
    // fetchOrders();
    
    // Por enquanto, mostra mensagem vazia
    setLoading(false);
  }, [user]);

  if (loading) {
    return (
      <div className="max-w-5xl mx-auto p-6">
        <h1 className="text-2xl font-bold text-indigo-900 mb-4">Meus pedidos</h1>
        <p className="text-slate-600">Carregando...</p>
      </div>
    );
  }

  return (
    <div className="max-w-5xl mx-auto p-6">
      <h1 className="text-2xl font-bold text-indigo-900 mb-4">Meus pedidos</h1>
      
      {orders.length === 0 ? (
        <div className="rounded-xl border p-8 text-center">
          <p className="text-slate-600 mb-2">
            Você ainda não fez nenhum pedido.
          </p>
          <p className="text-sm text-slate-500">
            Quando você finalizar uma compra, seus pedidos aparecerão aqui.
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {orders.map((o) => (
            <div key={o.id} className="rounded-xl border p-4 bg-white">
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
      )}
    </div>
  );
}
