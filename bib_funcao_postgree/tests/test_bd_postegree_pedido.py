import unittest
from unittest.mock import patch, MagicMock
from src.funcao_postgree.bd_postgree_pedido import BdPedido

class TestBdPedido(unittest.TestCase):

    @patch("src.funcao_postgree.bd_postgree_pedido.BdPedido.get_cursor")
    @patch("src.funcao_postgree.bd_postgree_pedido.BdPedido.commit")
    def test_database_init(self, mock_commit, mock_get_cursor):
        mock_cursor = MagicMock()
        mock_get_cursor.return_value = mock_cursor

        bd_funcionario = BdPedido.__new__(BdPedido)
        bd_funcionario.database_init()

        mock_get_cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with("""
                CREATE TABLE IF NOT EXISTS Pedido (
                    id SERIAL PRIMARY KEY,
                    mesa INT NOT NULL,
                    status VARCHAR(255) NOT NULL,
                    data_hora TIMESTAMP NOT NULL
                );
            """)
        mock_commit.assert_called_once()
        mock_cursor.close.assert_called_once()

if __name__ == "__main__":
    unittest.main()
