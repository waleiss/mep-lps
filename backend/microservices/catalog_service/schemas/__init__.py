# Schemas package for Catalog Service
# Pydantic schemas for request/response validation

from .book_schemas import (
    BookBase,
    BookCreate,
    BookUpdate,
    BookResponse,
    BookListResponse,
    CategoryResponse,
    ConditionResponse
)

__all__ = [
    "BookBase",
    "BookCreate",
    "BookUpdate",
    "BookResponse",
    "BookListResponse",
    "CategoryResponse",
    "ConditionResponse"
]
