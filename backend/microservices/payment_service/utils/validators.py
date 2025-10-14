# Validadores de CPF e CNPJ
# Implementa validação completa com dígitos verificadores

import re


def validar_cpf(cpf: str) -> bool:
    """
    Valida CPF brasileiro com dígitos verificadores
    
    Args:
        cpf: CPF com ou sem formatação
        
    Returns:
        True se CPF válido, False caso contrário
    """
    # Remove formatação
    cpf_limpo = re.sub(r'\D', '', cpf)
    
    # Verifica tamanho
    if len(cpf_limpo) != 11:
        return False
    
    # Verifica se todos os dígitos são iguais (CPFs inválidos conhecidos)
    if cpf_limpo == cpf_limpo[0] * 11:
        return False
    
    # Calcula primeiro dígito verificador
    soma = sum(int(cpf_limpo[i]) * (10 - i) for i in range(9))
    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto
    
    # Verifica primeiro dígito
    if int(cpf_limpo[9]) != digito1:
        return False
    
    # Calcula segundo dígito verificador
    soma = sum(int(cpf_limpo[i]) * (11 - i) for i in range(10))
    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto
    
    # Verifica segundo dígito
    if int(cpf_limpo[10]) != digito2:
        return False
    
    return True


def validar_cnpj(cnpj: str) -> bool:
    """
    Valida CNPJ brasileiro com dígitos verificadores
    
    Args:
        cnpj: CNPJ com ou sem formatação
        
    Returns:
        True se CNPJ válido, False caso contrário
    """
    # Remove formatação
    cnpj_limpo = re.sub(r'\D', '', cnpj)
    
    # Verifica tamanho
    if len(cnpj_limpo) != 14:
        return False
    
    # Verifica se todos os dígitos são iguais (CNPJs inválidos conhecidos)
    if cnpj_limpo == cnpj_limpo[0] * 14:
        return False
    
    # Calcula primeiro dígito verificador
    multiplicadores1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma = sum(int(cnpj_limpo[i]) * multiplicadores1[i] for i in range(12))
    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto
    
    # Verifica primeiro dígito
    if int(cnpj_limpo[12]) != digito1:
        return False
    
    # Calcula segundo dígito verificador
    multiplicadores2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma = sum(int(cnpj_limpo[i]) * multiplicadores2[i] for i in range(13))
    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto
    
    # Verifica segundo dígito
    if int(cnpj_limpo[13]) != digito2:
        return False
    
    return True


def validar_cpf_cnpj(documento: str) -> tuple[bool, str]:
    """
    Valida CPF ou CNPJ e retorna o tipo
    
    Args:
        documento: CPF ou CNPJ com ou sem formatação
        
    Returns:
        Tupla (válido, tipo) onde tipo é 'CPF', 'CNPJ' ou 'INVALIDO'
    """
    # Remove formatação
    doc_limpo = re.sub(r'\D', '', documento)
    
    if len(doc_limpo) == 11:
        if validar_cpf(doc_limpo):
            return True, 'CPF'
        else:
            return False, 'INVALIDO'
    elif len(doc_limpo) == 14:
        if validar_cnpj(doc_limpo):
            return True, 'CNPJ'
        else:
            return False, 'INVALIDO'
    else:
        return False, 'INVALIDO'


def formatar_cpf(cpf: str) -> str:
    """
    Formata CPF para exibição
    
    Args:
        cpf: CPF apenas com dígitos
        
    Returns:
        CPF formatado (123.456.789-01)
    """
    cpf_limpo = re.sub(r'\D', '', cpf)
    if len(cpf_limpo) == 11:
        return f"{cpf_limpo[:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-{cpf_limpo[9:]}"
    return cpf


def formatar_cnpj(cnpj: str) -> str:
    """
    Formata CNPJ para exibição
    
    Args:
        cnpj: CNPJ apenas com dígitos
        
    Returns:
        CNPJ formatado (12.345.678/0001-90)
    """
    cnpj_limpo = re.sub(r'\D', '', cnpj)
    if len(cnpj_limpo) == 14:
        return f"{cnpj_limpo[:2]}.{cnpj_limpo[2:5]}.{cnpj_limpo[5:8]}/{cnpj_limpo[8:12]}-{cnpj_limpo[12:]}"
    return cnpj

