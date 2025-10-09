-- Inicialização do banco de dados PostgreSQL para Recommendation Service
-- Criação de usuários e permissões básicas

-- Criar usuário específico para o serviço
CREATE USER recommendation_user WITH PASSWORD 'recommendation_pass';

-- Conceder permissões
GRANT ALL PRIVILEGES ON DATABASE mundo_palavras_recommendations TO recommendation_user;
GRANT ALL PRIVILEGES ON SCHEMA public TO recommendation_user;

-- Comentário sobre o banco
COMMENT ON DATABASE mundo_palavras_recommendations IS 'Banco de dados para o microserviço de Recommendations';
