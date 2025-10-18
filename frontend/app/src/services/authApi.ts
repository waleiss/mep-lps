// src/services/authApi.ts
import axios from "axios";

const baseURL = import.meta.env.VITE_AUTH_SERVICE_URL;

export const authApi = axios.create({
  baseURL,
  withCredentials: false,
});


export type LoginInput = { email: string; password: string };
export type RegisterInput = { name: string; email: string; password: string,  password_confirmation: string; };
export type AuthUser = { id: string; name: string; email: string };
export type AuthResponse = {
  access_token: string; 
  refresh_token?: string;
  user: AuthUser;
  
};

export async function login(data: LoginInput): Promise<AuthResponse> {
  const res = await authApi.post<AuthResponse>("/login", data);
  return res.data;
}

export async function register(data: RegisterInput): Promise<AuthResponse> {
  const res = await authApi.post<AuthResponse>("/register", data);
  return res.data;
}

export async function refresh(): Promise<{ access_token: string }> {
  const res = await authApi.post<{ access_token: string }>("/auth/refresh");
  return res.data;
}
