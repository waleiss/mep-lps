# Repository para acesso a dados de endereços
# Camada de acesso ao banco de dados

from sqlalchemy.orm import Session
from typing import List, Optional
from models import Endereco
from schemas.endereco_schemas import EnderecoCreate, EnderecoUpdate


class EnderecoRepository:
    """Repository para operações de banco de dados de endereços"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def criar(self, endereco_data: EnderecoCreate) -> Endereco:
        """
        Cria um novo endereço no banco de dados
        
        Args:
            endereco_data: Dados do endereço
            
        Returns:
            Endereço criado
        """
        endereco = Endereco(**endereco_data.model_dump())
        self.db.add(endereco)
        self.db.commit()
        self.db.refresh(endereco)
        return endereco
    
    def obter_por_id(self, endereco_id: int) -> Optional[Endereco]:
        """
        Obtém um endereço por ID
        
        Args:
            endereco_id: ID do endereço
            
        Returns:
            Endereço ou None se não encontrado
        """
        return self.db.query(Endereco).filter(
            Endereco.id == endereco_id,
            Endereco.ativo == True
        ).first()
    
    def listar_por_usuario(self, usuario_id: int) -> List[Endereco]:
        """
        Lista todos os endereços ativos de um usuário
        
        Args:
            usuario_id: ID do usuário
            
        Returns:
            Lista de endereços
        """
        return self.db.query(Endereco).filter(
            Endereco.usuario_id == usuario_id,
            Endereco.ativo == True
        ).order_by(Endereco.principal.desc(), Endereco.data_criacao.desc()).all()
    
    def obter_principal_usuario(self, usuario_id: int) -> Optional[Endereco]:
        """
        Obtém o endereço principal do usuário
        
        Args:
            usuario_id: ID do usuário
            
        Returns:
            Endereço principal ou None
        """
        return self.db.query(Endereco).filter(
            Endereco.usuario_id == usuario_id,
            Endereco.principal == True,
            Endereco.ativo == True
        ).first()
    
    def atualizar(self, endereco_id: int, endereco_data: EnderecoUpdate) -> Endereco:
        """
        Atualiza um endereço
        
        Args:
            endereco_id: ID do endereço
            endereco_data: Dados a serem atualizados
            
        Returns:
            Endereço atualizado
        """
        endereco = self.db.query(Endereco).filter(Endereco.id == endereco_id).first()
        
        # Atualiza apenas campos fornecidos
        update_data = endereco_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(endereco, field, value)
        
        self.db.commit()
        self.db.refresh(endereco)
        return endereco
    
    def deletar(self, endereco_id: int) -> bool:
        """
        Deleta (soft delete) um endereço
        
        Args:
            endereco_id: ID do endereço
            
        Returns:
            True se deletado com sucesso
        """
        endereco = self.db.query(Endereco).filter(Endereco.id == endereco_id).first()
        endereco.ativo = False
        self.db.commit()
        return True
    
    def remover_principal_usuario(self, usuario_id: int) -> None:
        """
        Remove o status de principal de todos os endereços do usuário
        
        Args:
            usuario_id: ID do usuário
        """
        self.db.query(Endereco).filter(
            Endereco.usuario_id == usuario_id
        ).update({"principal": False})
        self.db.commit()
    
    def definir_principal(self, endereco_id: int) -> Endereco:
        """
        Define um endereço como principal
        
        Args:
            endereco_id: ID do endereço
            
        Returns:
            Endereço atualizado
        """
        endereco = self.db.query(Endereco).filter(Endereco.id == endereco_id).first()
        endereco.principal = True
        self.db.commit()
        self.db.refresh(endereco)
        return endereco

