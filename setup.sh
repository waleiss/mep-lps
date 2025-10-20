#!/bin/bash

# Script de Setup - Mundo em Palavras
# Configuração inicial do ambiente de desenvolvimento
# Instala dependências e inicia os serviços

echo "🚀 Configurando Mundo em Palavras - E-commerce de Livros"
echo "=================================================="

# Verificar se Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não está instalado. Por favor, instale o Docker primeiro."
    exit 1
fi

# Verificar se Docker está rodando
echo "🔍 Verificando se Docker está rodando..."
if ! docker info >/dev/null 2>&1; then
    echo "❌ Docker não está rodando!"
    echo "💡 Por favor, inicie o Docker Desktop e tente novamente."
    echo "💡 Aguarde alguns segundos após iniciar o Docker Desktop."
    exit 1
fi

# Verificar se Docker Compose está instalado
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose não está instalado. Por favor, instale o Docker Compose primeiro."
    exit 1
fi

# Verificar se Python está instalado
if ! command -v python &> /dev/null; then
    echo "❌ Python não está instalado. Por favor, instale o Python 3.9+ primeiro."
    exit 1
fi

# Verificar se pip está instalado
if ! command -v pip &> /dev/null; then
    echo "❌ pip não está instalado. Por favor, instale o pip primeiro."
    exit 1
fi

echo "✅ Docker e Docker Compose encontrados"
echo "✅ Python encontrado"

# Verificar Node.js (opcional)
if command -v npm &> /dev/null; then
    echo "✅ Node.js encontrado"
else
    echo "⚠️  Node.js não encontrado - frontend será executado via Docker"
fi

# Criar diretórios necessários
echo "📁 Criando diretórios necessários..."
mkdir -p logs
mkdir -p backend/data/postgres_users
mkdir -p backend/data/postgres_catalog
mkdir -p backend/data/postgres_cart
mkdir -p backend/data/postgres_orders
mkdir -p backend/data/postgres_payments
mkdir -p backend/data/redis

# Definir permissões
chmod 755 backend/data/postgres_*
chmod 755 backend/data/redis

echo "✅ Diretórios criados com sucesso"

# Criar/recriar ambiente virtual Python
echo "🐍 Configurando ambiente virtual Python..."
if [ -d ".venv" ]; then
    echo "🗑️  Removendo ambiente virtual existente..."
    rm -rf .venv
fi

echo "🆕 Criando novo ambiente virtual..."
python -m venv .venv

if [ $? -eq 0 ]; then
    echo "✅ Ambiente virtual criado com sucesso"
else
    echo "❌ Erro ao criar ambiente virtual"
    exit 1
fi

# Ativar ambiente virtual
echo "🔄 Ativando ambiente virtual..."

# Detectar sistema operacional e ativar ambiente virtual
if [ -f ".venv/Scripts/activate" ]; then
    # Windows (Git Bash)
    echo "🪟 Detectado Windows - ativando ambiente virtual..."
    source .venv/Scripts/activate
elif [ -f ".venv/bin/activate" ]; then
    # Linux/Mac
    echo "🐧 Detectado Linux/Mac - ativando ambiente virtual..."
    source .venv/bin/activate
else
    echo "❌ Arquivo de ativação do ambiente virtual não encontrado"
    echo "⚠️  Continuando sem ativar o ambiente virtual..."
    echo "💡 Para ativar manualmente no Windows: .venv\\Scripts\\activate"
    echo "💡 Para ativar manualmente no Linux/Mac: source .venv/bin/activate"
fi

if [ $? -eq 0 ]; then
    echo "✅ Ambiente virtual ativado"
else
    echo "⚠️  Ambiente virtual não foi ativado, mas continuando..."
fi

# Criar arquivo .env
echo "⚙️  Configurando arquivo .env..."
if [ -f ".env" ]; then
    echo "📋 Arquivo .env já existe, mantendo configurações existentes"
else
    if [ -f "env.example" ]; then
        cp env.example .env
        echo "✅ Arquivo .env criado a partir do env.example"
        echo "⚠️  Lembre-se de ajustar as configurações no arquivo .env conforme necessário"
    else
        echo "❌ Arquivo env.example não encontrado"
        exit 1
    fi
fi

# Instalar dependências do frontend (inclui devDependencies como TypeScript e @types/*)
echo "📦 Instalando dependências do frontend (frontend/app)..."
if command -v npm >/dev/null 2>&1; then
    cd frontend/app || { echo "❌ Diretório frontend/app não encontrado"; cd - > /dev/null; }
    if [ -f "package.json" ]; then
        # prefer deterministic install when lockfile exists
        if [ -f "package-lock.json" ] || [ -f "npm-shrinkwrap.json" ]; then
            echo "➡️  Executando: npm ci"
            npm ci --unsafe-perm
            rc=$?
        else
            echo "➡️  Executando: npm install"
            npm install --unsafe-perm
            rc=$?
        fi

        if [ $rc -eq 0 ]; then
            echo "✅ Dependências do frontend instaladas com sucesso"
            # Run a quick TypeScript build check so devDependencies (typescript, @types/...) are validated
            if command -v npx >/dev/null 2>&1; then
                echo "🧪 Executando checagem TypeScript (npx tsc -b)..."
                npx tsc -b --pretty || echo "⚠️  Checagem TypeScript retornou erro, mas continuando"
            fi
        else
            echo "❌ Erro ao instalar dependências do frontend (exit code $rc)"
            echo "⚠️  Continuando sem as dependências do frontend..."
        fi
    else
        echo "⚠️  package.json não encontrado em frontend/app"
    fi
    cd - > /dev/null
else
    echo "⚠️  npm não encontrado - pulando instalação do frontend"
    echo "💡 Para instalar Node.js: https://nodejs.org/"
    echo "💡 Ou use Docker para executar o frontend"
fi

# Instalar dependências Python globais
echo "🐍 Instalando dependências Python globais..."
if [ -f "backend/pyproject.toml" ]; then
    cd backend
    # Instalar dependências diretamente do pyproject.toml
    pip install fastapi uvicorn sqlalchemy psycopg2-binary redis python-jose[cryptography] passlib[bcrypt] pydantic python-multipart python-dotenv requests numpy scikit-learn pandas pillow stripe xmltodict zeep
    if [ $? -eq 0 ]; then
        echo "✅ Dependências Python globais instaladas com sucesso"
    else
        echo "❌ Erro ao instalar dependências Python globais"
        echo "⚠️  Continuando sem as dependências globais..."
    fi
    cd ..
else
    echo "⚠️  pyproject.toml não encontrado no backend"
fi

# Instalar dependências dos microserviços individualmente
echo "🐍 Instalando dependências dos microserviços Python..."
for service in backend/microservices/*/; do
    if [ -f "$service/pyproject.toml" ]; then
        echo "📦 Instalando dependências em $(basename $service)..."
        cd "$service"
        # Instalar dependências básicas do FastAPI
        pip install fastapi uvicorn sqlalchemy psycopg2-binary redis pydantic python-multipart python-dotenv
        if [ $? -eq 0 ]; then
            echo "✅ Dependências de $(basename $service) instaladas"
        else
            echo "❌ Erro ao instalar dependências de $(basename $service)"
        fi
        cd - > /dev/null
    fi
done

# Desativar ambiente virtual (opcional, pois o Docker usará suas próprias dependências)
echo "🔄 Desativando ambiente virtual..."
if command -v deactivate >/dev/null 2>&1; then
    deactivate
    echo "✅ Ambiente virtual desativado"
else
    echo "⚠️  Ambiente virtual não estava ativado"
fi

# Construir imagens Docker
echo "🔨 Construindo imagens Docker..."

# Verificar novamente se Docker está rodando antes de construir
if ! docker info >/dev/null 2>&1; then
    echo "❌ Docker parou de funcionar durante a execução!"
    echo "💡 Por favor, inicie o Docker Desktop e execute novamente:"
    echo "   docker-compose build"
    echo "   docker-compose up -d"
    exit 1
fi

docker-compose build

if [ $? -eq 0 ]; then
    echo "✅ Imagens construídas com sucesso"
else
    echo "❌ Erro ao construir imagens Docker"
    echo "💡 Verifique se o Docker Desktop está rodando"
    echo "💡 Tente executar manualmente: docker-compose build"
    exit 1
fi

# Iniciar serviços
echo "🚀 Iniciando serviços..."
docker-compose up -d

if [ $? -eq 0 ]; then
    echo "✅ Serviços iniciados com sucesso"
else
    echo "❌ Erro ao iniciar serviços"
    exit 1
fi

# Aguardar serviços ficarem prontos
echo "⏳ Aguardando serviços ficarem prontos..."
sleep 30

# Verificar status dos serviços
echo "🔍 Verificando status dos serviços..."
docker-compose ps

echo ""
echo "🎉 Setup concluído com sucesso!"
echo ""
echo "🐳 Imagens Docker utilizadas:"
echo "   • postgres:15-alpine (5 instâncias para bancos de dados)"
echo "   • redis:7-alpine (cache compartilhado)"
echo "   • nginx:alpine (API Gateway)"
echo "   • python:3.11-slim (7 microserviços FastAPI)"
echo "   • node:18-alpine (frontend ReactJS)"
echo ""
echo "📋 Serviços disponíveis:"
echo "   • Frontend: http://localhost:3000"
echo "   • API Gateway: http://localhost:8080"
echo "   • Auth Service: http://localhost:8001"
echo "   • Catalog Service: http://localhost:8002"
echo "   • Cart Service: http://localhost:8003"
echo "   • Shipping Service: http://localhost:8004"
echo "   • Payment Service: http://localhost:8005"
echo "   • Order Service: http://localhost:8006"
echo "   • Recommendation Service: http://localhost:8007"
echo ""
echo "🗄️ Bancos de dados:"
echo "   • PostgreSQL Users: localhost:5432"
echo "   • PostgreSQL Catalog: localhost:5433"
echo "   • PostgreSQL Cart: localhost:5434"
echo "   • PostgreSQL Orders: localhost:5435"
echo "   • PostgreSQL Payments: localhost:5436"
echo "   • Redis Cache: localhost:6379"
echo ""
echo "📚 Comandos úteis:"
echo "   • Parar serviços: docker-compose down"
echo "   • Ver logs: docker-compose logs -f [serviço]"
echo "   • Produção: docker-compose -f docker-compose.prod.yml up -d"
echo "   • Rebuild: docker-compose build --no-cache"
echo ""
echo "🔐 Credenciais padrão dos bancos:"
echo "   • Usuário: admin"
echo "   • Senha: admin1234"
echo ""
echo "🌐 Acesse o sistema em: http://localhost:3000"
echo ""
echo "📝 Notas importantes:"
echo "   • Se o Node.js não estiver instalado, o frontend será executado via Docker"
echo "   • Para desenvolvimento local do frontend, instale Node.js: https://nodejs.org/"
echo "   • Todos os microserviços funcionam independentemente via Docker"
