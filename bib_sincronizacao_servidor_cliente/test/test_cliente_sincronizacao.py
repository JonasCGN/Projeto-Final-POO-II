import unittest
from unittest.mock import patch, Mock, call
from src.sincronizacao_servidor_cliente.cliente_sincronizacao import ClienteSincronizado, ErroCliente

class TestClienteSincronizado(unittest.TestCase):
    """
    Classe de testes unitários para a classe ClienteSincronizado.

    Essa classe utiliza a biblioteca unittest para validar os comportamentos 
    da classe ClienteSincronizado, simulando conexões de rede com o auxílio 
    de mocks para evitar dependências externas.
    """

    @patch('socket.socket')
    def setUp(self, mock_socket):
        """
        Configura o ambiente de teste antes de cada caso de teste.

        Args:
            mock_socket (MagicMock): Mock para a classe socket.
        """
        self.mock_socket_instance = mock_socket.return_value  # Instância mock do socket
        self.cliente = ClienteSincronizado()  # Instância do cliente a ser testada

    def test_iniciar_ja_conectado(self):
        """
        Testa a tentativa de iniciar o cliente quando ele já está conectado.

        Verifica se a exceção ErroCliente é lançada ao tentar iniciar o cliente 
        novamente enquanto ele já está executando.
        """
        self.cliente.executando = True  # Simula que o cliente já está ativo
        with self.assertRaises(ErroCliente):
            self.cliente.iniciar(Mock())  # Deve lançar a exceção

    def test_escutar_conexao_perdida(self):
        """
        Testa o comportamento do cliente ao perder a conexão com o servidor.

        Simula um ConnectionResetError durante a escuta e verifica se o cliente 
        encerra a execução corretamente.
        """
        mock_callback = Mock()  # Mock para o callback
        self.cliente.soket_cliente = self.mock_socket_instance  # Configura o socket do cliente
        self.mock_socket_instance.recv.side_effect = ConnectionResetError  # Simula erro de conexão

        self.cliente._escutar(mock_callback)  # Chama o método privado _escutar
        self.assertFalse(self.cliente.executando)  # Verifica se o cliente foi encerrado

    def test_enviar_mensagem_sucesso(self):
        """
        Testa o envio bem-sucedido de uma mensagem para o servidor.

        Verifica se o método `sendall` do socket é chamado corretamente com os 
        dados esperados.
        """
        self.cliente.executando = True  # Simula que o cliente está ativo
        self.cliente.soket_cliente = self.mock_socket_instance  # Configura o socket do cliente
        self.cliente.enviar_mensagem("mensagem")  # Envia uma mensagem
        self.mock_socket_instance.sendall.assert_called_with(b"mensagem")  # Verifica a chamada

    def test_enviar_mensagem_nao_conectado(self):
        """
        Testa o envio de mensagem quando o cliente não está conectado.

        Verifica se a exceção ErroCliente é lançada corretamente.
        """
        with self.assertRaises(ErroCliente):
            self.cliente.enviar_mensagem("mensagem")  # Deve lançar a exceção

    def test_parar(self):
        """
        Testa o encerramento da conexão com o servidor.

        Verifica se o método `close` do socket é chamado corretamente e se a 
        execução do cliente é encerrada.
        """
        self.cliente.soket_cliente = self.mock_socket_instance  # Configura o socket do cliente
        self.cliente.executando = True  # Simula que o cliente está ativo
        self.cliente.parar()  # Encerra o cliente
        self.assertFalse(self.cliente.executando)  # Verifica se o cliente foi encerrado
        self.mock_socket_instance.close.assert_called_once()  # Verifica se o socket foi fechado

    def test_parar_sem_conexao(self):
        """
        Testa o encerramento da execução quando não há conexão ativa.

        Verifica se o cliente é encerrado sem erros mesmo sem um socket configurado.
        """
        self.cliente.soket_cliente = None  # Remove o socket do cliente
        self.cliente.executando = True  # Simula que o cliente está ativo
        self.cliente.parar()  # Encerra o cliente
        self.assertFalse(self.cliente.executando)  # Verifica se o cliente foi encerrado

    @patch('socket.socket')
    def test_iniciar_falha_conexao(self, mock_socket):
        """
        Testa o comportamento ao tentar iniciar o cliente com uma falha de conexão.

        Verifica se a exceção ErroCliente é lançada e se o estado do cliente 
        permanece consistente após o erro.
        """
        mock_socket_instance = mock_socket.return_value  # Mock para o socket
        mock_socket_instance.connect.side_effect = Exception("Erro de conexão")  # Simula erro de conexão
        mock_callback = Mock()  # Mock para o callback

        with self.assertRaises(ErroCliente):
            self.cliente.iniciar(mock_callback)  # Deve lançar a exceção

        self.assertFalse(self.cliente.executando)  # Verifica se o cliente não está ativo
        mock_socket_instance.connect.assert_called_with(('localhost', 12345))  # Verifica o endereço de conexão

    @patch('socket.socket')
    def test_iniciar_falha_thread(self, mock_socket):
        """
        Testa o comportamento ao tentar iniciar o cliente com uma falha na thread de escuta.

        Verifica se a exceção ErroCliente é lançada e se o estado do cliente 
        permanece consistente após o erro.
        """
        mock_socket_instance = mock_socket.return_value  # Mock para o socket
        mock_socket_instance.connect.return_value = None  # Simula conexão bem-sucedida
        mock_callback = Mock()  # Mock para o callback

        with patch('threading.Thread', side_effect=Exception("Erro de thread")):
            with self.assertRaises(ErroCliente):
                self.cliente.iniciar(mock_callback)  # Deve lançar a exceção

            self.assertFalse(self.cliente.executando)  # Verifica se o cliente não está ativo
            mock_socket_instance.connect.assert_called_with(('localhost', 12345))  # Verifica o endereço de conexão


if __name__ == '__main__':
    unittest.main()
