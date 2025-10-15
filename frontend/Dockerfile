# Dockerfile para Frontend ReactJS
# Imagem base Node.js com Vite para build
# Configuração para produção

FROM node:18-alpine

WORKDIR /app

COPY app/package*.json ./

RUN npm install

COPY app/ .

RUN npm run build

EXPOSE 3000

CMD ["npm", "run", "preview"]