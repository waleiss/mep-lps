-- Script para atualizar usuário existente para tipo ADMIN
-- Execute este script no banco postgres-users

-- Atualizar usuário admin@mundopalavras.com para tipo admin
UPDATE usuarios 
SET tipo = 'admin' 
WHERE email = 'admin@mundopalavras.com';

-- Verificar se funcionou
SELECT id, nome, email, tipo, ativo 
FROM usuarios 
WHERE email LIKE '%admin%';
