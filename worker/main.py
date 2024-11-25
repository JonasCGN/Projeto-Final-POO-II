import sys
import os

# Adicione o diretório do pacote ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from utils.worker.src.bd import DB_POSTGRES,Pedido
from utils.script_redis.src.bd import DB_Redis

# from src.dic_request import DicRequest

qtd_requests = 1_000_000

if __name__ == '__main__':
    db_postgress = DB_POSTGRES()
    
    # db_redis = DB_Redis()
    # print(int(db_redis.get("qtd_inseridos")))
    
    # dic = DicRequest()

    
    if(db_postgress.test_connection()):
        db_postgress.database_init()
        
        print(db_postgress.get_all())
        
        # pedido = Pedido(
        #     pedidos = [1,2,3,4,5],
        #     data = "2021-10-10",
        #     hora = "10:10:10"
        # )
        
        # db.insert(pedido)
        
        
        
        # db.set_initial_values()
    # for _ in range(qtd_requests):
    #     db.insert(db.get("qtd_inseridos"), dic.string_pedido(dic.criar_pedido()))
    #     db.increment("qtd_inseridos")
