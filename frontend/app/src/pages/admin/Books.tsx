import React, { useMemo, useState } from "react";
import {
  type Livro,
  type Categoria,
  type Condicao,
  MOCK_LIVROS,
} from "../../mocks/info-admin";
import BookFormModal from "../../components/book/BookFormModal";

export default function Books() {
  const [data, setData] = useState<Livro[]>(() => MOCK_LIVROS);
  const [query, setQuery] = useState("");
  const [categoria, setCategoria] = useState<"" | Categoria>("");
  const [condicao, setCondicao] = useState<"" | Condicao>("");
  const [modalOpen, setModalOpen] = useState(false);
  const [editing, setEditing] = useState<Livro | null>(null);

  const filtered = useMemo(() => {
    let list = [...data];
    if (query.trim()) {
      const q = query.toLowerCase();
      list = list.filter(
        (l) =>
          l.titulo.toLowerCase().includes(q) ||
          l.autor.toLowerCase().includes(q) ||
          (l.isbn ?? "").toLowerCase().includes(q)
      );
    }
    if (categoria) list = list.filter((l) => l.categoria === categoria);
    if (condicao) list = list.filter((l) => l.condicao === condicao);
    return list;
  }, [data, query, categoria, condicao]);

  function onCreate() {
    setEditing(null);
    setModalOpen(true);
  }
  function onEdit(item: Livro) {
    setEditing(item);
    setModalOpen(true);
  }
  function onDelete(id: number) {
    setData((prev) => prev.filter((l) => l.id !== id));
  }
  function upsert(livro: Omit<Livro, "id"> & { id?: number }) {
    setData((prev) => {
      if (livro.id)
        return prev.map((p) => (p.id === livro.id ? { ...p, ...livro } : p));
      const nextId = Math.max(0, ...prev.map((p) => p.id)) + 1;
      return [...prev, { ...(livro as Livro), id: nextId }];
    });
  }

  return (
    <div className="bg-white rounded-2xl p-6 shadow-sm border">
      <div className="flex flex-wrap gap-3 mb-4">
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Buscar..."
          className="px-3 py-2 border rounded-lg flex-1"
        />
        <button
          onClick={onCreate}
          className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
        >
          Novo Livro
        </button>
      </div>

      <table className="w-full text-sm">
        <thead className="text-slate-600">
          <tr>
            <th className="text-left p-2">Título</th>
            <th className="text-left p-2">Autor</th>
            <th className="text-left p-2">Categoria</th>
            <th className="text-left p-2">Condição</th>
            <th className="text-left p-2">Preço</th>
            <th className="text-left p-2">Estoque</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {filtered.map((l) => (
            <tr key={l.id} className="border-t hover:bg-slate-50">
              <td className="p-2">{l.titulo}</td>
              <td className="p-2">{l.autor}</td>
              <td className="p-2">{l.categoria}</td>
              <td className="p-2">{l.condicao}</td>
              <td className="p-2">R$ {l.preco.toFixed(2)}</td>
              <td className="p-2">{l.estoque}</td>
              <td className="p-2 flex gap-2">
                <button
                  onClick={() => onEdit(l)}
                  className="px-3 py-1 bg-amber-500 text-white rounded"
                >
                  Editar
                </button>
                <button
                  onClick={() => onDelete(l.id)}
                  className="px-3 py-1 bg-rose-600 text-white rounded"
                >
                  Remover
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {modalOpen && (
        <BookFormModal
          initial={editing ?? undefined}
          onClose={() => setModalOpen(false)}
          onSave={(values) => {
            upsert(values);
            setModalOpen(false);
          }}
        />
      )}
    </div>
  );
}
