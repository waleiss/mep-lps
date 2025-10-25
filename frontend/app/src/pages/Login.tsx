import { type FormEvent, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import logo from "../assets/logo.svg";

export default function Login() {
  const nav = useNavigate();
  const { login, loading, isAdmin } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    try {
      await login({ email, password });
      
      // Redirecionar para /admin se o usuário for administrador
      // Verifica se o email contém padrões admin ou aguarda isAdmin atualizar
      const isAdminEmail = email.toLowerCase().includes('@admin') || 
                          email.toLowerCase().startsWith('admin@');
      
      if (isAdminEmail || isAdmin) {
        nav("/admin");
      } else {
        nav("/");
      }
    } catch (error) {
      console.error("Erro no login:", error);
      // Erro já é tratado pelo AuthContext
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
          Bem-vindo de volta ao{" "}
          <span className="text-indigo-700">Mundo em Palavras</span>
        </h1>
        <p className="text-slate-600 mt-2 text-sm">
          Onde cada livro é uma porta para o conhecimento, e a leitura é a chave
          da inteligência.
        </p>
      </div>

      <form
        onSubmit={onSubmit}
        className="w-full max-w-sm bg-white shadow-lg rounded-2xl p-8 border border-slate-100"
      >
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
          className="w-full border border-slate-300 rounded-lg px-3 py-2 mb-6 focus:ring-2 focus:ring-indigo-400 outline-none"
          placeholder="••••••••"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-indigo-700 hover:bg-indigo-800 text-white font-semibold py-2.5 rounded-lg transition-all"
        >
          {loading ? "Entrando..." : "Entrar"}
        </button>

        <p className="text-center text-sm mt-6 text-slate-600">
          Não tem uma conta?{" "}
          <Link
            to="/register"
            className="text-indigo-700 font-medium hover:underline"
          >
            Cadastre-se
          </Link>
        </p>
      </form>
    </div>
  );
}
