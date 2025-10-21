# Book Schemas - Pydantic models for request/response validation
# Defines data structures for API endpoints

from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime


class BookBase(BaseModel):
    """Base book schema with common fields"""
    titulo: str = Field(..., min_length=1, max_length=255, description="Título do livro")
    autor: str = Field(..., min_length=1, max_length=255, description="Autor do livro")
    isbn: str = Field(..., min_length=10, max_length=13, description="ISBN do livro")
    editora: Optional[str] = Field(None, max_length=100, description="Editora")
    ano_publicacao: Optional[int] = Field(None, ge=1000, le=9999, description="Ano de publicação")
    edicao: Optional[str] = Field(None, max_length=50, description="Edição")
    numero_paginas: Optional[int] = Field(None, ge=1, description="Número de páginas")
    sinopse: Optional[str] = Field(None, description="Sinopse do livro")
    imagem_url: Optional[str] = Field(None, max_length=500, description="URL da imagem de capa")
    preco: float = Field(..., ge=0, description="Preço do livro")
    estoque: int = Field(default=0, ge=0, description="Quantidade em estoque")
    categoria: str = Field(..., description="Categoria do livro")
    condicao: str = Field(default="novo", description="Condição do livro")
    
    @validator('isbn')
    def validate_isbn(cls, v):
        """Validate ISBN format"""
        # Remove hyphens and spaces
        isbn_clean = v.replace('-', '').replace(' ', '')
        if len(isbn_clean) not in [10, 13]:
            raise ValueError('ISBN deve ter 10 ou 13 dígitos')
        if not isbn_clean.isdigit():
            raise ValueError('ISBN deve conter apenas dígitos')
        return isbn_clean
    
    @validator('categoria')
    def validate_categoria(cls, v):
        """Validate category"""
        valid_categories = ['ficcao', 'nao_ficcao', 'tecnico', 'academico', 'infantil', 'outros']
        if v not in valid_categories:
            raise ValueError(f'Categoria deve ser uma das seguintes: {", ".join(valid_categories)}')
        return v
    
    @validator('condicao')
    def validate_condicao(cls, v):
        """Validate condition"""
        valid_conditions = ['novo', 'usado', 'semi_novo']
        if v not in valid_conditions:
            raise ValueError(f'Condição deve ser uma das seguintes: {", ".join(valid_conditions)}')
        return v


class BookCreate(BookBase):
    """Schema for creating a new book"""
    pass


class BookUpdate(BaseModel):
    """Schema for updating a book (all fields optional)"""
    titulo: Optional[str] = Field(None, min_length=1, max_length=255)
    autor: Optional[str] = Field(None, min_length=1, max_length=255)
    isbn: Optional[str] = Field(None, min_length=10, max_length=13)
    editora: Optional[str] = Field(None, max_length=100)
    ano_publicacao: Optional[int] = Field(None, ge=1000, le=9999)
    edicao: Optional[str] = Field(None, max_length=50)
    numero_paginas: Optional[int] = Field(None, ge=1)
    sinopse: Optional[str] = None
    imagem_url: Optional[str] = Field(None, max_length=500)
    preco: Optional[float] = Field(None, ge=0)
    estoque: Optional[int] = Field(None, ge=0)
    categoria: Optional[str] = None
    condicao: Optional[str] = None
    ativo: Optional[bool] = None
    
    @validator('isbn')
    def validate_isbn(cls, v):
        """Validate ISBN format"""
        if v is None:
            return v
        isbn_clean = v.replace('-', '').replace(' ', '')
        if len(isbn_clean) not in [10, 13]:
            raise ValueError('ISBN deve ter 10 ou 13 dígitos')
        if not isbn_clean.isdigit():
            raise ValueError('ISBN deve conter apenas dígitos')
        return isbn_clean
    
    @validator('categoria')
    def validate_categoria(cls, v):
        """Validate category"""
        if v is None:
            return v
        valid_categories = ['ficcao', 'nao_ficcao', 'tecnico', 'academico', 'infantil', 'outros']
        if v not in valid_categories:
            raise ValueError(f'Categoria deve ser uma das seguintes: {", ".join(valid_categories)}')
        return v
    
    @validator('condicao')
    def validate_condicao(cls, v):
        """Validate condition"""
        if v is None:
            return v
        valid_conditions = ['novo', 'usado', 'semi_novo']
        if v not in valid_conditions:
            raise ValueError(f'Condição deve ser uma das seguintes: {", ".join(valid_conditions)}')
        return v


class BookResponse(BaseModel):
    """Schema for book response"""
    id: int
    titulo: str
    autor: str
    isbn: str
    editora: Optional[str] = None
    ano_publicacao: Optional[int] = None
    edicao: Optional[str] = None
    numero_paginas: Optional[int] = None
    sinopse: Optional[str] = None
    imagem_url: Optional[str] = None
    preco: float
    estoque: int
    categoria: str
    condicao: str
    ativo: bool
    data_criacao: Optional[str] = None
    data_atualizacao: Optional[str] = None
    
    class Config:
        from_attributes = True


class BookListResponse(BaseModel):
    """Schema for paginated book list response"""
    items: List[BookResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_previous: bool
    search_term: Optional[str] = None


class CategoryResponse(BaseModel):
    """Schema for category response"""
    value: str
    label: str


class ConditionResponse(BaseModel):
    """Schema for condition response"""
    value: str
    label: str
