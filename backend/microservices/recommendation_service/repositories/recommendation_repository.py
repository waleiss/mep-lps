# Recommendation Repository - Data access layer for recommendation operations
# Implements repository pattern for recommendation data access

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from datetime import datetime, timedelta

from models import Recomendacao, TipoRecomendacao, StatusRecomendacao


class RecommendationRepository:
    """Repository for recommendation data operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, recommendation_data: dict) -> Recomendacao:
        """
        Create a new recommendation
        
        Args:
            recommendation_data: Recommendation data dictionary
            
        Returns:
            Created recommendation instance
        """
        db_recommendation = Recomendacao(**recommendation_data)
        self.db.add(db_recommendation)
        self.db.commit()
        self.db.refresh(db_recommendation)
        return db_recommendation
    
    def create_bulk(self, recommendations_data: List[dict]) -> List[Recomendacao]:
        """
        Create multiple recommendations
        
        Args:
            recommendations_data: List of recommendation data dictionaries
            
        Returns:
            List of created recommendation instances
        """
        db_recommendations = [Recomendacao(**data) for data in recommendations_data]
        self.db.add_all(db_recommendations)
        self.db.commit()
        
        for rec in db_recommendations:
            self.db.refresh(rec)
        
        return db_recommendations
    
    def get_by_usuario(
        self,
        usuario_id: int,
        limit: int = 10,
        tipo: Optional[TipoRecomendacao] = None
    ) -> List[Recomendacao]:
        """
        Get active recommendations for a user
        
        Args:
            usuario_id: User ID
            limit: Maximum number of recommendations
            tipo: Optional filter by recommendation type
            
        Returns:
            List of recommendations
        """
        query = self.db.query(Recomendacao).filter(
            Recomendacao.usuario_id == usuario_id,
            Recomendacao.status == StatusRecomendacao.ATIVA,
            Recomendacao.data_expiracao > datetime.now()
        )
        
        if tipo:
            query = query.filter(Recomendacao.tipo == tipo)
        
        return query.order_by(desc(Recomendacao.score)).limit(limit).all()
    
    def get_by_livro(self, livro_id: int, limit: int = 10) -> List[Recomendacao]:
        """
        Get recommendations that include a specific book
        
        Args:
            livro_id: Book ID
            limit: Maximum number of recommendations
            
        Returns:
            List of recommendations
        """
        return self.db.query(Recomendacao).filter(
            Recomendacao.livro_id == livro_id,
            Recomendacao.status == StatusRecomendacao.ATIVA
        ).order_by(desc(Recomendacao.score)).limit(limit).all()
    
    def get_popular_books(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get most recommended books (popularity based)
        
        Args:
            limit: Maximum number of books
            
        Returns:
            List of dictionaries with livro_id and count
        """
        results = self.db.query(
            Recomendacao.livro_id,
            func.count(Recomendacao.id).label('count')
        ).filter(
            Recomendacao.status == StatusRecomendacao.ATIVA
        ).group_by(
            Recomendacao.livro_id
        ).order_by(
            desc('count')
        ).limit(limit).all()
        
        return [{"livro_id": r.livro_id, "count": r.count} for r in results]
    
    def deactivate_old_recommendations(self, usuario_id: int) -> int:
        """
        Deactivate old recommendations for a user
        
        Args:
            usuario_id: User ID
            
        Returns:
            Number of deactivated recommendations
        """
        count = self.db.query(Recomendacao).filter(
            Recomendacao.usuario_id == usuario_id,
            Recomendacao.status == StatusRecomendacao.ATIVA
        ).update({
            "status": StatusRecomendacao.INATIVA
        })
        
        self.db.commit()
        return count
    
    def delete_expired(self) -> int:
        """
        Delete expired recommendations
        
        Returns:
            Number of deleted recommendations
        """
        count = self.db.query(Recomendacao).filter(
            Recomendacao.data_expiracao < datetime.now()
        ).delete()
        
        self.db.commit()
        return count
    
    def recommendation_exists(
        self,
        usuario_id: int,
        livro_id: int,
        tipo: TipoRecomendacao
    ) -> bool:
        """
        Check if a recommendation already exists
        
        Args:
            usuario_id: User ID
            livro_id: Book ID
            tipo: Recommendation type
            
        Returns:
            True if exists, False otherwise
        """
        return self.db.query(Recomendacao).filter(
            Recomendacao.usuario_id == usuario_id,
            Recomendacao.livro_id == livro_id,
            Recomendacao.tipo == tipo,
            Recomendacao.status == StatusRecomendacao.ATIVA
        ).first() is not None
