import { createBrowserRouter } from "react-router-dom";
import { Layout } from "../components/layout/Layout";
import Home from "../pages/Home";
// import BookDetails from "../pages/BookDetails";
// import Checkout from "../pages/Checkout";
// import Login from "../pages/Login"; // página de login simples
import { ProtectedRoute } from "./ProtectedRoute";

export const router = createBrowserRouter([
  {
    path: "/",
    element: (
      <Layout>
        <Home />
      </Layout>
    ),
  },
  // {
  //   path: "/book/:id",
  //   element: (
  //     <Layout>
  //       <BookDetails />
  //     </Layout>
  //   ),
  // },
  // {
  //   path: "/checkout",
  //   element: (
  //     <Layout>
  //       <ProtectedRoute>
  //         <Checkout />
  //       </ProtectedRoute>
  //     </Layout>
  //   ),
  // },
  // {
  //   path: "/login",
  //   element: (
  //     <Layout>
  //       <Login />
  //     </Layout>
  //   ),
  // },
]);
