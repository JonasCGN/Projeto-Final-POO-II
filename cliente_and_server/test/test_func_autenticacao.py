import unittest
from unittest.mock import patch, MagicMock
from src.func.func_autenticacao import inserir_funcionario
import json

class TestFuncAutenticacao(unittest.TestCase):

    @patch('src.func.func_autenticacao.bd_funcionario')
    def test_inserir_funcionario_sucesso(self, mock_bd_funcionario):
        mock_bd_funcionario.insert_funcionario.return_value = True
        funcionario = {'usuario': 'test_user', 'senha': 'test_pass', 'email': 'test@example.com'}
        result = inserir_funcionario(funcionario)
        mock_bd_funcionario.insert_funcionario.assert_called_once_with(json.dumps(funcionario))

    @patch('src.func.func_autenticacao.bd_funcionario')
    def test_inserir_funcionario_falha(self, mock_bd_funcionario):
        mock_bd_funcionario.insert_funcionario.return_value = False
        funcionario = {'usuario': 'test_user', 'senha': 'test_pass', 'email': 'test@example.com'}
        result = inserir_funcionario(funcionario)
        mock_bd_funcionario.insert_funcionario.assert_called_once_with(json.dumps(funcionario))
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()