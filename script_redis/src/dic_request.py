import random
import time
import json

from src.produto import produtos

class DicRequest:
    """
    Classe DicRequest para manipulação de pedidos.
    Métodos:
        escolher_produtos():
            Seleciona aleatoriamente uma lista de produtos.
        criar_hora():
            Retorna a hora atual no formato HH:MM:SS.
        criar_data():
            Retorna a data atual no formato YYYY-MM:DD.
        criar_pedido():
            Cria um dicionário representando um pedido com produtos, data e hora.
        string_pedido(pedido):
            Converte um dicionário de pedido para uma string JSON.
    """

    def escolher_produtos(self):
        return [random.choice(list(produtos.keys())) for _ in range(random.randint(1, 10))]

    def criar_hora(self):
        return time.strftime("%H:%M:%S")

    def criar_data(self):
        return time.strftime("%Y-%m:%d")

    def criar_pedido(self):
        return {
            "pedidos": self.escolher_produtos(),
            "data": self.criar_data(),
            "hora": self.criar_hora()
        }

    def string_pedido(self, pedido):
        pedido_json = json.dumps(pedido)
        return pedido_json
