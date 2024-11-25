import psycopg2

import sys
import os


class DB_POSTGRES:

    def __init__(self):
        post_host = os.getenv('HOST_TO_POSTGRES', 'localhost')
        self.post_client = psycopg2.connect(host=post_host, database='database-postgres',
                                            user='root', password='root')

    def database_init(self):
        try:
            executar = self.post_client.cursor()
            executar.execute("""
                CREATE TABLE IF NOT EXISTS gerencia_pedidos (
                    id SERIAL PRIMARY KEY,
                    pedidos JSONB NOT NULL
                );
            """)

            print("Tabela inicializada com sucesso!")
        except Exception as e:
            print(f"Não foi possível criar a tabela: {e}")
        finally:
            if executar:
                executar.close()

        self.post_client.commit()

    def test_connection(self):
        retorno = False
        try:
            executar = self.post_client.cursor()

            executar.execute("SELECT version();")
            versao = executar.fetchone()

            print(f"Conectado ao PostgreSQL. Versão: {versao}")
            retorno = True
        except Exception as e:
            print(f"Não foi possível conectar ao PostgreSQL: {e}")
        finally:
            if executar:
                executar.close()

        return retorno

    def insert(self, pedido):
        retorno = False
        try:

            executar = self.post_client.cursor()

            executar.execute("""
                    INSERT INTO gerencia_pedidos (pedidos) 
                    VALUES (%s);
                """, [pedido])

            self.commit()

            # print("Dados inseridos com sucesso!")
            retorno = True
        except Exception as e:
            print(f"Erro ao inserir dados: {e}")
        finally:
            if executar:
                executar.close()

        return retorno

    def get_all(self):
        try:
            executar = self.post_client.cursor()
            executar.execute("SELECT * FROM gerencia_pedidos;")

            resultados = executar.fetchall()
            print("Dados consultados com sucesso!")

            return resultados
        except Exception as e:
            print(f"Erro ao consultar dados: {e}")
            return None

    def commit(self):
        self.post_client.commit()
