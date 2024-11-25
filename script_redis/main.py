import sys
import os

# Adicione o diretório do pacote ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from utils.script_redis.src.bd import DB_Redis
from utils.script_redis.src.dic_request import DicRequest

qtd_requests = 1_000_000

if __name__ == '__main__':
    db = DB_Redis()
    dic = DicRequest()

    db.test_connection()
    for _ in range(qtd_requests):
        db.insert(db.get("qtd_inseridos"), dic.string_pedido(dic.criar_pedido()))
        db.increment("qtd_inseridos")
