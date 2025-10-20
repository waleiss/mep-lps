# Backend - Mundo em Palavras

## Visão Geral
O backend do sistema "Mundo em Palavras" é implementado seguindo a arquitetura de microserviços, onde cada funcionalidade é um serviço independente e escalável.

## Estrutura do Projeto
```
backend/
├── microservices/          # Microserviços FastAPI
│   ├── auth_service/       # Autenticação e usuários
│   ├── catalog_service/    # Catálogo de livros
│   ├── cart_service/       # Carrinho de compras
│   ├── shipping_service/   # Cálculo de frete
│   ├── payment_service/    # Processamento de pagamentos
│   ├── order_service/      # Gerenciamento de pedidos
│   └── recommendation_service/ # Sistema de recomendações
├── api_gateway/            # Nginx/Kong para roteamento
├── databases/              # Scripts de banco de dados
│   ├── postgres_users/     # Banco de usuários
│   ├── postgres_catalog/   # Banco de catálogo
│   ├── postgres_cart/      # Banco de carrinho
│   ├── postgres_orders/    # Banco de pedidos
│   ├── postgres_payments/  # Banco de pagamentos
│   └── redis/              # Configuração Redis
└── README.md
```

## Arquitetura
- **API Gateway**: Nginx/Kong para roteamento e autenticação
- **Microserviços**: 7 serviços independentes em FastAPI
- **Bancos de Dados**: PostgreSQL para persistência e Redis para cache
- **Containerização**: Docker para padronização de ambientes

## Microserviços

### 1. Auth Service (Porta 8001)
- **Função**: Gerenciamento de usuários e autenticação
- **Banco**: PostgreSQL Users
- **Endpoints**: /register, /login, /recover-password, /profile

### 2. Catalog Service (Porta 8002)
- **Função**: Catálogo de livros, busca e filtros
- **Banco**: PostgreSQL Catalog + Redis Cache
- **Endpoints**: /books, /search, /filters, /details

### 3. Cart Service (Porta 8003)
- **Função**: Carrinho de compras
- **Banco**: PostgreSQL Cart + Redis Cache
- **Endpoints**: /add-item, /remove-item, /update-quantity

### 4. Shipping Service (Porta 8004)
- **Função**: Cálculo de frete e endereços
- **Integração**: API Correios
- **Endpoints**: /calculate-shipping, /addresses

### 5. Payment Service (Porta 8005)
- **Função**: Processamento de pagamentos
- **Banco**: PostgreSQL Payments
- **Integração**: Gateway de pagamento
- **Endpoints**: /process-payment, /payment-methods

### 6. Order Service (Porta 8006)
- **Função**: Gerenciamento de pedidos
- **Banco**: PostgreSQL Orders
- **Endpoints**: /orders, /order-history, /confirmation

### 7. Recommendation Service (Porta 8007)
- **Função**: Sistema de recomendações
- **Banco**: PostgreSQL + Redis Cache
- **Endpoints**: /recommendations, /related-books, /best-sellers

## Tecnologias
- **Framework**: FastAPI (Python)
- **Banco de Dados**: PostgreSQL + Redis
- **Containerização**: Docker
- **API Gateway**: Nginx
- **Autenticação**: JWT

## Como Executar
1. Execute o script de setup: `./setup.sh`
   - Instala dependências do frontend (npm install)
   - Instala dependências Python globais (pyproject.toml)
   - Instala dependências de cada microserviço
   - Constrói imagens Docker
   - Inicia todos os serviços
2. Acesse os serviços nas portas indicadas
3. Use as credenciais padrão: admin/admin1234

## Gerenciamento de Dependências
- **Global**: `backend/pyproject.toml` - Dependências compartilhadas
- **Microserviços**: Cada serviço tem seu próprio `pyproject.toml`
- **Frontend**: `frontend/package.json` - Dependências Node.js

## Estrutura de Dados
Cada microserviço possui seu próprio banco de dados PostgreSQL, garantindo isolamento e independência. O Redis é usado para cache compartilhado entre os serviços.

## Segurança
- Senhas criptografadas com bcrypt
- Comunicação HTTPS/SSL
- Proteção contra XSS e SQL Injection
- Autenticação JWT para APIs
