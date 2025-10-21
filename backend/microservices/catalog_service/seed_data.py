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
        # Limpar livros existentes para garantir que temos a nova estrutura com imagem_url
        count_existing = db.query(Livro).count()
        if count_existing > 0:
            print(f"Removendo {count_existing} livros existentes para recriar com nova estrutura...")
            db.query(Livro).delete()
            db.commit()
        
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
                "imagem_url": "https://covers.openlibrary.org/b/isbn/9788533613379-L.jpg",
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
                "imagem_url": "https://covers.openlibrary.org/b/isbn/9788535914849-L.jpg",
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
                "imagem_url": "https://covers.openlibrary.org/b/isbn/9788535928198-L.jpg",
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
                "imagem_url": "https://covers.openlibrary.org/b/isbn/9780132350884-L.jpg",
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
                "imagem_url": "https://covers.openlibrary.org/b/isbn/9788535908053-L.jpg",
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
                "imagem_url": "https://covers.openlibrary.org/b/isbn/9788535928199-L.jpg",
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
                "imagem_url": "https://covers.openlibrary.org/b/isbn/9788532530783-L.jpg",
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
                "imagem_url": "https://covers.openlibrary.org/b/isbn/9788532647306-L.jpg",
                "preco": Decimal("22.90"),
                "estoque": 18,
                "categoria": Categoria.NAO_FICCAO,
                "condicao": CondicaoLivro.USADO,
                "ativo": True
            },
            # ROMANCE
            {
                "titulo": "Orgulho e Preconceito",
                "autor": "Jane Austen",
                "isbn": "9788544001509",
                "editora": "Martin Claret",
                "ano_publicacao": 2014,
                "edicao": "1ª Edição",
                "numero_paginas": 424,
                "sinopse": "Romance clássico sobre Elizabeth Bennet e Mr. Darcy.",
                "imagem_url": "https://covers.openlibrary.org/b/isbn/9788544001509-L.jpg",
                "preco": Decimal("24.90"),
                "estoque": 45,
                "categoria": Categoria.FICCAO,
                "condicao": CondicaoLivro.NOVO,
                "ativo": True
            },
            {
                "titulo": "A Culpa é das Estrelas",
                "autor": "John Green",
                "isbn": "9788580573466",
                "editora": "Intrínseca",
                "ano_publicacao": 2012,
                "edicao": "1ª Edição",
                "numero_paginas": 288,
                "sinopse": "História de amor entre dois adolescentes com câncer.",
                "imagem_url": "https://covers.openlibrary.org/b/isbn/9788580573466-L.jpg",
                "preco": Decimal("32.90"),
                "estoque": 60,
                "categoria": Categoria.FICCAO,
                "condicao": CondicaoLivro.NOVO,
                "ativo": True
            },
            {
                "titulo": "Como Eu Era Antes de Você",
                "autor": "Jojo Moyes",
                "isbn": "9788580573541",
                "editora": "Intrínseca",
                "ano_publicacao": 2013,
                "edicao": "1ª Edição",
                "numero_paginas": 368,
                "sinopse": "Romance emocionante sobre amor, escolhas e superação.",
                "imagem_url": "https://covers.openlibrary.org/b/isbn/9788580573541-L.jpg",
                "preco": Decimal("34.90"),
                "estoque": 40,
                "categoria": Categoria.FICCAO,
                "condicao": CondicaoLivro.NOVO,
                "ativo": True
            },
            {
                "titulo": "O Morro dos Ventos Uivantes",
                "autor": "Emily Brontë",
                "isbn": "9788544001363",
                "editora": "Martin Claret",
                "ano_publicacao": 2014,
                "edicao": "1ª Edição",
                "numero_paginas": 368,
                "sinopse": "Romance gótico sobre amor obsessivo e vingança.",
                "imagem_url": "https://covers.openlibrary.org/b/isbn/9788544001363-L.jpg",
                "preco": Decimal("26.90"),
                "estoque": 30,
                "categoria": Categoria.FICCAO,
                "condicao": CondicaoLivro.NOVO,
                "ativo": True
            },
            # CIÊNCIA DE DADOS
            {
                "titulo": "Python para Análise de Dados",
                "autor": "Wes McKinney",
                "isbn": "9788575226476",
                "editora": "Novatec",
                "ano_publicacao": 2018,
                "edicao": "2ª Edição",
                "numero_paginas": 616,
                "sinopse": "Tratamento de dados com Pandas, NumPy e IPython.",
                "imagem_url": "https://covers.openlibrary.org/b/isbn/9788575226476-L.jpg",
                "preco": Decimal("98.00"),
                "estoque": 22,
                "categoria": Categoria.TECNICO,
                "condicao": CondicaoLivro.NOVO,
                "ativo": True
            },
            {
                "titulo": "Data Science do Zero",
                "autor": "Joel Grus",
                "isbn": "9788550803401",
                "editora": "Alta Books",
                "ano_publicacao": 2021,
                "edicao": "2ª Edição",
                "numero_paginas": 384,
                "sinopse": "Primeiras regras com Python para ciência de dados.",
                "imagem_url": "https://covers.openlibrary.org/b/isbn/9788550803401-L.jpg",
                "preco": Decimal("89.90"),
                "estoque": 18,
                "categoria": Categoria.TECNICO,
                "condicao": CondicaoLivro.NOVO,
                "ativo": True
            },
            {
                "titulo": "Machine Learning: Guia de Referência Rápida",
                "autor": "Matt Harrison",
                "isbn": "9788575228067",
                "editora": "Novatec",
                "ano_publicacao": 2020,
                "edicao": "1ª Edição",
                "numero_paginas": 336,
                "sinopse": "Trabalhando com dados estruturados em Python.",
                "imagem_url": "https://covers.openlibrary.org/b/isbn/9788575228067-L.jpg",
                "preco": Decimal("72.00"),
                "estoque": 15,
                "categoria": Categoria.TECNICO,
                "condicao": CondicaoLivro.NOVO,
                "ativo": True
            },
            {
                "titulo": "Introdução à Mineração de Dados",
                "autor": "Pang-Ning Tan",
                "isbn": "9788576058892",
                "editora": "Ciência Moderna",
                "ano_publicacao": 2018,
                "edicao": "1ª Edição",
                "numero_paginas": 896,
                "sinopse": "Conceitos e técnicas fundamentais de mineração de dados.",
                "imagem_url": "https://covers.openlibrary.org/b/isbn/9788576058892-L.jpg",
                "preco": Decimal("145.00"),
                "estoque": 12,
                "categoria": Categoria.TECNICO,
                "condicao": CondicaoLivro.NOVO,
                "ativo": True
            },
            {
                "titulo": "Deep Learning",
                "autor": "Ian Goodfellow",
                "isbn": "9780262035613",
                "editora": "MIT Press",
                "ano_publicacao": 2016,
                "edicao": "1ª Edição",
                "numero_paginas": 800,
                "sinopse": "Livro definitivo sobre aprendizado profundo.",
                "imagem_url": "https://covers.openlibrary.org/b/isbn/9780262035613-L.jpg",
                "preco": Decimal("180.00"),
                "estoque": 10,
                "categoria": Categoria.TECNICO,
                "condicao": CondicaoLivro.NOVO,
                "ativo": True
            },
            # ENGENHARIA DE SOFTWARE
            {
                "titulo": "Arquitetura Limpa",
                "autor": "Robert C. Martin",
                "isbn": "9788550804606",
                "editora": "Alta Books",
                "ano_publicacao": 2019,
                "edicao": "1ª Edição",
                "numero_paginas": 432,
                "sinopse": "O guia do artesão para estrutura e design de software.",
                "imagem_url": "https://covers.openlibrary.org/b/isbn/9788550804606-L.jpg",
                "preco": Decimal("79.90"),
                "estoque": 25,
                "categoria": Categoria.TECNICO,
                "condicao": CondicaoLivro.NOVO,
                "ativo": True
            },
            {
                "titulo": "Padrões de Projetos",
                "autor": "Erich Gamma",
                "isbn": "9788577800469",
                "editora": "Bookman",
                "ano_publicacao": 2007,
                "edicao": "1ª Edição",
                "numero_paginas": 364,
                "sinopse": "Soluções reutilizáveis de software orientado a objetos.",
                "imagem_url": "https://covers.openlibrary.org/b/isbn/9788577800469-L.jpg",
                "preco": Decimal("95.00"),
                "estoque": 20,
                "categoria": Categoria.TECNICO,
                "condicao": CondicaoLivro.NOVO,
                "ativo": True
            },
            {
                "titulo": "Código Limpo",
                "autor": "Robert C. Martin",
                "isbn": "9788576082675",
                "editora": "Alta Books",
                "ano_publicacao": 2011,
                "edicao": "1ª Edição",
                "numero_paginas": 425,
                "sinopse": "Habilidades práticas do Agile Software Craftsmanship.",
                "imagem_url": "https://covers.openlibrary.org/b/isbn/9788576082675-L.jpg",
                "preco": Decimal("84.90"),
                "estoque": 30,
                "categoria": Categoria.TECNICO,
                "condicao": CondicaoLivro.NOVO,
                "ativo": True
            },
            {
                "titulo": "Refatoração",
                "autor": "Martin Fowler",
                "isbn": "9788575227244",
                "editora": "Novatec",
                "ano_publicacao": 2020,
                "edicao": "2ª Edição",
                "numero_paginas": 456,
                "sinopse": "Aperfeiçoando o design de códigos existentes.",
                "imagem_url": "https://covers.openlibrary.org/b/isbn/9788575227244-L.jpg",
                "preco": Decimal("92.00"),
                "estoque": 18,
                "categoria": Categoria.TECNICO,
                "condicao": CondicaoLivro.NOVO,
                "ativo": True
            },
            {
                "titulo": "Engenharia de Software Moderna",
                "autor": "Marco Tulio Valente",
                "isbn": "9786500019704",
                "editora": "Independente",
                "ano_publicacao": 2020,
                "edicao": "1ª Edição",
                "numero_paginas": 395,
                "sinopse": "Princípios e práticas para desenvolvimento ágil.",
                "imagem_url": "https://covers.openlibrary.org/b/isbn/9786500019704-L.jpg",
                "preco": Decimal("65.00"),
                "estoque": 22,
                "categoria": Categoria.TECNICO,
                "condicao": CondicaoLivro.NOVO,
                "ativo": True
            },
            # HISTÓRIA
            {
                "titulo": "Uma Breve História do Tempo",
                "autor": "Stephen Hawking",
                "isbn": "9788580575460",
                "editora": "Intrínseca",
                "ano_publicacao": 2015,
                "edicao": "1ª Edição",
                "numero_paginas": 256,
                "sinopse": "Do Big Bang aos Buracos Negros.",
                "imagem_url": "https://covers.openlibrary.org/b/isbn/9788580575460-L.jpg",
                "preco": Decimal("42.90"),
                "estoque": 35,
                "categoria": Categoria.NAO_FICCAO,
                "condicao": CondicaoLivro.NOVO,
                "ativo": True
            },
            {
                "titulo": "21 Lições para o Século 21",
                "autor": "Yuval Noah Harari",
                "isbn": "9788535930733",
                "editora": "Companhia das Letras",
                "ano_publicacao": 2018,
                "edicao": "1ª Edição",
                "numero_paginas": 432,
                "sinopse": "Reflexões sobre o presente e o futuro da humanidade.",
                "imagem_url": "https://covers.openlibrary.org/b/isbn/9788535930733-L.jpg",
                "preco": Decimal("44.90"),
                "estoque": 28,
                "categoria": Categoria.NAO_FICCAO,
                "condicao": CondicaoLivro.NOVO,
                "ativo": True
            },
            {
                "titulo": "Homo Deus",
                "autor": "Yuval Noah Harari",
                "isbn": "9788535928181",
                "editora": "Companhia das Letras",
                "ano_publicacao": 2016,
                "edicao": "1ª Edição",
                "numero_paginas": 448,
                "sinopse": "Uma breve história do amanhã.",
                "imagem_url": "https://covers.openlibrary.org/b/isbn/9788535928181-L.jpg",
                "preco": Decimal("42.90"),
                "estoque": 30,
                "categoria": Categoria.NAO_FICCAO,
                "condicao": CondicaoLivro.NOVO,
                "ativo": True
            },
            {
                "titulo": "Escravidão - Volume 1",
                "autor": "Laurentino Gomes",
                "isbn": "9788525065902",
                "editora": "Globo Livros",
                "ano_publicacao": 2019,
                "edicao": "1ª Edição",
                "numero_paginas": 448,
                "sinopse": "História da escravidão no Brasil.",
                "imagem_url": "https://covers.openlibrary.org/b/isbn/9788525065902-L.jpg",
                "preco": Decimal("54.90"),
                "estoque": 25,
                "categoria": Categoria.NAO_FICCAO,
                "condicao": CondicaoLivro.NOVO,
                "ativo": True
            },
            {
                "titulo": "1808",
                "autor": "Laurentino Gomes",
                "isbn": "9788574885971",
                "editora": "Planeta",
                "ano_publicacao": 2007,
                "edicao": "1ª Edição",
                "numero_paginas": 424,
                "sinopse": "Como uma rainha louca, um príncipe medroso e uma corte corrupta enganaram Napoleão.",
                "imagem_url": "https://covers.openlibrary.org/b/isbn/9788574885971-L.jpg",
                "preco": Decimal("49.90"),
                "estoque": 20,
                "categoria": Categoria.NAO_FICCAO,
                "condicao": CondicaoLivro.NOVO,
                "ativo": True
            },
            # FINANÇAS
            {
                "titulo": "Pai Rico, Pai Pobre",
                "autor": "Robert Kiyosaki",
                "isbn": "9788550801469",
                "editora": "Alta Books",
                "ano_publicacao": 2017,
                "edicao": "Edição de 20 anos",
                "numero_paginas": 336,
                "sinopse": "O que os ricos ensinam a seus filhos sobre dinheiro.",
                "imagem_url": "https://covers.openlibrary.org/b/isbn/9788550801469-L.jpg",
                "preco": Decimal("42.90"),
                "estoque": 50,
                "categoria": Categoria.NAO_FICCAO,
                "condicao": CondicaoLivro.NOVO,
                "ativo": True
            },
            {
                "titulo": "Os Segredos da Mente Milionária",
                "autor": "T. Harv Eker",
                "isbn": "9788575422489",
                "editora": "Sextante",
                "ano_publicacao": 2006,
                "edicao": "1ª Edição",
                "numero_paginas": 176,
                "sinopse": "Aprenda a enriquecer mudando seus conceitos sobre dinheiro.",
                "imagem_url": "https://covers.openlibrary.org/b/isbn/9788575422489-L.jpg",
                "preco": Decimal("34.90"),
                "estoque": 45,
                "categoria": Categoria.NAO_FICCAO,
                "condicao": CondicaoLivro.NOVO,
                "ativo": True
            },
            {
                "titulo": "Do Mil ao Milhão",
                "autor": "Thiago Nigro",
                "isbn": "9788595081556",
                "editora": "HarperCollins",
                "ano_publicacao": 2018,
                "edicao": "1ª Edição",
                "numero_paginas": 272,
                "sinopse": "Sem cortar o cafezinho.",
                "imagem_url": "https://covers.openlibrary.org/b/isbn/9788595081556-L.jpg",
                "preco": Decimal("38.90"),
                "estoque": 40,
                "categoria": Categoria.NAO_FICCAO,
                "condicao": CondicaoLivro.NOVO,
                "ativo": True
            },
            {
                "titulo": "O Homem Mais Rico da Babilônia",
                "autor": "George S. Clason",
                "isbn": "9788595083189",
                "editora": "HarperCollins",
                "ano_publicacao": 2017,
                "edicao": "1ª Edição",
                "numero_paginas": 160,
                "sinopse": "Lições de sucesso financeiro vindas da antiguidade.",
                "imagem_url": "https://covers.openlibrary.org/b/isbn/9788595083189-L.jpg",
                "preco": Decimal("29.90"),
                "estoque": 55,
                "categoria": Categoria.NAO_FICCAO,
                "condicao": CondicaoLivro.NOVO,
                "ativo": True
            },
            {
                "titulo": "Investimentos Inteligentes",
                "autor": "Gustavo Cerbasi",
                "isbn": "9788543108063",
                "editora": "Sextante",
                "ano_publicacao": 2019,
                "edicao": "2ª Edição",
                "numero_paginas": 288,
                "sinopse": "Estratégias para multiplicar seu patrimônio.",
                "imagem_url": "https://covers.openlibrary.org/b/isbn/9788543108063-L.jpg",
                "preco": Decimal("39.90"),
                "estoque": 32,
                "categoria": Categoria.NAO_FICCAO,
                "condicao": CondicaoLivro.NOVO,
                "ativo": True
            },
            # AUTOAJUDA
            {
                "titulo": "O Poder do Hábito",
                "autor": "Charles Duhigg",
                "isbn": "9788539004119",
                "editora": "Objetiva",
                "ano_publicacao": 2012,
                "edicao": "1ª Edição",
                "numero_paginas": 408,
                "sinopse": "Por que fazemos o que fazemos na vida e nos negócios.",
                "imagem_url": "https://covers.openlibrary.org/b/isbn/9788539004119-L.jpg",
                "preco": Decimal("44.90"),
                "estoque": 38,
                "categoria": Categoria.NAO_FICCAO,
                "condicao": CondicaoLivro.NOVO,
                "ativo": True
            },
            {
                "titulo": "Hábitos Atômicos",
                "autor": "James Clear",
                "isbn": "9788550807911",
                "editora": "Alta Books",
                "ano_publicacao": 2019,
                "edicao": "1ª Edição",
                "numero_paginas": 320,
                "sinopse": "Pequenas mudanças, resultados notáveis.",
                "imagem_url": "https://covers.openlibrary.org/b/isbn/9788550807911-L.jpg",
                "preco": Decimal("42.90"),
                "estoque": 60,
                "categoria": Categoria.NAO_FICCAO,
                "condicao": CondicaoLivro.NOVO,
                "ativo": True
            },
            {
                "titulo": "Mindset: A Nova Psicologia do Sucesso",
                "autor": "Carol S. Dweck",
                "isbn": "9788547001391",
                "editora": "Objetiva",
                "ano_publicacao": 2017,
                "edicao": "1ª Edição",
                "numero_paginas": 312,
                "sinopse": "Como podemos aprender a realizar nosso potencial.",
                "imagem_url": "https://covers.openlibrary.org/b/isbn/9788547001391-L.jpg",
                "preco": Decimal("39.90"),
                "estoque": 35,
                "categoria": Categoria.NAO_FICCAO,
                "condicao": CondicaoLivro.NOVO,
                "ativo": True
            },
            {
                "titulo": "A Coragem de Ser Imperfeito",
                "autor": "Brené Brown",
                "isbn": "9788543104324",
                "editora": "Sextante",
                "ano_publicacao": 2016,
                "edicao": "1ª Edição",
                "numero_paginas": 176,
                "sinopse": "Como aceitar a própria vulnerabilidade, vencer a vergonha e ousar ser quem você é.",
                "imagem_url": "https://covers.openlibrary.org/b/isbn/9788543104324-L.jpg",
                "preco": Decimal("34.90"),
                "estoque": 42,
                "categoria": Categoria.NAO_FICCAO,
                "condicao": CondicaoLivro.NOVO,
                "ativo": True
            },
            {
                "titulo": "O Poder do Agora",
                "autor": "Eckhart Tolle",
                "isbn": "9788543102030",
                "editora": "Sextante",
                "ano_publicacao": 2016,
                "edicao": "1ª Edição",
                "numero_paginas": 224,
                "sinopse": "Um guia para a iluminação espiritual.",
                "imagem_url": "https://covers.openlibrary.org/b/isbn/9788543102030-L.jpg",
                "preco": Decimal("36.90"),
                "estoque": 48,
                "categoria": Categoria.NAO_FICCAO,
                "condicao": CondicaoLivro.NOVO,
                "ativo": True
            },
            {
                "titulo": "Mais Esperto que o Diabo",
                "autor": "Napoleon Hill",
                "isbn": "9788568014004",
                "editora": "Citadel",
                "ano_publicacao": 2014,
                "edicao": "1ª Edição",
                "numero_paginas": 208,
                "sinopse": "O mistério revelado da liberdade e do sucesso.",
                "imagem_url": "https://covers.openlibrary.org/b/isbn/9788568014004-L.jpg",
                "preco": Decimal("32.90"),
                "estoque": 36,
                "categoria": Categoria.NAO_FICCAO,
                "condicao": CondicaoLivro.NOVO,
                "ativo": True
            },
            {
                "titulo": "Inteligência Emocional",
                "autor": "Daniel Goleman",
                "isbn": "9788539004225",
                "editora": "Objetiva",
                "ano_publicacao": 2012,
                "edicao": "Edição revisada",
                "numero_paginas": 384,
                "sinopse": "A teoria revolucionária que redefine o que é ser inteligente.",
                "imagem_url": "https://covers.openlibrary.org/b/isbn/9788539004225-L.jpg",
                "preco": Decimal("49.90"),
                "estoque": 40,
                "categoria": Categoria.NAO_FICCAO,
                "condicao": CondicaoLivro.NOVO,
                "ativo": True
            },
            {
                "titulo": "A Sutil Arte de Ligar o F*da-se",
                "autor": "Mark Manson",
                "isbn": "9788551001943",
                "editora": "Intrínseca",
                "ano_publicacao": 2017,
                "edicao": "1ª Edição",
                "numero_paginas": 224,
                "sinopse": "Uma estratégia inusitada para uma vida melhor.",
                "imagem_url": "https://covers.openlibrary.org/b/isbn/9788551001943-L.jpg",
                "preco": Decimal("34.90"),
                "estoque": 65,
                "categoria": Categoria.NAO_FICCAO,
                "condicao": CondicaoLivro.NOVO,
                "ativo": True
            }
        ]
        
        for livro_data in livros_data:
            livro = Livro(**livro_data)
            db.add(livro)
        
        db.commit()
        print(f"✅ Criados {len(livros_data)} livros com sucesso!")
        
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
