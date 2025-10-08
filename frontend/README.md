# Frontend - Mundo em Palavras

## Visão Geral
O frontend do sistema "Mundo em Palavras" é uma aplicação ReactJS responsiva que fornece uma interface intuitiva para o e-commerce de livros.

## Tecnologias
- **Framework**: ReactJS
- **Build Tool**: Vite
- **Roteamento**: React Router DOM
- **HTTP Client**: Axios
- **Styling**: CSS3 responsivo
- **Containerização**: Docker

## Funcionalidades Implementadas

### 1. Autenticação (RF1)
- **Login/Cadastro**: Formulários responsivos com validação
- **Recuperação de Senha**: Envio de link por email
- **Perfil do Usuário**: Edição de informações pessoais
- **Segurança**: Comunicação HTTPS com backend

### 2. Catálogo de Livros (RF2)
- **Exibição**: Lista responsiva de livros com paginação
- **Busca**: Busca por título, autor, ISBN ou palavra-chave
- **Filtros**: Filtros por gênero, preço e condição
- **Detalhes**: Página completa com informações do livro
- **Ordenação**: Ordenação por relevância, preço e título

### 3. Carrinho de Compras (RF3)
- **Adicionar Itens**: Botão em cada livro do catálogo
- **Visualização**: Lista de itens com subtotal e frete
- **Gerenciamento**: Remover itens e alterar quantidades
- **Cálculos**: Total automático da compra

### 4. Checkout (RF4)
- **Frete**: Cálculo automático por CEP
- **Endereços**: Seleção ou cadastro de endereços
- **Pagamento**: Múltiplas formas (PIX, Cartão, Boleto)
- **Confirmação**: Tela de confirmação com número do pedido
- **Histórico**: Visualização de pedidos anteriores

### 5. Recomendações (RF5)
- **Livros Relacionados**: Baseado em autor e gênero
- **Mais Vendidos**: Lista de livros populares
- **Novidades**: Lançamentos recentes

## Características de Usabilidade (RNF3)

### Design Responsivo
- **Desktop**: Layout otimizado para telas grandes
- **Tablet**: Adaptação para telas médias
- **Mobile**: Interface touch-friendly

### Performance
- **Carregamento**: Páginas carregam em menos de 3s
- **Busca**: Resultados em menos de 1s
- **Cache**: Dados em cache para melhor performance

### Experiência do Usuário
- **Navegação**: Interface intuitiva e clara
- **Mensagens**: Feedback claro para ações do usuário
- **Consistência**: Layout uniforme em todas as páginas

## Estrutura do Projeto
```
frontend/
├── src/
│   ├── components/     # Componentes reutilizáveis
│   ├── pages/         # Páginas da aplicação
│   ├── services/      # Comunicação com API
│   └── App.jsx        # Componente principal
├── public/            # Arquivos estáticos
├── package.json       # Dependências
└── Dockerfile         # Containerização
```

## Como Executar

### Desenvolvimento
```bash
npm install
npm run dev
```

### Produção
```bash
npm run build
npm run preview
```

### Docker
```bash
docker build -t mundo-em-palavras-frontend .
docker run -p 3000:3000 mundo-em-palavras-frontend
```

## Integração com Backend
O frontend se comunica com os microserviços através do API Gateway (porta 8080), que roteia as requisições para os serviços apropriados.

## Responsividade
- **Mobile First**: Design otimizado para dispositivos móveis
- **Breakpoints**: Adaptação para diferentes tamanhos de tela
- **Touch**: Interface otimizada para toque