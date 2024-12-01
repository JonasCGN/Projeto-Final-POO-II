"""
Este módulo contém testes para a classe DB_Redis, utilizando a biblioteca unittest.

Os testes verificam:
- Conexão bem-sucedida ao banco de dados Redis.
- Tratamento de falhas na conexão com o Redis.

Mocks são utilizados para simular o comportamento da classe Redis e garantir testes isolados.
"""
import unittest
import redis
import sys
import os
from unittest.mock import patch, MagicMock
from script_redis.src.bd import DB_Redis

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))


class TestDBRedis(unittest.TestCase):
    """
    Classe de testes para a classe DB_Redis.

    Atributos:
        Nenhum.

    Métodos:
        test_connection_success: Testa a conexão bem-sucedida com o Redis.
        test_connection_fail: Testa a falha na conexão com o Redis.

    """

    @patch('src.bd.redis.Redis')
    def test_connection_success(self, mock_redis):
        """
        Testa a conexão bem-sucedida com o Redis.

        Parâmetros:
            mock_redis (MagicMock): Mock da classe Redis.
        
        Retorna:
            mensagem de sucesso ao conectar ao Redis.
        
        """
        mock_instance = MagicMock()
        mock_redis.return_value = mock_instance

        db_redis = DB_Redis()

        with patch('builtins.print') as mocked_print:
            db_redis.test_connection()

        mocked_print.assert_called_with(
            "Conexão com o Redis estabelecida com sucesso!")

    @patch('src.bd.redis.Redis')
    def test_connection_fail(self, mock_redis):

        """
        Testa a falha na conexão com o Redis.

        Parâmetros:
            mock_redis (MagicMock): Mock da classe Redis.
        
        Retorna:
            mensagem de falha ao conectar ao Redis.
            
        
        """
        mock_instance = MagicMock()
        mock_instance.ping.side_effect = redis.ConnectionError
        mock_redis.return_value = mock_instance

        db_redis = DB_Redis()

        with patch('builtins.print') as mocked_print:
            db_redis.test_connection()

        mocked_print.assert_called_with("Não foi possível conectar ao Redis.")
