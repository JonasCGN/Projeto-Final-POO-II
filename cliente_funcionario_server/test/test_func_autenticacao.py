import unittest
from unittest.mock import patch, MagicMock
from src.func.func_autenticacao import inserir_funcionario
import json

class TestFuncAutenticacao(unittest.TestCase):
    """
    Classe de testes para validar a funcionalidade de inserção de funcionários.
    """

    @patch('src.func.func_autenticacao.bd_funcionario')
    def test_inserir_funcionario_sucesso(self, mock_bd_funcionario):
        """
        Testa a inserção de um funcionário com sucesso.

        Simula a interação com o banco de dados, onde o retorno da inserção é True.
        Verifica se a função chama corretamente o método `insert_funcionario` 
        com os dados esperados.
        """
        mock_bd_funcionario.insert_funcionario.return_value = True
        funcionario = {'usuario': 'test_user', 'senha': 'test_pass', 'email': 'test@example.com'}
        result = inserir_funcionario(funcionario)
        mock_bd_funcionario.insert_funcionario.assert_called_once_with(json.dumps(funcionario))
        self.assertTrue(result)

    @patch('src.func.func_autenticacao.bd_funcionario')
    def test_inserir_funcionario_falha(self, mock_bd_funcionario):
        """
        Testa a falha ao tentar inserir um funcionário.

        Simula a interação com o banco de dados, onde o retorno da inserção é False.
        Verifica se a função chama corretamente o método `insert_funcionario` 
        com os dados esperados e retorna False.
        """
        mock_bd_funcionario.insert_funcionario.return_value = False
        funcionario = {'usuario': 'test_user', 'senha': 'test_pass', 'email': 'test@example.com'}
        result = inserir_funcionario(funcionario)
        mock_bd_funcionario.insert_funcionario.assert_called_once_with(json.dumps(funcionario))
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()