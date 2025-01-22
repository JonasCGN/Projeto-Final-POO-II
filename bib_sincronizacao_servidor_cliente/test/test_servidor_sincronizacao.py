import unittest
from unittest.mock import patch, MagicMock
from src.sincronizacao_servidor_cliente.servidor_sincronizacao import ServidorSincronizacao, ErroServidor

class TestServidorSincronizacao(unittest.TestCase):
    """
    Classe de testes unitários para a classe ServidorSincronizacao.

    Essa classe utiliza a biblioteca unittest para validar os comportamentos 
    do servidor de sincronização, simulando conexões e operações com o auxílio 
    de mocks para evitar dependências externas.
    """

    @patch('src.sincronizacao_servidor_cliente.servidor_sincronizacao.socket.socket')
    def test_iniciar_servidor(self, mock_socket):
        """
        Testa o processo de inicialização do servidor.

        Verifica se o servidor:
        - Entra no estado de execução (`executando = True`).
        - Chama os métodos `bind` e `listen` no socket para configurar e iniciar 
          a escuta por conexões.
        
        Args:
            mock_socket (MagicMock): Mock para o objeto socket.
        """
        servidor = ServidorSincronizacao()
        mock_callback = MagicMock()  # Mock para a função de callback

        servidor.iniciar(mock_callback)  # Inicia o servidor

        self.assertTrue(servidor.executando)  # Verifica se o servidor está em execução
        mock_socket.return_value.bind.assert_called_with(('localhost', 12345))  # Verifica o bind no endereço correto
        mock_socket.return_value.listen.assert_called_once()  # Verifica a chamada do método listen

    def test_iniciar_servidor_ja_em_execucao(self):
        """
        Testa a tentativa de iniciar o servidor enquanto ele já está em execução.

        Verifica se a exceção ErroServidor é lançada corretamente nesse cenário.
        """
        servidor = ServidorSincronizacao()
        servidor.executando = True  # Simula que o servidor já está ativo
        mock_callback = MagicMock()  # Mock para a função de callback

        with self.assertRaises(ErroServidor):
            servidor.iniciar(mock_callback)  # Deve lançar a exceção

    @patch('src.sincronizacao_servidor_cliente.servidor_sincronizacao.socket.socket')
    def test_parar_servidor(self, mock_socket):
        """
        Testa o processo de encerramento do servidor.

        Verifica se o servidor:
        - Sai do estado de execução (`executando = False`).
        - Chama o método `close` no socket para fechar a conexão.
        
        Args:
            mock_socket (MagicMock): Mock para o objeto socket.
        """
        servidor = ServidorSincronizacao()
        servidor.servidor_socket = mock_socket.return_value  # Configura o socket do servidor
        servidor.executando = True  # Simula que o servidor está ativo

        servidor.parar()  # Encerra o servidor

        self.assertFalse(servidor.executando)  # Verifica se o servidor foi encerrado
        mock_socket.return_value.close.assert_called_once()  # Verifica se o socket foi fechado

    @patch('src.sincronizacao_servidor_cliente.servidor_sincronizacao.socket.socket')
    def test_enviar_msg_para_todos_clientes(self, mock_socket):
        """
        Testa o envio de uma mensagem para todos os clientes conectados.

        Verifica se o método `sendall` é chamado corretamente para cada cliente.

        Args:
            mock_socket (MagicMock): Mock para o objeto socket.
        """
        servidor = ServidorSincronizacao()
        mock_socket_instance = MagicMock()  # Mock para o socket do cliente
        servidor.sockets_enderecos_clientes = [(mock_socket_instance, ('127.0.0.1', 12345))]  # Simula um cliente conectado

        servidor.enviar_msg_para_todos_clientes("Test message")  # Envia uma mensagem para todos os clientes

        mock_socket_instance.sendall.assert_called_with(b"Test message")  # Verifica a chamada do método sendall

    @patch('src.sincronizacao_servidor_cliente.servidor_sincronizacao.socket.socket')
    def test_remover_cliente(self, mock_socket):
        """
        Testa a remoção de um cliente do servidor.

        Verifica se:
        - O cliente é removido corretamente da lista de clientes conectados.
        - O método `close` é chamado no socket do cliente.

        Args:
            mock_socket (MagicMock): Mock para o objeto socket.
        """
        servidor = ServidorSincronizacao()
        mock_socket_instance = MagicMock()  # Mock para o socket do cliente
        servidor.sockets_enderecos_clientes = [(mock_socket_instance, ('127.0.0.1', 12345))]  # Simula um cliente conectado

        servidor.remover_cliente(('127.0.0.1', 12345))  # Remove o cliente

        self.assertEqual(len(servidor.sockets_enderecos_clientes), 0)  # Verifica se a lista está vazia
        mock_socket_instance.close.assert_called_once()  # Verifica se o socket do cliente foi fechado

if __name__ == '__main__':
    unittest.main()
