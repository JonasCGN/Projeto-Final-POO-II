import sys
import os

from src.bd import DB_Redis
from src.dic_request import DicRequest

qtd_requests = 1_000_000

if __name__ == '__main__':
    db = DB_Redis()
    dic = DicRequest()

    db.test_connection()
    for _ in range(qtd_requests):
        pedido_string = dic.string_pedido(dic.criar_pedido())
        print(pedido_string)
        db.insert(db.get("qtd_inseridos"), pedido_string)
        db.increment("qtd_inseridos")
