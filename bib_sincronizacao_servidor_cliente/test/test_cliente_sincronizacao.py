import unittest
from unittest.mock import patch, Mock, call
from src.sincronizacao_servidor_cliente.cliente_sincronizacao import ClienteSincronizado, ErroCliente

class TestClienteSincronizado(unittest.TestCase):

    @patch('socket.socket')
    def setUp(self, mock_socket):
        self.mock_socket_instance = mock_socket.return_value
        self.cliente = ClienteSincronizado()

    def test_iniciar_ja_conectado(self):
        self.cliente.executando = True
        with self.assertRaises(ErroCliente):
            self.cliente.iniciar(Mock())

    def test_escutar_conexao_perdida(self):
        mock_callback = Mock()
        self.cliente.soket_cliente = self.mock_socket_instance
        self.mock_socket_instance.recv.side_effect = ConnectionResetError

        self.cliente._escutar(mock_callback)
        self.assertFalse(self.cliente.executando)

    def test_enviar_mensagem_sucesso(self):
        self.cliente.executando = True
        self.cliente.soket_cliente = self.mock_socket_instance
        self.cliente.enviar_mensagem("mensagem")
        self.mock_socket_instance.sendall.assert_called_with(b"mensagem")

    def test_enviar_mensagem_nao_conectado(self):
        with self.assertRaises(ErroCliente):
            self.cliente.enviar_mensagem("mensagem")

    def test_parar(self):
        self.cliente.soket_cliente = self.mock_socket_instance
        self.cliente.executando = True
        self.cliente.parar()
        self.assertFalse(self.cliente.executando)
        self.mock_socket_instance.close.assert_called_once()

    def test_parar_sem_conexao(self):
        self.cliente.soket_cliente = None
        self.cliente.executando = True
        self.cliente.parar()
        self.assertFalse(self.cliente.executando)
    
    @patch('socket.socket')
    def test_iniciar_falha_conexao(self, mock_socket):
            mock_socket_instance = mock_socket.return_value
            mock_socket_instance.connect.side_effect = Exception("Erro de conexão")
            mock_callback = Mock()

            with self.assertRaises(ErroCliente):
                self.cliente.iniciar(mock_callback)
            
            self.assertFalse(self.cliente.executando)
            mock_socket_instance.connect.assert_called_with(('localhost', 12345))

    @patch('socket.socket')
    def test_iniciar_falha_thread(self, mock_socket):
            mock_socket_instance = mock_socket.return_value
            mock_socket_instance.connect.return_value = None
            mock_callback = Mock()

            with patch('threading.Thread', side_effect=Exception("Erro de thread")):
                with self.assertRaises(ErroCliente):
                    self.cliente.iniciar(mock_callback)
                
                self.assertFalse(self.cliente.executando)
                mock_socket_instance.connect.assert_called_with(('localhost', 12345))
if __name__ == '__main__':
    unittest.main()