// Tipos para pagamentos

export type PaymentMethod = "card" | "pix" | "boleto";

export type PaymentStatus = 
  | "pendente" 
  | "processando" 
  | "aprovado" 
  | "recusado" 
  | "cancelado" 
  | "estornado";

export type CardPaymentRequest = {
  usuario_id: number;
  pedido_id: number;
  valor: number;
  numero_cartao: string;
  nome_titular: string;
  validade: string; // MM/YY
  cvv: string;
  parcelas?: number;
};

export type PixPaymentRequest = {
  usuario_id: number;
  pedido_id: number;
  valor: number;
};

export type BoletoPaymentRequest = {
  usuario_id: number;
  pedido_id: number;
  valor: number;
  cpf_cnpj: string;
};

export type PaymentResponse = {
  id: number;
  usuario_id: number;
  pedido_id: number;
  forma_pagamento: string;
  status: PaymentStatus;
  valor: number;
  codigo_transacao: string;
  dados_pagamento?: string;
  data_processamento?: string;
  data_aprovacao?: string;
  observacoes?: string;
  data_criacao: string;
  data_atualizacao: string;
  
  // Campos extras
  mensagem?: string;
  qr_code?: string; // Para PIX
  codigo_barras?: string; // Para Boleto
  linha_digitavel?: string; // Para Boleto
};

