import axios from "axios";
import { CATALOG } from "../mocks/catalog";
import type { Book } from "../types/book";

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL, // seu API Gateway, se houver
});

export async function listBooks(): Promise<Book[]> {
// troque por fetch real quando tiver backend
await new Promise((r) => setTimeout(r, 200));
return CATALOG;
}


export async function getBook(id: string): Promise<Book | undefined> {
await new Promise((r) => setTimeout(r, 150));
return CATALOG.find((b) => b.id === id);
}

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("mp_token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});
