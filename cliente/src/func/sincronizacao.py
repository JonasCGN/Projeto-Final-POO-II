from typing import Callable

from sincronizacao_servidor_cliente import ClienteSincronizado


cliente_sincronizado = ClienteSincronizado()


def iniciar_cliente_sincronizado(on_mensage):
    cliente_sincronizado.iniciar(on_mensage)


def enviar_mensagem_de_sincronizacao(msg):
    cliente_sincronizado.enviar_mensagem(msg)
