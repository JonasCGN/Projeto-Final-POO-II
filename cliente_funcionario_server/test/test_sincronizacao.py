import unittest
from unittest.mock import patch, MagicMock
from cliente_funcionario_server.src.func.func_sincronizacao import iniciar_cliente_sincronizado, cliente_sincronizado

class TestSincronizacao(unittest.TestCase):

    @patch('src.func.sincronizacao.cliente_sincronizado.iniciar')
    def test_iniciar_cliente_sincronizado(self, mock_iniciar):
        # Mock callback function
        mock_callback = MagicMock()

        # Call the function to be tested
        iniciar_cliente_sincronizado(mock_callback)

        # Assert the iniciar method was called once with the mock callback
        mock_iniciar.assert_called_once_with(mock_callback)

if __name__ == '__main__':
    unittest.main()