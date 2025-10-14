# Book Repository - Data access layer for book operations
# Implements repository pattern for book data access

from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, asc

from models import Livro, Categoria, CondicaoLivro


class BookRepository:
    """Repository for book data operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, book_data: dict) -> Livro:
        """
        Create a new book
        
        Args:
            book_data: Book data dictionary
            
        Returns:
            Created book instance
        """
        db_book = Livro(**book_data)
        self.db.add(db_book)
        self.db.commit()
        self.db.refresh(db_book)
        return db_book
    
    def get_by_id(self, book_id: int) -> Optional[Livro]:
        """
        Get book by ID
        
        Args:
            book_id: Book ID
            
        Returns:
            Book instance or None if not found
        """
        return self.db.query(Livro).filter(
            and_(Livro.id == book_id, Livro.ativo == True)
        ).first()
    
    def get_by_isbn(self, isbn: str) -> Optional[Livro]:
        """
        Get book by ISBN
        
        Args:
            isbn: Book ISBN
            
        Returns:
            Book instance or None if not found
        """
        return self.db.query(Livro).filter(
            and_(Livro.isbn == isbn, Livro.ativo == True)
        ).first()
    
    def get_all(
        self,
        skip: int = 0,
        limit: int = 20,
        categoria: Optional[Categoria] = None,
        condicao: Optional[CondicaoLivro] = None,
        preco_min: Optional[float] = None,
        preco_max: Optional[float] = None,
        order_by: str = "data_criacao",
        order_direction: str = "desc"
    ) -> Tuple[List[Livro], int]:
        """
        Get all books with filters and pagination
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            categoria: Filter by category
            condicao: Filter by condition
            preco_min: Minimum price filter
            preco_max: Maximum price filter
            order_by: Field to order by
            order_direction: Order direction (asc or desc)
            
        Returns:
            Tuple of (list of books, total count)
        """
        query = self.db.query(Livro).filter(Livro.ativo == True)
        
        # Apply filters
        if categoria:
            query = query.filter(Livro.categoria == categoria)
        
        if condicao:
            query = query.filter(Livro.condicao == condicao)
        
        if preco_min is not None:
            query = query.filter(Livro.preco >= preco_min)
        
        if preco_max is not None:
            query = query.filter(Livro.preco <= preco_max)
        
        # Get total count before pagination
        total = query.count()
        
        # Apply ordering
        order_field = getattr(Livro, order_by, Livro.data_criacao)
        if order_direction == "asc":
            query = query.order_by(asc(order_field))
        else:
            query = query.order_by(desc(order_field))
        
        # Apply pagination
        books = query.offset(skip).limit(limit).all()
        
        return books, total
    
    def search(
        self,
        search_term: str,
        skip: int = 0,
        limit: int = 20,
        categoria: Optional[Categoria] = None,
        condicao: Optional[CondicaoLivro] = None,
        preco_min: Optional[float] = None,
        preco_max: Optional[float] = None,
        order_by: str = "data_criacao",
        order_direction: str = "desc"
    ) -> Tuple[List[Livro], int]:
        """
        Search books by term with filters and pagination
        
        Args:
            search_term: Term to search in title, author, or ISBN
            skip: Number of records to skip
            limit: Maximum number of records to return
            categoria: Filter by category
            condicao: Filter by condition
            preco_min: Minimum price filter
            preco_max: Maximum price filter
            order_by: Field to order by
            order_direction: Order direction (asc or desc)
            
        Returns:
            Tuple of (list of books, total count)
        """
        # Build search filter
        search_filter = or_(
            Livro.titulo.ilike(f"%{search_term}%"),
            Livro.autor.ilike(f"%{search_term}%"),
            Livro.isbn.ilike(f"%{search_term}%")
        )
        
        query = self.db.query(Livro).filter(
            and_(Livro.ativo == True, search_filter)
        )
        
        # Apply additional filters
        if categoria:
            query = query.filter(Livro.categoria == categoria)
        
        if condicao:
            query = query.filter(Livro.condicao == condicao)
        
        if preco_min is not None:
            query = query.filter(Livro.preco >= preco_min)
        
        if preco_max is not None:
            query = query.filter(Livro.preco <= preco_max)
        
        # Get total count before pagination
        total = query.count()
        
        # Apply ordering
        order_field = getattr(Livro, order_by, Livro.data_criacao)
        if order_direction == "asc":
            query = query.order_by(asc(order_field))
        else:
            query = query.order_by(desc(order_field))
        
        # Apply pagination
        books = query.offset(skip).limit(limit).all()
        
        return books, total
    
    def update(self, book_id: int, update_data: dict) -> Optional[Livro]:
        """
        Update book data
        
        Args:
            book_id: Book ID
            update_data: Dictionary with fields to update
            
        Returns:
            Updated book instance or None if not found
        """
        book = self.get_by_id(book_id)
        if not book:
            return None
        
        for field, value in update_data.items():
            if hasattr(book, field):
                setattr(book, field, value)
        
        self.db.commit()
        self.db.refresh(book)
        return book
    
    def delete(self, book_id: int) -> bool:
        """
        Soft delete book (set ativo = False)
        
        Args:
            book_id: Book ID
            
        Returns:
            True if deleted successfully, False otherwise
        """
        book = self.get_by_id(book_id)
        if not book:
            return False
        
        book.ativo = False
        self.db.commit()
        return True
    
    def update_stock(self, book_id: int, quantity_change: int) -> Optional[Livro]:
        """
        Update book stock
        
        Args:
            book_id: Book ID
            quantity_change: Quantity to add (positive) or remove (negative)
            
        Returns:
            Updated book instance or None if not found
        """
        book = self.get_by_id(book_id)
        if not book:
            return None
        
        book.estoque = book.estoque + quantity_change
        if book.estoque < 0:
            book.estoque = 0
        
        self.db.commit()
        self.db.refresh(book)
        return book
    
    def isbn_exists(self, isbn: str, exclude_id: Optional[int] = None) -> bool:
        """
        Check if ISBN already exists
        
        Args:
            isbn: ISBN to check
            exclude_id: Book ID to exclude from check (for updates)
            
        Returns:
            True if ISBN exists, False otherwise
        """
        query = self.db.query(Livro).filter(Livro.isbn == isbn)
        if exclude_id:
            query = query.filter(Livro.id != exclude_id)
        return query.first() is not None
