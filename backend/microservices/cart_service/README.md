# Cart Service - Mundo em Palavras

## Descrição
Microserviço responsável pelo gerenciamento do carrinho de compras do sistema Mundo em Palavras. Implementa funcionalidades de adição, remoção e atualização de itens, com cálculo dinâmico de totais e cache em Redis.

## Funcionalidades Implementadas

### RF3.1 - Adicionar item ao carrinho
- Endpoint: `POST /api/v1/carrinho/{usuario_id}/add`
- Adiciona ou incrementa quantidade de livros no carrinho
- Validação de quantidade máxima por item
- Cache automático em Redis

### RF3.2 - Remover item do carrinho
- Endpoint: `DELETE /api/v1/carrinho/{usuario_id}/remove/{livro_id}`
- Remove completamente um item do carrinho
- Atualização automática dos totais

### RF3.3 - Atualizar quantidade de item
- Endpoint: `PUT /api/v1/carrinho/{usuario_id}/update/{livro_id}`
- Atualiza quantidade de um item específico
- Quantidade 0 remove o item
- Validação de quantidade máxima

### RF3.4 - Visualizar carrinho
- Endpoint: `GET /api/v1/carrinho/{usuario_id}`
- Retorna carrinho completo com todos os itens
- Inclui resumo com totais calculados

### RF3.5 - Calcular total do carrinho
- Cálculo dinâmico de subtotal por item
- Cálculo automático do valor total
- Contador de itens no carrinho

## Arquitetura

```
cart_service/
├── config.py              # Configurações centralizadas
├── database.py            # Conexão PostgreSQL
├── models.py              # Modelos de dados (Carrinho, ItemCarrinho)
├── main.py                # Aplicação FastAPI
├── routes.py              # Endpoints da API
├── schemas/
│   ├── __init__.py
│   └── cart_schemas.py    # Schemas Pydantic
├── repositories/
│   ├── __init__.py
│   └── cart_repository.py # Camada de acesso a dados
└── services/
    ├── __init__.py
    ├── redis_service.py   # Cache Redis
    └── cart_service.py    # Lógica de negócio
```

## Tecnologias

- **Framework**: FastAPI 0.104+
- **Banco de Dados**: PostgreSQL (porta 5434)
- **Cache**: Redis (porta 6379, database 2)
- **ORM**: SQLAlchemy 2.0+
- **Validação**: Pydantic 2.0+
- **Servidor**: Uvicorn

## Modelos de Dados

### Carrinho
- `id`: Identificador único
- `usuario_id`: ID do usuário (referência externa)
- `ativo`: Status do carrinho
- `itens`: Lista de itens no carrinho
- `total_itens`: Total de unidades (calculado)
- `valor_total`: Valor total (calculado)

### ItemCarrinho
- `id`: Identificador único
- `carrinho_id`: ID do carrinho
- `livro_id`: ID do livro (referência externa ao catalog_service)
- `quantidade`: Quantidade do item
- `preco_unitario`: Preço unitário do livro
- `subtotal`: Valor do item (quantidade × preço_unitario)

## Endpoints da API

### Health Check
```
GET /api/v1/
GET /api/v1/health
```

### Carrinho
```
GET    /api/v1/carrinho/{usuario_id}
POST   /api/v1/carrinho/{usuario_id}/add
PUT    /api/v1/carrinho/{usuario_id}/update/{livro_id}
DELETE /api/v1/carrinho/{usuario_id}/remove/{livro_id}
DELETE /api/v1/carrinho/{usuario_id}/clear
```

## Exemplos de Uso

### Adicionar item ao carrinho
```bash
curl -X POST "http://localhost:8003/api/v1/carrinho/1/add" \
  -H "Content-Type: application/json" \
  -d '{
    "livro_id": 101,
    "quantidade": 2
  }'
```

### Atualizar quantidade
```bash
curl -X PUT "http://localhost:8003/api/v1/carrinho/1/update/101" \
  -H "Content-Type: application/json" \
  -d '{
    "quantidade": 5
  }'
```

### Remover item
```bash
curl -X DELETE "http://localhost:8003/api/v1/carrinho/1/remove/101"
```

### Visualizar carrinho
```bash
curl -X GET "http://localhost:8003/api/v1/carrinho/1"
```

## Configuração

### Variáveis de Ambiente
Crie um arquivo `.env` no diretório do serviço:

```env
# Database
DATABASE_URL=postgresql://admin:admin1234@localhost:5434/mundo_palavras_cart

# Redis
REDIS_URL=redis://localhost:6379/2
REDIS_TTL=86400

# API
DEBUG=True
ALLOWED_ORIGINS=["http://localhost:3000", "http://localhost:5173"]

# Cart Settings
MAX_QUANTITY_PER_ITEM=99
CART_EXPIRATION_DAYS=30
```

## Instalação

### Usando pip
```bash
cd backend/microservices/cart_service
pip install -e .
```

### Usando Poetry
```bash
cd backend/microservices/cart_service
poetry install
```

## Execução

### Modo Desenvolvimento
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8003
```

### Modo Produção
```bash
uvicorn main:app --host 0.0.0.0 --port 8003 --workers 4
```

### Docker
```bash
docker-compose up cart-service
```

## Cache Redis

O serviço utiliza Redis para cache de sessão do carrinho:

- **TTL Padrão**: 24 horas (86400 segundos)
- **Database**: 2 (separado de outros serviços)
- **Sincronização**: Automática após cada operação
- **Fallback**: Se Redis indisponível, usa apenas PostgreSQL

### Chaves Redis
- Formato: `cart:user:{usuario_id}`
- Dados: JSON serializado do carrinho completo

## Integração com Outros Serviços

### Catalog Service (Futuro)
- Buscar preço atual do livro
- Validar disponibilidade em estoque
- Obter informações do produto

### Auth Service (Futuro)
- Validar autenticação do usuário
- Verificar permissões

### Order Service (Futuro)
- Transferir itens do carrinho para pedido
- Limpar carrinho após checkout

## Performance

- **RNF1.1**: Cache Redis para sessões de carrinho
- **Pool de Conexões**: 10 conexões ativas, até 20 overflow
- **Índices**: Otimizados para consultas por usuario_id e livro_id

## Testes

```bash
# Instalar dependências de desenvolvimento
pip install -e ".[dev]"

# Executar testes
pytest

# Com coverage
pytest --cov=. --cov-report=html
```

## Documentação da API

Após iniciar o serviço, acesse:
- **Swagger UI**: http://localhost:8003/docs
- **ReDoc**: http://localhost:8003/redoc

## Status do Desenvolvimento

✅ Task 5 - Serviço de Carrinho de Compras - **CONCLUÍDA**

### Implementado
- ✅ Configuração completa do serviço
- ✅ Modelos de dados (Carrinho, ItemCarrinho)
- ✅ Repository pattern para acesso a dados
- ✅ Service layer com lógica de negócio
- ✅ Cache Redis para sessões
- ✅ Endpoints REST completos
- ✅ Cálculo dinâmico de totais
- ✅ Validações e tratamento de erros
- ✅ Documentação automática (OpenAPI)

### Próximos Passos
- [ ] Integração com Catalog Service para buscar preços
- [ ] Middleware de autenticação
- [ ] Testes unitários e de integração
- [ ] Validação de estoque antes de adicionar item
- [ ] Logs estruturados
- [ ] Métricas e monitoramento

## Contribuindo

Siga os padrões estabelecidos no auth_service:
- Arquitetura em camadas (routes → services → repositories)
- Separação de responsabilidades
- Type hints em todas as funções
- Docstrings completas
- Tratamento de erros consistente

## Licença

Projeto acadêmico - Linha de Produto de Software (LPS)
