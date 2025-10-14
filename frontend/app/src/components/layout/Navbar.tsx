import { Link } from "react-router-dom";
import { IconButton } from "../ui/IconButton";
import { useCart } from "../../context/CartContext";
import logo from "../../assets/logo.svg";

export default function Navbar() {
  const { count } = useCart();

  return (
    <nav className="sticky top-0 z-20 backdrop-blur bg-white/70 border-b border-slate-200">
      <div className="max-w-6xl mx-auto px-4 py-3 flex items-center gap-4">
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

        <IconButton title="Favoritos">
          <span>♥</span>
        </IconButton>

        <Link
          to="/checkout"
          className="rounded-full border border-slate-200 px-3 py-1.5 hover:bg-indigo-50 transition"
        >
          🛒 Carrinho ({count})
        </Link>

        <a
          className="text-sm text-slate-600 hover:text-indigo-700 transition"
          href="#"
        >
          Conta
        </a>
      </div>
    </nav>
  );
}
