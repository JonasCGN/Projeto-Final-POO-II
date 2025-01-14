"""
Módulo responsável por gerenciar a autenticação do usuário.
"""

import json
from typing import Tuple, Union
from funcao_postgree.bd_postgree_funcionario import BdFuncionario

CREDENCIAIS_FILE = "credenciais.json"

bd_funcionario = BdFuncionario()

def carregar_credenciais():
    """
    Carrega as credenciais do arquivo JSON ao importar o módulo.
    """
    global email_autenticado_atual, usuario_autenticado_atual
    try:
        with open(CREDENCIAIS_FILE, "r") as f:
            dados = json.load(f)
            email_autenticado_atual = dados.get("email")
            usuario_autenticado_atual = dados.get("usuario")
    except FileNotFoundError:
        pass

def salvar_credenciais(email: str, usuario: str):
    """
    Salva as credenciais no arquivo JSON.
    """
    with open(CREDENCIAIS_FILE, "w") as f:
        json.dump({"email": email, "usuario": usuario}, f)

def get_email_autenticado() -> str:
    """
    Retorna o email autenticado.
    """
    with open(CREDENCIAIS_FILE, "r") as f:
        return json.load(f).get("email")

def inserir_funcionario(funcionario: dict[str, str]) -> bool:
    """
    Insere um funcionário no banco de dados.
    """
    confirm = bd_funcionario.insert_funcionario(json.dumps(funcionario))
    with open(CREDENCIAIS_FILE, "w") as f:
        json.dump({"email": funcionario["email"], "usuario": funcionario["usuario"]}, f)
    return confirm

def validar_acesso(usuario: str, senha: str) -> bool:
    """
    Valida o acesso do usuário.
    """
    global email_autenticado_atual, usuario_autenticado_atual

    confirm = bd_funcionario.validar_acesso(usuario, senha)
    if confirm:
        email_autenticado_atual = bd_funcionario.get_email(usuario)
        usuario_autenticado_atual = usuario
        salvar_credenciais(email_autenticado_atual, usuario_autenticado_atual)
    return confirm

def recuperar_senha(email: str) -> Union[Tuple[str, str], bool]:
    """
    Recupera a senha do usuário.
    """
    return bd_funcionario.recuperar_senha_usuario(email)

def esquecer_credenciais():
    """
    Esquece as credenciais do usuário.
    """
    with open(CREDENCIAIS_FILE, "w") as f:
        json.dump({}, f)

carregar_credenciais()