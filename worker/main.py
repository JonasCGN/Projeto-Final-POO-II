from time import sleep

from src.bd_postgres import DB_POSTGRES
from src.bd_redis import DB_Redis

if __name__ == '__main__':
    db_postgress = DB_POSTGRES()
    db_redis = DB_Redis()

    i = int(db_redis.get("qtd_removidos"))

    if (db_postgress.test_connection()):
        db_postgress.database_init()

        print((db_postgress.get_all()))
        while True:
            pedido = db_redis.get(f"{i}")
            
            print(pedido)
            
            if db_postgress.insert(pedido):
                db_redis.increment("qtd_removidos")
                db_redis.remove(f"{i}")
                i += 1
            else:
                print(f"Não foi possível inserir o pedido {i}")
                sleep(2)
    else:
        print("Não foi possível conectar ao banco de dados")