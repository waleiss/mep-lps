# Dockerfile para o microserviço de Carrinho
# Imagem base Python com FastAPI
# Configuração para produção

FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar arquivos de configuração
COPY pyproject.toml ./

# Instalar dependências Python
RUN pip install --no-cache-dir -e .

# Copiar código fonte
COPY . .

# Expor porta
EXPOSE 8003

# Comando para executar a aplicação
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8003"]