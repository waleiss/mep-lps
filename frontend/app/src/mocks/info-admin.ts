export type Categoria =
  | "FICCAO"
  | "NAO_FICCAO"
  | "TECNICO"
  | "ACADEMICO"
  | "INFANTIL"
  | "OUTROS";

export type Condicao = "NOVO" | "USADO" | "SEMI_NOVO";

export const ALL_CATEGORIES: readonly Categoria[] = [
  "FICCAO",
  "NAO_FICCAO",
  "TECNICO",
  "ACADEMICO",
  "INFANTIL",
  "OUTROS",
];

export type Livro = {
  id: number;
  titulo: string;
  autor: string;
  categoria: Categoria;
  condicao: Condicao;
  preco: number;
  estoque: number;
  isbn?: string;
};

export type Pedido = {
  id: string;
  cliente: string;
  email: string;
  itens: Array<{ livroId: number; titulo: string; qtd: number; preco: number }>;
  total: number;
  status: "PENDENTE" | "PAGO" | "ENVIADO" | "CANCELADO";
  criadoEm: string;
};

export const MOCK_LIVROS: Livro[] = [
  { id: 1, titulo: "Dom Casmurro", autor: "Machado de Assis", categoria: "FICCAO", condicao: "NOVO", preco: 39.9, estoque: 12 },
  { id: 2, titulo: "Capitães da Areia", autor: "Jorge Amado", categoria: "FICCAO", condicao: "USADO", preco: 24.5, estoque: 4 },
  { id: 3, titulo: "Introdução ao Node.js", autor: "Fulano", categoria: "TECNICO", condicao: "NOVO", preco: 89.0, estoque: 8 },
  { id: 4, titulo: "Metodologia Científica", autor: "Beltrano", categoria: "ACADEMICO", condicao: "NOVO", preco: 59.0, estoque: 5 },
  { id: 5, titulo: "Histórias para Dormir", autor: "Ciclano", categoria: "INFANTIL", condicao: "SEMI_NOVO", preco: 25.0, estoque: 10 },
];


export const MOCK_PEDIDOS: Pedido[] = [
  {
    id: "2025-0001",
    cliente: "Ana Souza",
    email: "ana@example.com",
    itens: [{ livroId: 1, titulo: "Dom Casmurro", qtd: 1, preco: 39.9 }],
    total: 39.9,
    status: "PAGO",
    criadoEm: new Date().toISOString(),
  },
];
