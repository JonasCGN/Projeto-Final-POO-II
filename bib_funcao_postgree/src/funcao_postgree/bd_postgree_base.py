"""
Módulo com a classe base para conexão com o banco de dados PostgreSQL.
"""

import psycopg2
from time import sleep
import os

class Bd_Base:
    """
    Classe base para conexão com o banco de dados PostgreSQL.
    """

    post_client = None

    def __init__(self, host: str = "localhost", database: str = "database-postgres", user: str = "root", password: str = "root") -> None:
        """
        Inicializa a conexão com o banco de dados.
        """
        if Bd_Base.post_client is None:
            self.host = host
            self.database = database
            self.user = user
            self.password = password
            self._conectar()

    def _conectar(self) -> None:
        """
        Conecta ao banco de dados PostgreSQL.
        """
        while True:
            try:
                print("[LOG INFO] Tentando conectar ao PostgreSQL em:", self.host)
                print("[LOG INFO] database:", self.database)
                Bd_Base.post_client = psycopg2.connect(
                    host=self.host,
                    database=self.database,
                    user=self.user,
                    password=self.password
                )
                print("[LOG INFO] Conectado ao PostgreSQL em:", self.host)
                break
            except psycopg2.OperationalError as e:
                print(f"[LOG ERRO] Erro ao conectar ao PostgreSQL: {e}")
                print("[LOG INFO] Tentando novamente em 2 segundos...")
                sleep(2)

    def get_cursor(self) -> psycopg2.extensions.cursor:
        """
        Retorna um cursor para a conexão com o banco de dados.

        Returns:
            psycopg2.extensions.cursor: Cursor para a conexão com o banco de dados.
        """
        if Bd_Base.post_client.closed:
            print("[LOG INFO] Conexão perdida. Tentando restabelecer...")
            self._reiniciar_coneccao()
        return Bd_Base.post_client.cursor()

    def _reiniciar_coneccao(self) -> None:
        """
        Reinicia a conexão com o banco de dados.
        """
        if Bd_Base.post_client is not None:
            try:
                Bd_Base.post_client.close()
                print("[LOG INFO] Conexão anterior fechada.")
            except Exception as e:
                print(f"[LOG ERRO] Erro ao fechar a conexão anterior: {e}")
        self._conectar()

    def commit(self) -> None:
        """
        Realiza o commit da transação.
        """
        qtd_tentativas = 0
        while True and qtd_tentativas < 3:
            try:
                Bd_Base.post_client.commit()
                break
            except Exception as e:
                print(f"[LOG ERRO] Erro ao tentar fazer commit: {e}")
                print("T[LOG INFO] Tentando reiniciar a conexão...")
                self._reiniciar_coneccao()
                qtd_tentativas += 1
        
        if qtd_tentativas == 3:
            print("[LOG ERRO] Não foi possível fazer commit após 3 tentativas. Encerrando...")
            exit(1)
