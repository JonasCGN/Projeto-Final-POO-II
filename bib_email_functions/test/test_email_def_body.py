import unittest
from src.email_functions.email_def_body import criar_corpo_email_recupercao_de_conta_html

class TestCriarCorpoEmailRecupercaoDeContaHtml(unittest.TestCase):
    """
    Classe de teste para a função criar_corpo_email_recupercao_de_conta_html.

    Essa classe contém métodos para verificar se o corpo do e-mail de recuperação de conta
    está correto, incluindo a presença do nome de usuário, senha e estrutura HTML esperada.
    """

    def test_email_body_contains_username(self):
        """
        Verifica se o corpo do e-mail contém o nome de usuário formatado corretamente.
        """
        usuario = "test_user"
        senha = "test_password"
        result = criar_corpo_email_recupercao_de_conta_html(usuario, senha)
        self.assertIn(f"<strong>{usuario}</strong>", result)

    def test_email_body_contains_password(self):
        """
        Verifica se o corpo do e-mail contém a senha formatada corretamente.
        """
        usuario = "test_user"
        senha = "test_password"
        result = criar_corpo_email_recupercao_de_conta_html(usuario, senha)
        self.assertIn(f"<strong>{senha}</strong>", result)

    def test_email_body_structure(self):
        """
        Verifica se o corpo do e-mail possui a estrutura HTML esperada.
        """
        usuario = "test_user"
        senha = "test_password"
        result = criar_corpo_email_recupercao_de_conta_html(usuario, senha)
        self.assertIn("<html>", result)
        self.assertIn("<head>", result)
        self.assertIn("<style>", result)
        self.assertIn("<body>", result)
        self.assertIn('<div class="container">', result)
        self.assertIn('<div class="header">', result)
        self.assertIn('<div class="content">', result)
        self.assertIn('<div class="footer">', result)
        self.assertIn("</html>", result)

if __name__ == '__main__':
    unittest.main()
