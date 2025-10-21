import { Link, NavLink, Outlet, useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import logo from "../../assets/logo.svg";

export default function AdminLayout() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login", { replace: true });
  };

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 text-slate-900">
      <header className="bg-white/80 backdrop-blur border-b shadow-sm sticky top-0 z-30">
        <div className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
          {/* Logo */}
          <Link
            to="/"
            className="flex items-center gap-2 font-bold text-lg text-indigo-900 hover:text-indigo-700 transition"
          >
            <img
              src={logo}
              alt="Logo Mundo em Palavras"
              className="w-8 h-8 object-contain"
            />
            <span>Painel&nbsp;Administrativo</span>
          </Link>

          {/* Usuário + Logout */}
          <div className="flex items-center gap-3">
            <div className="text-sm text-slate-600">
              {user?.name ?? user?.email}
            </div>
            <button
              onClick={handleLogout}
              className="px-3 py-1.5 text-sm rounded-lg border hover:bg-slate-100 transition"
            >
              Sair
            </button>
          </div>
        </div>

        <nav className="border-t border-slate-200 bg-white">
          <div className="max-w-7xl mx-auto px-4 flex gap-4">
            <NavLink
              to="/admin/livros"
              className={({ isActive }) =>
                `py-3 px-2 text-sm font-medium transition border-b-2 ${
                  isActive
                    ? "border-indigo-600 text-indigo-700"
                    : "border-transparent text-slate-600 hover:text-indigo-600"
                }`
              }
            >
              Livros
            </NavLink>
            <NavLink
              to="/admin/pedidos"
              className={({ isActive }) =>
                `py-3 px-2 text-sm font-medium transition border-b-2 ${
                  isActive
                    ? "border-indigo-600 text-indigo-700"
                    : "border-transparent text-slate-600 hover:text-indigo-600"
                }`
              }
            >
              Pedidos
            </NavLink>
          </div>
        </nav>
      </header>

      <main className="flex-1 max-w-7xl mx-auto w-full p-4 md:p-6">
        <Outlet />
      </main>

      <footer className="border-t text-center py-4 text-xs text-slate-500">
        © {new Date().getFullYear()} Mundo em Palavras — Administração
      </footer>
    </div>
  );
}
