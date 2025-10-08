# Catalog Service - Mundo em Palavras
# Microserviço responsável pelo catálogo de livros
# Gerencia produtos, categorias, busca e filtros

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

# Configuração da aplicação FastAPI
app = FastAPI(
    title="Catalog Service",
    description="Microserviço de catálogo de livros",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Modelos Pydantic
class Book(BaseModel):
    id: str
    title: str
    author: str
    isbn: str
    price: float
    description: str
    category: str
    stock: int
    image_url: Optional[str] = None

class BookCreate(BaseModel):
    title: str
    author: str
    isbn: str
    price: float
    description: str
    category: str
    stock: int
    image_url: Optional[str] = None

# Dados mock para demonstração
books_db = [
    Book(
        id="1",
        title="O Senhor dos Anéis",
        author="J.R.R. Tolkien",
        isbn="978-8533613377",
        price=49.90,
        description="A trilogia épica de fantasia",
        category="Fantasia",
        stock=10,
        image_url="https://example.com/lotr.jpg"
    ),
    Book(
        id="2",
        title="1984",
        author="George Orwell",
        isbn="978-8535906552",
        price=29.90,
        description="Distopia clássica sobre totalitarismo",
        category="Ficção Científica",
        stock=15,
        image_url="https://example.com/1984.jpg"
    )
]

# Rotas básicas
@app.get("/")
async def root():
    """Endpoint raiz do serviço de catálogo"""
    return {
        "service": "Catalog Service",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Health check do serviço"""
    return {"status": "healthy", "service": "catalog"}

@app.get("/books", response_model=List[Book])
async def get_books(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    category: Optional[str] = None,
    search: Optional[str] = None
):
    """Listar livros com filtros opcionais"""
    filtered_books = books_db
    
    if category:
        filtered_books = [book for book in filtered_books if book.category.lower() == category.lower()]
    
    if search:
        filtered_books = [
            book for book in filtered_books 
            if search.lower() in book.title.lower() or search.lower() in book.author.lower()
        ]
    
    return filtered_books[skip:skip + limit]

@app.get("/books/{book_id}", response_model=Book)
async def get_book(book_id: str):
    """Obter detalhes de um livro específico"""
    book = next((book for book in books_db if book.id == book_id), None)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.post("/books", response_model=Book)
async def create_book(book: BookCreate):
    """Criar um novo livro"""
    new_book = Book(
        id=str(len(books_db) + 1),
        **book.dict()
    )
    books_db.append(new_book)
    return new_book

@app.get("/categories")
async def get_categories():
    """Listar categorias disponíveis"""
    categories = list(set(book.category for book in books_db))
    return {"categories": categories}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)