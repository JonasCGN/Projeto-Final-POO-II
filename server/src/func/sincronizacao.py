from typing import Callable
from sincronizacao_servidor_cliente import ServidorSincronizacao


sync_server = ServidorSincronizacao()

def iniciar_servidor_sincronizado(on_message: Callable):
    sync_server.iniciar(on_message)
    
def enviar_mensagem_de_sincronizacao(msg: str):
    sync_server.enviar_msg_para_todos_clientes(msg)

