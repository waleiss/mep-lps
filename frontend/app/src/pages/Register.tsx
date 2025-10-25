import { type FormEvent, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import logo from "../assets/logo.svg";
import { register as apiRegister } from "../services/authApi";

export default function Register() {
  const nav = useNavigate();
  const [loading, setLoading] = useState(false);

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [passwordConf, setPasswordConf] = useState("");

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    if (password !== passwordConf) {
      alert("As senhas não coincidem.");
      return;
    }

    setLoading(true);
    try {
      const res = await apiRegister({
        name,
        email,
        password,
        password_confirmation: passwordConf,
      });

      console.log("Registro bem-sucedido:", res);

      // Salvar token e usuário no localStorage
      localStorage.setItem("mp_token", res.access_token ?? "");
      localStorage.setItem("mp_user", JSON.stringify({
        id: String(res.user_id),
        name: res.nome,
        email: res.email,
        tipo: res.tipo,
        ativo: res.ativo
      }));

      // Redirecionar para /admin se for admin, senão para home
      const isAdminEmail = email.toLowerCase().includes('@admin') || 
                          email.toLowerCase().startsWith('admin@');
      
      if (isAdminEmail || res.tipo?.toLowerCase() === 'admin') {
        nav("/admin");
      } else {
        nav("/");
      }
    } catch (err: any) {
      // Mostra erro legível
      const msg =
        err?.response?.data?.message ||
        err?.response?.data?.error ||
        "Falha ao registrar.";
      alert(msg);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-indigo-50 via-white to-indigo-100 flex flex-col items-center justify-center px-4">
      <div className="text-center mb-10 max-w-md">
        <img
          src={logo}
          alt="Logo Mundo em Palavras"
          className="w-14 h-14 mx-auto mb-4 drop-shadow-sm"
        />
        <h1 className="text-2xl font-bold text-indigo-900">
          Crie sua conta no{" "}
          <span className="text-indigo-700">Mundo em Palavras</span>
        </h1>
        <p className="text-slate-600 mt-2 text-sm">
          Uma livraria para quem acredita que a leitura expande a inteligência e
          transforma realidades.
        </p>
      </div>

      <form
        onSubmit={onSubmit}
        className="w-full max-w-sm bg-white shadow-lg rounded-2xl p-8 border border-slate-100"
      >
        <label className="block text-sm text-slate-700 mb-1">
          Nome completo
        </label>
        <input
          className="w-full border border-slate-300 rounded-lg px-3 py-2 mb-4 focus:ring-2 focus:ring-indigo-400 outline-none"
          placeholder="João Leitor"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />

        <label className="block text-sm text-slate-700 mb-1">Email</label>
        <input
          type="email"
          className="w-full border border-slate-300 rounded-lg px-3 py-2 mb-4 focus:ring-2 focus:ring-indigo-400 outline-none"
          placeholder="seu@email.com"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        <label className="block text-sm text-slate-700 mb-1">Senha</label>
        <input
          type="password"
          className="w-full border border-slate-300 rounded-lg px-3 py-2 mb-4 focus:ring-2 focus:ring-indigo-400 outline-none"
          placeholder="••••••••"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <label className="block text-sm text-slate-700 mb-1">
          Confirmar senha
        </label>
        <input
          type="password"
          className="w-full border border-slate-300 rounded-lg px-3 py-2 mb-6 focus:ring-2 focus:ring-indigo-400 outline-none"
          placeholder="••••••••"
          value={passwordConf}
          onChange={(e) => setPasswordConf(e.target.value)}
          required
        />

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-indigo-700 hover:bg-indigo-800 text-white font-semibold py-2.5 rounded-lg transition-all"
        >
          {loading ? "Criando conta..." : "Registrar"}
        </button>

        <p className="text-center text-sm mt-6 text-slate-600">
          Já tem conta?{" "}
          <Link
            to="/login"
            className="text-indigo-700 font-medium hover:underline"
          >
            Entrar
          </Link>
        </p>
      </form>
    </div>
  );
}
