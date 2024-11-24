import random
import time
from src.produtos_mock import produtos


class dic_request:
    def __init__(self):
        self.produtos = produtos

    def escolher_produtos(self):
        return [random.choice(list(self.produtos.values())) for _ in range(random.randint(1, 10))]

    def criar_hora(self):
        return time.strftime("%Y-%m:%d")

    def criar_data(self):
        return time.strftime("%H:%M:%S")

    def criar_pedido(self):
        return {
            "id": self.escolher_produtos(),
            "data": self.criar_data(),
            "hora": self.criar_hora()
        }
