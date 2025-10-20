# Schemas package for Recommendation Service
# Pydantic schemas for request/response validation

from .recommendation_schemas import (
    BookRecommendationResponse,
    RecommendationListResponse,
    SimilarBooksResponse
)

__all__ = [
    "BookRecommendationResponse",
    "RecommendationListResponse",
    "SimilarBooksResponse"
]
