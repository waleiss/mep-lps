import { Link, useNavigate } from "react-router-dom";
import { useCart } from "../../context/CartContext";

const money = (v: number) =>
  v.toLocaleString(undefined, { style: "currency", currency: "BRL" });

export default function CartBar() {
  const nav = useNavigate();
  const { items, total, clear } = useCart();
  if (!items.length) return null;

  const goCheckout = () => nav("/checkout");

  return (
    <section className="sticky bottom-4 z-10">
      <div className="max-w-6xl mx-auto px-4">
        <div className="rounded-2xl border bg-white/95 backdrop-blur p-4 shadow-md flex items-center justify-between">
          <div className="text-sm text-slate-600">
            <strong>{items.reduce((a, c) => a + c.qty, 0)} item(s)</strong> —
            Subtotal {money(total)}
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={clear}
              className="rounded-full border border-slate-200 bg-white px-4 py-2"
            >
              Limpar
            </button>

            <Link
              to="/checkout"
              className="rounded-full bg-emerald-600 text-white px-4 py-2 hover:bg-emerald-700"
            >
              Finalizar compra
            </Link>

            {/* Opção 2: botão com navigate
            <button
              onClick={goCheckout}
              className="rounded-full bg-emerald-600 text-white px-4 py-2 hover:bg-emerald-700"
            >
              Finalizar compra
            </button>
            */}
          </div>
        </div>
      </div>
    </section>
  );
}
