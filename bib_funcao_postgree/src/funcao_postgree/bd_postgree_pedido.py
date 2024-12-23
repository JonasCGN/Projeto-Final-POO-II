from .bd_postgree_base import Bd_Base
from typing import Union
import json
from datetime import datetime


class BdPedido(Bd_Base):

    def __init__(self) -> None:
        super().__init__()
        self.database_init()

    def database_init(self) -> None:

        try:
            cursor = self.get_cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Pedido (
                    id SERIAL PRIMARY KEY,
                    mesa INT NOT NULL,
                    status VARCHAR(255) NOT NULL,
                    data_hora TIMESTAMP NOT NULL
                );
            """)
            self.commit()
            print("[LOG INFO] Tabela inicializada com sucesso!")
        except Exception as e:
            print(f"[LOG ERRO] Não foi possível criar a tabela: {e}")
        finally:
            cursor.close()
    
    def _format_from_inserct(self, pedido: str) -> dict:
        valor =  json.loads(pedido)
        return (valor['mesa'], valor["status"], valor["data_hora"])

    def insert_pedido(self, pedido: str) -> bool:
        retorno = True
        try:
            valor = self._format_from_inserct(pedido)
            query = """
                INSERT INTO Pedido (mesa, status, data_hora) 
                VALUES (%s, %s, %s)
            """
            cursor = self.get_cursor()
            cursor.execute(query, valor)
            self.commit()
            
        except Exception as e:
            print("[LOG ERRO] Erro ao inserir pedido: ", e)
            self.post_client.rollback()
            retorno = False
        finally:
            cursor.close()

        return retorno
    
    def get_last_1000(self) -> Union[list, None]:
        try:
            cursor = self.get_cursor()
            cursor.execute("SELECT * FROM Pedido ORDER BY id DESC LIMIT 1000;")
            resultados = cursor.fetchall()
            return resultados
        except Exception:
            return None
        finally:
            cursor.close()


    def get_all(self) -> Union[list, None]:
        try:
            cursor = self.get_cursor()
            cursor.execute("SELECT * FROM Pedido;")
            resultados = cursor.fetchall()
            return resultados
        except Exception:
            return None
        finally:
            cursor.close()
