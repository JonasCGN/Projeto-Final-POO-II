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
import redis  # type: ignore
import os


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
        self.redis_client = redis.Redis(host=redis_host, port=6379, decode_responses=True)
        print("Conexão estabelecida com sucesso!")

    def test_connection(self) -> bool:
        """
        Testa a conexão com o Redis.
        """
        confirm = True

        try:
            self.redis_client.ping()
            print("Conexão com o Redis estabelecida com sucesso!")
        except redis.ConnectionError:
            print("Não foi possível conectar ao Redis.")
            confirm = False

        return confirm

    def insert(self, key: str, value: str) -> None:
        """
        Insere um par chave-valor no Redis.

        Argumentos:
            key (str): A chave do par chave-valor.
            value (str): O valor do par chave-valor.
        """
        # Salvar em formator de lista
        self.redis_client.set(key, value)

    def remove(self, key: str) -> None:
        """
        Remove uma chave do Redis.

        Argumentos:
            key (str): A chave a ser removida.
        """
        self.redis_client.delete(key)
