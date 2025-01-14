from email_functions.email_sand import EmailSender
from email_functions.email_def_body import criar_corpo_email_recupercao_de_conta_html, criar_corpo_envio_arquivo_html
from dotenv import load_dotenv
from os import getenv

load_dotenv("src/.env")
email_sender = EmailSender(getenv('EMAIL'), getenv('PASSWORD'))

def enviar_email_recuperacao_de_conta(email, usuario, senha):
    try:
      corpo_email = criar_corpo_email_recupercao_de_conta_html(usuario, senha)
      email_sender.send_email('Recuperação de Conta', corpo_email, email)
    except Exception as e:
      print(f"[LOG ERRO] Erro ao enviar email de recuperação de conta: {e}")

def enviar_relatorio_vendas(email, html):
    try:
      email_sender.send_email('Relatório de Vendas', html, email)
    except Exception as e:
      print(f"[LOG ERRO] Erro ao enviar email de relatório de vendas: {e}")
      
def enviar_arquivos(email, csvs_list: list[str], csvs_names: list[str]):
    try:
      email_sender.send_email_csvs('Arquivos', criar_corpo_envio_arquivo_html(), email, csvs_list, csvs_names)
    except Exception as e:
      print(f"[LOG ERRO] Erro ao enviar email de arquivos: {e}")