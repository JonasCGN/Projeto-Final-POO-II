"""
Módulo com a classe para manipulação de dados da tabela Produto no banco de dados PostgreSQL.
"""

from .bd_postgree_base import Bd_Base
from typing import Union
import json

class BdProduto(Bd_Base):
    """
    Classe para manipulação de dados da tabela Produto no banco de dados PostgreSQL.
    """
    

    def __init__(self) -> None:
        """
        Inicializa a conexão com o banco de dados, e cria a tabela Produto caso não exista.
        """
        super().__init__()
        self.database_init()

    def database_init(self) -> None:
        """
        Inicia a estrutura do banco de dados, criando a tabela Produto caso não exista.
        """
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
        """
        Formata os dados para inserção no banco de dados.
        
        Args:
            produto (str): Dados do produto em formato JSON.
        
        Returns:
            dict: Dicionário com os dados formatados.
        """
        valor =  json.loads(produto)
        return (valor['nome'], valor["preco"], valor["disponivel"])

    def insert_produto(self, produto: str) -> bool:
        """
        Insere um produto no banco de dados.
        
        Args:
            produto (str): Dados do produto em formato JSON.
            
        returns:
            bool: True se a inserção foi bem sucedida, False caso contrário.
        """
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
        """
        Atualiza um produto no banco de dados.
        
        Args:
            produto (str): Dados do produto em formato JSON.
            id_produto (int): ID do produto a ser atualizado.
        
        Returns:
            bool: True se a atualização foi bem sucedida, False caso contrário.
        """
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
        """
        Remove um produto do banco de dados.
        
        Args:
            id_produto (int): ID do produto a ser removido.
            
        Returns:
            bool: True se a remoção foi bem sucedida, False caso contrário.
        """
        
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
        """
        Troca a disponibilidade de um produto no banco de dados.
        
        Args:
            id_produto (int): ID do produto a ter a disponibilidade trocada.
        
        Returns:
            bool: True se a troca foi bem sucedida, False caso contrário.
        """
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
        """
        Consulta um produto no banco de dados.
        
        Args:
            id (int): ID do produto a ser consultado.
            
        Returns:
            Union[tuple, None]: Tupla com os dados do produto, ou None caso não seja encontrado.
        """
        
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
        """
        Consulta todos os produtos no banco de dados.
        
        Returns:
            list: Lista com os dados dos produtos.
        """
        try:
            cursor = self.get_cursor()
            cursor.execute("SELECT * FROM Produto ORDER BY id ASC;")
            resultados = cursor.fetchall()
            return resultados
        except Exception:
            return []
        finally:
            cursor.close()
