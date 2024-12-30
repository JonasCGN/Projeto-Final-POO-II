import unittest
from unittest.mock import patch, MagicMock
from src.funcao_postgree.bd_postgree_produto import BdProduto

class TestBdProduto(unittest.TestCase):

    @patch("src.funcao_postgree.bd_postgree_produto.BdProduto.get_cursor")
    @patch("src.funcao_postgree.bd_postgree_produto.BdProduto.commit")
    def test_database_init(self, mock_commit, mock_get_cursor):
        mock_cursor = MagicMock()
        mock_get_cursor.return_value = mock_cursor

        bd_funcionario = BdProduto.__new__(BdProduto)
        bd_funcionario.database_init()

        mock_get_cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with("""
                CREATE TABLE IF NOT EXISTS Produto (
                    id SERIAL PRIMARY KEY,
                    nome VARCHAR(255) UNIQUE,
                    preco DECIMAL(10, 2) NOT NULL,
                    disponivel BOOLEAN DEFAULT TRUE
                );
            """)
        mock_commit.assert_called_once()
        mock_cursor.close.assert_called_once()

if __name__ == "__main__":
    unittest.main()
