import unittest
from unittest.mock import patch, MagicMock
from cliente_funcionario_server.src.func.func_sincronizacao import iniciar_cliente_sincronizado, cliente_sincronizado

class TestSincronizacao(unittest.TestCase):
    """
    Classe de testes para validar a funcionalidade de inicialização do cliente sincronizado.
    """

    @patch('src.func.sincronizacao.cliente_sincronizado.iniciar')
    def test_iniciar_cliente_sincronizado(self, mock_iniciar):
        """
        Verifica se o método `iniciar` do cliente sincronizado é chamado corretamente.

        Cenário:
        - A função `iniciar_cliente_sincronizado` é chamada com um callback mockado.

        Valida:
        - Se o método `iniciar` foi chamado uma vez.
        - Se o callback fornecido foi passado corretamente ao método `iniciar`.

        Dependências Mockadas:
        - `cliente_sincronizado.iniciar`: Método responsável por inicializar a sincronização do cliente.
        """
        # Mock callback function
        mock_callback = MagicMock()

        # Chama a função a ser testada
        iniciar_cliente_sincronizado(mock_callback)

        # Verifica se o método iniciar foi chamado uma vez com o callback mockado
        mock_iniciar.assert_called_once_with(mock_callback)
if __name__ == '__main__':
    unittest.main()