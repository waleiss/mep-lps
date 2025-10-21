import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { listBooks } from "../services/api";
import type { Book } from "../types/book";

import BookCard from "../components/book/BookCard";
import CartBar from "../components/cart/CartBar";
import { Badge } from "../components/ui/Badge";
import { RatingStars } from "../components/book/RatingStars";

const money = (v: number) =>
  v.toLocaleString(undefined, { style: "currency", currency: "BRL" });

export default function Home() {
  const [books, setBooks] = useState<Book[]>([]);
  const [query, setQuery] = useState("");
  const [featuredIndex, setFeaturedIndex] = useState(0);

  const featured = books.length
    ? books[featuredIndex % books.length]
    : undefined;

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    return q
      ? books.filter((b) => `${b.title} ${b.author}`.toLowerCase().includes(q))
      : books;
  }, [books, query]);

  useEffect(() => {
    listBooks().then(setBooks);
  }, []);

  return (
    <div>
      {/* Hero */}
      {featured && (
        <section className="max-w-6xl mx-auto px-4 pt-10 pb-6 grid md:grid-cols-2 items-center gap-8">
          <div>
            <Badge>Em destaque</Badge>
            <h1 className="mt-3 text-3xl md:text-4xl font-extrabold tracking-tight">
              {featured.tagline || featured.title}
            </h1>
            <p className="mt-3 text-slate-600 max-w-prose">
              {featured.description || "Descrição breve do livro."}
            </p>
            <div className="mt-3">
              <RatingStars rating={featured.rating} />
            </div>
            <div className="mt-4 flex items-center gap-3">
              <Link
                to={`/book/${featured.id}`} // <- Link do router
                className="rounded-full bg-indigo-600 text-white px-4 py-2"
              >
                Comprar — {money(featured.price)}
              </Link>
              <button
                onClick={() => setFeaturedIndex((i) => (i + 1) % books.length)}
                className="rounded-full border px-4 py-2 bg-white"
              >
                Próximo
              </button>
            </div>
          </div>
          <div className="relative">
            <div className="absolute -inset-6 bg-indigo-200/30 rounded-full blur-3xl" />
            <img
              src={featured.cover}
              alt={featured.title}
              className="relative z-10 w-72 md:w-80 mx-auto drop-shadow-xl rounded"
            />
          </div>
        </section>
      )}

      {/* Catálogo */}
      <section className="max-w-6xl mx-auto px-4 py-8">
        <div className="flex items-center justify-between mb-4">
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Buscar livros…"
            className="w-72 max-w-full rounded-full border border-slate-200 pl-4 pr-10 py-2"
          />
          <span className="text-sm text-slate-500">
            {filtered.length} resultados
          </span>
        </div>
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-6">
          {filtered.map((b) => (
            <BookCard key={b.id} b={b} />
          ))}
        </div>
      </section>

      <CartBar />
    </div>
  );
}
