# Recommendation Service - Mundo em Palavras
# Microserviço responsável por recomendações personalizadas
# Gerencia algoritmos de recomendação baseados em comportamento e preferências

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

# Configuração da aplicação FastAPI
app = FastAPI(
    title="Recommendation Service",
    description="Microserviço de recomendações personalizadas",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Modelos Pydantic
class BookRecommendation(BaseModel):
    book_id: str
    title: str
    author: str
    price: float
    score: float
    reason: str

class RecommendationRequest(BaseModel):
    user_id: str
    limit: int = 10
    categories: Optional[List[str]] = None

# Dados mock para demonstração
recommendations_db = {
    "user_123": [
        BookRecommendation(
            book_id="1",
            title="O Senhor dos Anéis",
            author="J.R.R. Tolkien",
            price=49.90,
            score=0.95,
            reason="Baseado em seus livros de fantasia favoritos"
        ),
        BookRecommendation(
            book_id="2",
            title="1984",
            author="George Orwell",
            price=29.90,
            score=0.88,
            reason="Outros usuários com gostos similares também gostaram"
        )
    ]
}

# Rotas básicas
@app.get("/")
async def root():
    """Endpoint raiz do serviço de recomendações"""
    return {
        "service": "Recommendation Service",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Health check do serviço"""
    return {"status": "healthy", "service": "recommendation"}

@app.post("/recommendations", response_model=List[BookRecommendation])
async def get_recommendations(request: RecommendationRequest):
    """Obter recomendações personalizadas para um usuário"""
    # TODO: Implementar algoritmos de recomendação reais
    # Por enquanto, retorna recomendações mock
    
    user_recommendations = recommendations_db.get(request.user_id, [])
    
    # Filtrar por categorias se especificado
    if request.categories:
        user_recommendations = [
            rec for rec in user_recommendations 
            if any(cat.lower() in rec.title.lower() or cat.lower() in rec.author.lower() 
                  for cat in request.categories)
        ]
    
    return user_recommendations[:request.limit]

@app.get("/recommendations/{user_id}", response_model=List[BookRecommendation])
async def get_user_recommendations(
    user_id: str,
    limit: int = Query(10, ge=1, le=50),
    category: Optional[str] = None
):
    """Obter recomendações para um usuário específico"""
    user_recommendations = recommendations_db.get(user_id, [])
    
    if category:
        user_recommendations = [
            rec for rec in user_recommendations 
            if category.lower() in rec.title.lower() or category.lower() in rec.author.lower()
        ]
    
    return user_recommendations[:limit]

@app.post("/feedback")
async def submit_feedback(
    user_id: str,
    book_id: str,
    rating: int,
    feedback_type: str = "view"  # view, purchase, like, dislike
):
    """Enviar feedback do usuário para melhorar recomendações"""
    # TODO: Implementar sistema de feedback real
    return {
        "message": "Feedback received",
        "user_id": user_id,
        "book_id": book_id,
        "rating": rating,
        "feedback_type": feedback_type
    }

@app.get("/trending")
async def get_trending_books(limit: int = Query(10, ge=1, le=50)):
    """Obter livros em alta"""
    # TODO: Implementar algoritmo de trending real
    trending_books = [
        BookRecommendation(
            book_id="3",
            title="Duna",
            author="Frank Herbert",
            price=39.90,
            score=0.92,
            reason="Livro mais vendido esta semana"
        ),
        BookRecommendation(
            book_id="4",
            title="O Hobbit",
            author="J.R.R. Tolkien",
            price=34.90,
            score=0.89,
            reason="Tendência crescente entre leitores de fantasia"
        )
    ]
    
    return trending_books[:limit]

@app.get("/similar/{book_id}")
async def get_similar_books(book_id: str, limit: int = Query(5, ge=1, le=20)):
    """Obter livros similares a um livro específico"""
    # TODO: Implementar algoritmo de similaridade real
    similar_books = [
        BookRecommendation(
            book_id="5",
            title="As Crônicas de Nárnia",
            author="C.S. Lewis",
            price=42.90,
            score=0.85,
            reason="Similar em gênero e tema"
        )
    ]
    
    return similar_books[:limit]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8007)