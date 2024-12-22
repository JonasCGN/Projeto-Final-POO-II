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
                    id SERIAL PRIMARY KEY,
                    nome VARCHAR(255) UNIQUE,
                    preco DECIMAL(10, 2) NOT NULL,
                    disponivel BOOLEAN DEFAULT TRUE
                );
            """)

            self.commit()
        except Exception as e:
            print(f"[LOG ERRO] Não foi possível criar a tabela: {e}")
        finally:
            cursor.close()

    def _format_from_inserct(self, produto: str) -> dict:
        valor =  json.loads(produto)
        return (valor['nome'], valor["preco"], valor["disponivel"])

    def insert_produto(self, produto: str) -> bool:
        retorno = True
        try:
            valor = self._format_from_inserct(produto)
            query = """
                INSERT INTO Produto (nome, preco, disponivel) 
                VALUES (%s, %s, %s)
            """
            cursor = self.get_cursor()
            cursor.execute(query, valor)
            self.commit()
            
        except Exception as e:
            print("[LOG ERRO] Erro ao inserir produto: ", e)
            self.post_client.rollback()
            retorno = False
        finally:
            cursor.close()

        return retorno

    def atualizar_produto(self, produto: str, id_produto: int) -> bool:
        retorno = True
        try:
            valor = self._format_from_inserct(produto)
            query = """
                UPDATE Produto 
                SET nome = %s, preco = %s, disponivel = %s
                WHERE id = %s
            """
            
            valor = (*valor, id_produto)
            
            cursor = self.get_cursor()
            cursor.execute(query, valor)
            self.commit() 
            
        except Exception as e:
            print("[LOG ERRO] Erro ao atualizar produto: ", e)
            self.post_client.rollback() 
            retorno = False
        finally:
            cursor.close()

        return retorno

    def remover_produto(self, id_produto: int) -> bool:
        retorno = True
        try:
            cursor = self.get_cursor()
            cursor.execute("DELETE FROM Produto WHERE id = %s;", (id_produto))
            self.commit()
        except Exception as e:
            print("[LOG ERRO] Erro ao remover produto: ", e)
            self.post_client.rollback()
            retorno = False
        finally:
            cursor.close()

        return retorno

    def trocar_disponibilidade(self, id_produto: int) -> bool:
        retorno = True
        try:
            cursor = self.get_cursor()
            cursor.execute("SELECT disponivel FROM Produto WHERE id = %s;", [id_produto])
            disponivel = cursor.fetchone()[0]
            cursor.execute("UPDATE Produto SET disponivel = %s WHERE id = %s;", [not disponivel, id_produto])
            self.commit()
        except Exception as e:
            print("[LOG ERRO] Erro ao trocar disponibilidade: ", e)
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
            print(f"[LOG ERRO] Erro ao consultar dados: {e}")
            return None
        finally:
            cursor.close()

    def get_all(self) -> Union[list]:
        try:
            cursor = self.get_cursor()
            cursor.execute("SELECT * FROM Produto;")
            resultados = cursor.fetchall()
            return resultados
        except Exception:
            return []
        finally:
            cursor.close()
