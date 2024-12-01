"""
Este módulo define a classe Produto e um dicionário de produtos predefinidos.

A classe Produto permite representar produtos com nome, preço e quantidade disponíveis.

O dicionário `produtos` armazena instâncias da classe Produto, associadas a identificadores únicos.
"""

import json

class Produto:
    """
    Classe Produto representa um produto com nome, preço e quantidade.

    Atributos:
        nome (str): O nome do produto.
        preco (float): O preço do produto.
        quantidade (int): A quantidade disponível do produto.

    Métodos:
        __init__(nome: str, preco: float, quantidade: int): Inicializa uma nova instância da classe Produto.
    """
    def __init__(self, nome: str = None, preco: float = None, quantidade: int = None) -> None:
        """
        Inicializa uma instância da classe Produto.

        Args:
            nome (str, opcional): O nome do produto. Padrão é None.
            preco (float, opcional): O preço do produto. Padrão é None.
            quantidade (int, opcional): A quantidade do produto em estoque. Padrão é None.
        """
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
