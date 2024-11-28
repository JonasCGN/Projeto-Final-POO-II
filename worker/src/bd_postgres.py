import psycopg2
from time import sleep
import os
import json
from datetime import datetime


class DB_POSTGRES:

    def __init__(self):
        while True:
            try:
                post_host = os.getenv('HOST_TO_POSTGRES', 'localhost')
                self.post_client = psycopg2.connect(host=post_host, database='database-postgres',
                                                    user='root', password='root')
                print(f"Conectado ao PostgreSQL em {post_host}...")
                break
            except psycopg2.OperationalError:
                print("Não foi possível conectar ao PostgreSQL. Tentando novamente em 2 segundos...")
                sleep(2)
                continue

    def database_init(self):
        try:
            executar = self.post_client.cursor()
            
            executar.execute("""
                CREATE TABLE IF NOT EXISTS gerencia_pedidos (
                    id SERIAL PRIMARY KEY,
                    pedidos INTEGER[] NOT NULL,
                    data DATE NOT NULL,
                    hora TIME NOT NULL
                );
            """)

            print("Tabela inicializada com sucesso!")
        except Exception as e:
            print(f"Não foi possível criar a tabela: {e}")
        finally:
            if executar:
                executar.close()

        self.commit()

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

    def insert(self, pedido:str):
        retorno = False
        try:

            executar = self.post_client.cursor()
            pedido = json.loads(pedido)
            
            data_datetime = datetime.strptime(pedido['data'], '%Y-%m:%d').date()
            
            query = """
                INSERT INTO gerencia_pedidos (pedidos, data, hora) 
                VALUES (%s, %s, %s)
                RETURNING id;
            """
            valores = [pedido['pedidos'], data_datetime, pedido['hora']]

            # Executa o comando e captura o retorno
            executar.execute(query, valores)
            id_gerado = executar.fetchone()[0]

            print("ID gerado:", id_gerado)
            
            self.commit()

            retorno = True
        except Exception as e:
            print(f"Erro ao inserir dados: {e}")
            self.post_client.rollback()
        finally:
            if executar:
                executar.close()

        return retorno

    def get(self,id:int):
        try:
            executar = self.post_client.cursor()
            executar.execute("SELECT * FROM gerencia_pedidos WHERE id = %s;", [id])

            resultado = executar.fetchone()
            
            return resultado
        except Exception as e:
            print(f"Erro ao consultar dados: {e}")
            return None
    
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
