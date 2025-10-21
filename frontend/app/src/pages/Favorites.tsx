import { useEffect, useState } from "react";
import { useFavorites } from "../context/FavoritesContext";
import { getBook } from "../services/api";
import BookCard from "../components/book/BookCard";
import type { Book } from "../types/book";

export default function Favorites() {
  const { ids } = useFavorites();
  const [favBooks, setFavBooks] = useState<Book[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Buscar livros favoritos do backend
    const loadFavorites = async () => {
      setLoading(true);
      const books: Book[] = [];
      
      for (const id of ids) {
        try {
          const book = await getBook(id);
          if (book) books.push(book);
        } catch (error) {
          console.error(`Erro ao carregar livro ${id}:`, error);
        }
      }
      
      setFavBooks(books);
      setLoading(false);
    };

    loadFavorites();
  }, [ids]);

  if (loading) {
    return (
      <div className="max-w-6xl mx-auto p-6">
        <h1 className="text-2xl font-bold text-indigo-900 mb-4">
          Seus favoritos
        </h1>
        <p className="text-slate-600">Carregando...</p>
      </div>
    );
  }

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
