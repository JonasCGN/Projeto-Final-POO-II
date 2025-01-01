import unittest
from src.email_functions.email_def_body import criar_corpo_email_recupercao_de_conta_html

class TestCriarCorpoEmailRecupercaoDeContaHtml(unittest.TestCase):

  def test_email_body_contains_username(self):
    usuario = "test_user"
    senha = "test_password"
    result = criar_corpo_email_recupercao_de_conta_html(usuario, senha)
    self.assertIn(f"<strong>{usuario}</strong>", result)

  def test_email_body_contains_password(self):
    usuario = "test_user"
    senha = "test_password"
    result = criar_corpo_email_recupercao_de_conta_html(usuario, senha)
    self.assertIn(f"<strong>{senha}</strong>", result)

  def test_email_body_structure(self):
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