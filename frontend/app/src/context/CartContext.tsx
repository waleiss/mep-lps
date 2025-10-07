import React, { createContext, useContext, useMemo, useState } from "react";
import type { CartItem, Book } from "../types/book";
import { useLocalStorage } from "../hooks/useLocalStorage";

interface CartCtx {
  items: CartItem[];
  add: (b: Book) => void;
  remove: (id: string) => void;
  clear: () => void;
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
  const clear = () => setItems([]);

  const total = useMemo(
    () => items.reduce((a, c) => a + c.book.price * c.qty, 0),
    [items]
  );
  const count = useMemo(() => items.reduce((a, c) => a + c.qty, 0), [items]);

  return (
    <Ctx.Provider value={{ items, add, remove, clear, total, count }}>
      {children}
    </Ctx.Provider>
  );
};

export const useCart = () => {
  const ctx = useContext(Ctx);
  if (!ctx) throw new Error("useCart must be used inside CartProvider");
  return ctx;
};
