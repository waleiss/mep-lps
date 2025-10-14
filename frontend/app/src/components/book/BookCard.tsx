import type { Book } from "../../types/book";
import { RatingStars } from "./RatingStars";
import { IconButton } from "../ui/IconButton";
import { useFavorites } from "../../context/FavoritesContext";
import { useCart } from "../../context/CartContext";
import { Link } from "react-router-dom";

const money = (v: number) =>
  v.toLocaleString(undefined, { style: "currency", currency: "BRL" });

export default function BookCard({ b }: { b: Book }) {
  const { toggle, ids } = useFavorites();
  const { add } = useCart();

  return (
    <article className="group rounded-2xl border border-slate-200 bg-white p-3 hover:shadow-md transition grid">
      <Link to={`/book/${b.id}`}>
        <img
          src={b.cover}
          alt={b.title}
          className="h-44 w-full object-cover rounded-lg"
        />
      </Link>
      <div className="mt-3">
        <h3 className="font-semibold leading-tight group-hover:text-indigo-700">
          {b.title}
        </h3>
        <p className="text-sm text-slate-500">de {b.author}</p>
      </div>
      <div className="mt-2">
        <RatingStars rating={b.rating} />
      </div>
      <div className="mt-3 flex items-center justify-between">
        <span className="font-semibold">{money(b.price)}</span>
        <div className="flex items-center gap-2">
          <IconButton title="Favoritar" onClick={() => toggle(b.id)}>
            <span className={ids.includes(b.id) ? "opacity-100" : "opacity-40"}>
              ♥
            </span>
          </IconButton>
          <button
            onClick={() => add(b)}
            className="rounded-full bg-indigo-600 text-white text-sm px-3 py-1.5 hover:bg-indigo-700"
          >
            Adicionar
          </button>
        </div>
      </div>
    </article>
  );
}
