import { useMemo, useState } from "react";
import {
  type Livro,
  type Categoria,
  type Condicao,
  MOCK_LIVROS,
} from "../../mocks/info-admin";
import BookFormModal from "../../components/book/BookFormModal";

const LS_KEY = "publicEnabledCategories";

function CategoryVisibilityModal({
  categories,
  initialEnabled,
  onClose,
  onSave,
}: {
  categories: Categoria[];
  initialEnabled: Categoria[];
  onClose: () => void;
  onSave: (enabled: Categoria[]) => void;
}) {
  const [enabled, setEnabled] = useState<Set<Categoria>>(
    () => new Set(initialEnabled)
  );

  function toggle(cat: Categoria) {
    setEnabled((prev) => {
      const next = new Set(prev);
      next.has(cat) ? next.delete(cat) : next.add(cat);
      return next;
    });
  }

  function selectAll() {
    setEnabled(new Set(categories));
  }
  function clearAll() {
    setEnabled(new Set());
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
      <div className="w-[520px] max-w-[92vw] rounded-2xl border bg-white p-5 shadow-xl">
        <h3 className="mb-3 text-lg font-semibold">Categorias públicas</h3>
        <p className="mb-4 text-sm text-slate-600">
          Selecione as categorias que aparecem no site público do cliente.
        </p>

        <div className="mb-3 flex gap-2">
          <button
            className="rounded-lg border px-3 py-1.5 text-sm hover:bg-slate-50"
            onClick={selectAll}
          >
            Marcar todas
          </button>
          <button
            className="rounded-lg border px-3 py-1.5 text-sm hover:bg-slate-50"
            onClick={clearAll}
          >
            Desmarcar todas
          </button>
        </div>

        <div className="max-h-64 overflow-auto rounded-lg border p-3">
          <ul className="space-y-2">
            {categories.map((cat) => (
              <li key={String(cat)} className="flex items-center gap-2">
                <input
                  id={`cat-${String(cat)}`}
                  type="checkbox"
                  checked={enabled.has(cat)}
                  onChange={() => toggle(cat)}
                  className="h-4 w-4"
                />
                <label
                  htmlFor={`cat-${String(cat)}`}
                  className="cursor-pointer text-sm"
                >
                  {String(cat)}
                </label>
              </li>
            ))}
          </ul>
        </div>

        <div className="mt-5 flex justify-end gap-2">
          <button
            onClick={onClose}
            className="rounded-lg border px-4 py-2 text-sm hover:bg-slate-50"
          >
            Cancelar
          </button>
          <button
            onClick={() => onSave(Array.from(enabled))}
            className="rounded-lg bg-indigo-600 px-4 py-2 text-sm text-white hover:bg-indigo-700"
          >
            Salvar
          </button>
        </div>
      </div>
    </div>
  );
}

export default function Books() {
  const [data, setData] = useState<Livro[]>(() => MOCK_LIVROS);
  const [query, setQuery] = useState("");
  const [categoria] = useState<"" | Categoria>("");
  const [condicao] = useState<"" | Condicao>("");
  const [modalOpen, setModalOpen] = useState(false);
  const [editing, setEditing] = useState<Livro | null>(null);

  const allCategories = useMemo<Categoria[]>(
    () => Array.from(new Set(data.map((l) => l.categoria))),
    [data]
  );

  const [publicEnabled, setPublicEnabled] = useState<Categoria[]>([]);

  useMemo(() => {
    try {
      const raw = localStorage.getItem(LS_KEY);
      if (raw) {
        const arr = JSON.parse(raw) as Categoria[];

        const sanitized = arr.filter((c) => allCategories.includes(c));
        setPublicEnabled(sanitized);
      } else {
        setPublicEnabled(allCategories);
      }
    } catch {
      setPublicEnabled(allCategories);
    }
  }, [allCategories]);

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

  const [visModalOpen, setVisModalOpen] = useState(false);
  function savePublicEnabled(next: Categoria[]) {
    setPublicEnabled(next);
    localStorage.setItem(LS_KEY, JSON.stringify(next));
    setVisModalOpen(false);
  }

  return (
    <div className="rounded-2xl border bg-white p-6 shadow-sm">
      <div className="mb-4 flex flex-wrap items-center gap-3">
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Buscar..."
          className="flex-1 rounded-lg border px-3 py-2"
        />
        <button
          onClick={() => setVisModalOpen(true)}
          className="rounded-lg border px-4 py-2 hover:bg-slate-50"
          title="Configurar quais categorias aparecem no site público"
        >
          Categorias públicas
        </button>
        <button
          onClick={onCreate}
          className="rounded-lg bg-indigo-600 px-4 py-2 text-white hover:bg-indigo-700"
        >
          Novo Livro
        </button>
      </div>

      <div className="mb-3 flex flex-wrap gap-2">
        {publicEnabled.map((c) => (
          <span
            key={String(c)}
            className="rounded-full border bg-slate-50 px-3 py-1 text-xs text-slate-700"
            title="Habilitado no site público"
          >
            {String(c)}
          </span>
        ))}
        {!publicEnabled.length && (
          <span className="text-xs text-rose-600">
            Nenhuma categoria pública habilitada.
          </span>
        )}
      </div>

      <table className="w-full text-sm">
        <thead className="text-slate-600">
          <tr>
            <th className="p-2 text-left">Título</th>
            <th className="p-2 text-left">Autor</th>
            <th className="p-2 text-left">Categoria</th>
            <th className="p-2 text-left">Condição</th>
            <th className="p-2 text-left">Preço</th>
            <th className="p-2 text-left">Estoque</th>
            <th className="p-2 text-left">Público?</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {filtered.map((l) => {
            const isPublic = publicEnabled.includes(l.categoria);
            return (
              <tr key={l.id} className="border-t hover:bg-slate-50">
                <td className="p-2">{l.titulo}</td>
                <td className="p-2">{l.autor}</td>
                <td className="p-2">{l.categoria}</td>
                <td className="p-2">{l.condicao}</td>
                <td className="p-2">R$ {l.preco.toFixed(2)}</td>
                <td className="p-2">{l.estoque}</td>
                <td className="p-2">
                  <span
                    className={`rounded-full px-2 py-0.5 text-xs ${
                      isPublic
                        ? "bg-emerald-100 text-emerald-700"
                        : "bg-slate-200 text-slate-600"
                    }`}
                  >
                    {isPublic ? "Sim" : "Não"}
                  </span>
                </td>
                <td className="p-2 flex gap-2">
                  <button
                    onClick={() => onEdit(l)}
                    className="rounded bg-amber-500 px-3 py-1 text-white"
                  >
                    Editar
                  </button>
                  <button
                    onClick={() => onDelete(l.id)}
                    className="rounded bg-rose-600 px-3 py-1 text-white"
                  >
                    Remover
                  </button>
                </td>
              </tr>
            );
          })}
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

      {visModalOpen && (
        <CategoryVisibilityModal
          categories={allCategories}
          initialEnabled={publicEnabled}
          onClose={() => setVisModalOpen(false)}
          onSave={savePublicEnabled}
        />
      )}
    </div>
  );
}
// This function is not needed and can be removed.

