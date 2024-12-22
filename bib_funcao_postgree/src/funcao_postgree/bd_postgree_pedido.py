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
                    pedidos INTEGER[] NOT NULL,
                    data_hora TIMESTAMP NOT NULL,
                );
            """)
            self.commit()
            print("[LOG INFO] Tabela inicializada com sucesso!")
        except Exception as e:
            print(f"[LOG ERRO] Não foi possível criar a tabela: {e}")
        finally:
            cursor.close()
    
    def _format_from_inserct(self, pedido: str) -> dict:
        pedido = json.loads(pedido)
        data_datetime = datetime.strptime(pedido['data'], '%Y-%m:%d').date()

        return {
            "pedidos": pedido['pedidos'],
            "data": data_datetime,
            "hora": pedido['hora']
        }

    def insert_pedido(self, pedido: str) -> bool:
        retorno = True
        try:
            valores = self._format_from_inserct(pedido)
            query = """
                INSERT INTO Pedido (pedidos, data, hora) 
                VALUES (%s, %s, %s)
            """
            self.cursor_de_insercao.execute(query, valores)
        except Exception:
            self.post_client.rollback()
            retorno = False

        return retorno

    def get(self, id: int) -> Union[tuple, None]:
        try:
            cursor = self.get_cursor()
            cursor.execute("SELECT * FROM Pedido WHERE id = %s;", [id])
            resultado = cursor.fetchone()

            return resultado
        except Exception as e:
            print(f"[LOG ERRO] Erro ao consultar dados: {e}")
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
