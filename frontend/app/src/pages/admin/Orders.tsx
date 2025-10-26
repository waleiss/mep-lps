import { useEffect, useMemo, useState } from "react";
import { getOrders, updateOrderStatus, getOrder, type Order } from "../../services/ordersApi";

type OrderStatus = "PENDENTE" | "PROCESSANDO" | "PAGO" | "ENVIADO" | "ENTREGUE" | "CANCELADO";

export default function Orders() {
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [q, setQ] = useState("");
  const [status, setStatus] = useState<"" | OrderStatus>("");
  const [selectedOrder, setSelectedOrder] = useState<Order | null>(null);
  const [loadingDetails, setLoadingDetails] = useState(false);

  useEffect(() => {
    loadOrders();
  }, []);

  async function loadOrders() {
    setLoading(true);
    try {
      const data = await getOrders();
      setOrders(data);
    } catch (error) {
      console.error("Erro ao carregar pedidos:", error);
    } finally {
      setLoading(false);
    }
  }

  async function handleViewDetails(orderId: number) {
    setLoadingDetails(true);
    try {
      const orderDetails = await getOrder(orderId);
      if (orderDetails) {
        setSelectedOrder(orderDetails);
      }
    } catch (error) {
      console.error("Erro ao carregar detalhes do pedido:", error);
    } finally {
      setLoadingDetails(false);
    }
  }

  function mapStatus(st: string): string {
    const statusMap: Record<string, string> = {
      pending: "PENDENTE",
      processing: "PROCESSANDO",
      confirmado: "CONFIRMADO",
      paid: "PAGO",
      shipped: "ENVIADO",
      delivered: "ENTREGUE",
      cancelled: "CANCELADO",
      cancelado: "CANCELADO",
      devolvido: "DEVOLVIDO",
    };
    return statusMap[st.toLowerCase()] || st.toUpperCase();
  }

  function getStatusColor(st: string): string {
    const normalized = mapStatus(st);
    switch (normalized) {
      case "PAGO":
      case "ENTREGUE":
        return "bg-green-100 text-green-800";
      case "CONFIRMADO":
        return "bg-blue-100 text-blue-800";
      case "ENVIADO":
        return "bg-blue-100 text-blue-800";
      case "PROCESSANDO":
        return "bg-yellow-100 text-yellow-800";
      case "PENDENTE":
        return "bg-orange-100 text-orange-800";
      case "CANCELADO":
        return "bg-red-100 text-red-800";
      case "DEVOLVIDO":
        return "bg-slate-100 text-slate-800";
      default:
        return "bg-gray-100 text-gray-800";
    }
  }

  const filtered = useMemo(() => {
    let list = [...orders];
    if (q.trim()) {
      const s = q.toLowerCase();
      list = list.filter(
        (p) =>
          p.numero_pedido.toLowerCase().includes(s) ||
          p.id.toString().includes(s)
      );
    }
    if (status) {
      list = list.filter((p) => mapStatus(p.status).toUpperCase() === status);
    }
    return list;
  }, [orders, q, status]);

  if (loading) {
    return (
      <div className="bg-white rounded-2xl p-6 shadow-sm border">
        <p className="text-center text-slate-500">Carregando pedidos...</p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-2xl p-6 shadow-sm border">
      <h1 className="text-2xl font-bold text-slate-800 mb-4">Pedidos</h1>
      
      <div className="flex flex-wrap gap-3 mb-4">
        <input
          value={q}
          onChange={(e) => setQ(e.target.value)}
          placeholder="Buscar por número de pedido..."
          className="px-3 py-2 border rounded-lg flex-1"
        />
        <select
          value={status}
          onChange={(e) => setStatus(e.target.value as any)}
          className="px-3 py-2 border rounded-lg"
        >
          <option value="">Todos</option>
          <option value="CONFIRMADO">CONFIRMADO</option>
          <option value="PENDENTE">PENDENTE</option>
          <option value="PROCESSANDO">PROCESSANDO</option>
          <option value="PAGO">PAGO</option>
          <option value="ENVIADO">ENVIADO</option>
          <option value="ENTREGUE">ENTREGUE</option>
          <option value="CANCELADO">CANCELADO</option>
          <option value="DEVOLVIDO">DEVOLVIDO</option>
        </select>
      </div>

      {filtered.length === 0 ? (
        <p className="text-center text-slate-500 py-8">Nenhum pedido encontrado</p>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="text-slate-600 border-b">
              <tr>
                <th className="text-left p-3">Pedido</th>
                <th className="text-left p-3">Cliente</th>
                <th className="text-left p-3">Itens</th>
                <th className="text-left p-3">Total</th>
                <th className="text-left p-3">Status</th>
                <th className="text-left p-3">Ações</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((p) => (
                <tr key={p.id} className="border-b hover:bg-slate-50">
                  <td className="p-3">
                    <div className="font-medium">#{p.numero_pedido}</div>
                    <div className="text-xs text-slate-500">
                      {new Date(p.data_criacao).toLocaleDateString('pt-BR')}
                    </div>
                  </td>
                  <td className="p-3">
                    <div className="text-slate-600">ID: {p.usuario_id}</div>
                  </td>
                  <td className="p-3">
                    <div className="text-xs text-slate-600">
                      {p.items?.length || 0} item(ns)
                    </div>
                  </td>
                  <td className="p-3 font-semibold">
                    R$ {p.valor_total.toFixed(2)}
                  </td>
                  <td className="p-3">
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(p.status)}`}>
                      {mapStatus(p.status)}
                    </span>
                  </td>
                  <td className="p-3">
                    <button
                      onClick={() => handleViewDetails(p.id)}
                      disabled={loadingDetails}
                      className="px-3 py-1 text-sm bg-indigo-600 text-white rounded hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      {loadingDetails ? "Carregando..." : "Ver Detalhes"}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {selectedOrder && (
        <OrderDetailsModal
          order={selectedOrder}
          onClose={() => setSelectedOrder(null)}
          onUpdated={(updated) => {
            // Atualiza lista e o modal
            setOrders((prev) => prev.map((o) => (o.id === updated.id ? updated : o)));
            setSelectedOrder(updated);
          }}
        />
      )}
    </div>
  );
}

function OrderDetailsModal({ order, onClose, onUpdated }: { order: Order; onClose: () => void; onUpdated: (o: Order) => void }) {
  const [updating, setUpdating] = useState<string | null>(null);
  const [confirmData, setConfirmData] = useState<null | { status: string; label: string }>(null);

  function statusLabel(st: string) {
    const map: Record<string, string> = {
      confirmado: 'Confirmar',
      processando: 'Processando',
      enviado: 'Enviar',
      entregue: 'Concluir (Entregue)',
      cancelado: 'Cancelar',
      devolvido: 'Devolver',
    };
    return map[st] || st;
  }

  function askChange(status: string) {
    setConfirmData({ status, label: statusLabel(status) });
  }

  async function confirmChange() {
    if (!confirmData) return;
    const status = confirmData.status;
    setUpdating(status);
    try {
      const updated = await updateOrderStatus(order.id, status);
      onUpdated(updated);
    } catch (err: any) {
      alert(err?.response?.data?.detail || `Não foi possível atualizar para '${status}'.`);
    } finally {
      setUpdating(null);
      setConfirmData(null);
    }
  }
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4" onClick={onClose}>
      <div className="w-full max-w-4xl max-h-[90vh] overflow-y-auto rounded-2xl border bg-white p-6 shadow-xl" onClick={(e) => e.stopPropagation()}>
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-slate-800">
            Detalhes do Pedido #{order.numero_pedido}
          </h2>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-slate-600 text-3xl leading-none"
          >
            ×
          </button>
        </div>

        {/* Ações rápidas de status */}
        <div className="mb-6 flex flex-wrap gap-2">
          {(() => {
            const terminal = ['entregue','cancelado','devolvido'];
            const isTerminal = terminal.includes((order.status || '').toLowerCase());
            const disabledFor = (target: string) => updating !== null || isTerminal || !!confirmData || (order.status || '').toLowerCase() === target;

            return (
              <>
                <button
                  onClick={() => askChange('confirmado')}
                  disabled={disabledFor('confirmado')}
                  className={`px-3 py-1.5 text-sm rounded text-white ${disabledFor('confirmado') ? 'bg-slate-400 cursor-not-allowed opacity-60' : 'bg-blue-600 hover:bg-blue-700'}`}
                >
                  {updating === 'confirmado' ? 'Confirmando...' : 'Confirmar'}
                </button>

                <button
                  onClick={() => askChange('processando')}
                  disabled={disabledFor('processando')}
                  className={`px-3 py-1.5 text-sm rounded text-white ${disabledFor('processando') ? 'bg-slate-400 cursor-not-allowed opacity-60' : 'bg-yellow-600 hover:bg-yellow-700'}`}
                >
                  {updating === 'processando' ? 'Atualizando...' : 'Processando'}
                </button>

                <button
                  onClick={() => askChange('enviado')}
                  disabled={disabledFor('enviado')}
                  className={`px-3 py-1.5 text-sm rounded text-white ${disabledFor('enviado') ? 'bg-slate-400 cursor-not-allowed opacity-60' : 'bg-indigo-600 hover:bg-indigo-700'}`}
                >
                  {updating === 'enviado' ? 'Enviando...' : 'Enviar'}
                </button>

                <button
                  onClick={() => askChange('entregue')}
                  disabled={disabledFor('entregue')}
                  className={`px-3 py-1.5 text-sm rounded text-white ${disabledFor('entregue') ? 'bg-slate-400 cursor-not-allowed opacity-60' : 'bg-green-600 hover:bg-green-700'}`}
                >
                  {updating === 'entregue' ? 'Concluindo...' : 'Concluir (Entregue)'}
                </button>

                <button
                  onClick={() => askChange('cancelado')}
                  disabled={disabledFor('cancelado')}
                  className={`px-3 py-1.5 text-sm rounded text-white ${disabledFor('cancelado') ? 'bg-slate-400 cursor-not-allowed opacity-60' : 'bg-rose-600 hover:bg-rose-700'}`}
                >
                  {updating === 'cancelado' ? 'Cancelando...' : 'Cancelar'}
                </button>

                <button
                  onClick={() => askChange('devolvido')}
                  disabled={disabledFor('devolvido')}
                  className={`px-3 py-1.5 text-sm rounded text-white ${disabledFor('devolvido') ? 'bg-slate-400 cursor-not-allowed opacity-60' : 'bg-slate-600 hover:bg-slate-700'}`}
                >
                  {updating === 'devolvido' ? 'Devolvendo...' : 'Devolver'}
                </button>
              </>
            );
          })()}
        </div>

        {/* Modal de confirmação estilizado */}
        {confirmData && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
            <div className="w-full max-w-md bg-white rounded-xl shadow-xl border">
              <div className="px-5 py-4 border-b">
                <h4 className="text-lg font-semibold text-slate-800">Confirmar ação</h4>
              </div>
              <div className="px-5 py-4">
                <p className="text-slate-700">Deseja confirmar a ação: <span className="font-medium">{confirmData.label}</span>?</p>
              </div>
              <div className="px-5 py-3 border-t flex justify-end gap-2">
                <button
                  className="px-4 py-2 rounded-lg border hover:bg-slate-50"
                  onClick={() => setConfirmData(null)}
                  disabled={!!updating}
                >
                  Cancelar
                </button>
                <button
                  className={`px-4 py-2 rounded-lg text-white ${updating ? 'bg-slate-400 cursor-not-allowed' : 'bg-indigo-600 hover:bg-indigo-700'}`}
                  onClick={confirmChange}
                  disabled={!!updating}
                >
                  {updating ? 'Aplicando...' : 'Confirmar'}
                </button>
              </div>
            </div>
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Informações do Cliente */}
          <div className="border rounded-lg p-4 bg-slate-50">
            <h3 className="font-semibold text-slate-700 mb-3 flex items-center gap-2">
              <span className="text-lg">👤</span> Cliente
            </h3>
            <div className="space-y-2 text-sm">
              {order.usuario_info ? (
                <>
                  <div>
                    <span className="text-slate-500">Nome:</span>
                    <span className="ml-2 font-medium">{order.usuario_info.nome}</span>
                  </div>
                  <div>
                    <span className="text-slate-500">Email:</span>
                    <span className="ml-2 font-medium">{order.usuario_info.email}</span>
                  </div>
                  {order.usuario_info.telefone && (
                    <div>
                      <span className="text-slate-500">Telefone:</span>
                      <span className="ml-2 font-medium">{order.usuario_info.telefone}</span>
                    </div>
                  )}
                </>
              ) : (
                <div>
                  <span className="text-slate-500">ID do Usuário:</span>
                  <span className="ml-2 font-medium">{order.usuario_id}</span>
                </div>
              )}
              <div>
                <span className="text-slate-500">Data do Pedido:</span>
                <span className="ml-2 font-medium">
                  {new Date(order.data_criacao).toLocaleString('pt-BR')}
                </span>
              </div>
            </div>
          </div>

          {/* Endereço de Entrega */}
          <div className="border rounded-lg p-4 bg-slate-50">
            <h3 className="font-semibold text-slate-700 mb-3 flex items-center gap-2">
              <span className="text-lg">📍</span> Endereço de Entrega
            </h3>
            <div className="space-y-2 text-sm">
              {order.endereco_entrega ? (
                <>
                  <div>
                    <span className="text-slate-500">Rua:</span>
                    <span className="ml-2">{order.endereco_entrega.rua || '-'}, {order.endereco_entrega.numero || '-'}</span>
                  </div>
                  {order.endereco_entrega.complemento && (
                    <div>
                      <span className="text-slate-500">Complemento:</span>
                      <span className="ml-2">{order.endereco_entrega.complemento}</span>
                    </div>
                  )}
                  <div>
                    <span className="text-slate-500">Bairro:</span>
                    <span className="ml-2">{order.endereco_entrega.bairro || '-'}</span>
                  </div>
                  <div>
                    <span className="text-slate-500">Cidade/UF:</span>
                    <span className="ml-2">
                      {order.endereco_entrega.cidade || '-'} / {order.endereco_entrega.estado || '-'}
                    </span>
                  </div>
                  <div>
                    <span className="text-slate-500">CEP:</span>
                    <span className="ml-2">{order.endereco_entrega.cep || '-'}</span>
                  </div>
                </>
              ) : (
                <p className="text-slate-400 text-xs">Endereço ID: {order.endereco_entrega_id}</p>
              )}
            </div>
          </div>

          {/* Informações de Pagamento */}
          <div className="border rounded-lg p-4 bg-slate-50">
            <h3 className="font-semibold text-slate-700 mb-3 flex items-center gap-2">
              <span className="text-lg">💳</span> Pagamento
            </h3>
            <div className="space-y-2 text-sm">
              {order.pagamento_info ? (
                <>
                  <div>
                    <span className="text-slate-500">Método:</span>
                    <span className="ml-2 font-medium capitalize">
                      {order.pagamento_info.metodo_pagamento === 'card' ? 'Cartão de Crédito' :
                       order.pagamento_info.metodo_pagamento === 'pix' ? 'PIX' :
                       order.pagamento_info.metodo_pagamento === 'boleto' ? 'Boleto' :
                       order.pagamento_info.metodo_pagamento || '-'}
                    </span>
                  </div>
                  <div>
                    <span className="text-slate-500">Status:</span>
                    <span className="ml-2 capitalize">
                      {order.pagamento_info.status || '-'}
                    </span>
                  </div>
                </>
              ) : (
                <p className="text-slate-400 text-xs">Informações de pagamento não disponíveis</p>
              )}
            </div>
          </div>

          {/* Informações de Frete */}
          <div className="border rounded-lg p-4 bg-slate-50">
            <h3 className="font-semibold text-slate-700 mb-3 flex items-center gap-2">
              <span className="text-lg">📦</span> Frete
            </h3>
            <div className="space-y-2 text-sm">
              <div>
                <span className="text-slate-500">Valor do Frete:</span>
                <span className="ml-2 font-medium">R$ {order.valor_frete.toFixed(2)}</span>
              </div>
              {order.data_entrega_prevista && (
                <div>
                  <span className="text-slate-500">Previsão de Entrega:</span>
                  <span className="ml-2">
                    {new Date(order.data_entrega_prevista).toLocaleDateString('pt-BR')}
                  </span>
                </div>
              )}
              {order.data_entrega_realizada && (
                <div>
                  <span className="text-slate-500">Entregue em:</span>
                  <span className="ml-2 font-medium text-green-600">
                    {new Date(order.data_entrega_realizada).toLocaleDateString('pt-BR')}
                  </span>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Itens do Pedido */}
        <div className="mt-6 border rounded-lg p-4">
          <h3 className="font-semibold text-slate-700 mb-3 flex items-center gap-2">
            <span className="text-lg">📚</span> Itens do Pedido
          </h3>
          <div className="space-y-2">
            {order.items && order.items.length > 0 ? (
              order.items.map((item, idx) => (
                <div key={idx} className="flex justify-between items-center py-3 border-b last:border-0">
                  <div className="flex-1">
                    <div className="text-sm font-medium">Livro ID: {item.livro_id}</div>
                    <div className="text-xs text-slate-500">
                      Quantidade: {item.quantidade} × R$ {item.preco_unitario.toFixed(2)}
                    </div>
                  </div>
                  <div className="font-semibold text-indigo-600">
                    R$ {item.subtotal.toFixed(2)}
                  </div>
                </div>
              ))
            ) : (
              <p className="text-slate-400 text-sm">Nenhum item disponível</p>
            )}
          </div>

          <div className="mt-4 pt-4 border-t-2 border-slate-200">
            <div className="flex justify-between text-sm mb-2">
              <span className="text-slate-600">Subtotal:</span>
              <span className="font-medium">R$ {(order.valor_total - order.valor_frete).toFixed(2)}</span>
            </div>
            <div className="flex justify-between text-sm mb-3">
              <span className="text-slate-600">Frete:</span>
              <span className="font-medium">R$ {order.valor_frete.toFixed(2)}</span>
            </div>
            <div className="flex justify-between text-xl font-bold text-indigo-600">
              <span>Total:</span>
              <span>R$ {order.valor_total.toFixed(2)}</span>
            </div>
          </div>
        </div>

        {order.observacoes && (
          <div className="mt-4 border rounded-lg p-4 bg-amber-50 border-amber-200">
            <h3 className="font-semibold text-slate-700 mb-2 flex items-center gap-2">
              <span className="text-lg">📝</span> Observações
            </h3>
            <p className="text-sm text-slate-600">{order.observacoes}</p>
          </div>
        )}

        <div className="mt-6 flex justify-end gap-3">
          <button
            onClick={onClose}
            className="px-6 py-2 bg-slate-200 hover:bg-slate-300 rounded-lg font-medium transition-colors"
          >
            Fechar
          </button>
        </div>
      </div>
    </div>
  );
}
