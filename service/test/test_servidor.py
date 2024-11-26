import pytest
from unittest.mock import Mock, patch, MagicMock, call
from socket import AF_INET, SOCK_STREAM
from src.servidor import Servidor,User, HOST, PORT, NMR_CLIENTES

class TestServidor:
    """
    Classe de testes para a classe Servidor.
    Verifica a inicialização, conexões, gerenciamento de clientes e o processamento de mensagens no servidor.
    """

    @pytest.fixture
    def servidor(self):
        """
        Fixture para inicializar uma instância da classe Servidor antes de cada teste.
        
        Retorna:
        - Uma instância inicializada da classe Servidor.
        """
        server = Servidor()
        server.init()
        return server

    def test_init(self, servidor: Servidor):
        """
        Testa a inicialização do servidor.

        Verifica:
        - O endereço do servidor.
        - A configuração do socket para IPv4 (AF_INET) e TCP (SOCK_STREAM).
        """
        assert servidor.addr == (HOST, PORT)
        assert servidor.server_socket.family == AF_INET
        assert servidor.server_socket.type == SOCK_STREAM

    def test_is_suport_connect(self, servidor: Servidor):
        """
        Testa o método 'is_suport_connect', que verifica se há espaço para mais conexões no servidor.

        Cenários testados:
        - Servidor cheio (nenhum espaço disponível).
        - Servidor com espaço disponível após a remoção de um cliente.
        """
        servidor._clientes = {str(i): Mock() for i in range(NMR_CLIENTES)}
        assert not servidor.is_suport_connect()
        del servidor._clientes[str(NMR_CLIENTES - 1)]
        assert servidor.is_suport_connect()

    def test_add_clientes(self, servidor: Servidor):
        """
        Testa o método 'add_clientes', que adiciona um novo cliente ao servidor.

        Verifica:
        - Se o cliente é adicionado corretamente à lista de clientes.
        """
        servidor.add_clientes(("127.0.0.1", 12345), Mock(), "test_user")
        assert "test_user" in servidor._clientes

    def test_connect_user_full_server(self, servidor: Servidor):
        """
        Testa a conexão de um usuário quando o servidor está cheio.

        Verifica:
        - Se o cliente recebe uma mensagem informando que o servidor está cheio.
        - Se o socket do cliente é fechado corretamente.
        """
        servidor._clientes = {str(i): Mock() for i in range(NMR_CLIENTES)}
        mock_socket = MagicMock()
        mock_socket.recv.return_value = b'test_user'

        with patch('src.servidor.socket.socket.accept', return_value=(mock_socket, ('127.0.0.1', 12345))):
            servidor.connect_user()
            mock_socket.send.assert_called_with(b'disconnected: Servidor cheio!')
            mock_socket.close.assert_called_once()

    @patch('socket.socket.accept')
    def test_connect_user_name_in_use(self, accept, servidor: Servidor):
        """
        Testa a conexão de um usuário com um nome já em uso.

        Verifica:
        - Se o cliente recebe uma mensagem informando que o nome está em uso.
        - Se o socket do cliente é fechado corretamente.
        """
        servidor._clientes = {"test_user": Mock()}
        
        mock_socket = MagicMock()
        mock_socket.recv.return_value = b'test_user'
        
        accept.return_value = (mock_socket, ('127.0.0.1', 12345))
        
        servidor.connect_user()
        mock_socket.send.assert_called_with(b'disconnected: Nome em uso!')
        mock_socket.close.assert_called_once()

    @patch('src.servidor.socket.socket.accept')
    def test_connect_user_success(self, accept, servidor: Servidor):
        """
        Testa a conexão bem-sucedida de um usuário.

        Verifica:
        - Se o cliente recebe uma mensagem informando que foi conectado com sucesso.
        """
        mock_socket = MagicMock()
        mock_socket.recv.return_value = b'test_user'
        
        accept.return_value = (mock_socket, ('127.0.0.1', 12345))
        
        with patch.object(servidor, 'handle_client', return_value=None):
            servidor.connect_user()
            mock_socket.send.assert_called_with(b'connected: conectado!')

    @patch('src.servidor.produtos', {1: Mock(nome="Produto1", preco=10.0)})
    def test_handle_client(self, servidor: Servidor):
        """
        Testa o processamento de mensagens do cliente pelo servidor.

        Cenários testados:
        - Resposta ao comando 'QTD_PRODUTOS', que retorna a quantidade de produtos disponíveis.
        - Processamento de uma mensagem inválida, com impressão de erro.
        - Processamento de uma mensagem válida para compra de produto.

        Verifica:
        - A resposta correta do servidor ao cliente.
        - As mensagens impressas durante o processamento.
        """
        cliente_socket = Mock()
        cliente = User(cliente_socket, ("127.0.0.1", 12345), "test_user")
        servidor._clientes["test_user"] = cliente

        # Responde à quantidade de produtos disponíveis
        servidor.handle_process(cliente, "QTD_PRODUTOS")
        cliente_socket.send.assert_called_with(b"1")

        # Mensagem inválida
        with patch("builtins.print") as mock_print:
            servidor.handle_process(cliente, "test_user")
            mock_print.assert_has_calls(
                [call("Erro ao decodificar a mensagem do cliente ('127.0.0.1', 12345).")]
            )
            
        # Mensagem válida para compra de produto
        with patch("builtins.print") as mock_print:
            servidor.handle_process(cliente, '{"id": ["1"]}')
            mock_print.assert_has_calls(
                [call("Produto: Produto1 - R$10.00"), call("Total: R$10.00")]
            )

        