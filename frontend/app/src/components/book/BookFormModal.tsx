import React, { useEffect, useState } from "react";
import type { Categoria, Condicao, Livro } from "../../mocks/info-admin";

type Props = {
  initial?: Livro;
  onClose: () => void;
  onSave: (values: Omit<Livro, "id"> & { id?: number }) => void;
};

export default function BookFormModal({ initial, onClose, onSave }: Props) {
  const [form, setForm] = useState<Omit<Livro, "id"> & { id?: number }>(
    () =>
      initial ?? {
        titulo: "",
        autor: "",
        categoria: "OUTROS",
        condicao: "NOVO",
        preco: 0,
        estoque: 0,
        isbn: "",
      }
  );

  function set<K extends keyof typeof form>(key: K, value: (typeof form)[K]) {
    setForm((prev) => ({ ...prev, [key]: value }));
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!form.titulo.trim() || !form.autor.trim())
      return alert("Título e Autor são obrigatórios.");
    if (form.preco < 0) return alert("Preço inválido.");
    if (form.estoque < 0) return alert("Estoque inválido.");
    onSave(form);
  }

  useEffect(() => {
    if (initial) setForm(initial);
  }, [initial]);

  const CATEGORIAS: Categoria[] = [
    "FICCAO",
    "NAO_FICCAO",
    "TECNICO",
    "ACADEMICO",
    "INFANTIL",
    "OUTROS",
  ];

  const CONDICOES: Condicao[] = ["NOVO", "USADO", "SEMI_NOVO"];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4">
      <div className="w-full max-w-xl bg-white rounded-2xl shadow-xl border">
        <div className="flex items-center justify-between p-4 border-b">
          <h3 className="text-lg font-semibold">
            {initial ? "Editar Livro" : "Novo Livro"}
          </h3>
          <button
            onClick={onClose}
            className="text-slate-500 hover:text-slate-700"
          >
            ✕
          </button>
        </div>

        <form
          onSubmit={handleSubmit}
          className="p-4 grid grid-cols-1 md:grid-cols-2 gap-4"
        >
          <div className="md:col-span-2">
            <label className="text-sm text-slate-600">Título *</label>
            <input
              className="w-full mt-1 px-3 py-2 border rounded-lg"
              value={form.titulo}
              onChange={(e) => set("titulo", e.target.value)}
              placeholder="Ex.: Dom Casmurro"
            />
          </div>

          <div className="md:col-span-2">
            <label className="text-sm text-slate-600">Autor *</label>
            <input
              className="w-full mt-1 px-3 py-2 border rounded-lg"
              value={form.autor}
              onChange={(e) => set("autor", e.target.value)}
              placeholder="Ex.: Machado de Assis"
            />
          </div>

          <div>
            <label className="text-sm text-slate-600">Categoria</label>
            <select
              className="w-full mt-1 px-3 py-2 border rounded-lg bg-white"
              value={form.categoria}
              onChange={(e) => set("categoria", e.target.value as Categoria)}
            >
              {CATEGORIAS.map((c) => (
                <option key={c} value={c}>
                  {c}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="text-sm text-slate-600">Condição</label>
            <select
              className="w-full mt-1 px-3 py-2 border rounded-lg bg-white"
              value={form.condicao}
              onChange={(e) => set("condicao", e.target.value as Condicao)}
            >
              {CONDICOES.map((c) => (
                <option key={c} value={c}>
                  {c}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="text-sm text-slate-600">Preço (R$)</label>
            <input
              type="number"
              step="0.01"
              className="w-full mt-1 px-3 py-2 border rounded-lg"
              value={form.preco}
              onChange={(e) => set("preco", parseFloat(e.target.value || "0"))}
            />
          </div>

          <div>
            <label className="text-sm text-slate-600">Estoque</label>
            <input
              type="number"
              className="w-full mt-1 px-3 py-2 border rounded-lg"
              value={form.estoque}
              onChange={(e) => set("estoque", parseInt(e.target.value || "0"))}
            />
          </div>

          <div className="md:col-span-2">
            <label className="text-sm text-slate-600">ISBN</label>
            <input
              className="w-full mt-1 px-3 py-2 border rounded-lg"
              value={form.isbn ?? ""}
              onChange={(e) => set("isbn", e.target.value)}
              placeholder="Ex.: 9788535921349"
            />
          </div>

          <div className="md:col-span-2 flex justify-end gap-2 pt-2">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 rounded-lg border"
            >
              Cancelar
            </button>
            <button
              type="submit"
              className="px-4 py-2 rounded-lg bg-indigo-600 text-white hover:bg-indigo-700"
            >
              {initial ? "Salvar alterações" : "Cadastrar"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
