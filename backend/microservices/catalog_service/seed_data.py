#!/usr/bin/env python3
"""
Script para popular o banco de dados com dados de exemplo
Microserviço: Catalog Service
"""

import sys
import os
from decimal import Decimal
from sqlalchemy.orm import Session

# Adicionar o diretório atual ao path para importar os módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal, engine
from models import Base, Livro, Categoria, CondicaoLivro

def create_tables():
    """Criar todas as tabelas"""
    Base.metadata.create_all(bind=engine)

def seed_livros():
    """Popular tabela de livros com dados de exemplo"""
    db = SessionLocal()
    
    try:
        # Verificar se já existem livros
        if db.query(Livro).count() > 0:
            print("Livros já existem no banco. Pulando seed de livros.")
            return
        
        print("Inserindo livros...")
        
        livros_data = [
            {
                "titulo": "O Senhor dos Anéis: A Sociedade do Anel",
                "autor": "J.R.R. Tolkien",
                "isbn": "9788533613379",
                "editora": "Martins Fontes",
                "ano_publicacao": 2000,
                "edicao": "1ª Edição",
                "numero_paginas": 576,
                "sinopse": "A jornada épica de Frodo Baggins para destruir o Um Anel e salvar a Terra Média.",
                "preco": Decimal("45.90"),
                "estoque": 50,
                "categoria": Categoria.FICCAO,
                "condicao": CondicaoLivro.NOVO,
                "ativo": True
            },
            {
                "titulo": "1984",
                "autor": "George Orwell",
                "isbn": "9788535914849",
                "editora": "Companhia das Letras",
                "ano_publicacao": 2009,
                "edicao": "1ª Edição",
                "numero_paginas": 416,
                "sinopse": "Uma distopia clássica sobre vigilância e controle totalitário.",
                "preco": Decimal("32.50"),
                "estoque": 30,
                "categoria": Categoria.FICCAO,
                "condicao": CondicaoLivro.NOVO,
                "ativo": True
            },
            {
                "titulo": "Sapiens: Uma Breve História da Humanidade",
                "autor": "Yuval Noah Harari",
                "isbn": "9788535928198",
                "editora": "L&PM",
                "ano_publicacao": 2015,
                "edicao": "1ª Edição",
                "numero_paginas": 464,
                "sinopse": "Uma análise fascinante da evolução humana e das revoluções que moldaram nossa sociedade.",
                "preco": Decimal("39.90"),
                "estoque": 25,
                "categoria": Categoria.NAO_FICCAO,
                "condicao": CondicaoLivro.NOVO,
                "ativo": True
            },
            {
                "titulo": "Clean Code: A Handbook of Agile Software Craftsmanship",
                "autor": "Robert C. Martin",
                "isbn": "9780132350884",
                "editora": "Pearson",
                "ano_publicacao": 2008,
                "edicao": "1ª Edição",
                "numero_paginas": 464,
                "sinopse": "Um guia essencial para escrever código limpo e manutenível.",
                "preco": Decimal("89.90"),
                "estoque": 15,
                "categoria": Categoria.TECNICO,
                "condicao": CondicaoLivro.NOVO,
                "ativo": True
            },
            {
                "titulo": "O Pequeno Príncipe",
                "autor": "Antoine de Saint-Exupéry",
                "isbn": "9788535908053",
                "editora": "Agir",
                "ano_publicacao": 2007,
                "edicao": "1ª Edição",
                "numero_paginas": 96,
                "sinopse": "Uma fábula poética sobre amizade, amor e a essência da vida.",
                "preco": Decimal("19.90"),
                "estoque": 40,
                "categoria": Categoria.INFANTIL,
                "condicao": CondicaoLivro.NOVO,
                "ativo": True
            },
            {
                "titulo": "Dom Casmurro",
                "autor": "Machado de Assis",
                "isbn": "9788535928199",
                "editora": "Companhia das Letras",
                "ano_publicacao": 2019,
                "edicao": "1ª Edição",
                "numero_paginas": 256,
                "sinopse": "Um clássico da literatura brasileira sobre ciúme e traição.",
                "preco": Decimal("28.50"),
                "estoque": 20,
                "categoria": Categoria.ACADEMICO,
                "condicao": CondicaoLivro.NOVO,
                "ativo": True
            },
            {
                "titulo": "Harry Potter e a Pedra Filosofal",
                "autor": "J.K. Rowling",
                "isbn": "9788532530783",
                "editora": "Rocco",
                "ano_publicacao": 2000,
                "edicao": "1ª Edição",
                "numero_paginas": 264,
                "sinopse": "A primeira aventura do jovem bruxo Harry Potter em Hogwarts.",
                "preco": Decimal("35.90"),
                "estoque": 35,
                "categoria": Categoria.INFANTIL,
                "condicao": CondicaoLivro.NOVO,
                "ativo": True
            },
            {
                "titulo": "A Arte da Guerra",
                "autor": "Sun Tzu",
                "isbn": "9788532647306",
                "editora": "Vozes",
                "ano_publicacao": 2018,
                "edicao": "1ª Edição",
                "numero_paginas": 128,
                "sinopse": "Estratégias militares aplicáveis à vida pessoal e profissional.",
                "preco": Decimal("22.90"),
                "estoque": 18,
                "categoria": Categoria.NAO_FICCAO,
                "condicao": CondicaoLivro.USADO,
                "ativo": True
            }
        ]
        
        for livro_data in livros_data:
            livro = Livro(**livro_data)
            db.add(livro)
        
        db.commit()
        print(f"Criados {len(livros_data)} livros com sucesso!")
        
    except Exception as e:
        print(f"Erro ao criar livros: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    """Função principal para executar o seed"""
    print("Iniciando seed do Catalog Service...")
    
    # Criar tabelas
    print("Criando tabelas...")
    create_tables()
    
    # Popular dados
    print("Populando dados de livros...")
    seed_livros()
    
    print("Seed do Catalog Service concluído com sucesso!")

if __name__ == "__main__":
    main()
