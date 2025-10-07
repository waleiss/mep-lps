import React from "react";
export const Badge: React.FC<React.PropsWithChildren> = ({ children }) => (
  <span className="rounded-full border px-2 py-0.5 text-xs text-slate-600 border-slate-200 bg-white/70">
    {children}
  </span>
);
