import sys
import os

from src.bd import DB_Redis
from src.dic_request import DicRequest

qtd_requests = 100

if __name__ == '__main__':
    db = DB_Redis()
    dic = DicRequest()

    db.test_connection()
    for _ in range(qtd_requests):
        db.insert(db.get("qtd_inseridos"), dic.string_pedido(dic.criar_pedido()))
        db.increment("qtd_inseridos")
