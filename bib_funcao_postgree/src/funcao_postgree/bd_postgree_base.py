import psycopg2
from time import sleep
import os

class Bd_Base:

    post_client = None

    def __init__(self) -> None:
        if Bd_Base.post_client is None:
            self._conectar()

    def _conectar(self):
        while True:
            try:
                host = os.getenv("POSTGRES_HOST", "localhost")
                Bd_Base.post_client = psycopg2.connect(
                    host=host,
                    database='database-postgres',
                    user='root',
                    password='root'
                )
                print("[LOG INFO] Conectado ao PostgreSQL em: ", host)
                break
            except psycopg2.OperationalError as e:
                print(f"[LOG ERRO] Erro ao conectar ao PostgreSQL: {e}")
                print("[LOG INFO] Tentando novamente em 2 segundos...")
                sleep(2)

    def get_cursor(self) -> psycopg2.extensions.cursor:
        if Bd_Base.post_client.closed:
            print("[LOG INFO] Conexão perdida. Tentando restabelecer...")
            self._reiniciar_coneccao()
        return Bd_Base.post_client.cursor()

    def _reiniciar_coneccao(self):
        if Bd_Base.post_client is not None:
            try:
                Bd_Base.post_client.close()
                print("[LOG INFO] Conexão anterior fechada.")
            except Exception as e:
                print(f"[LOG ERRO] Erro ao fechar a conexão anterior: {e}")
        self._conectar()

    def commit(self) -> None:
        while True:
            try:
                Bd_Base.post_client.commit()
                break
            except Exception as e:
                print(f"[LOG ERRO] Erro ao tentar fazer commit: {e}")
                print("T[LOG INFO] Tentando reiniciar a conexão...")
                self._reiniciar_coneccao()
