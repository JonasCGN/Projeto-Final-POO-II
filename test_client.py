import pytest
from unittest.mock import Mock, patch, call
from src.cliente import Cliente

BUFFER = 1024

class TestCliente:
  @pytest.fixture
  def cliente(self):
    cliente = Cliente("test_user", Mock())
    return cliente

  def test_escutar_resposta(self, cliente):
    cliente.tcp_connection.recv.return_value = b"Teste"
    cliente.escutar_resposta()
    cliente.tcp_connection.recv.assert_called_once_with(BUFFER)

  @pytest.mark.parametrize("data, expected_output", [
      (["1", "1"], b'{"id": ["1", "1"]}'),
      (["2", "2"], b'{"id": ["2", "2"]}')
  ])
  def test_enviar_pedido(self, data, expected_output, cliente):
    cliente.enviar_pedido(data)
    cliente.tcp_connection.send.assert_called_with(expected_output)
  
  def test_menu_enviar_pedido(self, cliente):
    with patch("builtins.input", side_effect=["1", "0"]):
      cliente.tcp_connection.recv.return_value = b"2"
      with patch("builtins.print") as mock_print:
        cliente.menu_enviar_pedido()
        mock_print.assert_has_calls([call('{"id": ["1"]}')])
        
  def test_menu_enviar_pedido_sem_produtos(self, cliente):
    with patch("builtins.input", side_effect=["0"]):
      with patch("builtins.print") as mock_print:
        cliente.menu_enviar_pedido()
        mock_print.assert_has_calls([call('Comanda inválido, reiniciando pedido.')])
    
  def test_id_invalido(self, cliente):
    with patch("builtins.input", side_effect=["a", "0"]):
      with patch("builtins.print") as mock_print:
        cliente.menu_enviar_pedido()
        mock_print.assert_has_calls([call("Insira um id válido.")])
  
  def test_menu(self, cliente):
      with patch("builtins.input", side_effect=["0"]):  # Simula entrada do usuário
        with patch.object(cliente, "close_connection"):
          with patch("builtins.print") as mock_print:
            cliente.menu()
            mock_print.assert_has_calls([
              call("0 - Sair"),
              call("1 - Enviar pedido"),
              call("2 - Listar produtos"),
            ])
          
    
  def test_close_connection(self, cliente: Cliente):
    cliente.close_connection()
    cliente.tcp_connection.send.assert_called_once_with(b"test_user, exit")
    cliente.tcp_connection.close.assert_called_once()
