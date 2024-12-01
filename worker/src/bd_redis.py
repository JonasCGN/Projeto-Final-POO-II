from time import sleep
import redis
import os

import redis.exceptions

class DB_Redis:
    """
    Classe para gerenciar a conexão e operações com o banco de dados Redis.
    Métodos:
        __init__(): Inicializa a conexão com o Redis e carrega valores iniciais.
        set_initial_values(): Carrega valores iniciais do Redis ou define valores padrão.
        test_connection(): Testa a conexão com o Redis.
        insert(key, value): Insere um valor no Redis com a chave especificada.
        remove(key): Remove um valor do Redis com a chave especificada.
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
        a conexão com o Redis seja estabelecida ou ocorra um erro de carregamento.
        Exceções:
            redis.ConnectionError: Se a conexão com o Redis não puder ser estabelecida.
            redis.BusyLoadingError: Se o Redis estiver carregando dados e não puder responder.
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
            except redis.ConnectionError:
                print("Conexão com o Redis não estabelecida.")
                break
            except redis.BusyLoadingError:
                print("Aguarde, o Redis está carregando os dados...")
                sleep(2)

    def test_connection(self):
        """
        Testa a conexão com o servidor Redis.

        Tenta enviar um comando PING para o cliente Redis para verificar se a conexão
        está estabelecida corretamente. Se a conexão for bem-sucedida, uma mensagem
        de sucesso será impressa. Caso contrário, uma mensagem de erro será exibida.

        Raises:
            redis.ConnectionError: Se não for possível conectar ao Redis.
        """
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
