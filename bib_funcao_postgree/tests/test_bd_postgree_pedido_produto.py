import unittest
from unittest.mock import patch, MagicMock
from src.funcao_postgree.bd_postgree_pedido_produto import BdPedidoProduto

class TestBdFuncionario(unittest.TestCase):
    """
    Testes para a classe BdPedidoProduto
    """

    @patch("src.funcao_postgree.bd_postgree_pedido_produto.BdPedidoProduto.get_cursor")
    @patch("src.funcao_postgree.bd_postgree_pedido_produto.BdPedidoProduto.commit")
    def test_database_init(self, mock_commit, mock_get_cursor):
        """
        Testa o método database_init
        
        Verifica se o método cria a tabela Produto_Pedido
        """
        mock_cursor = MagicMock()
        mock_get_cursor.return_value = mock_cursor

        # Instanciar sem chamar o __init__
        bd_funcionario = BdPedidoProduto.__new__(BdPedidoProduto)
        bd_funcionario.database_init()

        mock_get_cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with("""
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
        mock_commit.assert_called_once()
        mock_cursor.close.assert_called_once()

if __name__ == "__main__":
    unittest.main()
