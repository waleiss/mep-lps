export type Category = {
  id: string;
  name: string;
  slug: string;
  image: string;
};

export const POP_CATEGORIES: Category[] = [
  {
    id: "he",
    name: "Ensino superior",
    slug: "ensino-superior",
    image: "https://images.unsplash.com/photo-1519681393784-d120267933ba?w=1200&q=80&auto=format",
  },
  {
    id: "gestao",
    name: "Gestão",
    slug: "gestao",
    image: "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=1200&q=80&auto=format",
  },
  {
    id: "eng",
    name: "Engenharia",
    slug: "engenharia",
    image: "https://images.unsplash.com/photo-1450849608880-6f787542c88a?w=1200&q=80&auto=format",
  },
  // adicione mais se quiser
];
