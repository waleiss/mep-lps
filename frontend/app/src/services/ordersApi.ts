// API de pedidos (Order Service)

import axios from "axios";

// Cria instância do axios para o serviço de pedidos
export const ordersApi = axios.create({
  baseURL: import.meta.env.VITE_ORDER_SERVICE_URL || "http://localhost:8006/api/v1",
});

// Adiciona token em todas as requisições
ordersApi.interceptors.request.use((config) => {
  const token = localStorage.getItem("mp_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export type OrderStatus = "pending" | "processing" | "shipped" | "delivered" | "cancelled";

export interface OrderItem {
  livro_id: number;
  quantidade: number;
  preco_unitario: number;
  subtotal: number;
}

export interface Order {
  id: number;
  usuario_id: number;
  endereco_entrega_id: number;
  numero_pedido: string;
  status: OrderStatus | string;
  valor_total: number;
  valor_frete: number;
  observacoes?: string;
  data_criacao: string;
  data_atualizacao: string;
  data_entrega_prevista?: string;
  data_entrega_realizada?: string;
  items?: OrderItem[];
  endereco_entrega?: any; // Detalhes do endereço (dict)
  pagamento_info?: any; // Info do pagamento (dict)
}

/**
 * Busca todos os pedidos do usuário logado
 */
export async function getOrders(usuario_id?: number): Promise<Order[]> {
  try {
    const params = usuario_id ? { usuario_id } : {};
    const response = await ordersApi.get('/pedidos', { params });
    
    // Pode retornar tanto 'pedidos' quanto 'items' dependendo da resposta
    return response.data.pedidos || response.data.items || [];
  } catch (error) {
    console.error("Erro ao buscar pedidos:", error);
    return [];
  }
}

/**
 * Busca um pedido específico por ID
 */
export async function getOrder(id: number): Promise<Order | null> {
  try {
    const response = await ordersApi.get(`/pedidos/${id}`);
    return response.data;
  } catch (error) {
    console.error(`Erro ao buscar pedido ${id}:`, error);
    return null;
  }
}

/**
 * Cria um novo pedido
 */
export async function createOrder(data: {
  usuario_id: number;
  endereco_entrega_id: number;
  valor_frete: number;
  items: Array<{ livro_id: number; quantidade: number; preco_unitario: number }>;
  observacoes?: string;
}): Promise<Order | null> {
  try {
    const response = await ordersApi.post('/pedidos', data);
    return response.data;
  } catch (error) {
    console.error("Erro ao criar pedido:", error);
    throw error;
  }
}

/**
 * Cancela um pedido (atualiza status para "cancelado")
 */
export async function cancelOrder(orderId: number): Promise<Order> {
  try {
    const response = await ordersApi.patch(`/pedidos/${orderId}/status`, {
      status: 'cancelado'
    });
    return response.data;
  } catch (error) {
    console.error(`Erro ao cancelar pedido ${orderId}:`, error);
    throw error;
  }
}

