# Book Service - Business logic for book operations
# Handles book catalog, search, filters, and caching

from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime

from models import Livro, Categoria, CondicaoLivro
from repositories.book_repository import BookRepository
from services.cache_service import cache_service


class BookService:
    """Service for book business logic operations"""
    
    def __init__(self, db: Session):
        self.book_repo = BookRepository(db)
        self.cache = cache_service
    
    def _serialize_book(self, book: Livro) -> Dict[str, Any]:
        """
        Serialize book object to dictionary
        
        Args:
            book: Book instance
            
        Returns:
            Dictionary representation of book
        """
        return {
            "id": book.id,
            "titulo": book.titulo,
            "autor": book.autor,
            "isbn": book.isbn,
            "editora": book.editora,
            "ano_publicacao": book.ano_publicacao,
            "edicao": book.edicao,
            "numero_paginas": book.numero_paginas,
            "sinopse": book.sinopse,
            "preco": float(book.preco) if book.preco else 0.0,
            "estoque": book.estoque,
            "categoria": book.categoria.value if book.categoria else None,
            "condicao": book.condicao.value if book.condicao else None,
            "ativo": book.ativo,
            "data_criacao": book.data_criacao.isoformat() if book.data_criacao else None,
            "data_atualizacao": book.data_atualizacao.isoformat() if book.data_atualizacao else None
        }
    
    def _build_cache_key(self, prefix: str, **kwargs) -> str:
        """
        Build cache key from prefix and parameters
        
        Args:
            prefix: Cache key prefix
            **kwargs: Additional parameters to include in key
            
        Returns:
            Cache key string
        """
        parts = [prefix]
        for key, value in sorted(kwargs.items()):
            if value is not None:
                parts.append(f"{key}:{value}")
        return ":".join(parts)
    
    def get_book_by_id(self, book_id: int) -> Dict[str, Any]:
        """
        Get book by ID with caching
        
        Args:
            book_id: Book ID
            
        Returns:
            Book data dictionary
            
        Raises:
            HTTPException: If book not found
        """
        # Try cache first
        cache_key = f"book:{book_id}"
        cached_book = self.cache.get(cache_key)
        if cached_book:
            return cached_book
        
        # Get from database
        book = self.book_repo.get_by_id(book_id)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Livro não encontrado"
            )
        
        # Serialize and cache
        book_data = self._serialize_book(book)
        self.cache.set(cache_key, book_data)
        
        return book_data
    
    def get_books(
        self,
        page: int = 1,
        page_size: int = 20,
        categoria: Optional[str] = None,
        condicao: Optional[str] = None,
        preco_min: Optional[float] = None,
        preco_max: Optional[float] = None,
        order_by: str = "data_criacao",
        order_direction: str = "desc"
    ) -> Dict[str, Any]:
        """
        Get books with filters, pagination, and caching
        
        Args:
            page: Page number (1-based)
            page_size: Number of items per page
            categoria: Filter by category
            condicao: Filter by condition
            preco_min: Minimum price filter
            preco_max: Maximum price filter
            order_by: Field to order by
            order_direction: Order direction (asc or desc)
            
        Returns:
            Dictionary with books list and pagination info
        """
        # Build cache key
        cache_key = self._build_cache_key(
            "books:list",
            page=page,
            page_size=page_size,
            categoria=categoria,
            condicao=condicao,
            preco_min=preco_min,
            preco_max=preco_max,
            order_by=order_by,
            order_direction=order_direction
        )
        
        # Try cache first
        cached_result = self.cache.get(cache_key)
        if cached_result:
            return cached_result
        
        # Convert enum strings if provided
        categoria_enum = None
        if categoria:
            try:
                categoria_enum = Categoria(categoria)
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Categoria inválida: {categoria}"
                )
        
        condicao_enum = None
        if condicao:
            try:
                condicao_enum = CondicaoLivro(condicao)
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Condição inválida: {condicao}"
                )
        
        # Calculate skip
        skip = (page - 1) * page_size
        
        # Get books from repository
        books, total = self.book_repo.get_all(
            skip=skip,
            limit=page_size,
            categoria=categoria_enum,
            condicao=condicao_enum,
            preco_min=preco_min,
            preco_max=preco_max,
            order_by=order_by,
            order_direction=order_direction
        )
        
        # Serialize books
        books_data = [self._serialize_book(book) for book in books]
        
        # Calculate pagination info
        total_pages = (total + page_size - 1) // page_size
        
        result = {
            "items": books_data,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_previous": page > 1
        }
        
        # Cache result
        self.cache.set(cache_key, result)
        
        return result
    
    def search_books(
        self,
        search_term: str,
        page: int = 1,
        page_size: int = 20,
        categoria: Optional[str] = None,
        condicao: Optional[str] = None,
        preco_min: Optional[float] = None,
        preco_max: Optional[float] = None,
        order_by: str = "data_criacao",
        order_direction: str = "desc"
    ) -> Dict[str, Any]:
        """
        Search books with filters, pagination, and caching
        
        Args:
            search_term: Term to search
            page: Page number (1-based)
            page_size: Number of items per page
            categoria: Filter by category
            condicao: Filter by condition
            preco_min: Minimum price filter
            preco_max: Maximum price filter
            order_by: Field to order by
            order_direction: Order direction (asc or desc)
            
        Returns:
            Dictionary with books list and pagination info
        """
        # Build cache key
        cache_key = self._build_cache_key(
            "books:search",
            term=search_term,
            page=page,
            page_size=page_size,
            categoria=categoria,
            condicao=condicao,
            preco_min=preco_min,
            preco_max=preco_max,
            order_by=order_by,
            order_direction=order_direction
        )
        
        # Try cache first
        cached_result = self.cache.get(cache_key)
        if cached_result:
            return cached_result
        
        # Convert enum strings if provided
        categoria_enum = None
        if categoria:
            try:
                categoria_enum = Categoria(categoria)
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Categoria inválida: {categoria}"
                )
        
        condicao_enum = None
        if condicao:
            try:
                condicao_enum = CondicaoLivro(condicao)
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Condição inválida: {condicao}"
                )
        
        # Calculate skip
        skip = (page - 1) * page_size
        
        # Search books from repository
        books, total = self.book_repo.search(
            search_term=search_term,
            skip=skip,
            limit=page_size,
            categoria=categoria_enum,
            condicao=condicao_enum,
            preco_min=preco_min,
            preco_max=preco_max,
            order_by=order_by,
            order_direction=order_direction
        )
        
        # Serialize books
        books_data = [self._serialize_book(book) for book in books]
        
        # Calculate pagination info
        total_pages = (total + page_size - 1) // page_size
        
        result = {
            "items": books_data,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_previous": page > 1,
            "search_term": search_term
        }
        
        # Cache result
        self.cache.set(cache_key, result)
        
        return result
    
    def create_book(self, book_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new book
        
        Args:
            book_data: Book data dictionary
            
        Returns:
            Created book data
            
        Raises:
            HTTPException: If ISBN already exists
        """
        # Check if ISBN already exists
        if self.book_repo.isbn_exists(book_data.get("isbn")):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ISBN já cadastrado"
            )
        
        # Create book
        book = self.book_repo.create(book_data)
        
        # Invalidate cache
        self.cache.delete_pattern("books:*")
        
        return self._serialize_book(book)
    
    def update_book(self, book_id: int, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update book data
        
        Args:
            book_id: Book ID
            update_data: Dictionary with fields to update
            
        Returns:
            Updated book data
            
        Raises:
            HTTPException: If book not found or ISBN already exists
        """
        # Check if ISBN exists (excluding current book)
        if "isbn" in update_data:
            if self.book_repo.isbn_exists(update_data["isbn"], exclude_id=book_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="ISBN já cadastrado para outro livro"
                )
        
        # Update book
        book = self.book_repo.update(book_id, update_data)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Livro não encontrado"
            )
        
        # Invalidate cache
        self.cache.delete(f"book:{book_id}")
        self.cache.delete_pattern("books:*")
        
        return self._serialize_book(book)
    
    def delete_book(self, book_id: int) -> Dict[str, str]:
        """
        Delete book (soft delete)
        
        Args:
            book_id: Book ID
            
        Returns:
            Success message
            
        Raises:
            HTTPException: If book not found
        """
        success = self.book_repo.delete(book_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Livro não encontrado"
            )
        
        # Invalidate cache
        self.cache.delete(f"book:{book_id}")
        self.cache.delete_pattern("books:*")
        
        return {"message": "Livro removido com sucesso"}
    
    def get_categories(self) -> List[Dict[str, str]]:
        """
        Get all available categories
        
        Returns:
            List of category dictionaries
        """
        return [
            {"value": cat.value, "label": cat.name}
            for cat in Categoria
        ]
    
    def get_conditions(self) -> List[Dict[str, str]]:
        """
        Get all available conditions
        
        Returns:
            List of condition dictionaries
        """
        return [
            {"value": cond.value, "label": cond.name}
            for cond in CondicaoLivro
        ]
