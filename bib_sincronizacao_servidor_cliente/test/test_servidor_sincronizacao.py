import unittest
from unittest.mock import patch, MagicMock
from src.sincronizacao_servidor_cliente.servidor_sincronizacao import ServidorSincronizacao, ErroServidor

class TestServidorSincronizacao(unittest.TestCase):

    @patch('src.sincronizacao_servidor_cliente.servidor_sincronizacao.socket.socket')
    def test_iniciar_servidor(self, mock_socket):
        servidor = ServidorSincronizacao()
        mock_callback = MagicMock()
        
        servidor.iniciar(mock_callback)
        
        self.assertTrue(servidor.executando)
        mock_socket.return_value.bind.assert_called_with(('localhost',12345))
        mock_socket.return_value.listen.assert_called_once()

    def test_iniciar_servidor_ja_em_execucao(self):
        servidor = ServidorSincronizacao()
        servidor.executando = True
        mock_callback = MagicMock()
        
        with self.assertRaises(ErroServidor):
            servidor.iniciar(mock_callback)

    @patch('src.sincronizacao_servidor_cliente.servidor_sincronizacao.socket.socket')
    def test_parar_servidor(self, mock_socket):
        servidor = ServidorSincronizacao()
        servidor.servidor_socket = mock_socket.return_value
        servidor.executando = True
        
        servidor.parar()
        
        self.assertFalse(servidor.executando)
        mock_socket.return_value.close.assert_called_once()


    @patch('src.sincronizacao_servidor_cliente.servidor_sincronizacao.socket.socket')
    def test_enviar_msg_para_todos_clientes(self, mock_socket):
        servidor = ServidorSincronizacao()
        mock_socket_instance = MagicMock()
        servidor.sockets_enderecos_clientes = [(mock_socket_instance, ('127.0.0.1', 12345))]
        
        servidor.enviar_msg_para_todos_clientes("Test message")
        
        mock_socket_instance.sendall.assert_called_with(b"Test message")

    @patch('src.sincronizacao_servidor_cliente.servidor_sincronizacao.socket.socket')
    def test_remover_cliente(self, mock_socket):
        servidor = ServidorSincronizacao()
        mock_socket_instance = MagicMock()
        servidor.sockets_enderecos_clientes = [(mock_socket_instance, ('127.0.0.1', 12345))]
        
        servidor.remover_cliente(('127.0.0.1', 12345))
        
        self.assertEqual(len(servidor.sockets_enderecos_clientes), 0)
        mock_socket_instance.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()