import React from "react";
import Navbar from "./Navbar";
import { CartProvider } from "../../context/CartContext";
import { FavoritesProvider } from "../../context/FavoritesContext";

const TopBar = () => (
  <div className="w-full bg-indigo-900 text-white text-center text-xs tracking-wide py-2">
    Cada página, uma nova aventura ✨
  </div>
);

export const Layout: React.FC<React.PropsWithChildren> = ({ children }) => (
  <div className="min-h-screen bg-gradient-to-b from-indigo-50/40 to-white text-slate-800">
    <FavoritesProvider>
      <CartProvider>
        <TopBar />
        <Navbar />
        <main>{children}</main>
      </CartProvider>
    </FavoritesProvider>
  </div>
);
