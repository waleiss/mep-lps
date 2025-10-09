#!/usr/bin/env python3
"""
Script para popular o banco de dados com dados de exemplo
Microserviço: Auth Service
"""

import sys
import os
from datetime import datetime, date
from sqlalchemy.orm import Session

# Adicionar o diretório atual ao path para importar os módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal, engine
from models import Base, Usuario, Endereco, TipoUsuario

def create_tables():
    """Criar todas as tabelas"""
    Base.metadata.create_all(bind=engine)

def seed_usuarios():
    """Popular tabela de usuários com dados de exemplo"""
    db = SessionLocal()
    
    try:
        # Verificar se já existem usuários
        if db.query(Usuario).count() > 0:
            print("Usuários já existem no banco. Pulando seed de usuários.")
            return
        
        usuarios_data = [
            {
                "nome": "João Silva",
                "email": "joao.silva@email.com",
                "senha_hash": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8Kz8Kz2",  # senha: 123456
                "telefone": "(11) 99999-9999",
                "data_nascimento": date(1990, 5, 15),
                "tipo": TipoUsuario.CLIENTE,
                "ativo": True
            },
            {
                "nome": "Maria Santos",
                "email": "maria.santos@email.com",
                "senha_hash": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8Kz8Kz2",  # senha: 123456
                "telefone": "(11) 88888-8888",
                "data_nascimento": date(1985, 8, 22),
                "tipo": TipoUsuario.CLIENTE,
                "ativo": True
            },
            {
                "nome": "Admin Sistema",
                "email": "admin@sistema.com",
                "senha_hash": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8Kz8Kz2",  # senha: 123456
                "telefone": "(11) 77777-7777",
                "data_nascimento": date(1980, 3, 10),
                "tipo": TipoUsuario.ADMIN,
                "ativo": True
            },
            {
                "nome": "Vendedor Livros",
                "email": "vendedor@livros.com",
                "senha_hash": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8Kz8Kz2",  # senha: 123456
                "telefone": "(11) 66666-6666",
                "data_nascimento": date(1988, 12, 5),
                "tipo": TipoUsuario.VENDEDOR,
                "ativo": True
            }
        ]
        
        for user_data in usuarios_data:
            usuario = Usuario(**user_data)
            db.add(usuario)
        
        db.commit()
        print(f"Criados {len(usuarios_data)} usuários com sucesso!")
        
    except Exception as e:
        print(f"Erro ao criar usuários: {e}")
        db.rollback()
    finally:
        db.close()

def seed_enderecos():
    """Popular tabela de endereços com dados de exemplo"""
    db = SessionLocal()
    
    try:
        # Verificar se já existem endereços
        if db.query(Endereco).count() > 0:
            print("Endereços já existem no banco. Pulando seed de endereços.")
            return
        
        # Buscar usuários para associar endereços
        usuarios = db.query(Usuario).all()
        if not usuarios:
            print("Nenhum usuário encontrado. Execute primeiro o seed de usuários.")
            return
        
        enderecos_data = [
            {
                "usuario_id": usuarios[0].id,
                "logradouro": "Rua das Flores",
                "numero": "123",
                "complemento": "Apto 45",
                "bairro": "Centro",
                "cidade": "São Paulo",
                "estado": "SP",
                "cep": "01234-567",
                "principal": True
            },
            {
                "usuario_id": usuarios[0].id,
                "logradouro": "Avenida Paulista",
                "numero": "1000",
                "complemento": "",
                "bairro": "Bela Vista",
                "cidade": "São Paulo",
                "estado": "SP",
                "cep": "01310-100",
                "principal": False
            },
            {
                "usuario_id": usuarios[1].id,
                "logradouro": "Rua da Consolação",
                "numero": "456",
                "complemento": "Casa 2",
                "bairro": "Consolação",
                "cidade": "São Paulo",
                "estado": "SP",
                "cep": "01302-000",
                "principal": True
            },
            {
                "usuario_id": usuarios[2].id,
                "logradouro": "Rua Augusta",
                "numero": "789",
                "complemento": "",
                "bairro": "Consolação",
                "cidade": "São Paulo",
                "estado": "SP",
                "cep": "01305-000",
                "principal": True
            }
        ]
        
        for endereco_data in enderecos_data:
            endereco = Endereco(**endereco_data)
            db.add(endereco)
        
        db.commit()
        print(f"Criados {len(enderecos_data)} endereços com sucesso!")
        
    except Exception as e:
        print(f"Erro ao criar endereços: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    """Função principal para executar o seed"""
    print("Iniciando seed do Auth Service...")
    
    # Criar tabelas
    print("Criando tabelas...")
    create_tables()
    
    # Popular dados
    print("Populando dados de usuários...")
    seed_usuarios()
    
    print("Populando dados de endereços...")
    seed_enderecos()
    
    print("Seed do Auth Service concluído com sucesso!")

if __name__ == "__main__":
    main()
