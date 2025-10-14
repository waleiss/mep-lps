# Service para integração com API ViaCEP
# API gratuita para consulta de CEPs brasileiros

import httpx
from typing import Optional
from fastapi import HTTPException, status
from schemas.frete_schemas import ViaCEPResponse


class ViaCEPService:
    """Serviço para consulta de CEPs via ViaCEP API"""
    
    BASE_URL = "https://viacep.com.br/ws"
    TIMEOUT = 5.0  # segundos
    
    @staticmethod
    async def consultar_cep(cep: str) -> ViaCEPResponse:
        """
        Consulta CEP na API ViaCEP
        
        Args:
            cep: CEP a ser consultado (apenas números)
            
        Returns:
            ViaCEPResponse com dados do endereço
            
        Raises:
            HTTPException: Se CEP for inválido ou houver erro na consulta
        """
        # Remove caracteres não numéricos
        cep_limpo = ''.join(filter(str.isdigit, cep))
        
        # Valida tamanho do CEP
        if len(cep_limpo) != 8:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="CEP deve conter 8 dígitos"
            )
        
        # Monta URL
        url = f"{ViaCEPService.BASE_URL}/{cep_limpo}/json/"
        
        try:
            # Faz requisição assíncrona
            async with httpx.AsyncClient(timeout=ViaCEPService.TIMEOUT) as client:
                response = await client.get(url)
                
                # Verifica status code
                if response.status_code != 200:
                    raise HTTPException(
                        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                        detail="Serviço de consulta de CEP temporariamente indisponível"
                    )
                
                # Parse JSON
                data = response.json()
                
                # Verifica se CEP foi encontrado
                if data.get("erro"):
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"CEP {cep_limpo} não encontrado"
                    )
                
                # Retorna resposta estruturada
                return ViaCEPResponse(**data)
                
        except httpx.TimeoutException:
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="Timeout ao consultar CEP. Tente novamente."
            )
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Erro ao conectar com serviço de CEP: {str(e)}"
            )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro interno ao processar CEP: {str(e)}"
            )
    
    @staticmethod
    def validar_cep(cep: str) -> bool:
        """
        Valida formato do CEP
        
        Args:
            cep: CEP a ser validado
            
        Returns:
            True se CEP for válido, False caso contrário
        """
        cep_limpo = ''.join(filter(str.isdigit, cep))
        return len(cep_limpo) == 8

