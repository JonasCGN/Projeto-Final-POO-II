import random
import time
from src.produtos_mock import produtos


class DicRequest:

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
        return f"Pedido: {pedido['pedidos']} - Data: {pedido['data']} - Hora: {pedido['hora']}"
