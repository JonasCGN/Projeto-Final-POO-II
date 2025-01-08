"""
Módulo responsável por grenciar a autenticação do usuário.
"""

import json
from typing import Tuple, Union
from funcao_postgree.bd_postgree_funcionario import BdFuncionario

bd_funcionario = BdFuncionario()

def inserir_funcionario(funcionario: dict[str, str]) -> bool:
    """
    Insere um funcionário no banco de dados.
    
    Args:
        funcionario (dict[str, str]): Dicionário com os dados do funcionário.
        chave: 'usuario', 'senha' e 'email'.
    Returns:
        bool: True se a inserção foi bem sucedida, False caso contrário.
    """
    return bd_funcionario.insert_funcionario(json.dumps(funcionario))

def validar_acesso(usuario: str, senha: str) -> bool:
    """
    Valida o acesso do usuário.
    
    Args:
        usuario (str): Nome de usuário do funcionário.
        senha (str): Senha do funcionário.
    
    Returns:
        bool: True se o acesso foi validado, False caso contrário.
    """
    
    return bd_funcionario.validar_acesso(usuario, senha)

def recuperar_senha(email: str) -> Tuple[str, str] | bool:
    """
    Recupera a senha do usuário.
    
    Args:
        email (str): Email do usuário.
    
    Returns:
        str: Senha do usuário.
    """
    
    return bd_funcionario.recuperar_senha_usuario(email)

    