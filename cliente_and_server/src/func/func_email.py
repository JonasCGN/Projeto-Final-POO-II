from email_functions.email_sand import EmailSender
from email_functions.email_def_body import criar_corpo_email_recupercao_de_conta_html
from dotenv import load_dotenv
from os import getenv

load_dotenv("src/.env")
print(getenv('EMAIL'), getenv('PASSWORD'))
email_sender = EmailSender(getenv('EMAIL'), getenv('PASSWORD'))

def enviar_email_recuperacao_de_conta(email, usuario, senha):
    try:
      corpo_email = criar_corpo_email_recupercao_de_conta_html(usuario, senha)
      email_sender.send_email('Recuperação de Conta', corpo_email, email)
    except Exception as e:
      print(f"[LOG ERRO] Erro ao enviar email de recuperação de conta: {e}")
