"""
Módulo que contém a classe Produto.
"""


import json


class Produto:
    """
    Utilizado para representar um produto em um sistema de gerenciamento de produtos.
    """

    def __init__(self, nome: str = None, preco: float = None, quantidade: int = None) -> None:
        """
        __init__

        Args:
            nome (str, optional): Nome do produto. Defaults to None.
            preco (float, optional): Preco do Produto. Defaults to None.
            quantidade (int, optional): Quantidade restantante do produto. Defaults to None.
        """
        self.nome = nome
        self.preco = preco
        self.quantidade = quantidade

    def dump(self) -> dict:
        """
        dump é usado para converter os atributos de uma instância da classe em um dicionário.

        Returns:
            dict: Dicionário com os atributos da instância.
        """

        return json.dumps({
            "nome": self.nome,
            "preco": self.preco,
            "quantidade": self.quantidade,
        })

    def load(self, data: dict):
        """
        load é usado para carregar os atributos de uma instância da classe a partir de um dicionário.

        Args:
            data (dict): Dicionário com os atributos da instância.
        """ 
        self.nome = data["nome"]
        self.preco = data["preco"]
        self.quantidade = data["quantidade"]

    def __str__(self) -> str:
        """
        __str__ é usado para retornar uma representação em string de uma instância da classe.

        Returns:
            str: Representação em string da instância.
        """
        return f"{self.nome} - R${self.preco:.2f} - {self.quantidade} unidades"
