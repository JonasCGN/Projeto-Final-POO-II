from time import sleep
from src.bd_postgres import DB_POSTGRES
from src.bd_redis import DB_Redis

"""
Este script é responsável por sincronizar dados entre um banco de dados PostgreSQL e um banco de dados Redis.
Classes Importadas:
- DB_POSTGRES: Classe para interagir com o banco de dados PostgreSQL.
- DB_Redis: Classe para interagir com o banco de dados Redis.
Funções:
- Nenhuma função definida fora do escopo principal.
Execução Principal:
- Inicializa instâncias das classes DB_POSTGRES e DB_Redis.
- Recupera a quantidade de itens removidos do Redis.
- Testa a conexão com o banco de dados PostgreSQL.
- Inicializa o banco de dados PostgreSQL.
- Recupera e imprime todos os registros do banco de dados PostgreSQL.
- Em um loop infinito, recupera pedidos do Redis e tenta inseri-los no PostgreSQL.
    - Se a inserção for bem-sucedida, incrementa o contador de itens removidos no Redis e remove o item processado.
    - Se a inserção falhar, imprime uma mensagem de erro e aguarda 2 segundos antes de tentar novamente.
- Se a conexão com o banco de dados PostgreSQL falhar, imprime uma mensagem de erro.
Variáveis:
- db_postgress: Instância da classe DB_POSTGRES.
- db_redis: Instância da classe DB_Redis.
- i: Contador de itens removidos, inicializado a partir do valor armazenado no Redis.
"""

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
