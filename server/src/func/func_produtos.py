import json
from typing import Union
from postgre_func.bd_postgree_produto import BdProduto

bd_produto = BdProduto()


def inserir_produto(product: dict[str, Union[str, int, float]]) -> bool:
    status = bd_produto.insert_produto(json.dumps(product))
    return status


def atualizar_produto(product: dict[str, Union[str, int, float]], id_product: str) -> bool:
    status = bd_produto.atualizar_produto(json.dumps(product), int(id_product))
    return status


def pegar_todos_itens_str():
    return [f"id: {item[0]}, Nome: {item[1]}, Preço: {item[2]}, Quantidade: {item[3]}" for item in bd_produto.get_all()]
