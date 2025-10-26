import { useEffect, useMemo, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { listBooks, getBook, getPublicSettings } from "../services/api";
import type { Book } from "../types/book";
import { useCart } from "../context/CartContext";
import { useFavorites } from "../context/FavoritesContext";
import BookCard from "../components/book/BookCard";

const money = (v: number) =>
  v.toLocaleString(undefined, { style: "currency", currency: "BRL" });

export default function BookDetails() {
  const { id } = useParams<{ id: string }>();
  const [books, setBooks] = useState<Book[]>([]);
  // null => não configurado (mostrar todas). [] => ocultar todas
  const [enabledCategories, setEnabledCategories] = useState<string[] | null>(null);
  const [book, setBook] = useState<Book | undefined>(undefined);
  const { add } = useCart();
  const { ids: favIds, toggle } = useFavorites();

  // Load public settings and the current book
  useEffect(() => {
    getPublicSettings()
      .then((s) => setEnabledCategories(s.enabledCategories ?? null))
      .catch(() => setEnabledCategories(null));
  }, []);

  useEffect(() => {
    if (!id) return;
    getBook(id).then(setBook);
    // Also fetch a list for recommendations
    listBooks().then(setBooks);
  }, [id]);

  // Apply public category visibility rules
  const allowed = useMemo(() => {
    if (!book) return false;
    if (enabledCategories === null) return true; // not configured => show
    const enabledLower = enabledCategories.map((c) => c.toLowerCase());
    const cat = (book.category || "").toLowerCase();
    return enabledLower.includes(cat);
  }, [book, enabledCategories]);

  const recommended = useMemo(() => {
    const enabledLower = (enabledCategories ?? []).map((c) => c.toLowerCase());
    const visible = enabledCategories === null
      ? books
      : books.filter((b) => b.category && enabledLower.includes(b.category.toLowerCase()));
    return visible.filter((b) => b.id !== book?.id).slice(0, 4);
  }, [books, book?.id, enabledCategories]);

  // Helpers to render category label and memoized text must be declared before any early returns
  function humanizeCategory(cat?: string): string {
    if (!cat) return "";
    const map: Record<string, string> = {
      FICCAO: "Ficção",
      NAO_FICCAO: "Não ficção",
      TECNICO: "Técnico",
      ACADEMICO: "Acadêmico",
      INFANTIL: "Infantil",
      OUTROS: "Outros",
      // Possíveis formatos do backend
      ficcao: "Ficção",
      nao_ficcao: "Não ficção",
      tecnico: "Técnico",
      academico: "Acadêmico",
      infantil: "Infantil",
      outros: "Outros",
    };
    const direct = map[cat as keyof typeof map] || map[cat.toUpperCase()] || map[cat.toLowerCase()];
    if (direct) return direct;
    // Fallback: "NAO_FICCAO" -> "Nao Ficcao"
    return cat
      .replace(/[_-]+/g, " ")
      .toLowerCase()
      .replace(/(^|\s)\p{L}/gu, (m) => m.toUpperCase());
  }

  const categoriesText = useMemo(() => {
    if (!book) return "—";
    // Se vier um array (futuro), exibe lista
    const list = (book as any)?.categories as string[] | undefined;
    if (Array.isArray(list) && list.length) {
      return list.map((c) => humanizeCategory(c)).join(" · ");
    }
    // Caso contrário, usa o campo único
    const single = humanizeCategory(book.category);
    return single || "—";
  }, [book]);

  if (!book || !allowed) {
    return (
      <div className="max-w-5xl mx-auto p-6">
        <h1 className="text-xl font-semibold">Livro não encontrado</h1>
        <p className="text-slate-600 mt-1">
          Verifique o link ou volte para a página inicial.
        </p>
        <Link to="/" className="text-indigo-700 underline mt-4 inline-block">
          Voltar
        </Link>
      </div>
    );
  }

  const isFav = favIds.includes(book.id);

  

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      {/* Detalhes */}
      <div className="grid md:grid-cols-2 gap-8">
        <img
          src={book.cover}
          alt={book.title}
          className="w-full rounded-2xl shadow"
        />

        <div>
          <h1 className="text-3xl font-extrabold text-indigo-900">
            {book.title}
          </h1>
          <p className="text-slate-600 mt-1">por {book.author}</p>

          <div className="mt-3 text-2xl font-semibold">{money(book.price)}</div>

          <p className="mt-4 text-slate-700 leading-relaxed">
            {book.description || "Descrição breve do livro."}
          </p>

          <div className="mt-6 text-sm text-slate-500">
            Categorias: {categoriesText}
          </div>

          <div className="mt-6 flex flex-wrap items-center gap-3">
            <button
              onClick={() => add(book)}
              className="rounded-full bg-indigo-700 text-white px-5 py-2 hover:bg-indigo-800"
            >
              Adicionar ao carrinho
            </button>

            <button
              onClick={() => toggle(book.id)}
              className={`rounded-full border px-4 py-2 ${
                isFav
                  ? "border-red-300 text-red-600 bg-red-50"
                  : "border-slate-200 text-slate-700 hover:bg-indigo-50"
              }`}
              title={
                isFav ? "Remover dos favoritos" : "Adicionar aos favoritos"
              }
            >
              {isFav ? "♥ Nos favoritos" : "♡ Favoritar"}
            </button>

            <Link
              to="/"
              className="px-5 py-2 rounded-full border hover:bg-indigo-50"
            >
              Voltar
            </Link>
          </div>
        </div>
      </div>

      {/* Recomendados */}
      {recommended.length > 0 && (
        <section className="mt-12">
          <h2 className="text-xl font-bold text-indigo-900 mb-4">
            Recomendados para você
          </h2>
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-6">
            {recommended.map((b) => (
              <BookCard key={b.id} b={b} />
            ))}
          </div>
        </section>
      )}
    </div>
  );
}
