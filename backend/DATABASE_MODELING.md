# Modelagem do Banco de Dados - Sistema de E-commerce

## Visão Geral

Este documento descreve a implementação da modelagem do banco de dados para o sistema de e-commerce baseado em microserviços. A modelagem foi implementada seguindo o padrão de arquitetura de microserviços, onde cada serviço possui seu próprio banco de dados.

## Estrutura dos Microserviços

### 1. Auth Service (Banco: postgres_users)
**Responsabilidade**: Gerenciamento de usuários e endereços

**Modelos**:
- `Usuario`: Informações dos usuários do sistema
- `Endereco`: Endereços de entrega dos usuários

**Enums**:
- `TipoUsuario`: CLIENTE, ADMIN, VENDEDOR

### 2. Catalog Service (Banco: postgres_catalog)
**Responsabilidade**: Catálogo de livros

**Modelos**:
- `Livro`: Informações dos livros disponíveis

**Enums**:
- `Categoria`: FICCAO, NAO_FICCAO, TECNICO, ACADEMICO, INFANTIL, OUTROS
- `CondicaoLivro`: NOVO, USADO, SEMI_NOVO

### 3. Cart Service (Banco: postgres_cart)
**Responsabilidade**: Carrinho de compras

**Modelos**:
- `Carrinho`: Carrinho de compras do usuário
- `ItemCarrinho`: Itens adicionados ao carrinho

### 4. Order Service (Banco: postgres_orders)
**Responsabilidade**: Gestão de pedidos

**Modelos**:
- `Pedido`: Pedidos realizados pelos usuários
- `ItemPedido`: Itens de cada pedido

**Enums**:
- `StatusPedido`: PENDENTE, CONFIRMADO, PROCESSANDO, ENVIADO, ENTREGUE, CANCELADO, DEVOLVIDO

### 5. Payment Service (Banco: postgres_payments)
**Responsabilidade**: Processamento de pagamentos

**Modelos**:
- `Pagamento`: Transações de pagamento

**Enums**:
- `FormaPagamento`: CARTAO_CREDITO, CARTAO_DEBITO, PIX, BOLETO, TRANSFERENCIA
- `StatusPagamento`: PENDENTE, PROCESSANDO, APROVADO, REJEITADO, CANCELADO, ESTORNADO

### 6. Shipping Service (Banco: postgres_shipping)
**Responsabilidade**: Gestão de fretes

**Modelos**:
- `Frete`: Informações de envio e rastreamento

**Enums**:
- `TipoFrete`: ECONOMICO, PADRAO, EXPRESSO, URGENTE
- `StatusFrete`: PENDENTE, COLETADO, EM_TRANSITO, ENTREGUE, DEVOLVIDO, CANCELADO

### 7. Recommendation Service (Banco: postgres_recommendations)
**Responsabilidade**: Sistema de recomendações

**Modelos**:
- `Recomendacao`: Recomendações de livros para usuários

**Enums**:
- `TipoRecomendacao`: BASEADA_USUARIO, BASEADA_ITEM, COLABORATIVA, CONTEUDO, HIBRIDA
- `StatusRecomendacao`: ATIVA, INATIVA, EXCLUIDA

## Relacionamentos Entre Modelos

### Relacionamentos Principais:
- `Usuario` 1:N `Endereco`
- `Usuario` 1:N `Carrinho`
- `Usuario` 1:N `Pedido`
- `Usuario` 1:N `Pagamento`
- `Usuario` 1:N `Recomendacao`
- `Carrinho` 1:N `ItemCarrinho`
- `Pedido` 1:N `ItemPedido`
- `Pedido` 1:N `Pagamento`
- `Pedido` 1:N `Frete`
- `Livro` 1:N `ItemCarrinho`
- `Livro` 1:N `ItemPedido`
- `Livro` 1:N `Recomendacao`
- `Endereco` 1:N `Pedido` (endereco_entrega)
- `Endereco` 1:N `Frete` (endereco_destino)

## Configuração e Uso

### 1. Configuração do Banco de Dados

Cada microserviço possui sua própria configuração de banco de dados no arquivo `database.py`:

```python
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres:postgres@localhost:5432/postgres_[service_name]"
)
```

### 2. Criação das Tabelas

Para criar as tabelas de um microserviço específico:

```bash
cd backend/microservices/[service_name]
python -c "from database import create_tables; create_tables()"
```

### 3. Execução das Migrations (Alembic)

Para executar migrations em um microserviço:

```bash
cd backend/microservices/[service_name]
alembic upgrade head
```

### 4. Popular Dados de Exemplo

#### Executar seed de um microserviço específico:
```bash
cd backend/microservices/[service_name]
python seed_data.py
```

#### Executar seed de todos os microserviços:
```bash
cd backend
python seed_all_services.py
```

## Dados de Exemplo Incluídos

### Usuários:
- 4 usuários (2 clientes, 1 admin, 1 vendedor)
- Senha padrão: `123456` (hash bcrypt)

### Livros:
- 8 livros de diferentes categorias
- Preços variados de R$ 19,90 a R$ 89,90
- Diferentes condições (novo, usado)

### Pedidos:
- 3 pedidos com diferentes status
- Itens de pedido associados

### Pagamentos:
- 3 pagamentos com diferentes formas
- Status variados (aprovado, processando)

### Fretes:
- 3 fretes com diferentes tipos
- Códigos de rastreamento

### Recomendações:
- 5 recomendações usando diferentes algoritmos
- Scores de similaridade

## Estrutura de Arquivos

```
backend/
├── microservices/
│   ├── auth_service/
│   │   ├── models.py          # Modelos Usuario e Endereco
│   │   ├── database.py        # Configuração do banco
│   │   ├── seed_data.py       # Script de seed
│   │   └── alembic/           # Configuração de migrations
│   ├── catalog_service/
│   │   ├── models.py          # Modelo Livro
│   │   ├── database.py        # Configuração do banco
│   │   └── seed_data.py       # Script de seed
│   └── ... (outros serviços)
├── seed_all_services.py       # Script principal de seed
└── DATABASE_MODELING.md       # Este arquivo
```

## Próximos Passos

1. **Configurar variáveis de ambiente** para as URLs dos bancos de dados
2. **Executar migrations** em cada microserviço
3. **Popular dados de exemplo** usando os scripts de seed
4. **Implementar APIs REST** para cada microserviço
5. **Configurar comunicação** entre microserviços
6. **Implementar autenticação** e autorização
7. **Adicionar testes** para os modelos e relacionamentos

## Considerações Técnicas

- **Isolamento de dados**: Cada microserviço possui seu próprio banco
- **Consistência eventual**: Relacionamentos entre microserviços são mantidos via IDs
- **Performance**: Índices criados em campos frequentemente consultados
- **Segurança**: Senhas criptografadas com bcrypt
- **Auditoria**: Campos de data de criação e atualização em todos os modelos
- **Soft delete**: Campo `ativo` para exclusão lógica
