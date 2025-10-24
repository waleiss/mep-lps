import { variability } from "../../config/variability";
// import { MetodoPagamento } from "../../types/enums";

export default function PaymentOptions() {
  const available = Object.entries(variability.enabledPayments).filter(
    ([, enabled]) => enabled
  );

  return (
    <div className="flex flex-wrap gap-2">
      {available.map(([method]) => (
        <button
          key={method}
          className="px-4 py-2 border rounded-lg hover:bg-slate-100"
        >
          {method.toUpperCase()}
        </button>
      ))}
    </div>
  );
}
