"""
Módulo para enviar pedidos para o Redis.
"""

from typing import Tuple
from src.bd import DB_Redis
from src.dic_request import DicRequest
from multiprocessing.pool import ThreadPool



class SenderToRedis:
    """
    Classe para gerar e enviar pedidos para o Redis.
    """

    def __init__(self):
        """
        Inicializa a classe com instâncias de DB_Redis e DicRequest.
        """
        self.db = DB_Redis()
        self.dic = DicRequest()

    def generate_pedido(self, _) -> str:
        """
        Generate pedido

        Args:
            _ (NONE): Não recebe argumentos

        Returns:
            str: _description_
        """
        pedido_dic = self.dic.criar_pedido()
        pedido_string = self.dic.string_pedido(pedido_dic)
        return pedido_string

    def produzir_pedido(self, num_records: int, num_theads: int) -> list[str]:
        """
        Producer pedido

        Args:
            num_records (int): Quantidade de registros
            num_theads (int): Quantidade de threads
            batch_num (int): Numero do lote

        Returns:
            list[tuple[str, int]]: Lista de pedidos gerados sendo uma lista contendo tupla com o pedido e o numero do
            lote
        """
        with ThreadPool(num_theads) as pool:
            list_objects = pool.map(self.generate_pedido, range(num_records))
        return list_objects

    def consumer_pedido(self, key_value: tuple[int, str]) -> None:
        """
        Consumer pedido

        Args:
            enum_value (tuple[int, int, int]): Tupla contendo o enumerate do valor, o numero do lote e o pedido.
        """
        self.db.insert(key_value[0], key_value[1])
    
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


    def run(self, total_registros: int, num_threads: int, tamanho_lote: int = 100_000) -> None:
        """
        Função principal para inserir pedidos no Redis. Gera pedidos e os insere no Redis em lotes.

        Args:
            total_registros (int): A quantidade total de registros a serem inseridos.
            num_threads (int): O número de threads a serem usadas para a inserção.
            tamanho_lote (int, opcional): O tamanho do lote de registros a serem inseridos de uma vez. Defaults to 100_000.
        """
        num_lotes = (total_registros + tamanho_lote - 1) // tamanho_lote

        for numero_lote in range(num_lotes):
            print(f"Iniciando lote {numero_lote + 1} de {num_lotes}...")
            tamanho_lote_atual = min(tamanho_lote, total_registros - numero_lote * tamanho_lote)
            print(f"O tamanho do lote atual é {tamanho_lote_atual}.")

            lista_objetos = self.produzir_pedido(tamanho_lote_atual, num_threads)
            print(f"Gerados {len(lista_objetos)} pedidos para o lote {numero_lote + 1}.")

            with ThreadPool(num_threads) as pool:
                inicio, fim = self.intervalo_chaves(numero_lote, tamanho_lote, tamanho_lote_atual)
                key_value = [(id_bd, lista_objetos[idx]) for idx, id_bd in enumerate(range(inicio, fim))]
                pool.map(self.consumer_pedido, key_value)

            print(f"Finalizado lote {numero_lote + 1} de {num_lotes}.")

