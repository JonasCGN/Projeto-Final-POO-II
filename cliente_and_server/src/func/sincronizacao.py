"""]
Módulo que contém funções para iniciar o cliente e o servidor de sincronização.
"""
from typing import Callable
from sincronizacao_servidor_cliente import ClienteSincronizado, ServidorSincronizacao


cliente_sincronizado = ClienteSincronizado()
sync_server = ServidorSincronizacao()

def iniciar_cliente_sincronizado(on_mensage: Callable) -> None:
    """
    Inicia o cliente sincronizado.
    
    Args:
        on_mensage (Callable): Função de callback para receber mensagens do servidor.
    """
    cliente_sincronizado.iniciar(on_mensage)

def enviar_mensagem_de_sincronizacao_cliente(msg: str) -> None:
    """
    Envia uma mensagem de sincronização para o servidor.
    
    Args:
        msg (str): Mensagem a ser enviada.
    """
    cliente_sincronizado.enviar_mensagem(msg)

def iniciar_servidor_sincronizado(on_message: Callable) -> None:
    """
    Inicia o servidor sincronizado.
    
    Args:
        on_message (Callable): Função de callback para receber mensagens dos clientes.
    """
    sync_server.iniciar(on_message)
    
def enviar_mensagem_de_sincronizacao_server(msg: str) -> None:
    """
    Envia uma mensagem de sincronização para todos os clientes.
    
    Args:
        msg (str): Mensagem a ser enviada.
    """
    sync_server.enviar_msg_para_todos_clientes(msg)

def close_server() -> None:
    """
    Encerra o servidor de sincronização.
    """
    enviar_mensagem_de_sincronizacao_server("server_down")
    sync_server.parar()
