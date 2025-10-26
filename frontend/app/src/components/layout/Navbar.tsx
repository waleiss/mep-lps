// src/components/layout/Navbar.tsx
import { Link } from "react-router-dom";
import { IconButton } from "../ui/IconButton";
import { useCart } from "../../context/CartContext";
import { useAuth } from "../../context/AuthContext";
import logo from "../../assets/logo.svg";
import { useEffect, useRef, useState } from "react";

export default function Navbar() {
  const { count } = useCart();
  const { user, logout } = useAuth();

  // estado e timeout para controlar abertura com atraso
  const [open, setOpen] = useState(false);
  const timeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const handleMouseEnter = () => {
    if (timeoutRef.current) clearTimeout(timeoutRef.current);
    setOpen(true);
  };

  const handleMouseLeave = () => {
    // fecha após 2 segundos
    timeoutRef.current = setTimeout(() => setOpen(false), 180);
  };

  // limpa timeout ao desmontar
  useEffect(() => {
    return () => {
      if (timeoutRef.current) clearTimeout(timeoutRef.current);
    };
  }, []);

  return (
    <nav className="sticky top-0 z-20 backdrop-blur bg-white/70 border-b border-slate-200">
      <div className="max-w-6xl mx-auto px-4 py-3 flex items-center gap-4">
        {/* Logo */}
        <Link
          to="/"
          className="flex items-center gap-2 font-bold text-lg text-indigo-900 hover:text-indigo-700 transition"
        >
          <img
            src={logo}
            alt="Logo Mundo em Palavras"
            className="w-7 h-7 object-contain"
          />
          <span>Mundo&nbsp;em&nbsp;Palavras</span>
        </Link>

        <div className="flex-1" />

        {/* Favoritos */}
        <Link to="/favorites" aria-label="Favoritos">
          <IconButton title="Favoritos">
            <span>♥</span>
          </IconButton>
        </Link>

        {/* Carrinho */}
        <Link
          to="/checkout"
          className="rounded-full border border-slate-200 px-3 py-1.5 hover:bg-indigo-50 transition text-slate-700"
        >
          🛒 Carrinho ({count})
        </Link>

        {/* Conta */}
        {user ? (
          <div
            className="relative"
            onMouseEnter={handleMouseEnter}
            onMouseLeave={handleMouseLeave}
          >
            <button className="text-sm text-slate-700 hover:text-indigo-700 transition flex items-center gap-1">
              👤 {user.name.split(" ")[0]}
            </button>

            {/* Dropdown controlado por estado (com fade) */}
            <div
              className={`absolute right-0 top-full mt-2 w-56 bg-white border border-slate-200 rounded-xl shadow-lg py-2 transition-opacity duration-200 ${
                open
                  ? "opacity-100 pointer-events-auto"
                  : "opacity-0 pointer-events-none"
              }`}
            >
              <Link
                to="/account"
                className="block px-5 py-3 text-sm text-slate-700 hover:bg-indigo-50"
              >
                Meus pedidos
              </Link>
              <Link
                to="/account/profile"
                className="block px-5 py-3 text-sm text-slate-700 hover:bg-indigo-50"
              >
                Dados da conta
              </Link>
              <hr className="my-2 border-slate-200" />
              <button
                onClick={logout}
                className="w-full text-left px-5 py-3 text-sm text-red-600 hover:bg-red-50"
              >
                Sair
              </button>
            </div>
          </div>
        ) : (
          <Link
            to="/login"
            className="rounded-full border border-indigo-600 text-indigo-700 font-medium px-4 py-1.5 hover:bg-indigo-50 transition"
          >
            Entrar ou criar conta
          </Link>
        )}
      </div>
    </nav>
  );
}
