import { CATALOG } from "../mocks/catalog";
import { useFavorites } from "../context/FavoritesContext";
import BookCard from "../components/book/BookCard";
import type { Book } from "../types/book";

export default function Favorites() {
  const { ids } = useFavorites();
  const favBooks: Book[] = CATALOG.filter((b) => ids.includes(b.id));

  return (
    <div className="max-w-6xl mx-auto p-6">
      <h1 className="text-2xl font-bold text-indigo-900 mb-4">
        Seus favoritos
      </h1>

      {favBooks.length === 0 ? (
        <p className="text-slate-600">Você ainda não favoritou livros.</p>
      ) : (
        <div className="grid sm:grid-cols-2 md:grid-cols-3 gap-6">
          {favBooks.map((b) => (
            <BookCard key={b.id} b={b} />
          ))}
        </div>
      )}
    </div>
  );
}
