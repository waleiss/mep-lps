// src/context/CartContext.tsx
import React, { createContext, useContext, useMemo } from "react";
import type { CartItem, Book } from "../types/book";
import { useLocalStorage } from "../hooks/useLocalStorage";

interface CartCtx {
  items: CartItem[];
  add: (b: Book) => void;
  remove: (id: string) => void; // remove tudo do item
  inc: (id: string) => void;    // +1
  dec: (id: string) => void;    // -1 (remove se chegar a 0)
  clear: () => void;
  subtotal: number;
  shipping: number;
  total: number;
  count: number;
}

const Ctx = createContext<CartCtx | null>(null);

export const CartProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [items, setItems] = useLocalStorage<CartItem[]>("cart:v1", []);

  const add = (book: Book) => {
    setItems((prev) => {
      const i = prev.findIndex((it) => it.book.id === book.id);
      if (i >= 0) {
        const cp = [...prev];
        cp[i] = { ...cp[i], qty: cp[i].qty + 1 };
        return cp;
      }
      return [...prev, { book, qty: 1 }];
    });
  };

  const remove = (id: string) =>
    setItems((prev) => prev.filter((it) => it.book.id !== id));

  const inc = (id: string) =>
    setItems((prev) => {
      const idx = prev.findIndex((it) => it.book.id === id);
      if (idx < 0) return prev;
      const cp = [...prev];
      cp[idx] = { ...cp[idx], qty: cp[idx].qty + 1 };
      return cp;
    });

  const dec = (id: string) =>
    setItems((prev) => {
      const idx = prev.findIndex((it) => it.book.id === id);
      if (idx < 0) return prev;
      const item = prev[idx];
      if (item.qty <= 1) {
        return prev.filter((it) => it.book.id !== id);
      }
      const cp = [...prev];
      cp[idx] = { ...cp[idx], qty: cp[idx].qty - 1 };
      return cp;
    });
  const clear = () => setItems([]);

  const subtotal = useMemo(
    () => items.reduce((acc, it) => acc + it.book.price * it.qty, 0),
    [items]
  );

  // regra mock de frete (ajuste como quiser)
  const shipping = useMemo(() => (items.length > 0 ? 19.9 : 0), [items]);

  const total = useMemo(() => subtotal + shipping, [subtotal, shipping]);

  const count = useMemo(
    () => items.reduce((acc, it) => acc + it.qty, 0),
    [items]
  );

  return (
    <Ctx.Provider
      value={{ items, add, remove, inc, dec, clear, subtotal, shipping, total, count }}
    >
      {children}
    </Ctx.Provider>
  );
};

export const useCart = () => {
  const ctx = useContext(Ctx);
  if (!ctx) throw new Error("useCart must be used inside CartProvider");
  return ctx;
};
