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

const CAT_LS_KEY = "publicEnabledCategories";

export default function Home() {
  const [books, setBooks] = useState<Book[]>([]);
  const [query, setQuery] = useState("");
  const [featuredIndex, setFeaturedIndex] = useState(0);
  const [enabledCategories, setEnabledCategories] = useState<string[]>([]);

  // Load enabled categories from localStorage
  useEffect(() => {
    const loadCategories = () => {
      try {
        const raw = localStorage.getItem(CAT_LS_KEY);
        if (raw) {
          const arr = JSON.parse(raw) as string[];
          setEnabledCategories(arr);
        } else {
          // If no config, show all categories
          setEnabledCategories([]);
        }
      } catch {
        setEnabledCategories([]);
      }
    };

    loadCategories();

    // Listen for storage changes (when admin updates settings)
    window.addEventListener('storage', loadCategories);
    
    // Custom event for same-window updates
    const handleCategoryChange = () => loadCategories();
    window.addEventListener('categoriesUpdated', handleCategoryChange);

    return () => {
      window.removeEventListener('storage', loadCategories);
      window.removeEventListener('categoriesUpdated', handleCategoryChange);
    };
  }, []);

  const filtered = useMemo(() => {
    let result = books;

    // Convert enabled categories to lowercase for comparison
    const enabledLower = enabledCategories.map(c => c.toLowerCase());
    
    // Filter by enabled categories
    result = result.filter((b) => {
      if (!b.category) return false;
      // Compare case-insensitive
      return enabledLower.includes(b.category.toLowerCase());
    });

    // Filter by search query
    const q = query.trim().toLowerCase();
    if (q) {
      result = result.filter((b) => 
        `${b.title} ${b.author}`.toLowerCase().includes(q)
      );
    }

    return result;
  }, [books, query, enabledCategories]);

  // Featured book from filtered list
  const featured = filtered.length
    ? filtered[featuredIndex % filtered.length]
    : undefined;

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
                onClick={() => setFeaturedIndex((i) => (i + 1) % filtered.length)}
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
        
        {filtered.length > 0 ? (
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-6">
            {filtered.map((b) => (
              <BookCard key={b.id} b={b} />
            ))}
          </div>
        ) : (
          <div className="flex flex-col items-center justify-center py-16 px-4">
            <div className="text-center max-w-md">
              <svg 
                className="mx-auto h-24 w-24 text-slate-300 mb-4" 
                fill="none" 
                viewBox="0 0 24 24" 
                stroke="currentColor"
              >
                <path 
                  strokeLinecap="round" 
                  strokeLinejoin="round" 
                  strokeWidth={1.5} 
                  d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" 
                />
              </svg>
              <h3 className="text-xl font-semibold text-slate-700 mb-2">
                Nenhum livro encontrado
              </h3>
              <p className="text-slate-500 mb-4">
                No momento, não há livros disponíveis para visualização.
              </p>
              <p className="text-sm text-slate-400">
                Entre em contato com o administrador para mais informações.
              </p>
            </div>
          </div>
        )}
      </section>

      <CartBar />
    </div>
  );
}
