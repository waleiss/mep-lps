import { createBrowserRouter } from "react-router-dom";
import { Layout } from "../components/layout/Layout";
import Home from "../pages/Home";
import Login from "../pages/Login";
import Register from "../pages/Register";
import Checkout from "../pages/Checkout";
import Orders from "../pages/Orders";
import Profile from "../pages/Profile";
import ProtectedRoute from "./ProtectedRoute";
import BookDetails from "../pages/BookDetails";
import Favorites from "../pages/Favorites";
import AdminLayout from "../components/layout/AdminLayout";
import AdminBooks from "../pages/admin/Books";
import AdminOrders from "../pages/admin/Orders";
import AdminProtected from "./AdminProtected";
import AdminSettings from "../pages/admin/SystemSettings";

export const router = createBrowserRouter([
  {
    path: "/",
    element: (
      <Layout>
        <Home />
      </Layout>
    ),
  },

  {
    path: "/book/:id",
    element: (
      <Layout>
        <BookDetails />
      </Layout>
    ),
  },
  { path: "/favorites", element: <Favorites /> },

  {
    path: "/login",
    element: <Login />,
  },
  {
    path: "/register",
    element: <Register />,
  },
  {
    element: <ProtectedRoute />,
    children: [
      {
        path: "/checkout",
        element: (
          <Layout>
            <Checkout />
          </Layout>
        ),
      },
      {
        path: "/account",
        element: (
          <Layout>
            <Orders />
          </Layout>
        ),
      },
      {
        path: "/account/profile",
        element: (
          <Layout>
            <Profile />
          </Layout>
        ),
      },
    ],
  },

  // 🧩 Admin area
  {
    path: "/admin",
    element: <AdminProtected />,
    children: [
      {
        element: <AdminLayout />,
        children: [
          { index: true, element: <AdminBooks /> },
          { path: "livros", element: <AdminBooks /> },
          { path: "pedidos", element: <AdminOrders /> },
          { path: "configuracoes", element: <AdminSettings /> },
        ],
      },
    ],
  },

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
