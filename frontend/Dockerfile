# Dockerfile para Frontend ReactJS
# Build da aplicação React com Vite

FROM node:20-alpine

WORKDIR /app

# Copiar package.json e package-lock.json
COPY app/package*.json ./

# Instalar dependências
RUN npm ci

# Copiar todo o código fonte
COPY app/ .

# Build da aplicação
RUN npm run build

# Expor porta
EXPOSE 3000

# Comando para servir a aplicação em preview mode
CMD npx vite preview --host 0.0.0.0 --port 3000