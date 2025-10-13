# Rotas da API REST para catálogo
# Endpoints: /livros, /livros/{id}, /buscar
# Implementa RF2.1, RF2.2, RF2.3, RF2.4, RF2.5

from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, List

from database import get_db
from schemas.book_schemas import (
    BookCreate,
    BookUpdate,
    BookResponse,
    BookListResponse,
    CategoryResponse,
    ConditionResponse
)
from services.book_service import BookService

router = APIRouter(tags=["Catálogo"])


def get_book_service(db: Session = Depends(get_db)) -> BookService:
    """Dependency to get book service instance"""
    return BookService(db)


@router.get("/livros", response_model=BookListResponse)
async def get_books(
    page: int = Query(1, ge=1, description="Número da página"),
    page_size: int = Query(20, ge=1, le=100, description="Itens por página"),
    categoria: Optional[str] = Query(None, description="Filtrar por categoria"),
    condicao: Optional[str] = Query(None, description="Filtrar por condição"),
    preco_min: Optional[float] = Query(None, ge=0, description="Preço mínimo"),
    preco_max: Optional[float] = Query(None, ge=0, description="Preço máximo"),
    order_by: str = Query("data_criacao", description="Campo para ordenação"),
    order_direction: str = Query("desc", regex="^(asc|desc)$", description="Direção da ordenação"),
    book_service: BookService = Depends(get_book_service)
):
    """
    Listar livros com filtros e paginação
    
    - **page**: Número da página (começa em 1)
    - **page_size**: Quantidade de itens por página (máx: 100)
    - **categoria**: Filtrar por categoria (ficcao, nao_ficcao, tecnico, academico, infantil, outros)
    - **condicao**: Filtrar por condição (novo, usado, semi_novo)
    - **preco_min**: Filtro de preço mínimo
    - **preco_max**: Filtro de preço máximo
    - **order_by**: Campo para ordenação (titulo, autor, preco, data_criacao, estoque)
    - **order_direction**: Direção da ordenação (asc ou desc)
    """
    result = book_service.get_books(
        page=page,
        page_size=page_size,
        categoria=categoria,
        condicao=condicao,
        preco_min=preco_min,
        preco_max=preco_max,
        order_by=order_by,
        order_direction=order_direction
    )
    return result


@router.get("/livros/{book_id}", response_model=BookResponse)
async def get_book(
    book_id: int,
    book_service: BookService = Depends(get_book_service)
):
    """
    Obter detalhes de um livro específico
    
    - **book_id**: ID do livro
    """
    return book_service.get_book_by_id(book_id)


@router.get("/buscar", response_model=BookListResponse)
async def search_books(
    q: str = Query(..., min_length=1, description="Termo de busca"),
    page: int = Query(1, ge=1, description="Número da página"),
    page_size: int = Query(20, ge=1, le=100, description="Itens por página"),
    categoria: Optional[str] = Query(None, description="Filtrar por categoria"),
    condicao: Optional[str] = Query(None, description="Filtrar por condição"),
    preco_min: Optional[float] = Query(None, ge=0, description="Preço mínimo"),
    preco_max: Optional[float] = Query(None, ge=0, description="Preço máximo"),
    order_by: str = Query("data_criacao", description="Campo para ordenação"),
    order_direction: str = Query("desc", regex="^(asc|desc)$", description="Direção da ordenação"),
    book_service: BookService = Depends(get_book_service)
):
    """
    Buscar livros por termo (título, autor ou ISBN)
    
    - **q**: Termo de busca (busca em título, autor e ISBN)
    - **page**: Número da página (começa em 1)
    - **page_size**: Quantidade de itens por página (máx: 100)
    - **categoria**: Filtrar por categoria
    - **condicao**: Filtrar por condição
    - **preco_min**: Filtro de preço mínimo
    - **preco_max**: Filtro de preço máximo
    - **order_by**: Campo para ordenação
    - **order_direction**: Direção da ordenação (asc ou desc)
    """
    result = book_service.search_books(
        search_term=q,
        page=page,
        page_size=page_size,
        categoria=categoria,
        condicao=condicao,
        preco_min=preco_min,
        preco_max=preco_max,
        order_by=order_by,
        order_direction=order_direction
    )
    return result


@router.post("/livros", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(
    book_data: BookCreate,
    book_service: BookService = Depends(get_book_service)
):
    """
    Criar um novo livro no catálogo
    
    Requer dados completos do livro conforme schema BookCreate
    """
    return book_service.create_book(book_data.model_dump())


@router.put("/livros/{book_id}", response_model=BookResponse)
async def update_book(
    book_id: int,
    book_data: BookUpdate,
    book_service: BookService = Depends(get_book_service)
):
    """
    Atualizar dados de um livro
    
    - **book_id**: ID do livro
    - Todos os campos são opcionais
    """
    # Remove None values
    update_data = {k: v for k, v in book_data.model_dump().items() if v is not None}
    return book_service.update_book(book_id, update_data)


@router.delete("/livros/{book_id}")
async def delete_book(
    book_id: int,
    book_service: BookService = Depends(get_book_service)
):
    """
    Remover um livro do catálogo (soft delete)
    
    - **book_id**: ID do livro
    """
    return book_service.delete_book(book_id)


@router.get("/categorias", response_model=List[CategoryResponse])
async def get_categories(
    book_service: BookService = Depends(get_book_service)
):
    """
    Listar todas as categorias disponíveis
    """
    return book_service.get_categories()


@router.get("/condicoes", response_model=List[ConditionResponse])
async def get_conditions(
    book_service: BookService = Depends(get_book_service)
):
    """
    Listar todas as condições disponíveis
    """
    return book_service.get_conditions()
