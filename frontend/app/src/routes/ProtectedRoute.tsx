import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function ProtectedRoute() {
  const { token, loading } = useAuth();
  
  // Aguarda o contexto carregar antes de redirecionar
  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <p className="text-slate-600">Carregando...</p>
        </div>
      </div>
    );
  }
  
  if (!token) return <Navigate to="/login" replace />;
  return <Outlet />;
}
