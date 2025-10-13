# Catalog Service - Mundo em Palavras

## Descrição

Microserviço responsável pelo gerenciamento do catálogo de livros. Implementa operações CRUD, busca, filtros e caching com Redis.

## Arquitetura

Este serviço segue a arquitetura limpa com separação em camadas:

```
catalog_service/
├── config.py              # Configurações centralizadas
├── database.py            # Configuração do banco de dados
├── main.py               # Aplicação FastAPI
├── models.py             # Modelos ORM (SQLAlchemy)
├── routes.py             # Rotas/Endpoints da API
├── repositories/         # Camada de acesso a dados
│   └── book_repository.py
├── schemas/              # Schemas Pydantic
│   └── book_schemas.py
└── services/             # Lógica de negócio
    ├── book_service.py
    └── cache_service.py
```

## Funcionalidades Implementadas

### RF2.1 - Visualização do Catálogo
- ✅ `GET /api/v1/livros` - Lista livros com paginação
- ✅ Filtros: categoria, condição, preço
- ✅ Ordenação configurável
- ✅ Cache Redis para performance

### RF2.2 - Busca de Livros
- ✅ `GET /api/v1/buscar?q={termo}` - Busca por título, autor ou ISBN
- ✅ Busca case-insensitive
- ✅ Combinação de busca com filtros

### RF2.3 - Detalhes do Livro
- ✅ `GET /api/v1/livros/{id}` - Detalhes completos do livro
- ✅ Cache individual por livro

### RF2.4 - Filtros e Ordenação
- ✅ Filtro por categoria (ficção, não-ficção, técnico, etc.)
- ✅ Filtro por condição (novo, usado, semi-novo)
- ✅ Filtro por faixa de preço
- ✅ Ordenação por: título, autor, preço, data, estoque

### RF2.5 - Gerenciamento de Livros (Admin)
- ✅ `POST /api/v1/livros` - Criar novo livro
- ✅ `PUT /api/v1/livros/{id}` - Atualizar livro
- ✅ `DELETE /api/v1/livros/{id}` - Remover livro (soft delete)

### Endpoints Auxiliares
- ✅ `GET /api/v1/categorias` - Listar categorias disponíveis
- ✅ `GET /api/v1/condicoes` - Listar condições disponíveis

## Tecnologias

- **FastAPI**: Framework web moderno e rápido
- **SQLAlchemy**: ORM para PostgreSQL
- **Pydantic**: Validação de dados
- **Redis**: Cache para performance
- **PostgreSQL**: Banco de dados relacional

## Configuração

### Variáveis de Ambiente

```env
DATABASE_URL=postgresql://admin:admin1234@localhost:5433/mundo_palavras_catalog
REDIS_URL=redis://localhost:6379/1
CACHE_TTL=3600
ENVIRONMENT=development
DEBUG=True
```

### Instalação de Dependências

```bash
cd backend/microservices/catalog_service
pip install -r pyproject.toml
```

Ou com Poetry:
```bash
poetry install
```

### Criar Tabelas

```bash
python -c "from database import create_tables; create_tables()"
```

### Popular com Dados de Teste

```bash
python seed_data.py
```

## Executar o Serviço

### Modo Desenvolvimento

```bash
uvicorn main:app --reload --port 8002
```

### Modo Produção

```bash
uvicorn main:app --host 0.0.0.0 --port 8002
```

### Com Docker

```bash
docker-compose up catalog_service
```

## Endpoints Disponíveis

### Listar Livros
```http
GET /api/v1/livros?page=1&page_size=20&categoria=ficcao&preco_min=10&preco_max=100&order_by=preco&order_direction=asc
```

**Parâmetros:**
- `page` (int): Número da página (padrão: 1)
- `page_size` (int): Itens por página (padrão: 20, max: 100)
- `categoria` (str): ficcao, nao_ficcao, tecnico, academico, infantil, outros
- `condicao` (str): novo, usado, semi_novo
- `preco_min` (float): Preço mínimo
- `preco_max` (float): Preço máximo
- `order_by` (str): titulo, autor, preco, data_criacao, estoque
- `order_direction` (str): asc, desc

**Resposta:**
```json
{
  "items": [
    {
      "id": 1,
      "titulo": "Clean Code",
      "autor": "Robert C. Martin",
      "isbn": "9780132350884",
      "preco": 89.90,
      "estoque": 25,
      "categoria": "tecnico",
      "condicao": "novo",
      ...
    }
  ],
  "total": 100,
  "page": 1,
  "page_size": 20,
  "total_pages": 5,
  "has_next": true,
  "has_previous": false
}
```

### Buscar Livros
```http
GET /api/v1/buscar?q=python&page=1&page_size=20
```

### Obter Livro por ID
```http
GET /api/v1/livros/1
```

### Criar Livro
```http
POST /api/v1/livros
Content-Type: application/json

{
  "titulo": "Python para Iniciantes",
  "autor": "João Silva",
  "isbn": "9781234567890",
  "editora": "Tech Books",
  "ano_publicacao": 2024,
  "preco": 59.90,
  "estoque": 10,
  "categoria": "tecnico",
  "condicao": "novo",
  "sinopse": "Aprenda Python do zero"
}
```

### Atualizar Livro
```http
PUT /api/v1/livros/1
Content-Type: application/json

{
  "preco": 49.90,
  "estoque": 5
}
```

### Remover Livro
```http
DELETE /api/v1/livros/1
```

### Listar Categorias
```http
GET /api/v1/categorias
```

### Listar Condições
```http
GET /api/v1/condicoes
```

## Performance

### Cache Redis

O serviço implementa cache em dois níveis:

1. **Cache de lista**: Resultados de listagem e busca são cacheados
2. **Cache individual**: Cada livro é cacheado individualmente

**Estratégia de invalidação:**
- Cache invalidado ao criar/atualizar/deletar livros
- TTL padrão: 3600 segundos (1 hora)

**Benefícios:**
- ✅ Redução de carga no banco de dados
- ✅ Resposta < 1 segundo em requisições repetidas
- ✅ Suporte a alta concorrência

## Validações

### Validação de ISBN
- Deve ter 10 ou 13 dígitos
- Apenas números permitidos

### Validação de Categoria
- Valores permitidos: ficcao, nao_ficcao, tecnico, academico, infantil, outros

### Validação de Condição
- Valores permitidos: novo, usado, semi_novo

### Validação de Preço
- Deve ser maior ou igual a 0

## Testes

### Executar Testes Unitários
```bash
pytest tests/
```

### Cobertura de Testes
```bash
pytest --cov=. tests/
```

## Monitoramento

### Health Check
```http
GET /health
```

### Documentação Interativa

- **Swagger UI**: http://localhost:8002/docs
- **ReDoc**: http://localhost:8002/redoc

## Próximos Passos

- [ ] Implementar testes unitários e de integração
- [ ] Adicionar logs estruturados
- [ ] Implementar métricas (Prometheus)
- [ ] Adicionar rate limiting
- [ ] Implementar versionamento de API
- [ ] Adicionar suporte a imagens de livros
- [ ] Implementar busca avançada (Elasticsearch)

## Requisitos Atendidos

### Funcionais
- ✅ RF2.1: Visualização do catálogo de livros
- ✅ RF2.2: Busca de livros
- ✅ RF2.3: Visualização de detalhes
- ✅ RF2.4: Filtros e ordenação
- ✅ RF2.5: Gerenciamento de livros

### Não Funcionais
- ✅ RNF1.1: Performance (cache Redis)
- ✅ RNF1.2: Tempo de resposta < 1s
- ✅ RNF2.1: Arquitetura limpa
- ✅ RNF3.1: Validação de dados
