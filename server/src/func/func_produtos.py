import json
from typing import Union
from postgre_func.bd_postgree_produto import BdProduto
from produt_maneger.gerenciar_produto import GerenciarProdutos
  
bd_produto = BdProduto()
gerenciar_produto = GerenciarProdutos(bd_produto.get_all())

  
def inserir_produto(product: dict[str, Union[str, int, float]]) -> bool:
  status = bd_produto.insert_pedido(json.dumps(product))
  return status

def get_all_itens_str():
  return [f"Nome: {item[0]}, Preço: {item[1]}, Quantidade: {item[0]}" for item in bd_produto.get_all()]