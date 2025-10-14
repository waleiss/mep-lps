import { createContext, useContext, useState } from "react";

type AuthCtx = {
  user: string | null;
  login: (username: string) => void;
  logout: () => void;
  isAuthenticated: boolean;
};

const Ctx = createContext<AuthCtx | null>(null);

export const AuthProvider: React.FC<React.PropsWithChildren> = ({
  children,
}) => {
  const [user, setUser] = useState<string | null>(null);

  const login = (username: string) => setUser(username);
  const logout = () => setUser(null);

  return (
    <Ctx.Provider value={{ user, login, logout, isAuthenticated: !!user }}>
      {children}
    </Ctx.Provider>
  );
};

export const useAuth = () => {
  const ctx = useContext(Ctx);
  if (!ctx) throw new Error("useAuth precisa estar dentro de AuthProvider");
  return ctx;
};
