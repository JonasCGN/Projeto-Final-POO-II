from email.mime.application import MIMEApplication
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailSender:
  def __init__(self, email=None, password=None):
    self.from_email = email
    self.from_password = password
    self.server = smtplib.SMTP('smtp.gmail.com', 587)
    self.server.starttls()
    self.server.login(self.from_email, self.from_password)

  def send_email(self, subject, body, to):
    msg = MIMEMultipart()
    msg['From'] = self.from_email
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))
    self.server.send_message(msg)
  
  def send_email_csvs(self, subject, body, to, csvs, csvs_names):
          """
          Envia um email com múltiplos arquivos CSV como anexos.

          Args:
              subject (str): Assunto do email.
              body (str): Corpo do email (em HTML).
              to (str): Endereço de email do destinatário.
              csvs (list[str]): Lista de caminhos para os arquivos CSV.
              csvs_names (list[str]): Lista de nomes para os arquivos anexados.
          """
          # Criação do email
          msg = MIMEMultipart()
          msg['From'] = self.from_email
          msg['To'] = to
          msg['Subject'] = subject

          # Adicionar corpo do email
          msg.attach(MIMEText(body, 'html'))

          # Adicionar anexos
          for csv, csv_name in zip(csvs, csvs_names):
              with open(csv, 'rb') as f:
                  part = MIMEApplication(f.read(), Name=csv_name)
                  part.add_header(
                      'Content-Disposition',
                      f'attachment; filename="{csv_name}"'
                  )
                  msg.attach(part)

          # Enviar o email
          self.server.send_message(msg)


  def quit(self):
    self.server.quit()

