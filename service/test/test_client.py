"""
Script: test_cliente.py
Descrição: Este script contém testes unitários para a classe Cliente. Ele utiliza o framework pytest para validar os métodos da classe Cliente, garantindo que interajam corretamente com a conexão TCP e com a entrada do usuário.

Funcionalidades:
- Testa os métodos da classe Cliente: escutar_resposta, enviar_pedido, menu_enviar_pedido, menu, e close_connection.
- Utiliza Mock e Patch para simular as interações com a conexão TCP e entradas do usuário.

Requisitos:
- Python 3.x
- Módulos: pytest, unittest.mock

Como usar:
1. Execute os testes com o comando `pytest` no terminal.
2. Os testes verificarão se os métodos interagem corretamente com a conexão TCP e com o console.
"""

import pytest
from unittest.mock import Mock, patch, call
from src.cliente import Cliente

BUFFER = 1024

class TestCliente:
  """
  Classe de testes para a classe Cliente.

  Atributos:
      Nenhum.
  
  Métodos:
      test_escutar_resposta: Testa o método escutar_resposta.
      test_enviar_pedido: Testa o método enviar_pedido.
      test_menu_enviar_pedido: Testa o método menu_enviar_pedido.
      test_menu_enviar_pedido_sem_produtos: Testa o método menu_enviar_pedido sem produtos.
      test_id_invalido: Testa o método menu_enviar_pedido com id inválido.
      test_menu: Testa o método menu.
      test_close_connection: Testa o método close_connection.
  """
  
  
  @pytest.fixture
  def cliente(self):
    """
    Fixture para instanciar um objeto Cliente com um Mock de socket.
    
    Parâmetros:
        Nenhum.
    
    Retorna:
        Cliente: Um objeto Cliente com um Mock de socket.

    """
    cliente = Cliente("test_user", Mock())
    return cliente

  def test_escutar_resposta(self, cliente):
    """
    Testa o método 'escutar_resposta' da classe Cliente. Este método é
      responsável por ouvir a resposta do servidor via a conexão TCP e realizar
      a leitura dos dados recebidos.

      O teste verifica se a função 'escutar_resposta' interage corretamente
      com o método 'recv' da conexão TCP e se o buffer é passado corretamente
      para a chamada de 'recv'.
    
    """
    cliente.tcp_connection.recv.return_value = b"Teste"
    cliente.escutar_resposta()
    cliente.tcp_connection.recv.assert_called_once_with(BUFFER)

  @pytest.mark.parametrize("data, expected_output", [
      (["1", "1"], b'{"id": ["1", "1"]}'),
      (["2", "2"], b'{"id": ["2", "2"]}')
  ])


  def test_enviar_pedido(self, data, expected_output, cliente):

    """
    Testa o método 'enviar_pedido' da classe Cliente. Este método é responsável por enviar um pedido ao servidor via a conexão TCP.
    O teste verifica se a função 'enviar_pedido' interage corretamente com o método 'send' da conexão TCP e se o pedido é enviado corretamente.

    """
    cliente.enviar_pedido(data)
    cliente.tcp_connection.send.assert_called_with(expected_output)
  
  def test_menu_enviar_pedido(self, cliente):
    """
    Testa o método 'menu_enviar_pedido' da classe Cliente. Este método é responsável por receber os produtos que o cliente deseja adicionar ao pedido e enviar ao servidor.
    O teste verifica:
    - Se a função interage corretamente com o método 'input', simulando a entrada do usuário.
    - Se os dados do pedido são enviados no formato correto.
    - Se as mensagens esperadas são exibidas no console.
    """
    with patch("builtins.input", side_effect=["1", "0"]):
      cliente.tcp_connection.recv.return_value = b"2"
      with patch("builtins.print") as mock_print:
        cliente.menu_enviar_pedido()
        mock_print.assert_has_calls([call('{"id": ["1"]}')])
        
  def test_menu_enviar_pedido_sem_produtos(self, cliente):
    """
      Testa o método 'menu_enviar_pedido' quando nenhum produto é adicionado ao pedido.
        O teste verifica:
    - Se a função detecta corretamente a ausência de produtos na entrada do usuário.
    - Se a mensagem apropriada ("Comanda inválido, reiniciando pedido.") é exibida no console.
    """
    with patch("builtins.input", side_effect=["0"]):
      with patch("builtins.print") as mock_print:
        cliente.menu_enviar_pedido()
        mock_print.assert_has_calls([call('Comanda inválido, reiniciando pedido.')])
    
  def test_id_invalido(self, cliente):
    """
    Testa o método 'menu_enviar_pedido' quando um id inválido é inserido pelo usuário.
    O teste verifica:
    - Se a função detecta corretamente um id inválido na entrada do usuário.
    - Se a mensagem apropriada ("Insira um id válido.") é exibida no console.
    """
    with patch("builtins.input", side_effect=["a", "0"]):
      with patch("builtins.print") as mock_print:
        cliente.menu_enviar_pedido()
        mock_print.assert_has_calls([call("Insira um id válido.")])
  
  def test_menu(self, cliente):
      """
      Testa o método 'menu' da classe Cliente. Este método é responsável por exibir o menu de opções para o cliente.
      O teste verifica:
      - Se as opções do menu são exibidas corretamente.
      - Se a função interage corretamente com o método 'input', simulando a entrada do usuário.
      - Se a função interage corretamente com o método 'close_connection'.
      """
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
    """
    Testa o método 'close_connection' da classe Cliente. Este método é responsável por fechar a conexão com o servidor.
    O teste verifica se a função 'close_connection' interage corretamente com o método 'send' da conexão TCP e se a conexão é fechada corretamente.
    """
    cliente.close_connection()
    cliente.tcp_connection.send.assert_called_once_with(b"test_user, exit")
    cliente.tcp_connection.close.assert_called_once()
