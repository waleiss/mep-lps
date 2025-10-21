export type Book = {
  id: string;
  title: string;
  author: string;
  price: number;
  rating: number;
  cover: string;
  coverUrl?: string;
  isbn?: string;
  publisher?: string;
  year?: number;
  pages?: number;
  description?: string;
  category?: string;
  condition?: string;
  stock?: number;
  tagline?: string;
  categories?: string[];
};

export type CartItem = { book: Book; qty: number };