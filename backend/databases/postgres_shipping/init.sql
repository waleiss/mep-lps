-- Inicialização do banco de dados PostgreSQL para Shipping Service
-- Criação de usuários e permissões básicas

-- Criar usuário específico para o serviço
CREATE USER shipping_user WITH PASSWORD 'shipping_pass';

-- Conceder permissões
GRANT ALL PRIVILEGES ON DATABASE mundo_palavras_shipping TO shipping_user;
GRANT ALL PRIVILEGES ON SCHEMA public TO shipping_user;

-- Comentário sobre o banco
COMMENT ON DATABASE mundo_palavras_shipping IS 'Banco de dados para o microserviço de Shipping/Frete';
