"""
Modulo responsável por realizar a comunicação com o banco de dados dos pedidos.
"""

from .bd_postgree_base import Bd_Base
from typing import Union
import json


class BdPedido(Bd_Base):
    """
    Classe para manipulação de dados da tabela Pedido no banco de dados PostgreSQL
    """

    def __init__(self) -> None:
        """
        Inicializa a conexão com o banco de dados, e cria a tabela Pedido caso não exista.
        """
        super().__init__()
        self.database_init()

    def database_init(self) -> None:
        """
        Inicia a estrutura do banco de dados, criando a tabela Pedido caso não exista.
        """

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
    
    def editar_status(self, status: str, id_pedido: int) -> bool:
        """
        Edita o status de um pedido no banco de dados.
        
        Args:
            status (str): Novo status do pedido.
            id_pedido (int): ID do pedido a ser editado.
            
        Returns:
            bool: True se a edição foi bem sucedida, False caso contrário.
        """
        retorno = True
        try:
            query = """
                UPDATE Pedido 
                SET status = %s
                WHERE id = %s
            """
            cursor = self.get_cursor()
            cursor.execute(query, (status, id_pedido))
            self.commit()
        except Exception as e:
            print("[LOG ERRO] Erro ao editar status do pedido: ", e)
            self.post_client.rollback()
            retorno = False
        finally:
            cursor.close()

        return retorno
    
    def _format_from_inserct(self, pedido: str) -> dict:
        """
        Formata os dados para inserção no banco de dados.
        
        Args:
            pedido (str): Dados do pedido em formato JSON.
        
        Returns:
            dict: Dicionário com os dados formatados.
        """
        valor =  json.loads(pedido)
        return (valor['mesa'], valor["status"], valor["data_hora"])

    def insert_pedido(self, pedido: str) -> bool:
        """
        Insere um pedido no banco de dados.
        
        Args:
            pedido (str): Dados do pedido em formato JSON.
            
        returns:
            bool: True se a inserção foi bem sucedida, False caso contrário.
        """
        
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
        """
        Retorna os 1000 últimos pedidos do banco de dados.
        
        Returns:
            Union[list, None]: Lista com os pedidos, ou None em caso de erro.
        """
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
        """
        Retorna todos os pedidos do banco de dados.
        
        Returns:
            Union[list, None]: Lista com os pedidos, ou None em caso de erro.
        """
        try:
            cursor = self.get_cursor()
            cursor.execute("SELECT * FROM Pedido;")
            resultados = cursor.fetchall()
            return resultados
        except Exception:
            return None
        finally:
            cursor.close()
