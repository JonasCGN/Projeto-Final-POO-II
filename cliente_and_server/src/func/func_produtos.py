"""
Módulo que contém as funções relacionadas a produtos.
"""

from typing import Tuple, Union
import json
from funcao_postgree.bd_postgree_produto import BdProduto

bd_produto = BdProduto()


def inserir_produto(product: dict[str, Union[str, int, bool]]) -> bool:
    """
    Insere um produto no banco de dados.
    
    Args:
        product (dict[str, Union[str, int, bool]]): Dicionário com os dados do produto.
        chave: 'nome', 'preco' e 'disponivel'.
    
    Returns:
        bool: True se a inserção foi bem sucedida, False caso contrário.
    """
    status = bd_produto.insert_produto(json.dumps(product))
    return status


def atualizar_produto(product: dict[str, Union[str, int, float]], id_product: str) -> bool:
    """
    Atualiza um produto no banco de dados.
    
    Args:
        product (dict[str, Union[str, int, float]]): Dicionário com os dados do produto.
        chave: 'nome', 'preco' e 'disponivel'.
        id_product (str): ID do produto a ser atualizado.
    
    Returns:
        bool: True se a atualização foi bem sucedida, False caso contrário.
    """
    status = bd_produto.atualizar_produto(json.dumps(product), int(id_product))
    return status

def trocar_disponibilidade(id_product: str) -> bool:
    """
    Troca a disponibilidade de um produto.
    
    Args:
        id_product (str): ID do produto a ser alterado.
    
    Returns:
        bool: True se a alteração foi bem sucedida, False caso contrário.
    """
    status = bd_produto.trocar_disponibilidade(id_product)
    return status


def remover_produto(id_product: str) -> bool:
    """
    Remove um produto do banco de dados.
    
    Args:
        id_product (str): ID do produto a ser removido.
    
    Returns:
        bool: True se a remoção foi bem sucedida, False caso contrário.
    """
    status = bd_produto.remover_produto(id_product)
    return status


def pegar_todos_itens_str() -> list[str]:
    """
    Retorna uma lista de strings com os produtos cadastrados.
    
    Returns:
        list[str]: Lista de strings com os produtos cadastrados.
    """
    produtos = []
    for product in bd_produto.get_all():
        id = product[0]
        nome = product[1]
        preco = product[2]
        disponivel = "disponível" if bool(product[3]) else "indisponível"
        produtos.append(f"ID: {id}, Nome: {nome}, Preço: {preco}, Status: {disponivel}")
    
    return produtos
  