# Service para gerenciamento de endereços
# Implementa regras de negócio para CRUD de endereços

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional
from models import Endereco
from schemas.endereco_schemas import EnderecoCreate, EnderecoUpdate
from repositories.endereco_repository import EnderecoRepository
from .viacep_service import ViaCEPService


class EnderecoService:
    """Serviço para gerenciamento de endereços"""
    
    def __init__(self, db: Session):
        self.db = db
        self.repository = EnderecoRepository(db)
    
    async def criar_endereco(self, endereco_data: EnderecoCreate) -> Endereco:
        """
        Cria um novo endereço para o usuário
        
        Args:
            endereco_data: Dados do endereço a ser criado
            
        Returns:
            Endereço criado
            
        Raises:
            HTTPException: Se houver erro na validação ou criação
        """
        # Valida CEP via ViaCEP
        cep_info = await ViaCEPService.consultar_cep(endereco_data.cep)
        
        # Verifica se dados do endereço batem com o CEP
        # (validação adicional opcional)
        
        # Se for endereço principal, remove principal dos outros
        if endereco_data.principal:
            self.repository.remover_principal_usuario(endereco_data.usuario_id)
        
        # Cria endereço
        endereco = self.repository.criar(endereco_data)
        
        return endereco
    
    def listar_enderecos_usuario(self, usuario_id: int) -> List[Endereco]:
        """
        Lista todos os endereços ativos de um usuário
        
        Args:
            usuario_id: ID do usuário
            
        Returns:
            Lista de endereços
        """
        return self.repository.listar_por_usuario(usuario_id)
    
    def obter_endereco(self, endereco_id: int, usuario_id: int) -> Endereco:
        """
        Obtém um endereço específico
        
        Args:
            endereco_id: ID do endereço
            usuario_id: ID do usuário (para validação de propriedade)
            
        Returns:
            Endereço encontrado
            
        Raises:
            HTTPException: Se endereço não for encontrado ou não pertencer ao usuário
        """
        endereco = self.repository.obter_por_id(endereco_id)
        
        if not endereco:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Endereço {endereco_id} não encontrado"
            )
        
        if endereco.usuario_id != usuario_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não tem permissão para acessar este endereço"
            )
        
        return endereco
    
    def obter_endereco_principal(self, usuario_id: int) -> Optional[Endereco]:
        """
        Obtém o endereço principal do usuário
        
        Args:
            usuario_id: ID do usuário
            
        Returns:
            Endereço principal ou None se não houver
        """
        return self.repository.obter_principal_usuario(usuario_id)
    
    async def atualizar_endereco(
        self, 
        endereco_id: int, 
        usuario_id: int, 
        endereco_data: EnderecoUpdate
    ) -> Endereco:
        """
        Atualiza um endereço existente
        
        Args:
            endereco_id: ID do endereço
            usuario_id: ID do usuário (para validação de propriedade)
            endereco_data: Dados a serem atualizados
            
        Returns:
            Endereço atualizado
            
        Raises:
            HTTPException: Se endereço não for encontrado ou não pertencer ao usuário
        """
        # Verifica se endereço existe e pertence ao usuário
        endereco = self.obter_endereco(endereco_id, usuario_id)
        
        # Se CEP for alterado, valida o novo CEP
        if endereco_data.cep and endereco_data.cep != endereco.cep:
            await ViaCEPService.consultar_cep(endereco_data.cep)
        
        # Se for marcar como principal, remove principal dos outros
        if endereco_data.principal and not endereco.principal:
            self.repository.remover_principal_usuario(usuario_id)
        
        # Atualiza endereço
        endereco_atualizado = self.repository.atualizar(endereco_id, endereco_data)
        
        return endereco_atualizado
    
    def deletar_endereco(self, endereco_id: int, usuario_id: int) -> bool:
        """
        Deleta (desativa) um endereço
        
        Args:
            endereco_id: ID do endereço
            usuario_id: ID do usuário (para validação de propriedade)
            
        Returns:
            True se deletado com sucesso
            
        Raises:
            HTTPException: Se endereço não for encontrado ou não pertencer ao usuário
        """
        # Verifica se endereço existe e pertence ao usuário
        self.obter_endereco(endereco_id, usuario_id)
        
        # Deleta (soft delete)
        return self.repository.deletar(endereco_id)
    
    def definir_endereco_principal(self, endereco_id: int, usuario_id: int) -> Endereco:
        """
        Define um endereço como principal
        
        Args:
            endereco_id: ID do endereço
            usuario_id: ID do usuário
            
        Returns:
            Endereço atualizado
        """
        # Verifica se endereço existe e pertence ao usuário
        self.obter_endereco(endereco_id, usuario_id)
        
        # Remove principal dos outros
        self.repository.remover_principal_usuario(usuario_id)
        
        # Define como principal
        return self.repository.definir_principal(endereco_id)

