import json

class Produto:
    def __init__(self, nome: str = None, preco: float = None, quantidade: int = None) -> None:
        self.nome = nome
        self.preco = preco
        self.quantidade = quantidade

produtos = {
    1: Produto("Coca-Cola", 5.00, 6),
    2: Produto("Pepsi", 4.00, 1),
    3: Produto("Guaraná", 3.00, 7),
    4: Produto("Fanta", 2.00, 4),
    5: Produto("Sprite", 1.00, 1),
}
