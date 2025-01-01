import unittest
from unittest.mock import patch, MagicMock
from src.email_functions.email_sand import EmailSender

class TestEmailSender(unittest.TestCase):

  @patch('smtplib.SMTP')
  def setUp(self, MockSMTP):
    self.mock_smtp = MockSMTP.return_value
    self.email_sender = EmailSender(email='test@example.com', password='password')


  def test_quit(self):
    self.email_sender.quit()
    self.mock_smtp.quit.assert_called_once()

  def test_send_email(self):
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