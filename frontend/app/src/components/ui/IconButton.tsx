import React from "react";
export const IconButton: React.FC<
  React.PropsWithChildren<{ title?: string; onClick?: () => void }>
> = ({ children, ...p }) => (
  <button
    {...p}
    className="h-10 w-10 grid place-items-center rounded-full border border-slate-200 bg-white hover:shadow-sm active:scale-95 transition"
  >
    {children}
  </button>
);
