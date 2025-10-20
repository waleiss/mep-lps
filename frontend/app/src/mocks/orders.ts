import type { Order } from "../types/order";
import { CATALOG } from "./catalog";

export const MOCK_ORDERS: Order[] = [
  {
    id: "ORD-2025-0001",
    items: [
      { book: CATALOG[0], qty: 1 },
      { book: CATALOG[1], qty: 1 },
    ],
    subtotal: 218.9,
    shipping: 19.9,
    total: 238.8,
    status: "delivered",
    createdAt: "2025-10-10T12:34:56Z",
  },
];
