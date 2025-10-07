import { createBrowserRouter } from "react-router-dom";
import { Layout } from "../components/layout/Layout";
import Home from "../pages/Home";
// import BookDetails from "../pages/BookDetails";
// import Checkout from "../pages/Checkout";

export const router = createBrowserRouter([
  {
    path: "/",
    element: (
      <Layout>
        <Home />
      </Layout>
    ),
  },
  //   {
  //     path: "/book/:id",
  //     element: (
  //       <Layout>
  //         <BookDetails />
  //       </Layout>
  //     ),
  //   },
  //   {
  //     path: "/checkout",
  //     element: (
  //       <Layout>
  //         <Checkout />
  //       </Layout>
  //     ),
  //   },
]);
