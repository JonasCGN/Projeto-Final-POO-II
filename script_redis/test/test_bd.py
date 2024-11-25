import unittest
from unittest.mock import patch, MagicMock

import redis

import sys
import os

# Adicione o diretório do pacote ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from script_redis.src.bd import DB_Redis


class TestDBRedis(unittest.TestCase):

    @patch('src.bd.redis.Redis')
    def test_connection_success(self, mock_redis):
        mock_instance = MagicMock()
        mock_redis.return_value = mock_instance

        db_redis = DB_Redis()

        with patch('builtins.print') as mocked_print:
            db_redis.test_connection()

        mocked_print.assert_called_with(
            "Conexão com o Redis estabelecida com sucesso!")

    @patch('src.bd.redis.Redis')
    def test_connection_fail(self, mock_redis):
        mock_instance = MagicMock()
        mock_instance.ping.side_effect = redis.ConnectionError
        mock_redis.return_value = mock_instance

        db_redis = DB_Redis()

        with patch('builtins.print') as mocked_print:
            db_redis.test_connection()

        mocked_print.assert_called_with("Não foi possível conectar ao Redis.")
