"""
Módulo com a classe base para conexão com o banco de dados PostgreSQL.
"""

import psycopg2
from time import sleep
import os

class Bd_Base:
    """
    Classe base para conexão com o banco de dados PostgreSQL.

    Essa classe gerencia a conexão com o banco de dados, permitindo obter cursores,
    realizar commits e reconectar automaticamente em caso de falhas na conexão.

    Atributos:
        post_client (psycopg2.extensions.connection): Instância da conexão com o banco de dados PostgreSQL.
        host (str): Endereço do host do banco de dados.
        database (str): Nome do banco de dados.
        user (str): Nome do usuário para autenticação.
        password (str): Senha do usuário para autenticação.
    """

    post_client = None

    def __init__(self, host: str = "localhost", database: str = "database-postgres", user: str = "root", password: str = "root") -> None:
        """
        Inicializa a conexão com o banco de dados.

        Args:
            host (str): Endereço do host do banco de dados. Default é "localhost".
            database (str): Nome do banco de dados. Default é "database-postgres".
            user (str): Nome do usuário para autenticação. Default é "root".
            password (str): Senha do usuário para autenticação. Default é "root".
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

        Estabelece uma conexão com o banco e tenta reconectar automaticamente
        em caso de falha.
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

        Verifica se a conexão está ativa antes de retornar o cursor.

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

        Fecha a conexão atual, se existir, e tenta estabelecer uma nova conexão.
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

        Tenta executar o commit até 3 vezes em caso de falha, reconectando automaticamente.

        Raises:
            SystemExit: Se não for possível realizar o commit após 3 tentativas.
        """
        qtd_tentativas = 0
        while True and qtd_tentativas < 3:
            try:
                Bd_Base.post_client.commit()
                break
            except Exception as e:
                print(f"[LOG ERRO] Erro ao tentar fazer commit: {e}")
                print("[LOG INFO] Tentando reiniciar a conexão...")
                self._reiniciar_coneccao()
                qtd_tentativas += 1

        if qtd_tentativas == 3:
            print("[LOG ERRO] Não foi possível fazer commit após 3 tentativas. Encerrando...")
            exit(1)
