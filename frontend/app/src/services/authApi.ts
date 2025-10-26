import axios from "axios";

const RAW_AUTH_URL = import.meta.env.VITE_AUTH_SERVICE_URL || "http://localhost:8001";
const BASE_AUTH_URL = RAW_AUTH_URL.endsWith("/api/v1")
  ? RAW_AUTH_URL
  : `${RAW_AUTH_URL.replace(/\/+$/, "")}/api/v1`;

export const authApi = axios.create({
  baseURL: BASE_AUTH_URL,
  withCredentials: false,
});

// Adiciona token nas requisições autenticadas
authApi.interceptors.request.use((config) => {
  const token = localStorage.getItem("mp_token");
  if (token) config.headers = { ...(config.headers || {}), Authorization: `Bearer ${token}` } as any;
  return config;
});

export type LoginInput = {
  email: string;
  password: string;
};

export type LoginResponse = {
  user_id: number;
  email: string;
  nome: string;
  tipo: string;
  ativo: boolean;
  access_token: string;
  refresh_token: string;
  token_type: "bearer";
};

export async function login(data: LoginInput): Promise<LoginResponse> {
  const res = await authApi.post<LoginResponse>("/login", data);
  return res.data;
}

export type RegisterInput = {
  name: string;
  email: string;
  password: string;
  password_confirmation: string;
};
export type RegisterResponse = LoginResponse;

export async function register(data: RegisterInput): Promise<RegisterResponse> {
  const res = await authApi.post<RegisterResponse>("/register", data);
  return res.data;
}

export async function refresh(): Promise<{ access_token: string }> {
  const res = await authApi.post<{ access_token: string }>("/refresh");
  return res.data;
}

export type UpdateMeInput = {
  telefone?: string | null;
  email?: string | null;
  nome?: string | null;
};

export async function getMe() {
  const res = await authApi.get("/me");
  return res.data as {
    user_id: number;
    email: string;
    nome: string;
    tipo: string;
    ativo: boolean;
    telefone?: string | null;
  };
}

export async function updateMe(data: UpdateMeInput) {
  const res = await authApi.put("/users/me", data);
  return res.data as {
    user_id: number;
    email: string;
    nome: string;
    tipo: string;
    ativo: boolean;
    telefone?: string | null;
  };
}

export async function changePassword(payload: {
  current_password: string;
  new_password: string;
  new_password_confirmation: string;
}) {
  const res = await authApi.post("/users/me/change-password", payload);
  return res.data as { status: string };
}
