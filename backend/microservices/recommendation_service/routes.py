# Recommendation Service Routes
# Defines API endpoints for recommendation operations

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from database import get_db
from services.recommendation_service import RecommendationService
from schemas.recommendation_schemas import (
    RecommendationListResponse,
    SimilarBooksResponse
)

router = APIRouter(prefix="/api/v1", tags=["recommendations"])


@router.get(
    "/recomendacoes",
    response_model=RecommendationListResponse,
    summary="Obter recomendações personalizadas",
    description="Retorna recomendações de livros para um usuário baseado em múltiplos critérios"
)
async def get_recommendations(
    usuario_id: int = Query(..., description="ID do usuário"),
    limit: int = Query(10, ge=1, le=50, description="Número máximo de recomendações"),
    db: Session = Depends(get_db)
):
    """
    Retorna recomendações personalizadas para um usuário.
    
    **Critérios de recomendação:**
    - Livros populares e novidades
    - Baseado em comportamento (futuro)
    
    **Parâmetros:**
    - `usuario_id`: ID do usuário (obrigatório)
    - `limit`: Número máximo de recomendações (1-50, padrão: 10)
    
    **Exemplo de resposta:**
    ```json
    {
        "items": [
            {
                "livro_id": 1,
                "titulo": "O Senhor dos Anéis",
                "autor": "J.R.R. Tolkien",
                "preco": 89.90,
                "score": 0.95,
                "motivo": "Livro popular entre os leitores",
                "tipo_recomendacao": "mais_vendidos"
            }
        ],
        "total": 10,
        "usuario_id": 123,
        "tipo_algoritmo": "hibrido"
    }
    ```
    """
    service = RecommendationService(db)
    
    try:
        recommendations = await service.get_recommendations_for_user(
            usuario_id=usuario_id,
            limit=limit
        )
        return recommendations
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao gerar recomendações: {str(e)}"
        )


@router.get(
    "/livros/{livro_id}/similares",
    response_model=SimilarBooksResponse,
    summary="Obter livros similares",
    description="Retorna livros similares a um livro específico baseado em autor e categoria"
)
async def get_similar_books(
    livro_id: int,
    limit: int = Query(10, ge=1, le=50, description="Número máximo de livros similares"),
    db: Session = Depends(get_db)
):
    """
    Retorna livros similares a um livro específico.
    
    **Critérios de similaridade:**
    1. Mesmo autor (score: 0.9)
    2. Mesma categoria (score: 0.7)
    3. Faixa de preço similar (score: 0.5)
    
    **Parâmetros:**
    - `livro_id`: ID do livro de referência
    - `limit`: Número máximo de livros similares (1-50, padrão: 10)
    
    **Exemplo de resposta:**
    ```json
    {
        "livro_original_id": 1,
        "livro_original_titulo": "O Hobbit",
        "similares": [
            {
                "livro_id": 2,
                "titulo": "O Senhor dos Anéis",
                "autor": "J.R.R. Tolkien",
                "preco": 89.90,
                "score": 0.9,
                "motivo": "Mesmo autor: J.R.R. Tolkien",
                "tipo_recomendacao": "mesmo_autor"
            }
        ],
        "criterio": "autor_e_categoria",
        "total": 5
    }
    ```
    """
    service = RecommendationService(db)
    
    try:
        similar_books = await service.get_similar_books(
            livro_id=livro_id,
            limit=limit
        )
        return similar_books
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar livros similares: {str(e)}"
        )


@router.get(
    "/livros/{livro_id}/por-autor",
    response_model=RecommendationListResponse,
    summary="Obter recomendações do mesmo autor",
    description="Retorna livros do mesmo autor"
)
async def get_recommendations_by_author(
    livro_id: int,
    limit: int = Query(10, ge=1, le=50, description="Número máximo de recomendações"),
    db: Session = Depends(get_db)
):
    """
    Retorna livros do mesmo autor que o livro especificado.
    
    **Parâmetros:**
    - `livro_id`: ID do livro de referência
    - `limit`: Número máximo de recomendações (1-50, padrão: 10)
    """
    service = RecommendationService(db)
    
    try:
        recommendations = await service.get_recommendations_by_author(
            livro_id=livro_id,
            limit=limit
        )
        return recommendations
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar recomendações por autor: {str(e)}"
        )


@router.get(
    "/categoria/{categoria}",
    response_model=RecommendationListResponse,
    summary="Obter recomendações por categoria",
    description="Retorna livros de uma categoria específica"
)
async def get_recommendations_by_category(
    categoria: str,
    limit: int = Query(10, ge=1, le=50, description="Número máximo de recomendações"),
    exclude_id: Optional[int] = Query(None, description="ID do livro a excluir"),
    db: Session = Depends(get_db)
):
    """
    Retorna livros de uma categoria específica.
    
    **Parâmetros:**
    - `categoria`: Nome da categoria
    - `limit`: Número máximo de recomendações (1-50, padrão: 10)
    - `exclude_id`: ID do livro a excluir (opcional)
    """
    service = RecommendationService(db)
    
    try:
        recommendations = await service.get_recommendations_by_category(
            categoria=categoria,
            limit=limit,
            exclude_id=exclude_id
        )
        return recommendations
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar recomendações por categoria: {str(e)}"
        )


@router.get(
    "/populares",
    response_model=RecommendationListResponse,
    summary="Obter livros populares",
    description="Retorna os livros mais populares (novidades e mais vendidos)"
)
async def get_popular_recommendations(
    limit: int = Query(10, ge=1, le=50, description="Número máximo de recomendações"),
    db: Session = Depends(get_db)
):
    """
    Retorna os livros mais populares.
    
    **Critérios:**
    - Novidades recentes
    - Livros mais vendidos
    
    **Parâmetros:**
    - `limit`: Número máximo de recomendações (1-50, padrão: 10)
    """
    service = RecommendationService(db)
    
    try:
        recommendations = await service.get_popular_recommendations(limit=limit)
        return recommendations
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar livros populares: {str(e)}"
        )


@router.get("/health", tags=["health"])
async def health_check():
    """
    Endpoint de health check.
    
    Retorna o status do serviço.
    """
    return {
        "status": "healthy",
        "service": "recommendation-service"
    }