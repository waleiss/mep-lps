import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import { getOrders, cancelOrder, type Order as OrderData } from "../services/ordersApi";
import { getBook } from "../services/api";
import type { Book } from "../types/book";

type OrderWithBooks = OrderData & {
  booksDetails?: Book[];
};

export default function Orders() {
  const { user } = useAuth();
  const [orders, setOrders] = useState<OrderWithBooks[]>([]);
  const [loading, setLoading] = useState(true);
  const [cancelling, setCancelling] = useState<number | null>(null);
  const [confirmCancelId, setConfirmCancelId] = useState<number | null>(null);

  useEffect(() => {
    const fetchOrders = async () => {
      if (!user) {
        setLoading(false);
        return;
      }
      
      try {
        const data = await getOrders(parseInt(user.id));
        
        // Buscar detalhes dos livros para cada pedido
        const ordersWithBooks = await Promise.all(
          data.map(async (order) => {
            if (!order.items || order.items.length === 0) {
              return { ...order, booksDetails: [] };
            }
            
            const booksPromises = order.items.map(item => 
              getBook(item.livro_id.toString())
            );
            const booksDetails = await Promise.all(booksPromises);
            
            return {
              ...order,
              booksDetails: booksDetails.filter((b): b is Book => b !== undefined),
            };
          })
        );
        
        setOrders(ordersWithBooks);
      } catch (error) {
        console.error("Erro ao carregar pedidos:", error);
      } finally {
        setLoading(false);
      }
    };
    
    fetchOrders();
  }, [user]);

  const handleCancelOrder = async (orderId: number) => {
    setCancelling(orderId);
    try {
      await cancelOrder(orderId);
      
      // Atualiza a lista de pedidos após cancelar
      setOrders(prevOrders =>
        prevOrders.map(order =>
          order.id === orderId
            ? { ...order, status: 'cancelado' }
            : order
        )
      );
    } catch (error: any) {
      console.error("Erro ao cancelar pedido:", error);
      alert(
        error.response?.data?.detail || 
        "Erro ao cancelar pedido. Tente novamente."
      );
    } finally {
      setCancelling(null);
      setConfirmCancelId(null);
    }
  };

  if (loading) {
    return (
      <div className="max-w-5xl mx-auto p-6">
        <h1 className="text-2xl font-bold text-indigo-900 mb-4">Meus pedidos</h1>
        <p className="text-slate-600">Carregando...</p>
      </div>
    );
  }

  const statusLabels: Record<string, string> = {
    pending: "Pendente",
    pendente: "Pendente",
    confirmado: "Confirmado",
    processing: "Processando",
    processando: "Processando",
    shipped: "Enviado",
    enviado: "Enviado",
    delivered: "Entregue",
    entregue: "Entregue",
    cancelled: "Cancelado",
    cancelado: "Cancelado",
    devolvido: "Devolvido",
  };

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
                  <div className="font-semibold">Pedido #{o.id}</div>
                  <div className="text-sm text-slate-500">
                    {new Date(o.data_criacao).toLocaleString('pt-BR')}
                  </div>
                  {o.observacoes && (
                    <div className="text-xs text-slate-400 mt-1">
                      {o.observacoes}
                    </div>
                  )}
                </div>
                <div className="text-sm flex flex-col items-end gap-2">
                  <span className="px-2 py-1 rounded bg-indigo-50 text-indigo-700">
                    {statusLabels[o.status] || o.status}
                  </span>
                  
                  {/* Botão de cancelar - só aparece se não estiver cancelado ou entregue */}
                  {o.status !== 'cancelado' && o.status !== 'entregue' && o.status !== 'devolvido' && (
                    <button
                      onClick={() => setConfirmCancelId(o.id)}
                      disabled={cancelling === o.id}
                      className="px-3 py-1 text-xs rounded border border-red-200 text-red-600 hover:bg-red-50 disabled:opacity-50 disabled:cursor-not-allowed transition"
                    >
                      {cancelling === o.id ? "Cancelando..." : "Cancelar pedido"}
                    </button>
                  )}
                </div>
              </div>
              
              {o.items && o.items.length > 0 && (
                <ul className="mt-3 text-sm text-slate-700 space-y-1">
                  {o.items.map((item, idx) => {
                    const book = o.booksDetails?.[idx];
                    return (
                      <li key={idx} className="flex justify-between">
                        <span>
                          {item.quantidade}x {book?.title || `Livro ID ${item.livro_id}`}
                        </span>
                        <span className="text-slate-600">
                          R$ {item.subtotal.toFixed(2)}
                        </span>
                      </li>
                    );
                  })}
                </ul>
              )}
              
              <div className="mt-3 pt-3 border-t flex justify-between items-center">
                <span className="text-sm text-slate-500">
                  Pedido: {o.numero_pedido}
                </span>
                <span className="font-semibold text-indigo-900">
                  Total: R$ {o.valor_total.toFixed(2)}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
      
      {/* Modal de confirmação estilizado para cancelamento */}
      {confirmCancelId !== null && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
          <div className="w-full max-w-md bg-white rounded-xl shadow-xl border">
            <div className="px-5 py-4 border-b">
              <h4 className="text-lg font-semibold text-slate-800">Confirmar cancelamento</h4>
            </div>
            <div className="px-5 py-4">
              <p className="text-slate-700 mb-2">Tem certeza que deseja cancelar este pedido?</p>
              <p className="text-slate-500 text-sm">Esta ação não pode ser desfeita.</p>
            </div>
            <div className="px-5 py-3 border-t flex justify-end gap-2">
              <button
                onClick={() => setConfirmCancelId(null)}
                disabled={cancelling === confirmCancelId}
                className="px-4 py-2 rounded-lg border hover:bg-slate-50 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Voltar
              </button>
              <button
                onClick={() => handleCancelOrder(confirmCancelId)}
                disabled={cancelling === confirmCancelId}
                className={`px-4 py-2 rounded-lg text-white ${cancelling === confirmCancelId ? 'bg-slate-400 cursor-not-allowed' : 'bg-rose-600 hover:bg-rose-700'}`}
              >
                {cancelling === confirmCancelId ? 'Cancelando...' : 'Confirmar cancelamento'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
