# 📚 Recommendation Service - Mundo em Palavras

Microserviço responsável por gerar recomendações personalizadas de livros baseadas em múltiplos critérios de similaridade e popularidade.

## 🎯 Funcionalidades

### Principais Features
- ✅ **Recomendações Personalizadas**: Sugestões baseadas em preferências do usuário
- ✅ **Livros Similares**: Recomendações baseadas em autor e categoria
- ✅ **Recomendações por Autor**: Livros do mesmo autor
- ✅ **Recomendações por Categoria**: Livros da mesma categoria
- ✅ **Livros Populares**: Novidades e best-sellers

### Algoritmos de Recomendação

#### 1. Similaridade por Autor (Score: 0.9)
- Busca livros do mesmo autor
- Maior peso de relevância
- Ideal para leitores que gostam de autores específicos

#### 2. Similaridade por Categoria (Score: 0.7)
- Busca livros da mesma categoria/gênero
- Peso médio de relevância
- Ideal para explorar o mesmo gênero literário

#### 3. Popularidade (Score: variável)
- Livros mais recentes
- Tendências de leitura
- Best-sellers

## 🔗 Endpoints da API

### Base URL
```
http://localhost:8007/api/v1
```

### 1. Obter Recomendações Personalizadas

**GET** `/recomendacoes`

Retorna recomendações personalizadas para um usuário.

**Query Parameters:**
- `usuario_id` (int, obrigatório): ID do usuário
- `limit` (int, opcional): Número máximo de recomendações (1-50, padrão: 10)

**Exemplo de Requisição:**
```bash
curl -X GET "http://localhost:8007/api/v1/recomendacoes?usuario_id=123&limit=5"
```

**Exemplo de Resposta:**
```json
{
  "items": [
    {
      "livro_id": 1,
      "titulo": "O Senhor dos Anéis",
      "autor": "J.R.R. Tolkien",
      "preco": 89.90,
      "categoria": "Fantasia",
      "isbn": "978-0544003415",
      "estoque": 50,
      "score": 0.95,
      "motivo": "Livro popular entre os leitores",
      "tipo_recomendacao": "mais_vendidos"
    }
  ],
  "total": 5,
  "usuario_id": 123,
  "tipo_algoritmo": "hibrido"
}
```

### 2. Obter Livros Similares

**GET** `/livros/{livro_id}/similares`

Retorna livros similares a um livro específico.

**Path Parameters:**
- `livro_id` (int): ID do livro de referência

**Query Parameters:**
- `limit` (int, opcional): Número máximo de livros similares (1-50, padrão: 10)

**Exemplo de Requisição:**
```bash
curl -X GET "http://localhost:8007/api/v1/livros/1/similares?limit=5"
```

**Exemplo de Resposta:**
```json
{
  "livro_original_id": 1,
  "livro_original_titulo": "O Hobbit",
  "similares": [
    {
      "livro_id": 2,
      "titulo": "O Senhor dos Anéis",
      "autor": "J.R.R. Tolkien",
      "preco": 89.90,
      "categoria": "Fantasia",
      "isbn": "978-0544003415",
      "estoque": 50,
      "score": 0.9,
      "motivo": "Mesmo autor: J.R.R. Tolkien",
      "tipo_recomendacao": "mesmo_autor"
    },
    {
      "livro_id": 5,
      "titulo": "As Crônicas de Nárnia",
      "autor": "C.S. Lewis",
      "preco": 65.00,
      "categoria": "Fantasia",
      "isbn": "978-0066238500",
      "estoque": 30,
      "score": 0.7,
      "motivo": "Mesma categoria: Fantasia",
      "tipo_recomendacao": "mesma_categoria"
    }
  ],
  "criterio": "autor_e_categoria",
  "total": 2
}
```

### 3. Recomendações por Autor

**GET** `/livros/{livro_id}/por-autor`

Retorna livros do mesmo autor.

**Path Parameters:**
- `livro_id` (int): ID do livro de referência

**Query Parameters:**
- `limit` (int, opcional): Número máximo de recomendações (1-50, padrão: 10)

**Exemplo de Requisição:**
```bash
curl -X GET "http://localhost:8007/api/v1/livros/1/por-autor?limit=5"
```

**Exemplo de Resposta:**
```json
{
  "items": [
    {
      "livro_id": 2,
      "titulo": "O Silmarillion",
      "autor": "J.R.R. Tolkien",
      "preco": 75.00,
      "score": 0.95,
      "motivo": "Mesmo autor: J.R.R. Tolkien",
      "tipo_recomendacao": "mesmo_autor"
    }
  ],
  "total": 1,
  "criterio": "mesmo_autor",
  "autor": "J.R.R. Tolkien"
}
```

### 4. Recomendações por Categoria

**GET** `/categoria/{categoria}`

Retorna livros de uma categoria específica.

**Path Parameters:**
- `categoria` (string): Nome da categoria

**Query Parameters:**
- `limit` (int, opcional): Número máximo de recomendações (1-50, padrão: 10)
- `exclude_id` (int, opcional): ID do livro a excluir

**Exemplo de Requisição:**
```bash
curl -X GET "http://localhost:8007/api/v1/categoria/Fantasia?limit=5&exclude_id=1"
```

**Exemplo de Resposta:**
```json
{
  "items": [
    {
      "livro_id": 5,
      "titulo": "As Crônicas de Nárnia",
      "autor": "C.S. Lewis",
      "preco": 65.00,
      "score": 0.8,
      "motivo": "Mesma categoria: Fantasia",
      "tipo_recomendacao": "mesma_categoria"
    }
  ],
  "total": 1,
  "criterio": "categoria",
  "categoria": "Fantasia"
}
```

### 5. Livros Populares

**GET** `/populares`

Retorna os livros mais populares (novidades e mais vendidos).

**Query Parameters:**
- `limit` (int, opcional): Número máximo de recomendações (1-50, padrão: 10)

**Exemplo de Requisição:**
```bash
curl -X GET "http://localhost:8007/api/v1/populares?limit=10"
```

**Exemplo de Resposta:**
```json
{
  "items": [
    {
      "livro_id": 3,
      "titulo": "Duna",
      "autor": "Frank Herbert",
      "preco": 79.90,
      "score": 1.0,
      "motivo": "Livro popular entre os leitores",
      "tipo_recomendacao": "mais_vendidos"
    }
  ],
  "total": 10,
  "criterio": "popularidade"
}
```

### 6. Health Check

**GET** `/health`

Verifica o status do serviço.

**Exemplo de Requisição:**
```bash
curl -X GET "http://localhost:8007/api/v1/health"
```

**Exemplo de Resposta:**
```json
{
  "status": "healthy",
  "service": "recommendation-service"
}
```

## 🏗️ Arquitetura

### Estrutura de Diretórios
```
recommendation_service/
├── main.py                 # Aplicação FastAPI principal
├── config.py              # Configurações e variáveis de ambiente
├── database.py            # Configuração do banco de dados
├── models.py              # Modelos SQLAlchemy
├── routes.py              # Definição de rotas da API
├── repositories/          # Camada de acesso a dados
│   └── recommendation_repository.py
├── services/              # Lógica de negócio
│   └── recommendation_service.py
└── schemas/               # Schemas Pydantic
    └── recommendation_schemas.py
```

### Padrão de Arquitetura

#### Repository Pattern
```python
# repositories/recommendation_repository.py
class RecommendationRepository:
    def get_by_usuario(self, usuario_id: int)
    def get_by_livro(self, livro_id: int)
    def get_popular_books(self, limit: int)
    def create(self, recommendation: Recomendacao)
    def update(self, id: int, data: dict)
```

#### Service Layer
```python
# services/recommendation_service.py
class RecommendationService:
    async def get_recommendations_for_user(usuario_id, limit)
    async def get_similar_books(livro_id, limit)
    async def get_recommendations_by_author(livro_id, limit)
    async def get_recommendations_by_category(categoria, limit)
    async def get_popular_recommendations(limit)
```

## 🗄️ Modelo de Dados

### Tabela: recomendacoes

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | Integer | PK, auto-increment |
| usuario_id | Integer | ID do usuário |
| livro_id | Integer | ID do livro recomendado |
| score | Float | Score de relevância (0-1) |
| motivo | String | Razão da recomendação |
| tipo_recomendacao | Enum | Tipo (mesmo_autor, mesma_categoria, etc.) |
| status | Enum | Status (ativa, visualizada, ignorada) |
| data_criacao | DateTime | Data de criação |
| data_atualizacao | DateTime | Data de atualização |

### Enums

#### TipoRecomendacao
- `mesmo_autor`: Recomendação baseada no mesmo autor
- `mesma_categoria`: Recomendação baseada na mesma categoria
- `historico_compras`: Baseada em compras anteriores
- `historico_navegacao`: Baseada em navegação
- `mais_vendidos`: Livros populares
- `novidades`: Lançamentos recentes
- `colaborativa`: Filtro colaborativo

#### StatusRecomendacao
- `ativa`: Recomendação ativa
- `visualizada`: Usuário visualizou
- `clicada`: Usuário clicou
- `ignorada`: Usuário ignorou
- `comprada`: Usuário comprou

## 🔧 Configuração

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do serviço:

```env
# Application
APP_NAME=Recommendation Service
DEBUG=True

# Database
DATABASE_URL=postgresql://admin:admin1234@localhost:5437/mundo_palavras_recommendations

# External Services
CATALOG_SERVICE_URL=http://localhost:8002/api/v1

# Recommendation Settings
MAX_RECOMMENDATIONS=20
SIMILARITY_THRESHOLD=0.3
CACHE_TTL=1800
```

### Configuração do Banco de Dados

O serviço usa PostgreSQL. As tabelas são criadas automaticamente na inicialização.

**Porta do banco:** 5437

## 🚀 Como Executar

### Usando Docker (Recomendado)

```bash
# Construir e iniciar o serviço
docker-compose up -d recommendation-service

# Ver logs
docker-compose logs -f recommendation-service
```

### Execução Local

```bash
# Instalar dependências
cd backend/microservices/recommendation_service
pip install -r requirements.txt

# Executar o serviço
python main.py
```

O serviço estará disponível em: **http://localhost:8007**

## 📊 Integração com Outros Serviços

### Catalog Service
- **URL**: `http://localhost:8002/api/v1`
- **Uso**: Buscar detalhes de livros, listar por categoria/autor
- **Endpoints utilizados**:
  - `GET /livros/{id}`: Detalhes do livro
  - `GET /livros?categoria={categoria}`: Livros por categoria
  - `GET /buscar?q={termo}`: Buscar livros

## 🧪 Testes

### Testar Endpoints

```bash
# Health check
curl http://localhost:8007/api/v1/health

# Recomendações personalizadas
curl "http://localhost:8007/api/v1/recomendacoes?usuario_id=1&limit=5"

# Livros similares
curl "http://localhost:8007/api/v1/livros/1/similares?limit=5"

# Livros populares
curl "http://localhost:8007/api/v1/populares?limit=10"
```

### Acessar Documentação Interativa

- **Swagger UI**: http://localhost:8007/docs
- **ReDoc**: http://localhost:8007/redoc

## ⚡ Performance

### Otimizações Implementadas

1. **Comunicação Assíncrona**: Uso de HTTPx para chamadas assíncronas
2. **Queries Otimizadas**: SQLAlchemy com queries eficientes
3. **Limitação de Resultados**: Parâmetros de paginação
4. **Timeout em Serviços**: 3 segundos para chamadas externas

### Metas de Performance

- ✅ Tempo de resposta < 1 segundo
- ✅ Suporte a requisições concorrentes
- ✅ Fallback em caso de falha de serviços externos

## 🔐 Segurança

### Validações Implementadas

- ✅ Validação de entrada com Pydantic
- ✅ Limites de quantidade (1-50 itens)
- ✅ Tratamento de erros robusto
- ✅ Sanitização de parâmetros

### CORS

Configurado para permitir todas as origens em desenvolvimento. **Configurar adequadamente em produção**.

## 📝 Logs

O serviço gera logs para:
- Inicialização do serviço
- Conexão com banco de dados
- Erros de comunicação com serviços externos
- Requisições de API

## 🛠️ Troubleshooting

### Erro: "Livro não encontrado"
- Verificar se o livro existe no catalog service
- Conferir se o catalog service está rodando

### Erro: "Erro ao buscar livros"
- Verificar conectividade com catalog service
- Conferir logs do catalog service
- Aumentar timeout se necessário

### Banco de dados não conecta
- Verificar se PostgreSQL está rodando na porta 5437
- Conferir credenciais no arquivo .env
- Verificar se o banco `mundo_palavras_recommendations` existe

## 📚 Referências

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [HTTPx Documentation](https://www.python-httpx.org/)

## 🤝 Contribuição

Para contribuir com melhorias nos algoritmos de recomendação:

1. Adicionar novos critérios de similaridade
2. Implementar machine learning para recomendações
3. Adicionar cache para recomendações frequentes
4. Implementar filtro colaborativo

## 📄 Licença

Este projeto faz parte do sistema Mundo em Palavras - Microservices Architecture.
