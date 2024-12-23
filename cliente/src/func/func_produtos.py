from typing import Tuple
from funcao_postgree.bd_postgree_produto import BdProduto

bd_produto = BdProduto()


def pegar_todos_itens_str() -> list[str]:
    produtos = []
    for product in bd_produto.get_all():
        id = product[0]
        nome = product[1]
        preco = product[2]
        disponivel = "disponível" if bool(product[3]) else "indisponível"
        produtos.append(f"ID: {id}, Nome: {nome}, Preço: {preco}, Status: {disponivel}")
    
    return produtos
  