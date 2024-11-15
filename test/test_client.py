import pytest
from unittest.mock import Mock, patch, call
from src.cliente import Cliente

BUFFER = 1024

class TestCliente:
  @pytest.fixture
  def cliente(self):
    return Cliente()

  def test_escutar_resposta(self, cliente):
    mock_socket = Mock()
    mock_socket.recv.return_value = b"Mensagem do servidor" # Simula resposta do servidor
    
    with patch("socket.socket", return_value=mock_socket):
      cliente.escutar_resposta(mock_socket)
      mock_socket.recv.assert_called_once_with(BUFFER)

  def test_enviar_pedido(self, cliente):
    mock_socket = Mock()
    mock_socket.recv.return_value = b"3"  # Suponha que existem 3 produtos disponíveis

    with patch("socket.socket", return_value=mock_socket):
      with patch("builtins.input", side_effect=["1", "2", "0"]):  # Simula entrada do usuário
        cliente.enviar_pedido(mock_socket)
        mock_socket.send.assert_called_with(b'{"id": ["1", "2"]}')
        
  def test_enviar_pedido_sem_produtos(self, cliente):
    mock_socket = Mock()
    mock_socket.recv.return_value = b"3"  # Suponha que existem 3 produtos disponíveis

    with patch("socket.socket", return_value=mock_socket):
      with patch("builtins.input", side_effect=["0"]):  # Simula entrada do usuário
        cliente.enviar_pedido(mock_socket)
        mock_socket.send.assert_not_called()
    
  def test_id_invalido(self, cliente):
    mock_socket = Mock()
    mock_socket.recv.return_value = b"3"  # Suponha que existem 3 produtos disponíveis

    with patch("socket.socket", return_value=mock_socket):
      with patch("builtins.input", side_effect=["4", "0"]):  # Simula entrada do usuário
        with patch("builtins.print") as mock_print:
          cliente.enviar_pedido(mock_socket)
          mock_print.assert_has_calls([
            call("Insira um id válido."),
            call("Comanda inválido, reiniciando pedido."),
          ])
  
  def test_menu(self, cliente):
    mock_socket = Mock()
    
    with patch("socket.socket", return_value=mock_socket):
      with patch("builtins.input", side_effect=["0"]):  # Simula entrada do usuário
        with patch.object(cliente, "close_connection"):
          with patch("builtins.print") as mock_print:
            cliente.menu()
            mock_print.assert_has_calls([
              call("0 - Sair"),
              call("1 - Enviar pedido"),
              call("2 - Listar produtos"),
            ])
          
    
  def test_close_connection(self, cliente):
    # Mock do socket
    mock_socket = Mock()
    cliente.name = "test_user"

    cliente.close_connection(mock_socket)
    mock_socket.send.assert_called_once_with(b"test_user, exit")
    mock_socket.close.assert_called_once()
