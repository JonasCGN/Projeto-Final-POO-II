"""
Módulo para sincronizar pedidos entre o Redis e o Postgres.
"""

from multiprocessing.pool import ThreadPool
from typing import Tuple
from .bd_postgres import DB_POSTGRES
from .bd_redis import DB_Redis


class Sincronizacao:
    def __init__(self):
        self.db_postgress = DB_POSTGRES()
        self.db_postgress.database_init()
        self.db_redis = DB_Redis()

    def sincronizar_lotes(self, value: str) -> None:
        """
        Sincroniza um lote de pedidos com o banco de dados Postgres.

        Args:
            value (str): Lote de pedidos a ser sincronizado.
        """

        self.db_postgress.insert(value)

    def remove_lotes(self, key: str) -> None:
        """
        Remove um lote de pedidos do banco de dados Redis.

        Args:
            key (str): Chave do lote a ser removido.
        """
        self.db_redis.remove(key)

    def intervalo_chaves(self, numero_do_lote: int, tamanho_do_lote: int, tamanho_do_lote_atual: int) -> Tuple[int, int]:
        """
        Retorna o intervalo de chaves para um lote.

        Args:
            numero_do_lote (int): Número do lote.
            tamanho_do_lote (int): Tamanho maximo do lote.
            tamanho_do_lote_atual (int): Tamanho do lote atual.

        Returns:
            Tuple[int, int]: Intervalo de chaves para o lote.
        """
        if tamanho_do_lote_atual < tamanho_do_lote:
            maximo = numero_do_lote * tamanho_do_lote + tamanho_do_lote_atual
        else:
            maximo = (numero_do_lote + 1) * tamanho_do_lote
        
        return numero_do_lote * tamanho_do_lote, maximo


    def run(self, numero_de_threads: int, tamanho_do_bacth_maximo: int = 100_000) -> None:
        """
        Função principal para sincronizar pedidos entre o Redis e o Postgres. Sincroniza pedidos em lotes.

        Args:
            numero_de_threads (int): O número de threads a serem usadas para a sincronização.
            tamanho_do_bacth_maximo (int, optional): O tamanho do lote de registros a serem sincronizados de uma vez.
            Defaults to 100_000.
        """
        quantidade_de_valores = self.db_redis.pegar_total_de_valores_presentes()
        print(f"Total de pedidos no Redis: {quantidade_de_valores}")

        quantidade_de_batches = (quantidade_de_valores + tamanho_do_bacth_maximo - 1) // tamanho_do_bacth_maximo

        for quantidade_de_batch in range(quantidade_de_batches):
            print(f"Sincronizando lote {quantidade_de_batch + 1}/{quantidade_de_batches}...")
            tamanho_do_batch_atual = min(tamanho_do_bacth_maximo, quantidade_de_valores - quantidade_de_batch * tamanho_do_bacth_maximo)
            print(f"Tamanho do lote atual: {tamanho_do_batch_atual}")

            chaves = self.db_redis.redis_client.scan(0, count=tamanho_do_batch_atual)[1]
            
            with ThreadPool(numero_de_threads) as pool:
                print("Pegando valores do Redis, lote {quantidade_de_batch + 1}...")
                pedidos = pool.map(self.db_redis.get, chaves)
                print("Valores pegos com sucesso!")

            self.db_postgress.start_cursor()
            with ThreadPool(numero_de_threads) as pool:
                print(f"Sincronizando lote {quantidade_de_batch + 1} com o PostgreSQL...")
                pool.map(self.sincronizar_lotes, pedidos)
                print(f"Lote {quantidade_de_batch +1} sincronizado com o PostgreSQL com sucesso!")
            self.db_postgress.commit() # Commit após cada lote
            self.db_postgress.close_cursor()

            with ThreadPool(numero_de_threads) as pool:
                print(f"Removendo lote {quantidade_de_batch + 1} do Redis...")
                pool.map(self.remove_lotes, chaves)
                print(f"Lote {quantidade_de_batch + 1} removido do Redis com sucesso!")
