from .bd_postgree_base import Bd_Base
from typing import Union
import json

class BdProduto(Bd_Base):

    def __init__(self) -> None:
        super().__init__()
        self.database_init()

    def database_init(self) -> None:
        try:
            cursor = self.get_cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Produto (
                    nome VARCHAR(255) PRIMARY KEY,
                    preco DECIMAL(10, 2) NOT NULL,
                    quantidade INT NOT NULL
                );
            """)

            self.commit()
        except Exception as e:
            print(f"Não foi possível criar a tabela: {e}")
        finally:
            cursor.close()

    def _format_from_inserct(self, produto: str) -> dict:
        valor =  json.loads(produto)
        return (valor['nome'], valor["preco"], valor["quantidade"])

    def insert_pedido(self, produto: str) -> bool:
        retorno = True
        try:
            valor = self._format_from_inserct(produto)
            query = """
                INSERT INTO Produto (nome, preco, quantidade) 
                VALUES (%s, %s, %s)
            """
            cursor = self.get_cursor()
            cursor.execute(query, valor)
            self.commit()
            
        except Exception as e:
            print("Erro ao inserir produto: ", e)
            self.post_client.rollback()
            retorno = False
        finally:
            cursor.close()

        return retorno

    def get(self, id: int) -> Union[tuple, None]:
        try:
            cursor = self.get_cursor()
            cursor.execute("SELECT * FROM Produto WHERE id = %s;", [id])
            resultado = cursor.fetchone()

            return resultado
        except Exception as e:
            print(f"Erro ao consultar dados: {e}")
            return None
        finally:
            cursor.close()

    def get_all(self) -> Union[list, None]:
        try:
            cursor = self.get_cursor()
            cursor.execute("SELECT * FROM Produto;")
            resultados = cursor.fetchall()
            return resultados
        except Exception:
            return None
        finally:
            cursor.close()
