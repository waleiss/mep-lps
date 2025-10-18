import { createBrowserRouter } from "react-router-dom";
import { Layout } from "../components/layout/Layout";
import Home from "../pages/Home";
import Login from "../pages/Login";
import Register from "../pages/Register";

// import ProtectedRoute from "./ProtectedRoute";

export const router = createBrowserRouter([
  // 🌐 Página inicial pública
  {
    path: "/",
    element: (
      <Layout>
        <Home />
      </Layout>
    ),
  },

  // 🔐 Rotas protegidas
  // {
  //   element: <ProtectedRoute />, // Tudo dentro daqui exige login
  //   children: [
  //     {
  //       path: "/checkout",
  //       element: (
  //         <Layout>
  //           <Checkout />
  //         </Layout>
  //       ),
  //     },
  //     // outras rotas privadas aqui (perfil, pedidos, etc.)
  //   ],
  // },

  {
    path: "/login",
    element: <Login />,
  },
  {
    path: "/register",
    element: <Register />,
  },

  // 🚫 404 (opcional)
  {
    path: "*",
    element: (
      <Layout>
        <h1 className="text-center mt-10 text-xl font-semibold">
          Página não encontrada
        </h1>
      </Layout>
    ),
  },
]);
