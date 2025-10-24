import axios from "axios";
import type { Book } from "../types/book";

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8080/api/v1",
});
 
// Instância para o catalog service
export const catalogApi = axios.create({
  baseURL: import.meta.env.VITE_CATALOG_SERVICE_URL || "http://localhost:8002/api/v1",
});

// Adiciona token em todas as requisições
[api, catalogApi].forEach(instance => {
  instance.interceptors.request.use((config) => {
    const token = localStorage.getItem("mp_token");
    if (token) config.headers.Authorization = `Bearer ${token}`;
    return config;
  });
});

/**
 * Lista todos os livros do catálogo
 */
export async function listBooks(): Promise<Book[]> {
  try {
    const response = await catalogApi.get('/livros', {
      params: {
        page: 1,
        page_size: 100, // Buscar muitos livros
      }
    });
    
    // Mapeia os dados do backend para o formato do frontend
    const livros = response.data.items || [];
    
    return livros.map((livro: any) => ({
      id: livro.id.toString(),
      title: livro.titulo,
      author: livro.autor,
      price: parseFloat(livro.preco),
      rating: 4.5, // Você pode adicionar avaliações depois
      cover: livro.imagem_url || "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=640&q=80&auto=format",
      coverUrl: livro.imagem_url || "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=640&q=80&auto=format",
      isbn: livro.isbn,
      publisher: livro.editora,
      year: livro.ano_publicacao,
      pages: livro.numero_paginas,
      description: livro.sinopse,
      category: livro.categoria,
      condition: livro.condicao,
      stock: livro.estoque,
    }));
  } catch (error) {
    console.error("Erro ao buscar livros:", error);
    return []; // Retorna array vazio em caso de erro
  }
}

/**
 * Busca um livro por ID
 */
export async function getBook(id: string): Promise<Book | undefined> {
  try {
    const response = await catalogApi.get(`/livros/${id}`);
    const livro = response.data;
    
    return {
      id: livro.id.toString(),
      title: livro.titulo,
      author: livro.autor,
      price: parseFloat(livro.preco),
      rating: 4.5,
      cover: livro.imagem_url || "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=640&q=80&auto=format",
      coverUrl: livro.imagem_url || "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=640&q=80&auto=format",
      isbn: livro.isbn,
      publisher: livro.editora,
      year: livro.ano_publicacao,
      pages: livro.numero_paginas,
      description: livro.sinopse,
      category: livro.categoria,
      condition: livro.condicao,
      stock: livro.estoque,
    };
  } catch (error) {
    console.error(`Erro ao buscar livro ${id}:`, error);
    return undefined;
  }
}
