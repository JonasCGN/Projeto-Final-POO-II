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

  def quit(self):
    self.server.quit()

