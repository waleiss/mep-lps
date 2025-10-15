# Service para simular gateway de pagamento
# Mock de processamento de cartão, PIX e boleto

import random
import string
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Dict, Tuple
import hashlib
import json


class PaymentGatewayService:
    """Serviço que simula integração com gateway de pagamento"""
    
    @staticmethod
    def processar_cartao(
        numero_cartao: str,
        nome_titular: str,
        validade: str,
        cvv: str,
        valor: Decimal,
        parcelas: int = 1
    ) -> Tuple[bool, str, Dict]:
        """
        Simula processamento de pagamento com cartão
        
        Args:
            numero_cartao: Número do cartão
            nome_titular: Nome do titular
            validade: Data de validade MM/YY
            cvv: Código de segurança
            valor: Valor da transação
            parcelas: Número de parcelas
            
        Returns:
            Tuple (sucesso, mensagem, dados_extras)
        """
        # Simula delay de processamento
        # time.sleep(0.5)
        
        # Regras de simulação:
        # Cartões terminados em par = aprovado
        # Cartões terminados em ímpar = recusado (10% de chance)
        # CVV 000 = sempre recusado
        
        ultimo_digito = int(numero_cartao[-1])
        
        if cvv == "000":
            return False, "Cartão recusado: CVV inválido", {}
        
        if ultimo_digito % 2 != 0 and random.random() < 0.1:
            return False, "Cartão recusado: Saldo insuficiente", {}
        
        # Gera código de autorização
        codigo_autorizacao = ''.join(random.choices(string.digits, k=6))
        
        # Mascara o cartão para segurança
        cartao_mascarado = f"****-****-****-{numero_cartao[-4:]}"
        
        dados_extras = {
            "codigo_autorizacao": codigo_autorizacao,
            "cartao_mascarado": cartao_mascarado,
            "parcelas": parcelas,
            "valor_parcela": float(valor / parcelas) if parcelas > 1 else float(valor),
            "bandeira": PaymentGatewayService._detectar_bandeira(numero_cartao),
            "data_aprovacao": datetime.now().isoformat()
        }
        
        mensagem = f"Pagamento aprovado! Código de autorização: {codigo_autorizacao}"
        if parcelas > 1:
            mensagem += f" - {parcelas}x de R$ {dados_extras['valor_parcela']:.2f}"
        
        return True, mensagem, dados_extras
    
    @staticmethod
    def processar_pix(valor: Decimal, usuario_id: int, pedido_id: int) -> Tuple[bool, str, Dict]:
        """
        Simula geração de PIX
        
        Args:
            valor: Valor da transação
            usuario_id: ID do usuário
            pedido_id: ID do pedido
            
        Returns:
            Tuple (sucesso, mensagem, dados_extras)
        """
        # Gera chave PIX aleatória
        chave_pix = PaymentGatewayService._gerar_chave_pix()
        
        # Gera QR Code (simulado - normalmente seria uma imagem base64)
        qr_code_data = PaymentGatewayService._gerar_qr_code_pix(valor, chave_pix, pedido_id)
        
        # Validade do PIX (30 minutos)
        validade = datetime.now() + timedelta(minutes=30)
        
        dados_extras = {
            "chave_pix": chave_pix,
            "qr_code": qr_code_data,
            "qr_code_base64": f"data:image/png;base64,{qr_code_data}",  # Simulado
            "validade": validade.isoformat(),
            "status": "aguardando_pagamento"
        }
        
        mensagem = f"PIX gerado com sucesso! Válido até {validade.strftime('%H:%M:%S')}"
        
        return True, mensagem, dados_extras
    
    @staticmethod
    def processar_boleto(
        valor: Decimal,
        cpf_cnpj: str,
        usuario_id: int,
        pedido_id: int
    ) -> Tuple[bool, str, Dict]:
        """
        Simula geração de boleto bancário
        
        Args:
            valor: Valor do boleto
            cpf_cnpj: CPF ou CNPJ do pagador
            usuario_id: ID do usuário
            pedido_id: ID do pedido
            
        Returns:
            Tuple (sucesso, mensagem, dados_extras)
        """
        # Gera código de barras
        codigo_barras = PaymentGatewayService._gerar_codigo_barras(valor, pedido_id)
        
        # Gera linha digitável
        linha_digitavel = PaymentGatewayService._gerar_linha_digitavel(codigo_barras)
        
        # Vencimento (3 dias)
        vencimento = datetime.now() + timedelta(days=3)
        
        dados_extras = {
            "codigo_barras": codigo_barras,
            "linha_digitavel": linha_digitavel,
            "vencimento": vencimento.isoformat(),
            "nosso_numero": f"{pedido_id:08d}",
            "banco": "237",  # Bradesco (simulado)
            "agencia": "1234-5",
            "conta": "67890-1",
            "status": "aguardando_pagamento"
        }
        
        mensagem = f"Boleto gerado com sucesso! Vencimento: {vencimento.strftime('%d/%m/%Y')}"
        
        return True, mensagem, dados_extras
    
    @staticmethod
    def verificar_status_pix(codigo_transacao: str) -> str:
        """
        Simula verificação de status do PIX
        (Em produção, consultaria a API do banco)
        
        Returns:
            Status: 'pendente', 'pago', 'expirado'
        """
        # Simula: 20% de chance de ter sido pago
        if random.random() < 0.2:
            return "pago"
        
        # Simula: 5% de chance de ter expirado
        if random.random() < 0.05:
            return "expirado"
        
        return "pendente"
    
    @staticmethod
    def verificar_status_boleto(codigo_transacao: str) -> str:
        """
        Simula verificação de status do boleto
        (Em produção, consultaria a API do banco)
        
        Returns:
            Status: 'pendente', 'pago', 'vencido'
        """
        # Simula: 15% de chance de ter sido pago
        if random.random() < 0.15:
            return "pago"
        
        # Simula: 3% de chance de ter vencido
        if random.random() < 0.03:
            return "vencido"
        
        return "pendente"
    
    # Métodos auxiliares privados
    
    @staticmethod
    def _detectar_bandeira(numero_cartao: str) -> str:
        """Detecta bandeira do cartão pelo número"""
        primeiro_digito = numero_cartao[0]
        
        if numero_cartao.startswith('4'):
            return "Visa"
        elif numero_cartao.startswith(('51', '52', '53', '54', '55')):
            return "Mastercard"
        elif numero_cartao.startswith(('34', '37')):
            return "American Express"
        elif numero_cartao.startswith('6'):
            return "Elo"
        else:
            return "Desconhecida"
    
    @staticmethod
    def _gerar_chave_pix() -> str:
        """Gera uma chave PIX aleatória (simulada)"""
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=32))
    
    @staticmethod
    def _gerar_qr_code_pix(valor: Decimal, chave: str, pedido_id: int) -> str:
        """Gera hash simulando QR Code do PIX"""
        data = f"PIX|{chave}|{valor}|{pedido_id}|{datetime.now().isoformat()}"
        return hashlib.sha256(data.encode()).hexdigest()
    
    @staticmethod
    def _gerar_codigo_barras(valor: Decimal, pedido_id: int) -> str:
        """Gera código de barras simulado (47 dígitos)"""
        # Formato simplificado: BBBMCCCCVVVVVVVVVV...
        # BBB = código do banco (237)
        # M = código da moeda (9)
        # CCCC = campo livre
        banco = "237"
        moeda = "9"
        valor_str = str(int(valor * 100)).zfill(10)
        campo_livre = str(pedido_id).zfill(25)
        
        codigo = banco + moeda + valor_str + campo_livre
        
        # Calcula dígito verificador (simplificado)
        dv = str(sum(int(d) for d in codigo) % 10)
        
        return codigo[:4] + dv + codigo[4:]
    
    @staticmethod
    def _gerar_linha_digitavel(codigo_barras: str) -> str:
        """Converte código de barras em linha digitável"""
        # Simplificado: divide em 5 campos separados por espaços
        return f"{codigo_barras[:5]}.{codigo_barras[5:10]} " \
               f"{codigo_barras[10:15]}.{codigo_barras[15:21]} " \
               f"{codigo_barras[21:26]}.{codigo_barras[26:32]} " \
               f"{codigo_barras[32]} " \
               f"{codigo_barras[33:]}"

