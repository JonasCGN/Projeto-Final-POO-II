import pytest
from unittest.mock import Mock, patch, MagicMock, call
from socket import AF_INET, SOCK_STREAM
from src.servidor import Servidor,User, HOST, PORT, NMR_CLIENTES

class TestServidor:
    @pytest.fixture
    def servidor(self):
        server = Servidor()
        server.init()
        return server
    
    def test_init(self, servidor: Servidor):
        assert servidor.addr == (HOST, PORT)
        assert servidor.server_socket.family == AF_INET
        assert servidor.server_socket.type == SOCK_STREAM

    def test_is_suport_connect(self, servidor: Servidor):
        servidor._clientes = {str(i): Mock() for i in range(NMR_CLIENTES)}
        assert not servidor.is_suport_connect()
        del servidor._clientes[str(NMR_CLIENTES-1)]
        assert servidor.is_suport_connect()
        
    def test_add_clientes(self, servidor: Servidor):
        servidor.add_clientes(("127.0.0.1", 12345), Mock(), "test_user")
        assert "test_user" in servidor._clientes
        

    def test_connect_user_full_server(self, servidor: Servidor):
        servidor._clientes = {str(i): Mock() for i in range(NMR_CLIENTES)}
        mock_socket = MagicMock()
        mock_socket.recv.return_value = b'test_user'
        
        with patch('src.servidor.socket.socket.accept', return_value=(mock_socket, ('127.0.0.1', 12345))):
            servidor.connect_user()
            mock_socket.send.assert_called_with(b'disconnected: Servidor cheio!')
            mock_socket.close.assert_called_once()

    def test_connect_user_name_in_use(self, servidor: Servidor):
        servidor._clientes = {"test_user": Mock()}
        
        mock_socket = MagicMock()
        mock_socket.recv.return_value = b'test_user'
        
        with patch('src.servidor.socket.socket.accept', return_value=(mock_socket, ('127.0.0.1', 12345))):
            servidor.connect_user()
            mock_socket.send.assert_called_with(b'disconnected: Nome em uso!')
            mock_socket.close.assert_called_once()

    def test_connect_user_success(self, servidor: Servidor):
        mock_socket = MagicMock()
        mock_socket.recv.return_value = b'test_user'
        with patch('src.servidor.socket.socket.accept', return_value=(mock_socket, ('127.0.0.1', 12345))):
            with patch.object(servidor, 'handle_client', return_value=None) as mock_handle_client:
                servidor.connect_user()
                mock_socket.send.assert_called_with(b'connected: conectado!')
                mock_handle_client.assert_called_once()
                assert "test_user" in servidor._clientes


    def test_handle_client(self, servidor: Servidor):
        cliente_socket = Mock()
        cliente = User(cliente_socket, ("127.0.0.1", 12345), "test_user")
        servidor._clientes["test_user"] = cliente

        with patch("src.servidor.produtos", {1: Mock(nome="Produto1", preco=10.0)}):
            servidor.handle_process(cliente, "QTD_PRODUTOS")
            cliente_socket.send.assert_called_with(b"1")

        with patch("src.servidor.produtos", {1: Mock(nome="Produto1", preco=10.0)}):
            with patch("builtins.print") as mock_print:
                servidor.handle_process(cliente, "test_user")
                mock_print.assert_has_calls(
                    [call("Erro ao decodificar a mensagem do cliente ('127.0.0.1', 12345).")]
                )
                
        with patch("src.servidor.produtos", {1: Mock(nome="Produto1", preco=10.0)}):
            with patch("builtins.print") as mock_print:
                servidor.handle_process(cliente, '{"id": ["1"]}')
                mock_print.assert_has_calls(
                    [call("Produto: Produto1 - R$10.00"), call("Total: R$10.00")]
                )
        