# Service para gerenciamento de pagamentos
# Implementa regras de negócio para processamento de pagamentos

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional
from decimal import Decimal
from datetime import datetime
import json

from models import Pagamento, FormaPagamento, StatusPagamento
from schemas.pagamento_schemas import (
    PagamentoCartaoRequest,
    PagamentoPixRequest,
    PagamentoBoletoRequest,
    PagamentoResponse
)
from repositories.payment_repository import PaymentRepository
from .payment_gateway_service import PaymentGatewayService


class PaymentService:
    """Serviço para gerenciamento de pagamentos"""
    
    def __init__(self, db: Session):
        self.db = db
        self.repository = PaymentRepository(db)
        self.gateway = PaymentGatewayService()
    
    def processar_cartao(self, request: PagamentoCartaoRequest) -> PagamentoResponse:
        """
        Processa pagamento com cartão de crédito/débito
        
        Args:
            request: Dados do cartão e pagamento
            
        Returns:
            PagamentoResponse com resultado do processamento
        """
        # Cria registro de pagamento com status processando
        pagamento = self.repository.criar_pagamento(
            usuario_id=request.usuario_id,
            pedido_id=request.pedido_id,
            forma_pagamento=FormaPagamento.CARTAO_CREDITO,
            valor=request.valor,
            status=StatusPagamento.PROCESSANDO
        )
        
        try:
            # Processa pagamento via gateway
            sucesso, mensagem, dados_extras = self.gateway.processar_cartao(
                numero_cartao=request.numero_cartao,
                nome_titular=request.nome_titular,
                validade=request.validade,
                cvv=request.cvv,
                valor=request.valor,
                parcelas=request.parcelas
            )
            
            if sucesso:
                # Atualiza pagamento para aprovado
                pagamento = self.repository.atualizar_status(
                    pagamento.id,
                    StatusPagamento.APROVADO,
                    dados_pagamento=json.dumps(dados_extras),
                    data_aprovacao=datetime.now()
                )
                
                # Registra log de sucesso
                self._registrar_log(pagamento, "APROVADO", mensagem)
                
            else:
                # Atualiza pagamento para rejeitado
                pagamento = self.repository.atualizar_status(
                    pagamento.id,
                    StatusPagamento.REJEITADO,
                    observacoes=mensagem
                )
                
                # Registra log de falha
                self._registrar_log(pagamento, "REJEITADO", mensagem)
            
            # Monta resposta
            response = PagamentoResponse.model_validate(pagamento)
            response.mensagem = mensagem
            
            return response
            
        except Exception as e:
            # Em caso de erro, marca como rejeitado
            self.repository.atualizar_status(
                pagamento.id,
                StatusPagamento.REJEITADO,
                observacoes=f"Erro no processamento: {str(e)}"
            )
            self._registrar_log(pagamento, "ERRO", str(e))
            
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao processar pagamento: {str(e)}"
            )
    
    def processar_pix(self, request: PagamentoPixRequest) -> PagamentoResponse:
        """
        Gera pagamento via PIX
        
        Args:
            request: Dados do pagamento PIX
            
        Returns:
            PagamentoResponse com QR Code e chave PIX
        """
        # Cria registro de pagamento pendente
        pagamento = self.repository.criar_pagamento(
            usuario_id=request.usuario_id,
            pedido_id=request.pedido_id,
            forma_pagamento=FormaPagamento.PIX,
            valor=request.valor,
            status=StatusPagamento.PENDENTE
        )
        
        try:
            # Gera PIX via gateway
            sucesso, mensagem, dados_extras = self.gateway.processar_pix(
                valor=request.valor,
                usuario_id=request.usuario_id,
                pedido_id=request.pedido_id
            )
            
            if sucesso:
                # Atualiza com dados do PIX
                pagamento = self.repository.atualizar_pagamento(
                    pagamento.id,
                    dados_pagamento=json.dumps(dados_extras)
                )
                
                # Registra log
                self._registrar_log(pagamento, "PIX_GERADO", mensagem)
                
                # Monta resposta
                response = PagamentoResponse.model_validate(pagamento)
                response.mensagem = mensagem
                response.qr_code = dados_extras.get("qr_code_base64")
                
                return response
            else:
                raise Exception(mensagem)
                
        except Exception as e:
            self.repository.atualizar_status(
                pagamento.id,
                StatusPagamento.REJEITADO,
                observacoes=f"Erro ao gerar PIX: {str(e)}"
            )
            self._registrar_log(pagamento, "ERRO", str(e))
            
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao gerar PIX: {str(e)}"
            )
    
    def processar_boleto(self, request: PagamentoBoletoRequest) -> PagamentoResponse:
        """
        Gera boleto bancário
        
        Args:
            request: Dados do pagamento boleto
            
        Returns:
            PagamentoResponse com código de barras e linha digitável
        """
        # Cria registro de pagamento pendente
        pagamento = self.repository.criar_pagamento(
            usuario_id=request.usuario_id,
            pedido_id=request.pedido_id,
            forma_pagamento=FormaPagamento.BOLETO,
            valor=request.valor,
            status=StatusPagamento.PENDENTE
        )
        
        try:
            # Gera boleto via gateway
            sucesso, mensagem, dados_extras = self.gateway.processar_boleto(
                valor=request.valor,
                cpf_cnpj=request.cpf_cnpj,
                usuario_id=request.usuario_id,
                pedido_id=request.pedido_id
            )
            
            if sucesso:
                # Atualiza com dados do boleto
                pagamento = self.repository.atualizar_pagamento(
                    pagamento.id,
                    dados_pagamento=json.dumps(dados_extras)
                )
                
                # Registra log
                self._registrar_log(pagamento, "BOLETO_GERADO", mensagem)
                
                # Monta resposta
                response = PagamentoResponse.model_validate(pagamento)
                response.mensagem = mensagem
                response.codigo_barras = dados_extras.get("codigo_barras")
                response.linha_digitavel = dados_extras.get("linha_digitavel")
                
                return response
            else:
                raise Exception(mensagem)
                
        except Exception as e:
            self.repository.atualizar_status(
                pagamento.id,
                StatusPagamento.REJEITADO,
                observacoes=f"Erro ao gerar boleto: {str(e)}"
            )
            self._registrar_log(pagamento, "ERRO", str(e))
            
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao gerar boleto: {str(e)}"
            )
    
    def consultar_status(self, pagamento_id: int) -> Pagamento:
        """
        Consulta status de um pagamento
        
        Args:
            pagamento_id: ID do pagamento
            
        Returns:
            Pagamento atualizado
        """
        pagamento = self.repository.obter_por_id(pagamento_id)
        
        if not pagamento:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Pagamento {pagamento_id} não encontrado"
            )
        
        # Se for PIX ou Boleto pendente, verifica status no gateway
        if pagamento.status == StatusPagamento.PENDENTE:
            if pagamento.forma_pagamento == FormaPagamento.PIX:
                novo_status = self.gateway.verificar_status_pix(pagamento.codigo_transacao)
                if novo_status == "pago":
                    pagamento = self.repository.atualizar_status(
                        pagamento.id,
                        StatusPagamento.APROVADO,
                        data_aprovacao=datetime.now()
                    )
                    self._registrar_log(pagamento, "PIX_CONFIRMADO", "Pagamento PIX confirmado")
                    
            elif pagamento.forma_pagamento == FormaPagamento.BOLETO:
                novo_status = self.gateway.verificar_status_boleto(pagamento.codigo_transacao)
                if novo_status == "pago":
                    pagamento = self.repository.atualizar_status(
                        pagamento.id,
                        StatusPagamento.APROVADO,
                        data_aprovacao=datetime.now()
                    )
                    self._registrar_log(pagamento, "BOLETO_CONFIRMADO", "Pagamento de boleto confirmado")
        
        return pagamento
    
    def listar_pagamentos_usuario(self, usuario_id: int) -> List[Pagamento]:
        """Lista pagamentos de um usuário"""
        return self.repository.listar_por_usuario(usuario_id)
    
    def listar_pagamentos_pedido(self, pedido_id: int) -> List[Pagamento]:
        """Lista pagamentos de um pedido"""
        return self.repository.listar_por_pedido(pedido_id)
    
    def cancelar_pagamento(self, pagamento_id: int, motivo: str) -> Pagamento:
        """
        Cancela um pagamento pendente
        
        Args:
            pagamento_id: ID do pagamento
            motivo: Motivo do cancelamento
            
        Returns:
            Pagamento cancelado
        """
        pagamento = self.repository.obter_por_id(pagamento_id)
        
        if not pagamento:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Pagamento {pagamento_id} não encontrado"
            )
        
        if pagamento.status != StatusPagamento.PENDENTE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Não é possível cancelar pagamento com status {pagamento.status.value}"
            )
        
        pagamento = self.repository.atualizar_status(
            pagamento.id,
            StatusPagamento.CANCELADO,
            observacoes=motivo
        )
        
        self._registrar_log(pagamento, "CANCELADO", motivo)
        
        return pagamento
    
    def _registrar_log(self, pagamento: Pagamento, acao: str, mensagem: str):
        """Registra log de transação (para auditoria)"""
        print(f"[LOG] Pagamento #{pagamento.id} | {acao} | {mensagem} | {datetime.now().isoformat()}")
        # Em produção, salvaria em tabela de logs ou sistema de logging

