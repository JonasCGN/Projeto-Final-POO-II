"""
Módulo responsável por gerenciar a autenticação do usuário.
"""

import json
from typing import Tuple, Union
from funcao_postgree.bd_postgree_funcionario import BdFuncionario

CREDENCIAIS_FILE = "credenciais.json"
bd_funcionario = BdFuncionario()


def carregar_credenciais() -> Tuple[str, str] | tuple[None, None]:
    """
    Carrega as credenciais do arquivo JSON ao importar o módulo.
    """
    email_autenticado_atual = None
    usuario_autenticado_atual = None
    try:
        with open(CREDENCIAIS_FILE, "r") as f:
            dados = json.load(f)
            usuario_autenticado_atual = dados.get("usuario")
            email_autenticado_atual = dados.get("email")
    except FileNotFoundError:
        pass

    return email_autenticado_atual, usuario_autenticado_atual


def salvar_credenciais(email: str, usuario: str):
    """
    Salva as credenciais no arquivo JSON.
    """
    with open(CREDENCIAIS_FILE, "w") as f:
        json.dump({"email": email, "usuario": usuario}, f)


def inserir_funcionario(funcionario: dict[str, str]) -> bool:
    """
    Insere um funcionário no banco de dados.
    """
    confirm = bd_funcionario.insert_funcionario(json.dumps(funcionario))
    with open(CREDENCIAIS_FILE, "w") as f:
        json.dump({"email": funcionario["email"],
                  "usuario": funcionario["usuario"]}, f)
    return confirm


def validar_acesso(usuario: str, senha: str) -> bool:
    """
    Valida o acesso do usuário.
    """
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


def trocar_senha(senha: str) -> bool:
    """
    Troca a senha do usuário.
    """
    email, usuario_autenticado_atual = carregar_credenciais()
    print(usuario_autenticado_atual, senha)
    return bd_funcionario.trocar_senha(usuario_autenticado_atual, senha)
