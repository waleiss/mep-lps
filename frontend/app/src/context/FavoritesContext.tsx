import React, { createContext, useContext } from "react";
import { useLocalStorage } from "../hooks/useLocalStorage";

interface FavCtx {
  ids: string[];
  toggle: (id: string) => void;
}
const Ctx = createContext<FavCtx | null>(null);

export const FavoritesProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [ids, setIds] = useLocalStorage<string[]>("fav:v1", []);
  const toggle = (id: string) =>
    setIds((prev) =>
      prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id]
    );
  return <Ctx.Provider value={{ ids, toggle }}>{children}</Ctx.Provider>;
};

export const useFavorites = () => {
  const ctx = useContext(Ctx);
  if (!ctx)
    throw new Error("useFavorites must be used inside FavoritesProvider");
  return ctx;
};
