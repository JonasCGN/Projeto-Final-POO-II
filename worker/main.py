import sys
import os

from src.bd_postgres import DB_POSTGRES
from src.bd_redis import DB_Redis

qtd_requests = 1_000_000

if __name__ == '__main__':
    db_postgress = DB_POSTGRES()
    db_redis = DB_Redis()

    i = int(db_redis.get("qtd_removidos"))

    # for i in range(10):
    #     print(db_redis.get(f"{i.dumps()}"))
    if (db_postgress.test_connection()):
        db_postgress.database_init()

        print((db_postgress.get_all()))
        while True:
            # quantidade = int(db_redis.get("qtd_inseridos"))
            pedido = db_redis.get(f"{i}")

            if db_postgress.insert(pedido):
                db_redis.increment("qtd_removidos")
                db_redis.remove(f"{i}")
                i += 1
            else:
                print(f"Não foi possível inserir o pedido {i}")
    else:
        print("Não foi possível conectar ao banco de dados")
        # db.set_initial_values()
    # for _ in range(qtd_requests):
    #     db.insert(db.get("qtd_inseridos"), dic.string_pedido(dic.criar_pedido()))
    #     db.increment("qtd_inseridos")
