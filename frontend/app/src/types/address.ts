// Tipos para endereços e CEP

export type Address = {
  id?: number;
  usuario_id?: number;
  cep: string;
  logradouro: string;
  numero: string;
  complemento?: string;
  bairro: string;
  cidade: string;
  estado: string;
  apelido?: string;
  principal?: boolean;
  ativo?: boolean;
  data_criacao?: string;
  data_atualizacao?: string;
};

export type AddressCreate = {
  usuario_id: number;
  cep: string;
  logradouro: string;
  numero: string;
  complemento?: string;
  bairro: string;
  cidade: string;
  estado: string;
  apelido?: string;
  principal?: boolean;
};

export type AddressResponse = Address;

export type AddressListResponse = {
  enderecos: AddressResponse[];
  total: number;
};

export type ViaCEPResponse = {
  cep: string;
  logradouro: string;
  complemento: string;
  bairro: string;
  localidade: string; // cidade
  uf: string; // estado
  ibge?: string;
  gia?: string;
  ddd?: string;
  siafi?: string;
  erro?: boolean;
};

