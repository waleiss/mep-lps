import { useEffect, useState } from "react";
import { ALL_CATEGORIES, type Categoria } from "../../mocks/info-admin";

const CAT_LS_KEY = "publicEnabledCategories";

export default function CategorySettings() {
  const [modalOpen, setModalOpen] = useState(false);
  const [enabled, setEnabled] = useState<Categoria[]>([]);
  const [showSavedMessage, setShowSavedMessage] = useState(false);

  useEffect(() => {
    try {
      const raw = localStorage.getItem(CAT_LS_KEY);
      if (raw) {
        const arr = JSON.parse(raw) as Categoria[];
        const sanitized = arr.filter((c) => ALL_CATEGORIES.includes(c));
        setEnabled(sanitized);
      } else {
        // Start with empty array (no categories enabled by default)
        setEnabled([]);
      }
    } catch {
      setEnabled([]);
    }
  }, []);

  function save(next: Categoria[]) {
    setEnabled(next);
    localStorage.setItem(CAT_LS_KEY, JSON.stringify(next));
    setModalOpen(false);
    
    // Show saved message
    setShowSavedMessage(true);
    setTimeout(() => setShowSavedMessage(false), 3000);
    
    // Dispatch custom event to notify other components
    window.dispatchEvent(new Event('categoriesUpdated'));
  }

  return (
    <div className="rounded-2xl border bg-white p-5 shadow-sm">
      <div className="mb-4 flex items-center justify-between">
        <h2 className="text-lg font-semibold text-slate-800">
          Categorias Públicas
        </h2>
        <button
          onClick={() => setModalOpen(true)}
          className="rounded-lg border px-3 py-1.5 text-sm hover:bg-slate-50"
        >
          Editar categorias
        </button>
      </div>

      {showSavedMessage && (
        <div className="mb-3 rounded-lg bg-green-50 border border-green-200 px-3 py-2 text-sm text-green-800">
          ✓ Configurações salvas! {enabled.length === 0 ? "Todas as categorias serão exibidas." : `${enabled.length} categoria(s) habilitada(s).`}
        </div>
      )}

      <div className="flex flex-wrap gap-2">
        {enabled.length > 0 ? (
          enabled.map((c) => (
            <span
              key={c}
              className="rounded-full border bg-slate-50 px-3 py-1 text-sm"
            >
              {c}
            </span>
          ))
        ) : (
          <span className="text-sm text-slate-500 italic">
            Nenhuma categoria selecionada - todas serão exibidas no site
          </span>
        )}
      </div>

      {modalOpen && (
        <Modal
          title="Selecionar categorias públicas"
          options={ALL_CATEGORIES}
          selected={enabled}
          onClose={() => setModalOpen(false)}
          onSave={save}
        />
      )}
    </div>
  );
}

function Modal({
  title,
  options,
  selected,
  onClose,
  onSave,
}: {
  title: string;
  options: readonly Categoria[];
  selected: Categoria[];
  onClose: () => void;
  onSave: (next: Categoria[]) => void;
}) {
  const [chosen, setChosen] = useState<Set<Categoria>>(() => new Set(selected));

  function toggle(opt: Categoria) {
    setChosen((prev) => {
      const next = new Set(prev);
      next.has(opt) ? next.delete(opt) : next.add(opt);
      return next;
    });
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
      <div className="w-[500px] max-w-[92vw] rounded-2xl border bg-white p-6 shadow-xl">
        <h3 className="mb-4 text-lg font-semibold">{title}</h3>
        <div className="mb-4 grid grid-cols-2 gap-2">
          {options.map((opt) => (
            <label key={opt} className="flex items-center gap-2 text-sm">
              <input
                type="checkbox"
                checked={chosen.has(opt)}
                onChange={() => toggle(opt)}
              />
              {opt}
            </label>
          ))}
        </div>
        <div className="flex justify-end gap-2">
          <button
            onClick={onClose}
            className="rounded-lg border px-4 py-2 text-sm hover:bg-slate-50"
          >
            Cancelar
          </button>
          <button
            onClick={() => onSave(Array.from(chosen))}
            className="rounded-lg bg-indigo-600 px-4 py-2 text-sm text-white hover:bg-indigo-700"
          >
            Salvar
          </button>
        </div>
      </div>
    </div>
  );
}
