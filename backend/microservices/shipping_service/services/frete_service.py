# Service para cálculo de frete
# Implementa regras de negócio para cálculo de frete

from decimal import Decimal
from typing import List
from schemas.frete_schemas import FreteOpcao, FreteCalculoRequest, FreteCalculoResponse
from .viacep_service import ViaCEPService


class FreteService:
    """Serviço para cálculo de frete"""
    
    # Configurações de frete
    FRETE_ECONOMICO_VALOR = Decimal("15.00")
    FRETE_ECONOMICO_PRAZO = 10
    FRETE_GRATIS_VALOR = Decimal("0.00")
    FRETE_GRATIS_PRAZO = 20
    
    @staticmethod
    async def calcular_frete(request: FreteCalculoRequest) -> FreteCalculoResponse:
        """
        Calcula opções de frete disponíveis
        
        Args:
            request: Dados para cálculo (CEP, peso, valor)
            
        Returns:
            FreteCalculoResponse com opções de frete
        """
        # Valida CEP via ViaCEP (verifica se existe)
        await ViaCEPService.consultar_cep(request.cep_destino)
        
        # Monta opções de frete
        opcoes_frete: List[FreteOpcao] = []
        
        # Opção 1: Frete Econômico (R$ 15,00 - 10 dias)
        frete_economico = FreteOpcao(
            tipo="ECONOMICO",
            nome="Frete Econômico",
            valor=FreteService.FRETE_ECONOMICO_VALOR,
            prazo_dias=FreteService.FRETE_ECONOMICO_PRAZO,
            descricao=f"Entrega em até {FreteService.FRETE_ECONOMICO_PRAZO} dias úteis por R$ {FreteService.FRETE_ECONOMICO_VALOR}"
        )
        opcoes_frete.append(frete_economico)
        
        # Opção 2: Frete Grátis (20 dias)
        frete_gratis = FreteOpcao(
            tipo="GRATIS",
            nome="Frete Grátis",
            valor=FreteService.FRETE_GRATIS_VALOR,
            prazo_dias=FreteService.FRETE_GRATIS_PRAZO,
            descricao=f"Entrega em até {FreteService.FRETE_GRATIS_PRAZO} dias úteis - Frete Grátis!"
        )
        opcoes_frete.append(frete_gratis)
        
        # Monta resposta
        response = FreteCalculoResponse(
            cep_destino=request.cep_destino,
            peso_total=request.peso_total,
            valor_produtos=request.valor_produtos,
            opcoes_frete=opcoes_frete,
            mensagem="Cálculo realizado com sucesso"
        )
        
        return response
    
    @staticmethod
    def validar_peso(peso: Decimal) -> bool:
        """
        Valida se o peso está dentro dos limites permitidos
        
        Args:
            peso: Peso em kg
            
        Returns:
            True se válido, False caso contrário
        """
        return Decimal("0") < peso <= Decimal("30")

