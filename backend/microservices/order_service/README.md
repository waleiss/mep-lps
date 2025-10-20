# Order Service - Mundo em Palavras

## Descrição

Microserviço responsável pelo gerenciamento de pedidos. Implementa operações de criação, consulta, atualização de status e histórico de pedidos.

## Arquitetura

Este serviço segue a arquitetura limpa com separação em camadas:

```
order_service/
├── config.py              # Configurações centralizadas
├── database.py            # Configuração do banco de dados
├── main.py               # Aplicação FastAPI
├── models.py             # Modelos ORM (SQLAlchemy)
├── routes.py             # Rotas/Endpoints da API
├── repositories/         # Camada de acesso a dados
│   └── order_repository.py
├── schemas/              # Schemas Pydantic
│   └── order_schemas.py
└── services/             # Lógica de negócio
    ├── order_service.py
    └── order_number_service.py
```

## Funcionalidades Implementadas

### RF4.4 - Criação de Pedidos
- ✅ `POST /api/v1/pedidos` - Criar pedido manualmente
- ✅ `POST /api/v1/pedidos/from-cart` - Criar pedido a partir do carrinho
- ✅ Geração automática de número de pedido (formato: MP-YYYYMMDD-NNNN)
- ✅ Validação de pagamento confirmado
- ✅ Cálculo automático de total e frete

### RF4.5 - Consulta de Pedidos
- ✅ `GET /api/v1/pedidos/{id}` - Detalhes do pedido por ID
- ✅ `GET /api/v1/pedidos/numero/{numero_pedido}` - Detalhes por número
- ✅ `GET /api/v1/historico/{usuario_id}` - Histórico do usuário
- ✅ `GET /api/v1/pedidos` - Listar todos (Admin)
- ✅ Filtros por status
- ✅ Paginação completa

### RF4.6 - Gerenciamento de Pedidos
- ✅ `PATCH /api/v1/pedidos/{id}/status` - Atualizar status
- ✅ Status: pendente, confirmado, processando, enviado, entregue, cancelado, devolvido
- ✅ Registro automático de data de entrega
- ✅ Associação com pagamento e frete

### Integrações com Outros Microserviços
- ✅ **Catalog Service**: Buscar detalhes dos livros
- ✅ **Cart Service**: Obter itens do carrinho
- ✅ **Payment Service**: Verificar pagamento confirmado
- ✅ **Shipping Service**: Calcular frete

## Tecnologias

- **FastAPI**: Framework web moderno e rápido
- **SQLAlchemy**: ORM para PostgreSQL
- **Pydantic**: Validação de dados
- **HTTPx**: Cliente HTTP assíncrono
- **PostgreSQL**: Banco de dados relacional

## Configuração

### Variáveis de Ambiente

```env
DATABASE_URL=postgresql://admin:admin1234@localhost:5435/mundo_palavras_orders
ENVIRONMENT=development
DEBUG=True
ORDER_NUMBER_PREFIX=MP

# URLs dos Microserviços
CATALOG_SERVICE_URL=http://localhost:8002/api/v1
CART_SERVICE_URL=http://localhost:8003/api/v1
PAYMENT_SERVICE_URL=http://localhost:8005/api/v1
SHIPPING_SERVICE_URL=http://localhost:8006/api/v1
```

### Instalação de Dependências

```bash
cd backend/microservices/order_service
pip install -e .
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
uvicorn main:app --reload --port 8004
```

### Modo Produção

```bash
uvicorn main:app --host 0.0.0.0 --port 8004
```

### Com Docker

```bash
docker-compose up order-service
```

## Endpoints Disponíveis

### Criar Pedido Manual
```http
POST /api/v1/pedidos
Content-Type: application/json

{
  "usuario_id": 1,
  "endereco_entrega_id": 1,
  "valor_frete": 15.50,
  "observacoes": "Entregar pela manhã",
  "items": [
    {
      "livro_id": 1,
      "quantidade": 2,
      "preco_unitario": 45.90
    },
    {
      "livro_id": 2,
      "quantidade": 1,
      "preco_unitario": 32.50
    }
  ]
}
```

**Resposta:**
```json
{
  "id": 1,
  "numero_pedido": "MP-20241016-0001",
  "usuario_id": 1,
  "endereco_entrega_id": 1,
  "status": "pendente",
  "valor_total": 139.80,
  "valor_frete": 15.50,
  "observacoes": "Entregar pela manhã",
  "data_criacao": "2024-10-16T14:30:00",
  "data_entrega_prevista": "2024-10-23T14:30:00",
  "items": [
    {
      "id": 1,
      "livro_id": 1,
      "quantidade": 2,
      "preco_unitario": 45.90,
      "subtotal": 91.80
    },
    {
      "id": 2,
      "livro_id": 2,
      "quantidade": 1,
      "preco_unitario": 32.50,
      "subtotal": 32.50
    }
  ]
}
```

### Criar Pedido do Carrinho
```http
POST /api/v1/pedidos/from-cart
Content-Type: application/json

{
  "usuario_id": 1,
  "endereco_entrega_id": 1,
  "pagamento_id": 1,
  "observacoes": "Entregar pela manhã"
}
```

### Obter Pedido por ID
```http
GET /api/v1/pedidos/1
```

### Obter Pedido por Número
```http
GET /api/v1/pedidos/numero/MP-20241016-0001
```

### Histórico de Pedidos do Usuário
```http
GET /api/v1/historico/1?page=1&page_size=20&status=confirmado
```

**Parâmetros:**
- `page` (int): Número da página (padrão: 1)
- `page_size` (int): Itens por página (padrão: 20, max: 100)
- `status` (str): Filtrar por status

### Listar Todos os Pedidos (Admin)
```http
GET /api/v1/pedidos?page=1&page_size=20&status=processando
```

### Atualizar Status do Pedido
```http
PATCH /api/v1/pedidos/1/status
Content-Type: application/json

{
  "status": "enviado"
}
```

**Status válidos:**
- `pendente`: Pedido criado, aguardando confirmação
- `confirmado`: Pedido confirmado, pronto para processamento
- `processando`: Pedido sendo preparado
- `enviado`: Pedido despachado para entrega
- `entregue`: Pedido entregue ao cliente
- `cancelado`: Pedido cancelado
- `devolvido`: Pedido devolvido

## Geração de Número de Pedido

O serviço gera automaticamente números de pedido únicos no formato:

```
MP-YYYYMMDD-NNNN
```

Onde:
- `MP`: Prefixo configurável (Mundo em Palavras)
- `YYYYMMDD`: Data de criação
- `NNNN`: Número sequencial do dia (0001, 0002, etc.)

Exemplo: `MP-20241016-0001`

## Fluxo de Criação de Pedido

1. **Cliente finaliza compra**
   - Pagamento é processado
   - Status: "confirmado"

2. **Pedido é criado**
   - Itens do carrinho são convertidos em itens do pedido
   - Número de pedido é gerado
   - Frete é calculado
   - Status: "pendente" ou "confirmado"

3. **Pedido é processado**
   - Separação de produtos
   - Status: "processando"

4. **Pedido é enviado**
   - Despachado para entrega
   - Status: "enviado"
   - Data de entrega prevista

5. **Pedido é entregue**
   - Cliente recebe o pedido
   - Status: "entregue"
   - Data de entrega realizada registrada

## Validações

### Validação de Criação
- Pedido deve ter pelo menos um item
- Pagamento deve estar confirmado (quando criado do carrinho)
- Carrinho não pode estar vazio

### Validação de Status
- Status deve ser um dos valores válidos
- Transições de status seguem lógica de negócio

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

- **Swagger UI**: http://localhost:8004/docs
- **ReDoc**: http://localhost:8004/redoc

## Próximos Passos

- [ ] Implementar testes unitários e de integração
- [ ] Adicionar notificações (email/SMS) de status
- [ ] Implementar retry logic para integrações
- [ ] Adicionar circuit breaker para serviços externos
- [ ] Implementar logs estruturados
- [ ] Adicionar métricas (Prometheus)
- [ ] Implementar rastreamento de pedidos
- [ ] Adicionar webhooks de status

## Requisitos Atendidos

### Funcionais
- ✅ RF4.4: Criação de pedidos
- ✅ RF4.5: Consulta de pedidos e histórico
- ✅ RF4.6: Gerenciamento de status

### Não Funcionais
- ✅ RNF2.1: Arquitetura limpa e modular
- ✅ RNF3.1: Validação de dados
- ✅ RNF4.1: Integração com outros microserviços
- ✅ RNF5.1: Documentação completa

## Dependências de Outros Serviços

- **Payment Service**: Verificação de pagamento confirmado
- **Cart Service**: Obtenção de itens do carrinho
- **Catalog Service**: Detalhes dos livros
- **Shipping Service**: Cálculo de frete
