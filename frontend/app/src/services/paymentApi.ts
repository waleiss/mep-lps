// API de pagamentos (Payment Service)

import axios from "axios";
import type {
  CardPaymentRequest,
  PixPaymentRequest,
  BoletoPaymentRequest,
  PaymentResponse,
} from "../types/payment";

// Cria instância do axios para o serviço de pagamento
export const paymentApi = axios.create({
  baseURL: import.meta.env.VITE_PAYMENT_SERVICE_URL || "http://localhost:8005/api/v1",
});

// Adiciona token de autenticação nas requisições
paymentApi.interceptors.request.use((config) => {
  const token = localStorage.getItem("mp_token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

/**
 * Processa pagamento com cartão
 */
export async function processarPagamentoCartao(
  data: CardPaymentRequest
): Promise<PaymentResponse> {
  const response = await paymentApi.post<PaymentResponse>(
    "/pagamento/processar/cartao",
    data
  );
  return response.data;
}

/**
 * Processa pagamento via PIX
 */
export async function processarPagamentoPix(
  data: PixPaymentRequest
): Promise<PaymentResponse> {
  const response = await paymentApi.post<PaymentResponse>(
    "/pagamento/processar/pix",
    data
  );
  return response.data;
}

/**
 * Processa pagamento via Boleto
 */
export async function processarPagamentoBoleto(
  data: BoletoPaymentRequest
): Promise<PaymentResponse> {
  const response = await paymentApi.post<PaymentResponse>(
    "/pagamento/processar/boleto",
    data
  );
  return response.data;
}

/**
 * Consulta status de um pagamento
 */
export async function consultarStatusPagamento(
  pagamentoId: number
): Promise<PaymentResponse> {
  const response = await paymentApi.get<PaymentResponse>(`/pagamento/${pagamentoId}`);
  return response.data;
}

/**
 * Confirma pagamento PIX (após pagamento ser realizado)
 */
export async function confirmarPagamentoPix(
  pagamentoId: number
): Promise<PaymentResponse> {
  const response = await paymentApi.post<PaymentResponse>(
    `/pagamento/${pagamentoId}/confirmar-pix`
  );
  return response.data;
}

