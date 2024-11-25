from time import sleep
import redis
import os

import redis.exceptions

class DB_Redis:

    def __init__(self):
        redis_host = os.getenv('HOST_TO_REDIS', 'localhost')
        print(f"Conectando ao Redis em {redis_host}...")
        self.redis_client = redis.Redis(
            host=redis_host, port=6379, decode_responses=True)
        print("Conexão estabelecida com sucesso!")

        self.set_initial_values()
    
    def set_initial_values(self):
        while True:
            try:
                print("Carregando valores iniciais do Redis...")
                self.qtd_removidos = self.get('qtd_removidos')
                self.qtd_inseridos = self.get('qtd_inseridos')

                if self.qtd_removidos is None:
                    self.insert('qtd_removidos', 0)

                if self.qtd_inseridos is None:
                    self.insert('qtd_inseridos', 0)

                print("Valores iniciais carregados com sucesso!")
                break
            except redis.ConnectionError:
                print("Conexão com o Redis não estabelecida.")
                break
            except redis.BusyLoadingError:
                print("Aguarde, o Redis está carregando os dados...")
                sleep(2)

    def test_connection(self):
        try:
            self.redis_client.ping()
            print("Conexão com o Redis estabelecida com sucesso!")
        except redis.ConnectionError:
            print("Não foi possível conectar ao Redis.")

    def insert(self, key, value):
        self.redis_client.set(key, value)

    def increment(self, key):
        self.redis_client.incr(key)

    def decrement(self, key):
        self.redis_client.decr(key)

    def get(self, key):
        return self.redis_client.get(key)
