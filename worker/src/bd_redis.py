"""
Este módulo gerencia a conexão com o banco de dados Redis e operações relacionadas a chaves e valores.
Classes:
    DB_Redis: Classe responsável pela conexão com o Redis e gerenciamento de chaves e valores.
"""

from time import sleep
import redis  # type: ignore
import os


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
            host=redis_host,
            port=6379,
            decode_responses=True
        )
        print("Conexão estabelecida com sucesso!")

    def remove(self, key: str) -> None:
        """
        Remove um valor do Redis com a chave especificada.

        Args:
            key (str): A chave do valor a ser removido.
            value (str): O valor a ser removido do Redis.
        """
        self.redis_client.delete(key)

    def get(self, key: str) -> tuple[str | None]:
        """
        Obtém o valor de uma chave no Redis.

        Args:
            key (str): A chave do valor a ser obtido.
        """
        response = self.redis_client.get(key)
        return response
    
    def pegar_total_de_valores_presentes(self) -> int:
        """
        Obtém o total de valores presentes no Redis.
        """
        return self.redis_client.dbsize()
