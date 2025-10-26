import { useEffect, useState } from "react";
import { ALL_PAYMENT_METHODS, type PaymentMethod } from "../../types/payment";
import { getPublicSettings, updatePublicSettings } from "../../services/api";

export default function PaymentSettings() {
  const [modalOpen, setModalOpen] = useState(false);
  // null => não configurado (mostrar todos). [] => nenhum disponível
  const [enabled, setEnabled] = useState<PaymentMethod[] | null>(null);

  useEffect(() => {
    getPublicSettings()
      .then((data) => {
        const methods = data.enabledPayments as PaymentMethod[] | null | undefined;
        if (methods == null) setEnabled(null); else setEnabled(methods.filter((m) => ALL_PAYMENT_METHODS.includes(m)));
      })
      .catch(() => setEnabled(null));
  }, []);

  function save(next: PaymentMethod[]) {
    setEnabled(next);
    updatePublicSettings({ enabledPayments: next }).catch((e) =>
      console.error("Falha ao salvar métodos de pagamento:", e)
    );
    setModalOpen(false);
  }

  return (
    <div className="rounded-2xl border bg-white p-5 shadow-sm">
      <div className="mb-4 flex items-center justify-between">
        <h2 className="text-lg font-semibold text-slate-800">
          Métodos de Pagamento
        </h2>
        <button
          onClick={() => setModalOpen(true)}
          className="rounded-lg border px-3 py-1.5 text-sm hover:bg-slate-50"
        >
          Editar métodos
        </button>
      </div>

      <div className="flex flex-wrap gap-2">
        {(enabled ?? ALL_PAYMENT_METHODS).map((m) => (
          <span
            key={m}
            className="rounded-full border bg-slate-50 px-3 py-1 text-sm"
          >
            {m === "pix" && "💸 Pix"}
            {m === "card" && "💳 Cartão"}
            {m === "boleto" && "🧾 Boleto"}
          </span>
        ))}
      </div>

      {modalOpen && (
        <Modal
          title="Selecionar métodos de pagamento"
          options={ALL_PAYMENT_METHODS}
          selected={enabled ?? [...ALL_PAYMENT_METHODS]}
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
  options: readonly PaymentMethod[];
  selected: PaymentMethod[];
  onClose: () => void;
  onSave: (next: PaymentMethod[]) => void;
}) {
  const [chosen, setChosen] = useState<Set<PaymentMethod>>(
    () => new Set(selected)
  );

  function toggle(opt: PaymentMethod) {
    setChosen((prev) => {
      const next = new Set(prev);
      next.has(opt) ? next.delete(opt) : next.add(opt);
      return next;
    });
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
      <div className="w-[400px] max-w-[92vw] rounded-2xl border bg-white p-6 shadow-xl">
        <h3 className="mb-4 text-lg font-semibold">{title}</h3>
        <div className="mb-4 space-y-2">
          {options.map((opt) => (
            <label key={opt} className="flex items-center gap-2 text-sm">
              <input
                type="checkbox"
                checked={chosen.has(opt)}
                onChange={() => toggle(opt)}
              />
              {opt === "pix" && "Pix"}
              {opt === "card" && "Cartão"}
              {opt === "boleto" && "Boleto"}
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
