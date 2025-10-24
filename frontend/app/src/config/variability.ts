import { Categoria, CondicaoLivro } from "../types/enum";

export const variability = {
  enabledCategories: [
    Categoria.FICCAO,
    Categoria.TECNICO,
    Categoria.INFANTIL,
  ],
  enabledConditions: [
    CondicaoLivro.NOVO,
    CondicaoLivro.SEMI_NOVO,
  ],
  enabledPayments: {
    PIX: true,
    CARTAO: true,
    BOLETO: false,
  },
};
