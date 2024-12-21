import psycopg2
from time import sleep


class Bd_Base:

    def __init__(self) -> None:
        self.post_client = None
        self._conectar()

    def _conectar(self):
        while True:
            try:
                self.post_client = psycopg2.connect(
                    host="localhost",
                    database='database-postgres',
                    user='root',
                    password='root'
                )
                print("Conectado ao PostgreSQL em localhost...")
                break
            except psycopg2.OperationalError as e:
                print(f"Erro ao conectar ao PostgreSQL: {e}")
                print("Tentando novamente em 2 segundos...")
                sleep(2)

    def get_cursor(self) -> psycopg2.extensions.cursor:
        if self.post_client.closed:
            print("Conexão perdida. Tentando restabelecer...")
            self._reiniciar_coneccao()
        return self.post_client.cursor()

    def _reiniciar_coneccao(self):
        if self.post_client is not None:
            try:
                self.post_client.close()
                print("Conexão anterior fechada.")
            except Exception as e:
                print(f"Erro ao fechar a conexão anterior: {e}")
        self.conectar()

    def commit(self) -> None:
        while True:
            try:
                self.post_client.commit()
                break
            except Exception as e:
                print(f"Erro ao tentar fazer commit: {e}")
                print("Tentando reiniciar a conexão...")
                self.reiniciar_coneccao()
