from .bd_postgree_base import Bd_Base
from typing import Union
import json
from datetime import datetime


class BdCliente(Bd_Base):

    def __init__(self) -> None:
        super().__init__()
        self.database_init()

    def database_init(self) -> None:
        try:
            cursor = self.get_cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Cliente (
                    id SERIAL PRIMARY KEY,
                    nome VARCHAR(100) NOT NULL,
                    email VARCHAR(100) NOT NULL,
                    senha VARCHAR(255) NOT NULL
                );
            """)
            self.commit()
            print("[LOG INFO] Tabela Cliente inicializada com sucesso!")
        except Exception as e:
            print(f"[LOG ERRO] Não foi possível criar a tabela Cliente: {e}")
        finally:
            cursor.close()

    def _format_from_insert(self, cliente: str) -> dict:
        cliente = json.loads(cliente)
        return (cliente['nome'], cliente['email'], cliente['senha'])

    def insert_cliente(self, cliente: str) -> bool:
        retorno = True
        try:
            valores = self._format_from_insert(cliente)
            query = """
                INSERT INTO Cliente (nome, email, senha) 
                VALUES (%s, %s, %s)
            """
            cursor = self.get_cursor()
            cursor.execute(query, valores)
            self.commit()

        except Exception as e:
            print(f"[LOG ERRO] Erro ao inserir o cliente: {e}")
            self.post_client.rollback()
            retorno = False
        finally:
            cursor.close()

        return retorno

    def get_cliente(self, id: int) -> Union[tuple, None]:
        try:
            cursor = self.get_cursor()
            cursor.execute("SELECT * FROM Cliente WHERE id = %s;", [id])
            resultado = cursor.fetchone()
            return resultado
        except Exception as e:
            print(f"[LOG ERRO] Erro ao consultar dados do cliente: {e}")
            return None
        finally:
            cursor.close()

    def get_all_clientes(self) -> Union[list, None]:
        try:
            cursor = self.get_cursor()
            cursor.execute("SELECT * FROM Cliente;")
            resultados = cursor.fetchall()
            return resultados
        except Exception as e:
            print(f"[LOG ERRO] Erro ao consultar todos os clientes: {e}")
            return None
        finally:
            cursor.close()

    def update_cliente(self, id: int, nome: str, email: str, senha: str) -> bool:
        try:
            cursor = self.get_cursor()
            query = """
                UPDATE Cliente
                SET nome = %s, email = %s, senha = %s
                WHERE id = %s
            """
            cursor.execute(query, (nome, email, senha, id))
            self.commit()
            print("[LOG INFO] Cliente atualizado com sucesso!")
            return True
        except Exception as e:
            print(f"[LOG ERRO] Erro ao atualizar cliente: {e}")
            self.post_client.rollback()
            return False
        finally:
            cursor.close()
