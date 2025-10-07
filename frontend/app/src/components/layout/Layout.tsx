import React from "react";
import Navbar from "./Navbar";

const TopBar = () => (
  <div className="w-full bg-indigo-900 text-white text-center text-xs tracking-wide py-2">
    ALGUMA FRASE LEGAL AQUI ✨
  </div>
);

export const Layout: React.FC<React.PropsWithChildren> = ({ children }) => (
  <div className="min-h-screen bg-gradient-to-b from-indigo-50/40 to-white text-slate-800">
    <TopBar />
    <Navbar />
    <main>{children}</main>
  </div>
);
