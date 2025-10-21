import { Navigate, Outlet, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { useEffect } from "react";

export default function AdminProtected() {
  const { isAuthenticated, isAdmin, user, token } = useAuth();
  const location = useLocation();

  useEffect(() => {
    console.log("[AdminProtected] location:", location.pathname);
    console.log("[AdminProtected] isAuthenticated:", isAuthenticated);
    console.log("[AdminProtected] isAdmin:", isAdmin);
    console.log("[AdminProtected] user:", user);
    console.log("[AdminProtected] token:", token?.slice(0, 12) + "...");
  }, [isAuthenticated, isAdmin, user, token, location.pathname]);

  if (!isAuthenticated) return <Navigate to="/login" replace />;
  if (!isAdmin)
    return (
      <h1 className="text-center mt-10 text-xl font-semibold">
        Acesso restrito a administradores
      </h1>
    );
  return <Outlet />;
}
