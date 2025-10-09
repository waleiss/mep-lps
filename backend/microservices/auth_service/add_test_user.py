#!/usr/bin/env python3
"""
Script para adicionar usuário de teste diretamente no banco
"""

import sys
import os
from datetime import date
from sqlalchemy.orm import Session

# Adicionar o diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal, engine
from models import Usuario, TipoUsuario, Base

# Criar tabelas se não existirem
Base.metadata.create_all(bind=engine)

def add_test_user():
    """Adiciona usuário de teste"""
    db = SessionLocal()
    
    try:
        # Verificar se usuário já existe
        existing_user = db.query(Usuario).filter(Usuario.email == "user@gmail.com").first()
        if existing_user:
            print("Usuário user@gmail.com já existe!")
            print(f"ID: {existing_user.id}")
            print(f"Email: {existing_user.email}")
            print(f"Nome: {existing_user.nome}")
            return
        
        # Criar usuário de teste
        user = Usuario(
            nome="Usuário Teste",
            email="user@gmail.com",
            senha_hash="test_hash_1234",  # Hash simples para teste
            telefone="(11) 99999-9999",
            data_nascimento=date(1990, 1, 1),
            tipo=TipoUsuario.CLIENTE,
            ativo=True
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        print(f"Usuário criado com sucesso!")
        print(f"ID: {user.id}")
        print(f"Email: {user.email}")
        print(f"Nome: {user.nome}")
        
    except Exception as e:
        print(f"Erro ao criar usuário: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_test_user()
