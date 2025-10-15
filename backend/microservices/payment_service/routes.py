# Rotas da API REST para pagamentos
# Endpoints: /pagamento/processar, /pagamento/status
# Implementa processamento de cartão, PIX e boleto

from fastapi import APIRouter, Depends, HTTPException, status, Path, Query
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from services.payment_service import PaymentService
from schemas.pagamento_schemas import (
    PagamentoCartaoRequest,
    PagamentoPixRequest,
    PagamentoBoletoRequest,
    PagamentoResponse,
    StatusPagamentoResponse,
    TransacaoLogResponse,
    PagamentoListResponse
)
from models import StatusPagamento


# Create router
router = APIRouter()


# ===================================
# HEALTH CHECK ENDPOINTS
# ===================================

@router.get("/")
async def root():
    """Endpoint raiz do serviço de pagamento"""
    return {
        "service": "Payment Service",
        "status": "running",
        "version": "2.0.0",
        "features": [
            "Processamento de cartão de crédito/débito",
            "Geração de PIX",
            "Geração de boleto bancário",
            "Consulta de status",
            "Logs de transação"
        ]
    }


@router.get("/health")
async def health_check():
    """Health check do serviço"""
    return {
        "status": "healthy",
        "service": "payment",
        "version": "2.0.0"
    }


# ===================================
# PAGAMENTO ENDPOINTS
# ===================================

@router.post("/pagamento/processar/cartao", response_model=PagamentoResponse, status_code=status.HTTP_201_CREATED)
async def processar_pagamento_cartao(
    request: PagamentoCartaoRequest,
    db: Session = Depends(get_db)
):
    """
    Processa pagamento com cartão de crédito/débito
    
    Simula processamento real:
    - Cartões terminados em número par: aprovados
    - Cartões terminados em número ímpar: 10% de chance de recusa
    - CVV 000: sempre recusado
    
    Args:
        request: Dados do cartão e pagamento
        db: Sessão do banco de dados
        
    Returns:
        Resultado do processamento com código de autorização
    """
    try:
        service = PaymentService(db)
        resultado = service.processar_cartao(request)
        return resultado
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao processar pagamento com cartão: {str(e)}"
        )


@router.post("/pagamento/processar/pix", response_model=PagamentoResponse, status_code=status.HTTP_201_CREATED)
async def processar_pagamento_pix(
    request: PagamentoPixRequest,
    db: Session = Depends(get_db)
):
    """
    Gera pagamento via PIX
    
    Retorna QR Code e chave PIX para pagamento.
    Validade: 30 minutos
    
    Args:
        request: Dados do pagamento PIX
        db: Sessão do banco de dados
        
    Returns:
        QR Code e chave PIX
    """
    try:
        service = PaymentService(db)
        resultado = service.processar_pix(request)
        return resultado
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao gerar PIX: {str(e)}"
        )


@router.post("/pagamento/processar/boleto", response_model=PagamentoResponse, status_code=status.HTTP_201_CREATED)
async def processar_pagamento_boleto(
    request: PagamentoBoletoRequest,
    db: Session = Depends(get_db)
):
    """
    Gera boleto bancário
    
    Retorna código de barras e linha digitável.
    Vencimento: 3 dias
    
    Args:
        request: Dados do pagamento boleto
        db: Sessão do banco de dados
        
    Returns:
        Código de barras e linha digitável
    """
    try:
        service = PaymentService(db)
        resultado = service.processar_boleto(request)
        return resultado
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao gerar boleto: {str(e)}"
        )


@router.get("/pagamento/status/{pagamento_id}", response_model=StatusPagamentoResponse)
async def consultar_status_pagamento(
    pagamento_id: int = Path(..., gt=0, description="ID do pagamento"),
    db: Session = Depends(get_db)
):
    """
    Consulta status de um pagamento
    
    Para PIX e Boleto pendentes, verifica status no gateway.
    
    Args:
        pagamento_id: ID do pagamento
        db: Sessão do banco de dados
        
    Returns:
        Status atualizado do pagamento
    """
    try:
        service = PaymentService(db)
        pagamento = service.consultar_status(pagamento_id)
        
        # Determina mensagem baseada no status
        mensagens = {
            StatusPagamento.PENDENTE: "Aguardando pagamento",
            StatusPagamento.PROCESSANDO: "Pagamento em processamento",
            StatusPagamento.APROVADO: "Pagamento aprovado com sucesso",
            StatusPagamento.REJEITADO: "Pagamento rejeitado",
            StatusPagamento.CANCELADO: "Pagamento cancelado",
            StatusPagamento.ESTORNADO: "Pagamento estornado"
        }
        
        response = StatusPagamentoResponse(
            id=pagamento.id,
            pedido_id=pagamento.pedido_id,
            status=pagamento.status.value,
            forma_pagamento=pagamento.forma_pagamento.value,
            valor=pagamento.valor,
            codigo_transacao=pagamento.codigo_transacao,
            data_criacao=pagamento.data_criacao,
            data_processamento=pagamento.data_processamento,
            data_aprovacao=pagamento.data_aprovacao,
            mensagem=mensagens.get(pagamento.status, "Status desconhecido")
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao consultar status: {str(e)}"
        )


@router.get("/pagamento/pedido/{pedido_id}/status", response_model=PagamentoListResponse)
async def consultar_pagamentos_pedido(
    pedido_id: int = Path(..., gt=0, description="ID do pedido"),
    db: Session = Depends(get_db)
):
    """
    Lista todos os pagamentos de um pedido
    
    Args:
        pedido_id: ID do pedido
        db: Sessão do banco de dados
        
    Returns:
        Lista de pagamentos do pedido
    """
    try:
        service = PaymentService(db)
        pagamentos = service.listar_pagamentos_pedido(pedido_id)
        
        logs = [
            TransacaoLogResponse(
                id=p.id,
                usuario_id=p.usuario_id,
                pedido_id=p.pedido_id,
                forma_pagamento=p.forma_pagamento.value,
                status=p.status.value,
                valor=p.valor,
                codigo_transacao=p.codigo_transacao,
                data_criacao=p.data_criacao
            )
            for p in pagamentos
        ]
        
        return PagamentoListResponse(
            pagamentos=logs,
            total=len(logs)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao listar pagamentos: {str(e)}"
        )


@router.get("/pagamento/usuario/{usuario_id}/historico", response_model=PagamentoListResponse)
async def listar_historico_pagamentos(
    usuario_id: int = Path(..., gt=0, description="ID do usuário"),
    db: Session = Depends(get_db)
):
    """
    Lista histórico de pagamentos de um usuário
    
    Args:
        usuario_id: ID do usuário
        db: Sessão do banco de dados
        
    Returns:
        Lista de pagamentos do usuário
    """
    try:
        service = PaymentService(db)
        pagamentos = service.listar_pagamentos_usuario(usuario_id)
        
        logs = [
            TransacaoLogResponse(
                id=p.id,
                usuario_id=p.usuario_id,
                pedido_id=p.pedido_id,
                forma_pagamento=p.forma_pagamento.value,
                status=p.status.value,
                valor=p.valor,
                codigo_transacao=p.codigo_transacao,
                data_criacao=p.data_criacao
            )
            for p in pagamentos
        ]
        
        return PagamentoListResponse(
            pagamentos=logs,
            total=len(logs)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao listar histórico: {str(e)}"
        )


@router.patch("/pagamento/{pagamento_id}/cancelar", response_model=PagamentoResponse)
async def cancelar_pagamento(
    pagamento_id: int = Path(..., gt=0, description="ID do pagamento"),
    motivo: str = Query(..., min_length=5, description="Motivo do cancelamento"),
    db: Session = Depends(get_db)
):
    """
    Cancela um pagamento pendente
    
    Apenas pagamentos com status PENDENTE podem ser cancelados.
    
    Args:
        pagamento_id: ID do pagamento
        motivo: Motivo do cancelamento
        db: Sessão do banco de dados
        
    Returns:
        Pagamento cancelado
    """
    try:
        service = PaymentService(db)
        pagamento = service.cancelar_pagamento(pagamento_id, motivo)
        
        response = PagamentoResponse.model_validate(pagamento)
        response.mensagem = f"Pagamento cancelado: {motivo}"
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao cancelar pagamento: {str(e)}"
        )


@router.get("/pagamento/{pagamento_id}", response_model=PagamentoResponse)
async def obter_detalhes_pagamento(
    pagamento_id: int = Path(..., gt=0, description="ID do pagamento"),
    db: Session = Depends(get_db)
):
    """
    Obtém detalhes completos de um pagamento
    
    Args:
        pagamento_id: ID do pagamento
        db: Sessão do banco de dados
        
    Returns:
        Detalhes do pagamento
    """
    try:
        service = PaymentService(db)
        pagamento = service.consultar_status(pagamento_id)
        
        return PagamentoResponse.model_validate(pagamento)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter pagamento: {str(e)}"
        )
