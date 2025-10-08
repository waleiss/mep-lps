# Mundo em Palavras - E-commerce de Livros

## 📚 Visão Geral
Sistema de e-commerce especializado em venda de livros online, implementado com arquitetura de microserviços para alta escalabilidade e manutenibilidade.

## 🏗️ Arquitetura
O sistema segue a arquitetura de microserviços com os seguintes componentes:

### Frontend
- **ReactJS**: Interface web responsiva
- **Porta**: 3000

### API Gateway
- **Nginx/Kong**: Roteamento e autenticação
- **Porta**: 8080

### Microserviços (FastAPI)
- **Auth Service**: Autenticação e usuários (8001)
- **Catalog Service**: Catálogo e busca (8002)
- **Cart Service**: Carrinho de compras (8003)
- **Shipping Service**: Cálculo de frete (8004)
- **Payment Service**: Processamento de pagamentos (8005)
- **Order Service**: Gerenciamento de pedidos (8006)
- **Recommendation Service**: Sistema de recomendações (8007)

### Bancos de Dados
- **PostgreSQL Users**: Dados de usuários (5432)
- **PostgreSQL Catalog**: Catálogo de livros (5433)
- **PostgreSQL Cart**: Carrinho de compras (5434)
- **PostgreSQL Orders**: Pedidos (5435)
- **PostgreSQL Payments**: Pagamentos (5436)
- **Redis Cache**: Cache compartilhado (6379)

## 🚀 Como Executar

### Pré-requisitos
- Docker
- Docker Compose
- Python 3.9+ (para desenvolvimento local)
- Node.js 18+ (para frontend)

### Setup Automático (Recomendado)
```bash
./setup.sh
```

O script `setup.sh` irá:
1. ✅ Verificar dependências (Docker, Docker Compose)
2. 📁 Criar diretórios necessários
3. 🐍 Criar/recriar ambiente virtual Python (.venv)
4. ⚙️ Criar arquivo .env a partir do env.example
5. 📦 Instalar dependências do frontend (npm install)
6. 🐍 Instalar dependências Python globais e dos microserviços
7. 🐳 Construir imagens Docker
8. 🚀 Iniciar todos os serviços

### Desenvolvimento Local
```bash
# Ativar ambiente virtual
source activate.sh

# Executar um microserviço individualmente
cd backend/microservices/auth_service
uvicorn main:app --reload --port 8001

# Executar frontend
cd frontend
npm run dev
```

### Setup Manual
```bash
# Construir imagens
docker-compose build

# Iniciar serviços
docker-compose up -d

# Verificar status
docker-compose ps
```

## 📋 Funcionalidades

### Requisitos Funcionais Implementados
- **RF1**: Cadastro e login de usuários
- **RF2**: Catálogo de livros com busca e filtros
- **RF3**: Carrinho de compras completo
- **RF4**: Checkout com frete e pagamento
- **RF5**: Sistema de recomendações

### Requisitos Não Funcionais
- **RNF1**: Performance otimizada (< 3s carregamento)
- **RNF2**: Segurança com HTTPS e JWT
- **RNF3**: Interface responsiva e intuitiva

## 🔧 Tecnologias

### Backend
- **FastAPI**: Framework Python para APIs
- **PostgreSQL**: Banco de dados relacional
- **Redis**: Cache em memória
- **Docker**: Containerização

### Frontend
- **ReactJS**: Framework JavaScript
- **Vite**: Build tool moderno
- **Axios**: Cliente HTTP
- **CSS3**: Styling responsivo

### Infraestrutura
- **Docker Compose**: Orquestração de containers
- **Nginx**: API Gateway e proxy reverso
- **Linux**: Sistema operacional base

## 📁 Estrutura do Projeto
```
mundo-em-palavras/
├── backend/               # Backend completo
│   ├── microservices/     # Microserviços FastAPI
│   │   ├── auth_service/
│   │   ├── catalog_service/
│   │   ├── cart_service/
│   │   ├── shipping_service/
│   │   ├── payment_service/
│   │   ├── order_service/
│   │   └── recommendation_service/
│   ├── api_gateway/       # Nginx/Kong
│   ├── databases/         # Scripts de banco de dados
│   └── README.md
├── frontend/              # Aplicação ReactJS
├── docker-compose.yml     # Orquestração
└── setup.sh              # Script de configuração
```

## 🔐 Credenciais Padrão
- **Usuário**: admin
- **Senha**: admin1234

## 📊 Portas dos Serviços
- Frontend: http://localhost:3000
- API Gateway: http://localhost:8080
- Auth Service: http://localhost:8001
- Catalog Service: http://localhost:8002
- Cart Service: http://localhost:8003
- Shipping Service: http://localhost:8004
- Payment Service: http://localhost:8005
- Order Service: http://localhost:8006
- Recommendation Service: http://localhost:8007

## 🛠️ Comandos Úteis
```bash
# Parar todos os serviços
docker-compose down

# Ver logs de um serviço
docker-compose logs -f [nome_do_serviço]

# Reiniciar um serviço
docker-compose restart [nome_do_serviço]

# Acessar shell de um container
docker-compose exec [nome_do_serviço] sh
```

## 📈 Escalabilidade
O sistema foi projetado para escalar horizontalmente:
- Cada microserviço pode ser escalado independentemente
- Bancos de dados separados evitam gargalos
- Cache Redis melhora performance
- API Gateway centraliza roteamento

## 🔒 Segurança
- Senhas criptografadas com bcrypt
- Comunicação HTTPS/SSL
- Proteção contra XSS e SQL Injection
- Autenticação JWT para APIs
- Rate limiting no API Gateway

## 📝 Licença
Este projeto é parte de um trabalho acadêmico para estudo de arquitetura de microserviços.