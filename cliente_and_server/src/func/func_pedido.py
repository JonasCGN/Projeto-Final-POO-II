"""
Módulo que contém funções relacionadas a pedidos.
"""

from typing import Tuple
from funcao_postgree.bd_postgree_pedido import BdPedido
from funcao_postgree.bd_postgree_pedido_produto import BdPedidoProduto

bd_pedido = BdPedido()
bd_pedido_produto = BdPedidoProduto()

def transformar_lista_str_em_lista_tuple(lista: list[str]) -> list[Tuple[str, int]]:
    """
    Transforma uma lista de strings em uma lista de tuplas.
    
    Args:
        lista (list[str]): Lista de strings, onde cada string é um item no formato "ID: id, Nome: nome, Preço: preço, Quantidade: quantidade".
    
    Returns:
        list[Tuple[str, int]]: Lista de tuplas onde cada tupla é um item no formato (id, preço, quantidade).
    """
    
    lista_tuple = []
    for item in lista:
        item_split = item.split(", ")
        id = item_split[0].split(": ")[1]
        preco = float(item_split[2].split(": ")[1])
        qtd = int(item_split[3].split(": ")[1])
        lista_tuple.append((id, preco, qtd))
    
    return lista_tuple

def editar_status_pedido(id_pedido: str, status: str) -> bool:
    """
    Edita o status de um pedido.
    
    Args:
        id_pedido (str): ID do pedido a ser editado.
        status (str): Novo status do pedido.
    
    Returns:
        bool: True se a edição foi bem sucedida, False caso contrário.
    """
    status = bd_pedido.editar_status(status, id_pedido)
    return status

def inserir_pedido(produtos: list[Tuple[int, float, int]], mesa: int, status: str) -> bool:
    """
    Insere um pedido no banco de dados.
    
    Args:
        produtos (list[Tuple[int, float, int]]): Lista de tuplas onde cada tupla é um item no formato (id, preço, quantidade).
        mesa (int): Número da mesa.
        status (str): Status do pedido.
    
    Returns:
        bool: True se a inserção foi bem sucedida, False caso contrário.
    """
    list_pedidos_dict = []
    for pedido in produtos:
        list_pedidos_dict.append({"produto_id": pedido[0], "preco_pago": pedido[1], "quantidade": pedido[2]})
        
    status = bd_pedido_produto.inserir_pedido_com_produtos(list_pedidos_dict, mesa, status)
    return status
  
def transformar_lista_str_em_lista_tuple(lista: list[str]) -> list[Tuple[str, int]]:
    """
    Transforma uma lista de strings em uma lista de tuplas.
    
    Args:
        lista (list[str]): Lista de strings, onde cada string é um item no formato "ID: id, Nome: nome, Preço: preço, Quantidade: quantidade".
    
    Returns:
        list[Tuple[str, int]]: Lista de tuplas onde cada tupla é um item no formato (id, preço, quantidade).
    """
    lista_tuple = []
    for item in lista:
        item_split = item.split(", ")
        id = item_split[0].split(": ")[1]
        preco = float(item_split[2].split(": ")[1])
        qtd = int(item_split[3].split(": ")[1])
        lista_tuple.append((id, preco, qtd))
    
    return lista_tuple

def get_utimos_1000_pedidos() -> list[str]:
    """
    Busca os últimos 1000 pedidos no banco de dados.
    
    Returns:
        list[str]: Lista de pedidos no formato "ID: id, Mesa: mesa, Status: status, Data/Hora: data_hora".
    """
    pedidos = []
    for pedido in bd_pedido.get_last_1000():
        id = pedido[0]
        mesa = pedido[1]
        status = pedido[2]
        data_hora = pedido[3]
        pedidos.append(f"ID: {id}, Mesa: {mesa}, Status: {status}, Data/Hora: {data_hora}")
    
    return pedidos

def editar_status_pedido(id_pedido: str, status: str) -> bool:
    """
    Edita o status de um pedido.
    
    Args:
        id_pedido (str): ID do pedido a ser editado.
        status (str): Novo status do pedido.
    
    Returns:
        bool: True se a edição foi bem sucedida, False caso contrário.
    """
    
    status = bd_pedido.editar_status(status, id_pedido)
    return status

def get_produtos_do_pedido(id_pedido: str) -> list[str]:
    """
    Busca os produtos de um pedido.
    
    Args:
        id_pedido (str): ID do pedido.
    
    Returns:
        list[str]: Lista de produtos no formato "ID: id, Nome: nome, Preço: preço, Quantidade: quantidade".
    """
    pedidos = bd_pedido_produto.get_produtos_do_pedido(id_pedido)
    return pedidos