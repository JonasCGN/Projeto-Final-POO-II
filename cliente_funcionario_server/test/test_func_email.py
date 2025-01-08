import unittest
from unittest.mock import patch, MagicMock
from src.func.func_email import enviar_email_recuperacao_de_conta

class TestFuncEmail(unittest.TestCase):

  @patch('src.func.func_email.email_sender')
  @patch('src.func.func_email.criar_corpo_email_recupercao_de_conta_html')
  def test_enviar_email_recuperacao_de_conta_sucesso(self, mock_criar_corpo_email, mock_email_sender):
    mock_criar_corpo_email.return_value = "corpo_email_mock"
    mock_email_sender.send_email.return_value = True

    email = 'test@example.com'
    usuario = 'test_user'
    senha = 'test_pass'
    
    enviar_email_recuperacao_de_conta(email, usuario, senha)
    
    mock_criar_corpo_email.assert_called_once_with(usuario, senha)
    mock_email_sender.send_email.assert_called_once_with('Recuperação de Conta', "corpo_email_mock", email)

if __name__ == '__main__':
  unittest.main()