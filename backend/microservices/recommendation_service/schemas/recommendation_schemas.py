    allow_origins=["*"],  # In productio# Recommendation Schemas - Pydantic models for request/response validation
# Defines data structures for API endpoints

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class BookRecommendationResponse(BaseModel):
    """Schema for book recommendation response"""
    livro_id: int = Field(..., description="ID do livro recomendado")
    titulo: str = Field(..., description="Título do livro")
    autor: str = Field(..., description="Autor do livro")
    preco: float = Field(..., description="Preço do livro")
    categoria: Optional[str] = Field(None, description="Categoria do livro")
    score: float = Field(..., ge=0, le=1, description="Pontuação de relevância (0-1)")
    motivo: str = Field(..., description="Motivo da recomendação")
    tipo_recomendacao: str = Field(..., description="Tipo de recomendação")
    isbn: Optional[str] = None
    estoque: Optional[int] = None
    
    class Config:
        from_attributes = True


class RecommendationListResponse(BaseModel):
    """Schema for recommendation list response"""
    items: List[BookRecommendationResponse]
    total: int
    usuario_id: int
    tipo_algoritmo: str = "hibrido"
    
    class Config:
        from_attributes = True


class SimilarBooksResponse(BaseModel):
    """Schema for similar books response"""
    livro_original_id: int
    livro_original_titulo: str
    similares: List[BookRecommendationResponse]
    criterio: str = Field(..., description="Critério de similaridade usado")
    total: int
    
    class Config:
        from_attributes = True


class RecommendationRequest(BaseModel):
    """Schema for creating recommendations"""
    usuario_id: int = Field(..., description="ID do usuário")
    limit: int = Field(10, ge=1, le=50, description="Número máximo de recomendações")
    tipo: Optional[str] = Field(None, description="Tipo de recomendação específico")
