import React, {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";
import {
  login as apiLogin,
  register as apiRegister,
  // refresh as apiRefresh, // Desabilitado temporariamente
  type LoginInput,
  type RegisterInput,
  type LoginResponse,
  type RegisterResponse,
} from "../services/authApi";

export type AuthUser = {
  id: string;
  name: string;
  email: string;
  tipo?: string;
  ativo: boolean;
};

type AuthState = {
  user: AuthUser | null;
  token: string | null;
  loading: boolean;
};

type AuthContextType = AuthState & {
  // derivados
  isAuthenticated: boolean;
  isAdmin: boolean;
  // ações
  login: (data: LoginInput) => Promise<void>;
  register: (data: RegisterInput) => Promise<void>;
  logout: () => void;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);
const TOKEN_KEY = "mp_token";
const USER_KEY = "mp_user";

/** Ajuste as regras conforme sua necessidade */
const ADMIN_EMAIL_RULES: RegExp[] = [
  /@admin\b/i, // ex.: fulano@admin ou fulano@admin.com
];

function inferIsAdmin(user: AuthUser | null): boolean {
  if (!user?.email) return false;
  const email = user.email.trim().toLowerCase();
  return ADMIN_EMAIL_RULES.some((re) => re.test(email));
}

export const AuthProvider: React.FC<React.PropsWithChildren> = ({
  children,
}) => {
  const [user, setUser] = useState<AuthUser | null>(() => {
    const raw = localStorage.getItem(USER_KEY);
    return raw ? JSON.parse(raw) : null;
  });

  const [token, setToken] = useState<string | null>(() =>
    localStorage.getItem(TOKEN_KEY)
  );

  const [loading, setLoading] = useState(false);

  const persist = (u: AuthUser | null, t: string | null) => {
    setUser(u);
    setToken(t);
    if (u) localStorage.setItem(USER_KEY, JSON.stringify(u));
    else localStorage.removeItem(USER_KEY);
    if (t) localStorage.setItem(TOKEN_KEY, t);
    else localStorage.removeItem(TOKEN_KEY);
  };

  const login = useCallback(async (data: LoginInput) => {
    setLoading(true);
    try {
      // normaliza e-mail antes de enviar
      const payload: LoginInput = {
        ...data,
        email: data.email.trim().toLowerCase(),
      };

      const res: LoginResponse = await apiLogin(payload);

      const mappedUser: AuthUser = {
        id: String(res.user_id),
        name: res.nome,
        email: res.email?.trim().toLowerCase(),
        tipo: res.tipo ?? undefined,
        ativo: res.ativo,
      };

      persist(mappedUser, res.access_token);
    } finally {
      setLoading(false);
    }
  }, []);

  const register = useCallback(async (data: RegisterInput) => {
    setLoading(true);
    try {
      const payload: RegisterInput = {
        ...data,
        email: data.email.trim().toLowerCase(),
      };

      const res: RegisterResponse = await apiRegister(payload);

      const mappedUser: AuthUser = {
        id: String(res.user_id),
        name: res.nome,
        email: res.email?.trim().toLowerCase(),
        tipo: res.tipo ?? undefined,
        ativo: res.ativo,
      };

      persist(mappedUser, res.access_token);
    } finally {
      setLoading(false);
    }
  }, []);

  const logout = useCallback(() => {
    persist(null, null);
  }, []);

<<<<<<< HEAD
  // opcional — tenta refresh quando app abre
  // DESABILITADO: estava causando logout ao recarregar
  // useEffect(() => {
  //   const tryRefresh = async () => {
  //     if (!token) return;
  //     try {
  //       const res = await apiRefresh();
  //       persist(user, res.access_token);
  //     } catch {
  //       persist(null, null);
  //     }
  //   };
  //   tryRefresh();
  //   // eslint-disable-next-line react-hooks/exhaustive-deps
  // }, []);
=======
  useEffect(() => {
    if (!token) return;
    (async () => {
      try {
      } catch (err: any) {
        const status = err?.response?.status;
        if (status === 404) {
          console.warn("[Auth] refresh não suportado. Mantendo sessão atual.");
          return;
        }
        if (status === 401) {
          persist(null, null);
        }
        console.warn("[Auth] erro no refresh, sessão mantida:", err);
      }
    })();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [token]);

  // derivados
  const isAuthenticated = !!token && !!user;
  const isAdmin = inferIsAdmin(user);
>>>>>>> b7dc6ec53f2a11a5f3ead1c6cea65c2022b19745

  const value = useMemo(
    () => ({
      user,
      token,
      loading,
      isAuthenticated,
      isAdmin,
      login,
      register,
      logout,
    }),
    [user, token, loading, isAuthenticated, isAdmin, login, register, logout]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
};
