# Rotas da API REST para frete e endereços
# Endpoints: /frete/calcular, /enderecos, /viacep
# Implementa RF4.1, RF4.2

from fastapi import APIRouter, Depends, HTTPException, status, Path, Query
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from services.endereco_service import EnderecoService
from services.frete_service import FreteService
from services.viacep_service import ViaCEPService
from schemas.endereco_schemas import (
    EnderecoCreate,
    EnderecoUpdate,
    EnderecoResponse,
    EnderecoListResponse
)
from schemas.frete_schemas import (
    FreteCalculoRequest,
    FreteCalculoResponse,
    ViaCEPResponse
)

# Create router
router = APIRouter()


# ===================================
# HEALTH CHECK ENDPOINTS
# ===================================

@router.get("/")
async def root():
    """Endpoint raiz do serviço de frete"""
    return {
        "service": "Shipping Service",
        "status": "running",
        "version": "2.0.0",
        "features": [
            "Cálculo de frete",
            "Gerenciamento de endereços",
            "Validação de CEP via ViaCEP",
            "Frete fixo: R$ 15,00 (10 dias) ou Grátis (20 dias)"
        ]
    }


@router.get("/health")
async def health_check():
    """Health check do serviço"""
    return {
        "status": "healthy",
        "service": "shipping",
        "version": "2.0.0"
    }


# ===================================
# FRETE ENDPOINTS
# ===================================

@router.post("/frete/calcular", response_model=FreteCalculoResponse)
async def calcular_frete(request: FreteCalculoRequest):
    """
    Calcula opções de frete disponíveis
    
    Args:
        request: Dados para cálculo (CEP de destino, peso total, valor dos produtos)
        
    Returns:
        Opções de frete com valores e prazos
        
    Raises:
        HTTPException: Se CEP for inválido ou houver erro no cálculo
    """
    try:
        resultado = await FreteService.calcular_frete(request)
        return resultado
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao calcular frete: {str(e)}"
        )


# ===================================
# VIACEP ENDPOINTS
# ===================================

@router.get("/viacep/{cep}", response_model=ViaCEPResponse)
async def consultar_cep(
    cep: str = Path(..., description="CEP a ser consultado (8 dígitos)")
):
    """
    Consulta informações de um CEP via API ViaCEP
    
    Args:
        cep: CEP a ser consultado
        
    Returns:
        Informações do endereço (rua, bairro, cidade, estado)
        
    Raises:
        HTTPException: Se CEP for inválido ou não encontrado
    """
    try:
        resultado = await ViaCEPService.consultar_cep(cep)
        return resultado
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao consultar CEP: {str(e)}"
        )


# ===================================
# ENDEREÇO ENDPOINTS
# ===================================

@router.post("/enderecos", response_model=EnderecoResponse, status_code=status.HTTP_201_CREATED)
async def criar_endereco(
    endereco_data: EnderecoCreate,
    db: Session = Depends(get_db)
):
    """
    Cria um novo endereço para o usuário
    
    Args:
        endereco_data: Dados do endereço
        db: Sessão do banco de dados
        
    Returns:
        Endereço criado
        
    Raises:
        HTTPException: Se houver erro na validação ou criação
    """
    try:
        service = EnderecoService(db)
        endereco = await service.criar_endereco(endereco_data)
        return endereco
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar endereço: {str(e)}"
        )


@router.get("/enderecos/usuario/{usuario_id}", response_model=EnderecoListResponse)
async def listar_enderecos_usuario(
    usuario_id: int = Path(..., gt=0, description="ID do usuário"),
    db: Session = Depends(get_db)
):
    """
    Lista todos os endereços de um usuário
    
    Args:
        usuario_id: ID do usuário
        db: Sessão do banco de dados
        
    Returns:
        Lista de endereços do usuário
    """
    try:
        service = EnderecoService(db)
        enderecos = service.listar_enderecos_usuario(usuario_id)
        return EnderecoListResponse(
            enderecos=enderecos,
            total=len(enderecos)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao listar endereços: {str(e)}"
        )


@router.get("/enderecos/{endereco_id}", response_model=EnderecoResponse)
async def obter_endereco(
    endereco_id: int = Path(..., gt=0, description="ID do endereço"),
    usuario_id: int = Query(..., gt=0, description="ID do usuário"),
    db: Session = Depends(get_db)
):
    """
    Obtém um endereço específico
    
    Args:
        endereco_id: ID do endereço
        usuario_id: ID do usuário (para validação)
        db: Sessão do banco de dados
        
    Returns:
        Endereço solicitado
        
    Raises:
        HTTPException: Se endereço não for encontrado ou não pertencer ao usuário
    """
    try:
        service = EnderecoService(db)
        endereco = service.obter_endereco(endereco_id, usuario_id)
        return endereco
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter endereço: {str(e)}"
        )


@router.get("/enderecos/usuario/{usuario_id}/principal", response_model=EnderecoResponse)
async def obter_endereco_principal(
    usuario_id: int = Path(..., gt=0, description="ID do usuário"),
    db: Session = Depends(get_db)
):
    """
    Obtém o endereço principal do usuário
    
    Args:
        usuario_id: ID do usuário
        db: Sessão do banco de dados
        
    Returns:
        Endereço principal do usuário
        
    Raises:
        HTTPException: Se usuário não tiver endereço principal
    """
    try:
        service = EnderecoService(db)
        endereco = service.obter_endereco_principal(usuario_id)
        
        if not endereco:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não possui endereço principal cadastrado"
            )
        
        return endereco
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter endereço principal: {str(e)}"
        )


@router.put("/enderecos/{endereco_id}", response_model=EnderecoResponse)
async def atualizar_endereco(
    endereco_id: int = Path(..., gt=0, description="ID do endereço"),
    endereco_data: EnderecoUpdate = ...,
    usuario_id: int = Query(..., gt=0, description="ID do usuário"),
    db: Session = Depends(get_db)
):
    """
    Atualiza um endereço existente
    
    Args:
        endereco_id: ID do endereço
        endereco_data: Dados a serem atualizados
        usuario_id: ID do usuário (para validação)
        db: Sessão do banco de dados
        
    Returns:
        Endereço atualizado
        
    Raises:
        HTTPException: Se endereço não for encontrado ou não pertencer ao usuário
    """
    try:
        service = EnderecoService(db)
        endereco = await service.atualizar_endereco(endereco_id, usuario_id, endereco_data)
        return endereco
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar endereço: {str(e)}"
        )


@router.delete("/enderecos/{endereco_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_endereco(
    endereco_id: int = Path(..., gt=0, description="ID do endereço"),
    usuario_id: int = Query(..., gt=0, description="ID do usuário"),
    db: Session = Depends(get_db)
):
    """
    Deleta (desativa) um endereço
    
    Args:
        endereco_id: ID do endereço
        usuario_id: ID do usuário (para validação)
        db: Sessão do banco de dados
        
    Returns:
        204 No Content
        
    Raises:
        HTTPException: Se endereço não for encontrado ou não pertencer ao usuário
    """
    try:
        service = EnderecoService(db)
        service.deletar_endereco(endereco_id, usuario_id)
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao deletar endereço: {str(e)}"
        )


@router.patch("/enderecos/{endereco_id}/principal", response_model=EnderecoResponse)
async def definir_endereco_principal(
    endereco_id: int = Path(..., gt=0, description="ID do endereço"),
    usuario_id: int = Query(..., gt=0, description="ID do usuário"),
    db: Session = Depends(get_db)
):
    """
    Define um endereço como principal do usuário
    
    Args:
        endereco_id: ID do endereço
        usuario_id: ID do usuário (para validação)
        db: Sessão do banco de dados
        
    Returns:
        Endereço atualizado como principal
        
    Raises:
        HTTPException: Se endereço não for encontrado ou não pertencer ao usuário
    """
    try:
        service = EnderecoService(db)
        endereco = service.definir_endereco_principal(endereco_id, usuario_id)
        return endereco
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao definir endereço principal: {str(e)}"
        )
