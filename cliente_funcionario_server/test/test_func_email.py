import unittest
from unittest.mock import patch, MagicMock
from src.func.func_email import enviar_email_recuperacao_de_conta

class TestFuncEmail(unittest.TestCase):
    """
    Classe de testes para validar a funcionalidade de envio de email de recuperação de conta.
    """

    @patch('src.func.func_email.email_sender')
    @patch('src.func.func_email.criar_corpo_email_recupercao_de_conta_html')
    def test_enviar_email_recuperacao_de_conta_sucesso(self, mock_criar_corpo_email, mock_email_sender):
        """
        Testa o envio de um email de recuperação de conta com sucesso.

        Simula o comportamento de:
        - Geração do corpo do email (`criar_corpo_email_recupercao_de_conta_html`) retornando uma string de exemplo.
        - Serviço de envio de email (`email_sender.send_email`) confirmando o envio com sucesso.

        Valida:
        - Se o corpo do email foi gerado corretamente com os parâmetros fornecidos.
        - Se a função `send_email` foi chamada com os argumentos esperados.
        """
        # Configurações dos mocks
        mock_criar_corpo_email.return_value = "corpo_email_mock"
        mock_email_sender.send_email.return_value = True

        # Dados de entrada para o teste
        email = 'test@example.com'
        usuario = 'test_user'
        senha = 'test_pass'
        
        # Chamada da função a ser testada
        enviar_email_recuperacao_de_conta(email, usuario, senha)
        
        # Validações
        mock_criar_corpo_email.assert_called_once_with(usuario, senha)
        mock_email_sender.send_email.assert_called_once_with('Recuperação de Conta', "corpo_email_mock", email)



if __name__ == '__main__':
  unittest.main()