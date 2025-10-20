// API de endereços (Shipping Service)

import axios from "axios";
import type { 
  Address, 
  AddressCreate, 
  AddressResponse, 
  AddressListResponse, 
  ViaCEPResponse 
} from "../types/address";

// Cria instância do axios para o serviço de shipping
export const shippingApi = axios.create({
  baseURL: import.meta.env.VITE_SHIPPING_SERVICE_URL || "http://localhost:8004/api/v1",
});

// Adiciona token de autenticação nas requisições
shippingApi.interceptors.request.use((config) => {
  const token = localStorage.getItem("mp_token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

/**
 * Consulta CEP via ViaCEP através do backend
 */
export async function consultarCEP(cep: string): Promise<ViaCEPResponse> {
  const cepLimpo = cep.replace(/\D/g, "");
  const response = await shippingApi.get<ViaCEPResponse>(`/viacep/${cepLimpo}`);
  return response.data;
}

/**
 * Cria um novo endereço
 */
export async function criarEndereco(data: AddressCreate): Promise<AddressResponse> {
  const response = await shippingApi.post<AddressResponse>("/enderecos", data);
  return response.data;
}

/**
 * Lista endereços de um usuário
 */
export async function listarEnderecos(usuarioId: number): Promise<AddressListResponse> {
  const response = await shippingApi.get<AddressListResponse>(
    `/enderecos/usuario/${usuarioId}`
  );
  return response.data;
}

/**
 * Obtém um endereço específico
 */
export async function obterEndereco(enderecoId: number): Promise<AddressResponse> {
  const response = await shippingApi.get<AddressResponse>(`/enderecos/${enderecoId}`);
  return response.data;
}

/**
 * Atualiza um endereço
 */
export async function atualizarEndereco(
  enderecoId: number,
  data: Partial<Address>
): Promise<AddressResponse> {
  const response = await shippingApi.put<AddressResponse>(
    `/enderecos/${enderecoId}`,
    data
  );
  return response.data;
}

/**
 * Remove (desativa) um endereço
 */
export async function removerEndereco(enderecoId: number): Promise<void> {
  await shippingApi.delete(`/enderecos/${enderecoId}`);
}

/**
 * Define um endereço como principal
 */
export async function definirEnderecoPrincipal(enderecoId: number): Promise<AddressResponse> {
  const response = await shippingApi.patch<AddressResponse>(
    `/enderecos/${enderecoId}/principal`
  );
  return response.data;
}

