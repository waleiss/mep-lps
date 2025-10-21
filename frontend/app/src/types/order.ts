import type { Book } from "./book";

export type CartItem = {
  book: Book;
  qty: number;
};

export type Order = {
  id: string;
  items: CartItem[];
  subtotal: number;
  shipping: number;
  total: number;
  status: "paid" | "processing" | "shipped" | "delivered" | "canceled";
  createdAt: string; 
};
