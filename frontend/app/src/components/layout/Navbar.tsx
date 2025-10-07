import { Link } from "react-router-dom";
import { IconButton } from "../ui/IconButton";
import { useCart } from "../../context/CartContext";

export default function Navbar() {
  const { count } = useCart();
  return (
    <nav className="sticky top-0 z-20 backdrop-blur bg-white/70 border-b border-slate-200">
      <div className="max-w-6xl mx-auto px-4 py-3 flex items-center gap-4">
        <Link to="/" className="font-bold text-lg">
          📚 Livraria
        </Link>
        <div className="flex-1" />
        <IconButton title="Favoritos">
          <span>♥</span>
        </IconButton>
        <Link to="/checkout" className="rounded-full border px-3 py-1.5">
          🛒 Carrinho ({count})
        </Link>
        <a className="text-sm text-slate-600 hover:text-indigo-700" href="#">
          Conta
        </a>
      </div>
    </nav>
  );
}
