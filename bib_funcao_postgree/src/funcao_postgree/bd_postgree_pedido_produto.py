"""
Modulo responsável por realizar a comunicação com o banco de dados dos pedidos e produtos.
"""

from .bd_postgree_base import Bd_Base
from typing import Union, List, Dict
from datetime import datetime


class BdPedidoProduto(Bd_Base):
    """
    Classe para manipulação de dados da tabela Produto_Pedido no banco de dados PostgreSQL.
    """

    def __init__(self, host: str = 'localhost', database: str = 'database-postgres', user: str = 'root', password: str = 'root') -> None:
        """
        Inicializa a conexão com o banco de dados, e cria a tabela Produto_Pedido caso não exista.
        """
        super().__init__(host, database, user, password)
        self.database_init()

    def database_init(self) -> None:
        """
        Inicia a estrutura do banco de dados, criando a tabela Produto_Pedido caso não exista.
        """
        try:
            cursor = self.get_cursor()

            print("[LOG INFO] Criando tabela Produto_Pedido...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Produto_Pedido (
                    id SERIAL PRIMARY KEY,
                    pedido_id INT NOT NULL,
                    produto_id INT NOT NULL,
                    quantidade INT NOT NULL,
                    preco_pago DECIMAL(10, 2) NOT NULL,
                    FOREIGN KEY (pedido_id) REFERENCES Pedido (id) ON DELETE CASCADE,
                    FOREIGN KEY (produto_id) REFERENCES Produto (id) ON DELETE CASCADE
                );
            """)

            self.commit()
            print("[LOG INFO] Estrutura do banco inicializada com sucesso!")
        except Exception as e:
            print(f"[LOG ERRO] Não foi possível inicializar o banco: {e}")
        finally:
            cursor.close()

    def inserir_pedido_com_produtos(self, produtos: List[Dict[int, float]], mesa: int, status: str) -> bool:
        """
        Insere um pedido e seus produtos no banco de dados.
        
        Args:
            produtos (List[Dict[int, float]]): Lista de produtos a serem inseridos no pedido,
            Cada produto é um dicionário com as chaves 'produto_id', 'quantidade' e 'preco_pago'.
            mesa (int): Número da mesa do pedido.
            status (str): Status do pedido.
            
        Returns:
            bool: True se a inserção foi bem sucedida, False caso contrário.
        """
        try:
            cursor = self.get_cursor()
            data_hora = datetime.now()

            print(f"[LOG INFO] Inserindo pedido com data/hora: {data_hora}")
            cursor.execute("""
                INSERT INTO Pedido (mesa, status, data_hora)
                VALUES (%s, %s, %s) RETURNING id;
                """, (mesa, status, data_hora)
            )
            
            pedido_id = cursor.fetchone()[0]
            print(f"[LOG INFO] Pedido inserido com ID: {pedido_id}")

            for produto in produtos:
                cursor.execute("""
                    INSERT INTO Produto_Pedido (pedido_id, produto_id, quantidade, preco_pago)
                    VALUES (%s, %s, %s, %s);
                """, (pedido_id, produto['produto_id'], produto['quantidade'], produto['preco_pago']))

            self.commit()
            print("[LOG INFO] Pedido e produtos inseridos com sucesso!")
            return True
        except Exception as e:
            print(f"[LOG ERRO] Erro ao inserir pedido e produtos: {e}")
            self.rollback()
            return False
        finally:
            cursor.close()

    def get_produtos_do_pedido(self, id_pedido: int) -> List[Dict[str, int | float]] | None:
        """
        Busca os produtos de um pedido no banco de dados.
        
        Args:
            id_pedido (int): ID do pedido.
        
        Returns:
            List[Dict[str, int | float]] | None: Lista de produtos do pedido, ou None em caso de erro.
            A lista contém dicionários com as chaves 'produto_id', 'nome', 'quantidade' e 'preco_pago'.
        """
        try:
            cursor = self.get_cursor()
            cursor.execute("""
                SELECT Produto_Pedido.produto_id, Produto.nome, Produto_Pedido.quantidade, Produto_Pedido.preco_pago
                FROM Produto_Pedido
                JOIN Produto ON Produto_Pedido.produto_id = Produto.id
                WHERE Produto_Pedido.pedido_id = %s;
            """, (id_pedido,))

            produtos = cursor.fetchall()
            produtos = [
                {
                    'produto_id': produto[0],
                    'nome': produto[1],
                    'quantidade': produto[2],
                    'preco_pago': produto[3]
                }
                for produto in produtos
            ]

            return produtos
        except Exception as e:
            print(f"[LOG ERRO] Erro ao buscar produtos do pedido: {e}")
            return None
        finally:
            cursor.close()