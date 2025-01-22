from email.mime.application import MIMEApplication
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailSender:
    """
    Uma classe para gerenciar o envio de e-mails usando o servidor SMTP do Gmail.

    Atributos:
        from_email (str): O endereço de e-mail do remetente.
        from_password (str): A senha ou senha específica do aplicativo do remetente.
        server (smtplib.SMTP): A instância do servidor SMTP para envio de e-mails.
    """

    def __init__(self, email=None, password=None):
        """
        Inicializa a instância do EmailSender e configura o servidor SMTP.

        Args:
            email (str): O endereço de e-mail do remetente.
            password (str): A senha ou senha específica do aplicativo do remetente.

        Execuções:
            smtplib.SMTPAuthenticationError: Se as credenciais de login estiverem incorretas.
        """
        self.from_email = email
        self.from_password = password
        self.server = smtplib.SMTP('smtp.gmail.com', 587)  # Conecta ao servidor SMTP do Gmail.
        self.server.starttls()  # Inicia a criptografia TLS.
        self.server.login(self.from_email, self.from_password)  # Autentica o remetente.

    def send_email(self, subject, body, to):
        """
        Envia um e-mail com o assunto, corpo e destinatário especificados.

        Args:
            subject (str): O assunto do e-mail.
            body (str): O conteúdo do corpo do e-mail, em formato HTML.
            to (str): O endereço de e-mail do destinatário.

        Execuções:
            smtplib.SMTPRecipientsRefused: Se o endereço de e-mail do destinatário for inválido.
            smtplib.SMTPException: Para erros gerais relacionados ao SMTP.
        """
        msg = MIMEMultipart()  # Cria uma nova mensagem de e-mail.
        msg['From'] = self.from_email
        msg['To'] = to
        msg['Subject'] = subject

        # Anexa o conteúdo do corpo como HTML.
        msg.attach(MIMEText(body, 'html'))

        # Envia a mensagem de e-mail.
        self.server.send_message(msg)



def quit(self):
    self.server.quit()

