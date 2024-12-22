from .bd_postgree_base import Bd_Base
from typing import Union, List, Dict
from datetime import datetime


class BdPedidoProduto(Bd_Base):

    def __init__(self) -> None:
        super().__init__()
        self.database_init()

    def database_init(self) -> None:
        try:
            cursor = self.get_cursor()

            print("[LOG INFO] Criando tabela Produto_Pedido...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Produto_Pedido (
                    id SERIAL PRIMARY KEY,
                    pedido_id INT NOT NULL,
                    produto_id INT NOT NULL,
                    quantidade INT NOT NULL,
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

    def inserir_pedido_com_produtos(self, produtos: List[Dict[str, int]]) -> bool:
        try:
            cursor = self.get_cursor()
            data_hora = datetime.now()

            print(f"[LOG INFO] Inserindo pedido com data/hora: {data_hora}")
            cursor.execute("INSERT INTO Pedido (data_hora) VALUES (%s) RETURNING id;", [data_hora])
            pedido_id = cursor.fetchone()[0]
            print(f"[LOG INFO] Pedido inserido com ID: {pedido_id}")

            for produto in produtos:
                print(f"[LOG INFO] Associando produto ID: {produto['produto_id']} com quantidade: {produto['quantidade']} ao pedido ID: {pedido_id}")
                cursor.execute("""
                    INSERT INTO Produto_Pedido (pedido_id, produto_id, quantidade)
                    VALUES (%s, %s, %s);
                """, (pedido_id, produto['produto_id'], produto['quantidade']))

            self.commit()
            print("[LOG INFO] Pedido e produtos inseridos com sucesso!")
            return True
        except Exception as e:
            print(f"[LOG ERRO] Erro ao inserir pedido e produtos: {e}")
            self.rollback()
            return False
        finally:
            cursor.close()

