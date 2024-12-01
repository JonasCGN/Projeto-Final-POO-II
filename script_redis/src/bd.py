"""
 Este módulo define a classe DB_Redis para interagir com um banco de dados Redis. 
    A classe DB_Redis fornece métodos para:
    - Inicializar a conexão com o Redis e carregar valores iniciais.
    - Inserir, remover, incrementar e decrementar pares chave-valor no Redis.
    - Testar a conexão com o Redis.
    - Obter o valor de uma chave no Redis.
    Classes:
        DB_Redis: Classe para interagir com um banco de dados Redis.
        redis.BusyLoadingError: Lançada quando o Redis está carregando dados.
        redis.ConnectionError: Lançada quando a conexão com o Redis não pode ser estabelecida.
"""
from time import sleep
import redis
import os

import redis.exceptions

class DB_Redis:
   
    """
    Classe para interagir com um banco de dados Redis.
    Métodos:
        __init__(): Inicializa a conexão com o Redis e carrega valores iniciais.
        set_initial_values(): Carrega valores iniciais do Redis ou define valores padrão.
        test_connection(): Testa a conexão com o Redis.
        insert(key, value): Insere um par chave-valor no Redis.
        remove(key): Remove uma chave do Redis.
        increment(key): Incrementa o valor de uma chave no Redis.
        decrement(key): Decrementa o valor de uma chave no Redis.
        get(key): Obtém o valor de uma chave no Redis.
    """

    def __init__(self):
        redis_host = os.getenv('HOST_TO_REDIS', 'localhost')
        print(f"Conectando ao Redis em {redis_host}...")
        self.redis_client = redis.Redis(
            host=redis_host, port=6379, decode_responses=True)
        print("Conexão estabelecida com sucesso!")
        self.set_initial_values()

    def set_initial_values(self):
        """
        Define os valores iniciais no Redis.
        Este método tenta carregar os valores iniciais de 'qtd_removidos' e 'qtd_inseridos' do Redis.
        Se os valores não existirem, eles são inicializados com 0. O método continua tentando até que
        os valores sejam carregados com sucesso ou uma conexão com o Redis não possa ser estabelecida.
        Exceções:
            redis.BusyLoadingError: Se o Redis estiver carregando os dados, o método aguardará 2 segundos e tentará novamente.
            redis.ConnectionError: Se a conexão com o Redis não puder ser estabelecida, o método será interrompido.
        """
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
            except redis.BusyLoadingError:
                print("Aguarde, o Redis está carregando os dados...")
                sleep(2)
            except redis.ConnectionError:
                print("Conexão com o Redis não estabelecida.")
                break

    def test_connection(self):
        try:
            self.redis_client.ping()
            print("Conexão com o Redis estabelecida com sucesso!")
        except redis.ConnectionError:
            print("Não foi possível conectar ao Redis.")

    def insert(self, key, value):
        self.redis_client.set(key, value)

    def remove(self, key):
        self.redis_client.delete(key)

    def increment(self, key):
        self.redis_client.incr(key)

    def decrement(self, key):
        self.redis_client.decr(key)

    def get(self, key):
        return self.redis_client.get(key)
