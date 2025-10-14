# Diagrama do Schema do Banco de Dados

## Visão Geral da Arquitetura

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           SISTEMA DE E-COMMERCE                                │
│                              MICROSERVIÇOS                                     │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  Auth Service   │  │ Catalog Service │  │  Cart Service   │  │ Order Service   │
│ postgres_users  │  │postgres_catalog │  │ postgres_cart   │  │postgres_orders  │
└─────────────────┘  └─────────────────┘  └─────────────────┘  └─────────────────┘

┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│Payment Service  │  │Shipping Service │  │Recommendation   │
│postgres_payments│  │postgres_shipping│  │Service          │
│                 │  │                 │  │postgres_recomm  │
└─────────────────┘  └─────────────────┘  └─────────────────┘
```

## Modelos por Microserviço

### 1. Auth Service (postgres_users)
```
┌─────────────────────────────────────────────────────────────┐
│                        USUARIO                              │
├─────────────────────────────────────────────────────────────┤
│ id (PK)                                                     │
│ nome                                                        │
│ email (UNIQUE)                                              │
│ senha_hash                                                  │
│ telefone                                                    │
│ data_nascimento                                             │
│ tipo (ENUM: CLIENTE, ADMIN, VENDEDOR)                      │
│ ativo                                                       │
│ data_criacao                                                │
│ data_atualizacao                                            │
└─────────────────────────────────────────────────────────────┘
                                │
                                │ 1:N
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                       ENDERECO                              │
├─────────────────────────────────────────────────────────────┤
│ id (PK)                                                     │
│ usuario_id (FK)                                             │
│ logradouro                                                  │
│ numero                                                      │
│ complemento                                                 │
│ bairro                                                      │
│ cidade                                                      │
│ estado                                                      │
│ cep                                                         │
│ principal                                                   │
│ data_criacao                                                │
│ data_atualizacao                                            │
└─────────────────────────────────────────────────────────────┘
```

### 2. Catalog Service (postgres_catalog)
```
┌─────────────────────────────────────────────────────────────┐
│                         LIVRO                               │
├─────────────────────────────────────────────────────────────┤
│ id (PK)                                                     │
│ titulo                                                      │
│ autor                                                       │
│ isbn (UNIQUE)                                               │
│ editora                                                     │
│ ano_publicacao                                              │
│ edicao                                                      │
│ numero_paginas                                              │
│ sinopse                                                     │
│ preco                                                       │
│ estoque                                                     │
│ categoria (ENUM: FICCAO, NAO_FICCAO, TECNICO, etc.)        │
│ condicao (ENUM: NOVO, USADO, SEMI_NOVO)                    │
│ ativo                                                       │
│ data_criacao                                                │
│ data_atualizacao                                            │
└─────────────────────────────────────────────────────────────┘
```

### 3. Cart Service (postgres_cart)
```
┌─────────────────────────────────────────────────────────────┐
│                       CARRINHO                              │
├─────────────────────────────────────────────────────────────┤
│ id (PK)                                                     │
│ usuario_id (FK)                                             │
│ ativo                                                       │
│ data_criacao                                                │
│ data_atualizacao                                            │
└─────────────────────────────────────────────────────────────┘
                                │
                                │ 1:N
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                    ITEM_CARRINHO                            │
├─────────────────────────────────────────────────────────────┤
│ id (PK)                                                     │
│ carrinho_id (FK)                                            │
│ livro_id (FK)                                               │
│ quantidade                                                  │
│ preco_unitario                                              │
│ data_criacao                                                │
│ data_atualizacao                                            │
└─────────────────────────────────────────────────────────────┘
```

### 4. Order Service (postgres_orders)
```
┌─────────────────────────────────────────────────────────────┐
│                        PEDIDO                               │
├─────────────────────────────────────────────────────────────┤
│ id (PK)                                                     │
│ usuario_id (FK)                                             │
│ endereco_entrega_id (FK)                                    │
│ numero_pedido (UNIQUE)                                      │
│ status (ENUM: PENDENTE, CONFIRMADO, etc.)                  │
│ valor_total                                                 │
│ valor_frete                                                 │
│ observacoes                                                 │
│ data_criacao                                                │
│ data_atualizacao                                            │
│ data_entrega_prevista                                       │
│ data_entrega_realizada                                      │
└─────────────────────────────────────────────────────────────┘
                                │
                                │ 1:N
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                     ITEM_PEDIDO                             │
├─────────────────────────────────────────────────────────────┤
│ id (PK)                                                     │
│ pedido_id (FK)                                              │
│ livro_id (FK)                                               │
│ quantidade                                                  │
│ preco_unitario                                              │
│ data_criacao                                                │
└─────────────────────────────────────────────────────────────┘
```

### 5. Payment Service (postgres_payments)
```
┌─────────────────────────────────────────────────────────────┐
│                      PAGAMENTO                              │
├─────────────────────────────────────────────────────────────┤
│ id (PK)                                                     │
│ usuario_id (FK)                                             │
│ pedido_id (FK)                                              │
│ forma_pagamento (ENUM: CARTAO_CREDITO, PIX, etc.)          │
│ status (ENUM: PENDENTE, APROVADO, etc.)                    │
│ valor                                                       │
│ codigo_transacao (UNIQUE)                                  │
│ dados_pagamento (JSON)                                      │
│ data_processamento                                          │
│ data_aprovacao                                              │
│ observacoes                                                 │
│ data_criacao                                                │
│ data_atualizacao                                            │
└─────────────────────────────────────────────────────────────┘
```

### 6. Shipping Service (postgres_shipping)
```
┌─────────────────────────────────────────────────────────────┐
│                        FRETE                                │
├─────────────────────────────────────────────────────────────┤
│ id (PK)                                                     │
│ pedido_id (FK)                                              │
│ endereco_destino_id (FK)                                    │
│ tipo_frete (ENUM: ECONOMICO, PADRAO, etc.)                 │
│ status (ENUM: PENDENTE, EM_TRANSITO, etc.)                 │
│ valor                                                       │
│ peso_total                                                  │
│ dimensoes                                                   │
│ codigo_rastreamento (UNIQUE)                               │
│ transportadora                                              │
│ prazo_entrega                                               │
│ observacoes                                                 │
│ data_coleta                                                 │
│ data_entrega                                                │
│ data_criacao                                                │
│ data_atualizacao                                            │
└─────────────────────────────────────────────────────────────┘
```

### 7. Recommendation Service (postgres_recommendations)
```
┌─────────────────────────────────────────────────────────────┐
│                    RECOMENDACAO                             │
├─────────────────────────────────────────────────────────────┤
│ id (PK)                                                     │
│ usuario_id (FK)                                             │
│ livro_id (FK)                                               │
│ tipo (ENUM: BASEADA_USUARIO, COLABORATIVA, etc.)           │
│ status (ENUM: ATIVA, INATIVA, EXCLUIDA)                    │
│ score (0.0000 - 1.0000)                                    │
│ algoritmo                                                   │
│ parametros (JSON)                                           │
│ data_criacao                                                │
│ data_atualizacao                                            │
│ data_expiracao                                              │
└─────────────────────────────────────────────────────────────┘
```

## Relacionamentos Entre Microserviços

```
USUARIO (Auth Service)
    │
    ├── 1:N → CARRINHO (Cart Service)
    │           │
    │           └── 1:N → ITEM_CARRINHO
    │                       │
    │                       └── N:1 → LIVRO (Catalog Service)
    │
    ├── 1:N → PEDIDO (Order Service)
    │           │
    │           ├── 1:N → ITEM_PEDIDO
    │           │           │
    │           │           └── N:1 → LIVRO (Catalog Service)
    │           │
    │           ├── 1:N → PAGAMENTO (Payment Service)
    │           │
    │           └── 1:N → FRETE (Shipping Service)
    │
    └── 1:N → RECOMENDACAO (Recommendation Service)
                │
                └── N:1 → LIVRO (Catalog Service)

ENDERECO (Auth Service)
    │
    ├── 1:N → PEDIDO (endereco_entrega)
    │
    └── 1:N → FRETE (endereco_destino)
```

## Enums Utilizados

### TipoUsuario
- CLIENTE
- ADMIN  
- VENDEDOR

### Categoria
- FICCAO
- NAO_FICCAO
- TECNICO
- ACADEMICO
- INFANTIL
- OUTROS

### CondicaoLivro
- NOVO
- USADO
- SEMI_NOVO

### StatusPedido
- PENDENTE
- CONFIRMADO
- PROCESSANDO
- ENVIADO
- ENTREGUE
- CANCELADO
- DEVOLVIDO

### FormaPagamento
- CARTAO_CREDITO
- CARTAO_DEBITO
- PIX
- BOLETO
- TRANSFERENCIA

### StatusPagamento
- PENDENTE
- PROCESSANDO
- APROVADO
- REJEITADO
- CANCELADO
- ESTORNADO

### TipoFrete
- ECONOMICO
- PADRAO
- EXPRESSO
- URGENTE

### StatusFrete
- PENDENTE
- COLETADO
- EM_TRANSITO
- ENTREGUE
- DEVOLVIDO
- CANCELADO

### TipoRecomendacao
- BASEADA_USUARIO
- BASEADA_ITEM
- COLABORATIVA
- CONTEUDO
- HIBRIDA

### StatusRecomendacao
- ATIVA
- INATIVA
- EXCLUIDA
