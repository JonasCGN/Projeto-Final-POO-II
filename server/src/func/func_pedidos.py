from typing import Tuple
from funcao_postgree.bd_postgree_pedido import BdPedido

bd_pedido = BdPedido()


def transformar_lista_str_em_lista_tuple(lista: list[str]) -> list[Tuple[str, int]]:
    lista_tuple = []
    for item in lista:
        item_split = item.split(", ")
        id = item_split[0].split(": ")[1]
        preco = float(item_split[2].split(": ")[1])
        qtd = int(item_split[3].split(": ")[1])
        lista_tuple.append((id, preco, qtd))
    
    return lista_tuple

def get_utimos_1000_pedidos() -> list[str]:
    pedidos = []
    for pedido in bd_pedido.get_last_1000():
        id = pedido[0]
        mesa = pedido[1]
        status = pedido[2]
        data_hora = pedido[3]
        pedidos.append(f"ID: {id}, Mesa: {mesa}, Status: {status}, Data/Hora: {data_hora}")
    
    return sorted(pedidos, key=lambda x: int(x.split(",")[0].split(": ")[1]))