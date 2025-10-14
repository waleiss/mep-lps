# Schemas package - Pydantic models for request/response validation
from .endereco_schemas import (
    EnderecoCreate,
    EnderecoUpdate,
    EnderecoResponse,
    EnderecoListResponse
)
from .frete_schemas import (
    FreteCalculoRequest,
    FreteOpcao,
    FreteCalculoResponse,
    ViaCEPResponse
)

__all__ = [
    "EnderecoCreate",
    "EnderecoUpdate",
    "EnderecoResponse",
    "EnderecoListResponse",
    "FreteCalculoRequest",
    "FreteOpcao",
    "FreteCalculoResponse",
    "ViaCEPResponse"
]

