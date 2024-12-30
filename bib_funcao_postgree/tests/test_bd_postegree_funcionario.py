import unittest
from unittest.mock import patch, MagicMock
from src.funcao_postgree.bd_postgree_funcionario import BdFuncionario

class TestBdFuncionario(unittest.TestCase):

    @patch("src.funcao_postgree.bd_postgree_funcionario.BdFuncionario.get_cursor")
    @patch("src.funcao_postgree.bd_postgree_funcionario.BdFuncionario.commit")
    def test_database_init(self, mock_commit, mock_get_cursor):
        mock_cursor = MagicMock()
        mock_get_cursor.return_value = mock_cursor

        bd_funcionario = BdFuncionario.__new__(BdFuncionario)
        bd_funcionario.database_init()

        mock_get_cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with("""
                CREATE TABLE IF NOT EXISTS funcionario (
                    id SERIAL PRIMARY KEY,
                    usuario VARCHAR(255) UNIQUE,
                    senha VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL
                );
            """)
        mock_commit.assert_called_once()
        mock_cursor.close.assert_called_once()

if __name__ == "__main__":
    unittest.main()
