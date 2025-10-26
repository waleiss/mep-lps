import { useAuth } from "../context/AuthContext";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { changePassword, updateMe } from "../services/authApi";

export default function Profile() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [name, setName] = useState(user?.name ?? "");
  const [phone, setPhone] = useState(user?.telefone ?? "");
  const [email, setEmail] = useState(user?.email ?? "");
  const [savingPhone, setSavingPhone] = useState(false);
  const [savingEmail, setSavingEmail] = useState(false);
  const [savingName, setSavingName] = useState(false);

  const [pwd, setPwd] = useState({ current: "", next: "", confirm: "" });
  const [changing, setChanging] = useState(false);
  const [message, setMessage] = useState<string>("");

  function formatPhone(p: string | null | undefined) {
    if (!p) return "-";
    const d = p.replace(/\D/g, "");
    if (d.length === 11) {
      return `(${d.slice(0, 2)}) ${d.slice(2, 7)}-${d.slice(7)}`;
    }
    if (d.length === 10) {
      return `(${d.slice(0, 2)}) ${d.slice(2, 6)}-${d.slice(6)}`;
    }
    return p;
  }

  async function savePhone() {
    if (!user) return;
    setSavingPhone(true);
    setMessage("");
    try {
      const updated = await updateMe({ telefone: phone.trim() || null });
      setMessage("Telefone atualizado com sucesso.");
      setPhone(updated.telefone ?? "");
      // Atualiza cache local do usuário (para refletir em outras telas)
      try {
        const key = "mp_user";
        const raw = localStorage.getItem(key);
        if (raw) {
          const u = JSON.parse(raw);
          u.telefone = updated.telefone ?? null;
          localStorage.setItem(key, JSON.stringify(u));
        }
      } catch {}
    } catch (e: any) {
      setMessage(e?.response?.data?.detail || "Não foi possível atualizar o telefone.");
    } finally {
      setSavingPhone(false);
    }
  }

  async function saveEmail() {
    if (!user) return;
    setSavingEmail(true);
    setMessage("");
    try {
      const updated = await updateMe({ email: email.trim().toLowerCase() || null });
      setMessage("Email atualizado com sucesso.");
      setEmail(updated.email);
      try {
        const key = "mp_user";
        const raw = localStorage.getItem(key);
        if (raw) {
          const u = JSON.parse(raw);
          u.email = updated.email;
          localStorage.setItem(key, JSON.stringify(u));
        }
      } catch {}
    } catch (e: any) {
      setMessage(e?.response?.data?.detail || "Não foi possível atualizar o email.");
    } finally {
      setSavingEmail(false);
    }
  }

  async function saveName() {
    if (!user) return;
    setSavingName(true);
    setMessage("");
    try {
      const updated = await updateMe({ nome: name.trim() || null });
      setMessage("Nome atualizado com sucesso.");
      setName(updated.nome);
      try {
        const key = "mp_user";
        const raw = localStorage.getItem(key);
        if (raw) {
          const u = JSON.parse(raw);
          u.name = updated.nome;
          localStorage.setItem(key, JSON.stringify(u));
        }
      } catch {}
    } catch (e: any) {
      setMessage(e?.response?.data?.detail || "Não foi possível atualizar o nome.");
    } finally {
      setSavingName(false);
    }
  }

  async function submitPassword() {
    if (!user) return;
    setChanging(true);
    setMessage("");
    try {
      await changePassword({
        current_password: pwd.current,
        new_password: pwd.next,
        new_password_confirmation: pwd.confirm,
      });
      // Ao alterar a senha, desconecta imediatamente
      setMessage("Senha alterada com sucesso. Você será desconectado.");
      setPwd({ current: "", next: "", confirm: "" });
      logout();
      navigate("/login");
      return;
    } catch (e: any) {
      setMessage(e?.response?.data?.detail || "Não foi possível alterar a senha.");
    } finally {
      setChanging(false);
    }
  }
  return (
    <div className="max-w-lg mx-auto p-6">
      <h1 className="text-2xl font-bold text-indigo-900 mb-4">
        Dados da conta
      </h1>
      {!user ? (
        <p>Você não está logado.</p>
      ) : (
        <div className="rounded-xl border p-4 space-y-5">
          <div>
            <span className="text-slate-500 text-sm">Nome</span>
            <div className="font-semibold">{name}</div>
          </div>
          <div>
            <span className="text-slate-500 text-sm">Email</span>
            <div className="font-semibold">{email}</div>
          </div>
          {/* Email */}
          <div className="pt-3 border-t">
            <h2 className="font-semibold mb-2">Email</h2>
            <div className="flex gap-2">
              <input
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="email@exemplo.com"
                className="flex-1 border rounded-lg px-3 py-2"
                type="email"
              />
              <button
                onClick={saveEmail}
                disabled={savingEmail}
                className={`px-4 py-2 rounded-lg ${savingEmail ? "bg-slate-300" : "bg-indigo-600 hover:bg-indigo-700"} text-white`}
              >
                {savingEmail ? "Salvando..." : "Salvar"}
              </button>
            </div>
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
          <div>
            <span className="text-slate-500 text-sm">Telefone</span>
            <div className="font-semibold">{formatPhone(phone || user.telefone)}</div>
          </div>

          {/* Telefone */}
          <div className="pt-3 border-t">
            <h2 className="font-semibold mb-2">Telefone</h2>
            <div className="flex gap-2">
              <input
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                placeholder="(00) 00000-0000"
                className="flex-1 border rounded-lg px-3 py-2"
              />
              <button
                onClick={savePhone}
                disabled={savingPhone}
                className={`px-4 py-2 rounded-lg ${savingPhone ? "bg-slate-300" : "bg-indigo-600 hover:bg-indigo-700"} text-white`}
              >
                {savingPhone ? "Salvando..." : "Salvar"}
              </button>
            </div>
          </div>

          {/* Nome */}
          <div className="pt-3 border-t">
            <h2 className="font-semibold mb-2">Nome</h2>
            <div className="flex gap-2">
              <input
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Seu nome"
                className="flex-1 border rounded-lg px-3 py-2"
              />
              <button
                onClick={saveName}
                disabled={savingName}
                className={`px-4 py-2 rounded-lg ${savingName ? "bg-slate-300" : "bg-indigo-600 hover:bg-indigo-700"} text-white`}
              >
                {savingName ? "Salvando..." : "Salvar"}
              </button>
            </div>
          </div>

          {/* Trocar senha */}
          <div className="pt-3 border-t">
            <h2 className="font-semibold mb-2">Trocar senha</h2>
            <div className="space-y-2">
              <input
                type="password"
                placeholder="Senha atual"
                value={pwd.current}
                onChange={(e) => setPwd((p) => ({ ...p, current: e.target.value }))}
                className="w-full border rounded-lg px-3 py-2"
              />
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                <input
                  type="password"
                  placeholder="Nova senha"
                  value={pwd.next}
                  onChange={(e) => setPwd((p) => ({ ...p, next: e.target.value }))}
                  className="border rounded-lg px-3 py-2"
                />
                <input
                  type="password"
                  placeholder="Confirmar nova senha"
                  value={pwd.confirm}
                  onChange={(e) => setPwd((p) => ({ ...p, confirm: e.target.value }))}
                  className="border rounded-lg px-3 py-2"
                />
              </div>
              <button
                onClick={submitPassword}
                disabled={changing}
                className={`px-4 py-2 rounded-lg ${changing ? "bg-slate-300" : "bg-indigo-600 hover:bg-indigo-700"} text-white`}
              >
                {changing ? "Alterando..." : "Alterar senha"}
              </button>
            </div>
          </div>

          {message && (
            <div className="text-sm text-slate-700 bg-slate-50 border rounded-lg p-2">{message}</div>
          )}
        </div>
      )}
    </div>
  );
}
