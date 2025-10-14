# Repository para acesso a dados de pagamentos
# Camada de acesso ao banco de dados

from sqlalchemy.orm import Session
from typing import List, Optional
from decimal import Decimal
from datetime import datetime
import uuid

from models import Pagamento, FormaPagamento, StatusPagamento


class PaymentRepository:
    """Repository para operações de banco de dados de pagamentos"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def criar_pagamento(
        self,
        usuario_id: int,
        pedido_id: int,
        forma_pagamento: FormaPagamento,
        valor: Decimal,
        status: StatusPagamento = StatusPagamento.PENDENTE,
        dados_pagamento: Optional[str] = None
    ) -> Pagamento:
        """
        Cria um novo pagamento no banco de dados
        
        Args:
            usuario_id: ID do usuário
            pedido_id: ID do pedido
            forma_pagamento: Forma de pagamento
            valor: Valor do pagamento
            status: Status inicial
            dados_pagamento: Dados extras em JSON
            
        Returns:
            Pagamento criado
        """
        # Gera código de transação único
        codigo_transacao = self._gerar_codigo_transacao()
        
        pagamento = Pagamento(
            usuario_id=usuario_id,
            pedido_id=pedido_id,
            forma_pagamento=forma_pagamento,
            status=status,
            valor=valor,
            codigo_transacao=codigo_transacao,
            dados_pagamento=dados_pagamento,
            data_processamento=datetime.now() if status == StatusPagamento.PROCESSANDO else None
        )
        
        self.db.add(pagamento)
        self.db.commit()
        self.db.refresh(pagamento)
        return pagamento
    
    def obter_por_id(self, pagamento_id: int) -> Optional[Pagamento]:
        """
        Obtém um pagamento por ID
        
        Args:
            pagamento_id: ID do pagamento
            
        Returns:
            Pagamento ou None
        """
        return self.db.query(Pagamento).filter(Pagamento.id == pagamento_id).first()
    
    def obter_por_codigo_transacao(self, codigo_transacao: str) -> Optional[Pagamento]:
        """
        Obtém um pagamento por código de transação
        
        Args:
            codigo_transacao: Código da transação
            
        Returns:
            Pagamento ou None
        """
        return self.db.query(Pagamento).filter(
            Pagamento.codigo_transacao == codigo_transacao
        ).first()
    
    def listar_por_usuario(self, usuario_id: int) -> List[Pagamento]:
        """
        Lista todos os pagamentos de um usuário
        
        Args:
            usuario_id: ID do usuário
            
        Returns:
            Lista de pagamentos
        """
        return self.db.query(Pagamento).filter(
            Pagamento.usuario_id == usuario_id
        ).order_by(Pagamento.data_criacao.desc()).all()
    
    def listar_por_pedido(self, pedido_id: int) -> List[Pagamento]:
        """
        Lista todos os pagamentos de um pedido
        
        Args:
            pedido_id: ID do pedido
            
        Returns:
            Lista de pagamentos
        """
        return self.db.query(Pagamento).filter(
            Pagamento.pedido_id == pedido_id
        ).order_by(Pagamento.data_criacao.desc()).all()
    
    def listar_por_status(self, status: StatusPagamento) -> List[Pagamento]:
        """
        Lista pagamentos por status
        
        Args:
            status: Status do pagamento
            
        Returns:
            Lista de pagamentos
        """
        return self.db.query(Pagamento).filter(
            Pagamento.status == status
        ).order_by(Pagamento.data_criacao.desc()).all()
    
    def atualizar_status(
        self,
        pagamento_id: int,
        novo_status: StatusPagamento,
        dados_pagamento: Optional[str] = None,
        data_aprovacao: Optional[datetime] = None,
        observacoes: Optional[str] = None
    ) -> Pagamento:
        """
        Atualiza status de um pagamento
        
        Args:
            pagamento_id: ID do pagamento
            novo_status: Novo status
            dados_pagamento: Dados extras (opcional)
            data_aprovacao: Data de aprovação (opcional)
            observacoes: Observações (opcional)
            
        Returns:
            Pagamento atualizado
        """
        pagamento = self.db.query(Pagamento).filter(Pagamento.id == pagamento_id).first()
        
        pagamento.status = novo_status
        
        if dados_pagamento is not None:
            pagamento.dados_pagamento = dados_pagamento
        
        if data_aprovacao is not None:
            pagamento.data_aprovacao = data_aprovacao
        
        if observacoes is not None:
            pagamento.observacoes = observacoes
        
        if novo_status == StatusPagamento.PROCESSANDO and not pagamento.data_processamento:
            pagamento.data_processamento = datetime.now()
        
        self.db.commit()
        self.db.refresh(pagamento)
        return pagamento
    
    def atualizar_pagamento(
        self,
        pagamento_id: int,
        **kwargs
    ) -> Pagamento:
        """
        Atualiza campos de um pagamento
        
        Args:
            pagamento_id: ID do pagamento
            **kwargs: Campos a serem atualizados
            
        Returns:
            Pagamento atualizado
        """
        pagamento = self.db.query(Pagamento).filter(Pagamento.id == pagamento_id).first()
        
        for field, value in kwargs.items():
            if hasattr(pagamento, field):
                setattr(pagamento, field, value)
        
        self.db.commit()
        self.db.refresh(pagamento)
        return pagamento
    
    def _gerar_codigo_transacao(self) -> str:
        """
        Gera código de transação único
        
        Returns:
            Código de transação
        """
        # Formato: TXN-YYYYMMDD-UUID
        data_hoje = datetime.now().strftime("%Y%m%d")
        uuid_curto = str(uuid.uuid4())[:8].upper()
        return f"TXN-{data_hoje}-{uuid_curto}"

