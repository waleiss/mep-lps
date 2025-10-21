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
  tipo: string;
  ativo: boolean;
};

type AuthState = {
  user: AuthUser | null;
  token: string | null;
  loading: boolean;
};

type AuthContextType = AuthState & {
  login: (data: LoginInput) => Promise<void>;
  register: (data: RegisterInput) => Promise<void>;
  logout: () => void;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);
const TOKEN_KEY = "mp_token";
const USER_KEY = "mp_user";

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
      const res: LoginResponse = await apiLogin(data);

      const mappedUser: AuthUser = {
        id: String(res.user_id),
        name: res.nome,
        email: res.email,
        tipo: res.tipo,
        ativo: res.ativo,
      };

      console.log("🔑 Login response:", res);
      console.log("👤 Mapeado para AuthUser:", mappedUser);

      persist(mappedUser, res.access_token);
    } finally {
      setLoading(false);
    }
  }, []);

  const register = useCallback(async (data: RegisterInput) => {
    setLoading(true);
    try {
      const res: RegisterResponse = await apiRegister(data);

      const mappedUser: AuthUser = {
        id: String(res.user_id),
        name: res.nome,
        email: res.email,
        tipo: res.tipo,
        ativo: res.ativo,
      };

      console.log("🆕 Register response:", res);
      persist(mappedUser, res.access_token);
    } finally {
      setLoading(false);
    }
  }, []);

  const logout = useCallback(() => {
    persist(null, null);
  }, []);

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

  const value = useMemo(
    () => ({ user, token, loading, login, register, logout }),
    [user, token, loading, login, register, logout]
  );

  // 🔍 debug visual
  useEffect(() => {
    console.log("👤 AuthContext — user atualizado:", user);
  }, [user]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
};
