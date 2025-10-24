import CategorySettings from "../../components/settings/CategorySettings";
import PaymentSettings from "../../components/settings/PaymentSettings";

export default function SystemSettings() {
  return (
    <div className="p-6">
      <h1 className="mb-6 text-2xl font-bold text-slate-800">
        Configurações do Sistema
      </h1>

      <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
        <CategorySettings />
        <PaymentSettings />
      </div>
    </div>
  );
}
