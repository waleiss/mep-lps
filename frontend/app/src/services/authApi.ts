import axios from "axios";

export const authApi = axios.create({
  baseURL: import.meta.env.VITE_AUTH_SERVICE_URL || "http://localhost:8001", 
  withCredentials: false, 
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
