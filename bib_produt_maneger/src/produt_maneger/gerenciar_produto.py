"""
Módulo responsável por gerenciar o estoque de produtos, incluindo funcionalidades como adicionar, listar, comprar, salvar e carregar produtos.
"""

import json
from produto import Produto

class GerenciarProdutos:
    """
    Classe responsável por gerenciar o estoque de produtos, incluindo funcionalidades como adicionar, listar, comprar, salvar e carregar produtos.
    """
  
    def __init__(self, produtos: dict = None) -> None:
        """
        Inicializa o gerenciador de produtos com um dicionário vazio de produtos.

        Args:
            produtos (dict, optional): Dicionário contendo os produtos. As chaves são os nomes dos produtos e os valores são objetos da classe Produto. Defaults to None.
        """
        
        self.produtos = produtos or {}

    def add_produto(self, produto: Produto):
        """
        Adiciona um produto ao estoque ou atualiza a quantidade de um produto existente.

        Args:
            produto (Produto): Objeto do tipo Produto a ser adicionado ou atualizado.
            quantidade (int): Quantidade do produto a ser adicionada.
        """
        self.produtos[produto.nome] = produto

    def listar_produtos(self):
        return [produto for produto in self.produtos.values()]

    def dump(self) -> dict:
        """
        Serializa o estoque de produtos para um formato JSON.

        Returno:
            str: String JSON representando o dicionário de produtos.
        """
        data = {}
        for key, value in self.produtos.items():
            data[key] = value.dump()
        return json.dumps(data)

    def load(self, data: dict):
        """
        Carrega produtos a partir de um dicionário de dados em formato JSON.

        Args:
            data (dict): Dicionário onde as chaves são os nomes dos produtos e os valores 
            são strings JSON representando os objetos Produto.
        """
        for key, value in data.items():
            produto = Produto()
            produto.load(json.loads(value))
            self.produtos[key] = produto

    def procurar_produto(self, nome: str) -> Produto:
        """
        Busca um produto pelo nome no estoque.

        Args:
            nome (str): Nome do produto a ser procurado.

        Returno:
            bool: Retorna True se o produto for encontrado; caso contrário, False.
        """
        return nome in self.produtos
