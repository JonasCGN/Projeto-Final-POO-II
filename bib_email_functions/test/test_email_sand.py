import unittest
from unittest.mock import patch, MagicMock
from src.email_functions.email_sand import EmailSender

class TestEmailSender(unittest.TestCase):
    """
    Classe de teste para a classe EmailSender.

    Esta classe contém testes para verificar o comportamento das funcionalidades principais
    da classe EmailSender, incluindo o envio de e-mails e a finalização da conexão com o servidor SMTP.
    """

    @patch('smtplib.SMTP')
    def setUp(self, MockSMTP):
        """
        Configuração inicial para os testes.

        Substitui o objeto smtplib.SMTP por um mock para evitar conexões reais durante os testes.

        Args:
            MockSMTP (Mock): Mock do objeto smtplib.SMTP.
        """
        self.mock_smtp = MockSMTP.return_value
        self.email_sender = EmailSender(email='test@example.com', password='password')

    def test_quit(self):
        """
        Testa se o método quit() da classe EmailSender chama o método quit() do servidor SMTP corretamente.
        """
        self.email_sender.quit()
        self.mock_smtp.quit.assert_called_once()

    def test_send_email(self):
        """
        Testa se o método send_email() envia corretamente um e-mail com os parâmetros fornecidos.

        Verifica:
        - Se o método send_message() do servidor SMTP foi chamado uma vez.
        - Se o remetente, destinatário, assunto e corpo do e-mail estão corretos.
        """
        subject = "Test Subject"
        body = "<h1>Test Body</h1>"
        to = "recipient@example.com"

        self.email_sender.send_email(subject, body, to)

        self.mock_smtp.send_message.assert_called_once()
        sent_msg = self.mock_smtp.send_message.call_args[0][0]
        self.assertEqual(sent_msg['From'], 'test@example.com')
        self.assertEqual(sent_msg['To'], to)
        self.assertEqual(sent_msg['Subject'], subject)
        self.assertEqual(sent_msg.get_payload()[0].get_payload(), body)

if __name__ == '__main__':
    unittest.main()
