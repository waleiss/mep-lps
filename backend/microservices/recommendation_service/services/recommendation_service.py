# Recommendation Service - Business logic for recommendation operations
# Implements recommendation algorithms based on various criteria

from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from fastapi import HTTPException, status as http_status
from datetime import datetime, timedelta
import httpx

from models import Recomendacao, TipoRecomendacao, StatusRecomendacao, Base
from repositories.recommendation_repository import RecommendationRepository
from config import settings


class RecommendationService:
    """Service for recommendation business logic operations"""
    
    def __init__(self, db: Session):
        self.db = db
        self.recommendation_repo = RecommendationRepository(db)
    
    async def _fetch_book_details(self, livro_id: int) -> Optional[Dict[str, Any]]:
        """
        Fetch book details from catalog service
        
        Args:
            livro_id: Book ID
            
        Returns:
            Book details dictionary or None
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{settings.catalog_service_url}/livros/{livro_id}",
                    timeout=3.0
                )
                if response.status_code == 200:
                    return response.json()
        except Exception as e:
            print(f"Error fetching book details: {e}")
        return None
    
    async def _fetch_books_by_author(self, autor: str, exclude_id: Optional[int] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Fetch books by the same author from catalog service
        
        Args:
            autor: Author name
            exclude_id: Book ID to exclude from results
            limit: Maximum number of books
            
        Returns:
            List of books
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{settings.catalog_service_url}/buscar",
                    params={"q": autor, "page_size": limit + 5},
                    timeout=3.0
                )
                if response.status_code == 200:
                    data = response.json()
                    books = data.get("items", [])
                    
                    # Filter by author and exclude current book
                    filtered = [
                        book for book in books
                        if book.get("autor", "").lower() == autor.lower()
                        and book.get("id") != exclude_id
                    ]
                    
                    return filtered[:limit]
        except Exception as e:
            print(f"Error fetching books by author: {e}")
        return []
    
    async def _fetch_books_by_category(self, categoria: str, exclude_id: Optional[int] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Fetch books from the same category from catalog service
        
        Args:
            categoria: Category name
            exclude_id: Book ID to exclude from results
            limit: Maximum number of books
            
        Returns:
            List of books
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{settings.catalog_service_url}/livros",
                    params={"categoria": categoria, "page_size": limit + 5},
                    timeout=3.0
                )
                if response.status_code == 200:
                    data = response.json()
                    books = data.get("items", [])
                    
                    # Exclude current book
                    filtered = [book for book in books if book.get("id") != exclude_id]
                    
                    return filtered[:limit]
        except Exception as e:
            print(f"Error fetching books by category: {e}")
        return []
    
    async def _fetch_popular_books(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Fetch popular/best-selling books from catalog service
        
        Args:
            limit: Maximum number of books
            
        Returns:
            List of books
        """
        try:
            async with httpx.AsyncClient() as client:
                # Fetch books ordered by creation date (novidades) or custom popularity metric
                response = await client.get(
                    f"{settings.catalog_service_url}/livros",
                    params={"page_size": limit, "order_by": "data_criacao", "order_direction": "desc"},
                    timeout=3.0
                )
                if response.status_code == 200:
                    data = response.json()
                    return data.get("items", [])
        except Exception as e:
            print(f"Error fetching popular books: {e}")
        return []
    
    def _create_recommendation_response(
        self,
        book: Dict[str, Any],
        score: float,
        motivo: str,
        tipo: str
    ) -> Dict[str, Any]:
        """
        Create a recommendation response from book data
        
        Args:
            book: Book data dictionary
            score: Recommendation score
            motivo: Reason for recommendation
            tipo: Type of recommendation
            
        Returns:
            Recommendation response dictionary
        """
        return {
            "livro_id": book.get("id"),
            "titulo": book.get("titulo", ""),
            "autor": book.get("autor", ""),
            "preco": book.get("preco", 0.0),
            "categoria": book.get("categoria"),
            "isbn": book.get("isbn"),
            "estoque": book.get("estoque", 0),
            "score": score,
            "motivo": motivo,
            "tipo_recomendacao": tipo
        }
    
    async def get_recommendations_for_user(
        self,
        usuario_id: int,
        limit: int = 10
    ) -> Dict[str, Any]:
        """
        Get personalized recommendations for a user
        
        Combines multiple recommendation strategies:
        - Popular books (novidades)
        - Trending books
        
        Args:
            usuario_id: User ID
            limit: Maximum number of recommendations
            
        Returns:
            Dictionary with recommendations
        """
        recommendations = []
        
        # Strategy 1: Popular/New books
        popular_books = await self._fetch_popular_books(limit)
        
        for i, book in enumerate(popular_books[:limit]):
            score = 1.0 - (i * 0.05)  # Decreasing score based on position
            rec = self._create_recommendation_response(
                book=book,
                score=max(score, 0.5),
                motivo="Livro popular e recente no catálogo",
                tipo="novidades"
            )
            recommendations.append(rec)
        
        return {
            "items": recommendations,
            "total": len(recommendations),
            "usuario_id": usuario_id,
            "tipo_algoritmo": "hibrido"
        }
    
    async def get_similar_books(
        self,
        livro_id: int,
        limit: int = 10
    ) -> Dict[str, Any]:
        """
        Get books similar to a given book
        
        Similarity criteria:
        1. Same author (highest priority)
        2. Same category
        3. Price range similarity
        
        Args:
            livro_id: Book ID
            limit: Maximum number of similar books
            
        Returns:
            Dictionary with similar books and criteria
        """
        # Fetch original book details
        original_book = await self._fetch_book_details(livro_id)
        
        if not original_book:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="Livro não encontrado"
            )
        
        similar_books = []
        
        # Strategy 1: Same author (score: 0.9)
        author_books = await self._fetch_books_by_author(
            original_book.get("autor", ""),
            exclude_id=livro_id,
            limit=5
        )
        
        for book in author_books:
            rec = self._create_recommendation_response(
                book=book,
                score=0.9,
                motivo=f"Mesmo autor: {book.get('autor')}",
                tipo="mesmo_autor"
            )
            similar_books.append(rec)
        
        # Strategy 2: Same category (score: 0.7)
        if len(similar_books) < limit and original_book.get("categoria"):
            category_books = await self._fetch_books_by_category(
                original_book.get("categoria", ""),
                exclude_id=livro_id,
                limit=limit - len(similar_books)
            )
            
            for book in category_books:
                # Skip if already in list
                if any(b["livro_id"] == book.get("id") for b in similar_books):
                    continue
                
                rec = self._create_recommendation_response(
                    book=book,
                    score=0.7,
                    motivo=f"Mesma categoria: {book.get('categoria')}",
                    tipo="mesma_categoria"
                )
                similar_books.append(rec)
        
        # Sort by score
        similar_books.sort(key=lambda x: x["score"], reverse=True)
        
        return {
            "livro_original_id": livro_id,
            "livro_original_titulo": original_book.get("titulo", ""),
            "similares": similar_books[:limit],
            "criterio": "autor_e_categoria",
            "total": len(similar_books[:limit])
        }
    
    async def get_recommendations_by_author(
        self,
        livro_id: int,
        limit: int = 10
    ) -> Dict[str, Any]:
        """
        Get recommendations based on the same author
        
        Args:
            livro_id: Book ID
            limit: Maximum number of recommendations
            
        Returns:
            Dictionary with recommendations
        """
        # Fetch book details
        book = await self._fetch_book_details(livro_id)
        
        if not book:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="Livro não encontrado"
            )
        
        # Get books by same author
        author_books = await self._fetch_books_by_author(
            book.get("autor", ""),
            exclude_id=livro_id,
            limit=limit
        )
        
        recommendations = []
        for book_item in author_books:
            rec = self._create_recommendation_response(
                book=book_item,
                score=0.95,
                motivo=f"Mesmo autor: {book_item.get('autor')}",
                tipo="mesmo_autor"
            )
            recommendations.append(rec)
        
        return {
            "items": recommendations,
            "total": len(recommendations),
            "criterio": "mesmo_autor",
            "autor": book.get("autor", "")
        }
    
    async def get_recommendations_by_category(
        self,
        categoria: str,
        limit: int = 10,
        exclude_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Get recommendations based on category
        
        Args:
            categoria: Category name
            limit: Maximum number of recommendations
            exclude_id: Optional book ID to exclude
            
        Returns:
            Dictionary with recommendations
        """
        # Get books from same category
        category_books = await self._fetch_books_by_category(
            categoria,
            exclude_id=exclude_id,
            limit=limit
        )
        
        recommendations = []
        for book in category_books:
            rec = self._create_recommendation_response(
                book=book,
                score=0.8,
                motivo=f"Mesma categoria: {categoria}",
                tipo="mesma_categoria"
            )
            recommendations.append(rec)
        
        return {
            "items": recommendations,
            "total": len(recommendations),
            "criterio": "categoria",
            "categoria": categoria
        }
    
    async def get_popular_recommendations(
        self,
        limit: int = 10
    ) -> Dict[str, Any]:
        """
        Get popular book recommendations (best sellers / trending)
        
        Args:
            limit: Maximum number of recommendations
            
        Returns:
            Dictionary with recommendations
        """
        # Get popular books
        popular_books = await self._fetch_popular_books(limit)
        
        recommendations = []
        for i, book in enumerate(popular_books):
            score = 1.0 - (i * 0.03)  # Slight decrease based on position
            rec = self._create_recommendation_response(
                book=book,
                score=max(score, 0.6),
                motivo="Livro popular entre os leitores",
                tipo="mais_vendidos"
            )
            recommendations.append(rec)
        
        return {
            "items": recommendations,
            "total": len(recommendations),
            "criterio": "popularidade"
        }
