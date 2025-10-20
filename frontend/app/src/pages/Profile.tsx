import { useAuth } from "../context/AuthContext";

export default function Profile() {
  const { user } = useAuth();
  return (
    <div className="max-w-lg mx-auto p-6">
      <h1 className="text-2xl font-bold text-indigo-900 mb-4">
        Dados da conta
      </h1>
      {!user ? (
        <p>Você não está logado.</p>
      ) : (
        <div className="rounded-xl border p-4 space-y-3">
          <div>
            <span className="text-slate-500 text-sm">Nome</span>
            <div className="font-semibold">{user.name}</div>
          </div>
          <div>
            <span className="text-slate-500 text-sm">Email</span>
            <div className="font-semibold">{user.email}</div>
          </div>
          <div>
            <span className="text-slate-500 text-sm">Tipo</span>
            <div className="font-semibold">{user.tipo}</div>
          </div>
          <div>
            <span className="text-slate-500 text-sm">Status</span>
            <div className="font-semibold">
              {user.ativo ? "Ativo" : "Inativo"}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
