from email_functions.email_sand import EmailSender
from email_functions.email_def_body import criar_corpo_email_recupercao_de_conta_html, criar_corpo_envio_arquivo_html
from dotenv import load_dotenv
from os import getenv

load_dotenv("src/.env")
email_sender = EmailSender(getenv('EMAIL'), getenv('PASSWORD'))

def enviar_email_recuperacao_de_conta(email, usuario, senha):
    """
    Envia um email de recuperação de conta para o usuário.

    Args:
        email (str): Endereço de email do destinatário.
        usuario (str): Nome do usuário para o qual a conta será recuperada.
        senha (str): Nova senha ou senha temporária gerada.

    Exceções Tratadas:
        Em caso de erro no envio do email, a exceção será capturada, 
        e um log de erro será impresso.
    """
    try:
        corpo_email = criar_corpo_email_recupercao_de_conta_html(usuario, senha)
        email_sender.send_email('Recuperação de Conta', corpo_email, email)
    except Exception as e:
        print(f"[LOG ERRO] Erro ao enviar email de recuperação de conta: {e}")


def enviar_relatorio_vendas(email, html):
    """
    Envia um relatório de vendas para o endereço de email especificado.

    Args:
        email (str): Endereço de email do destinatário.
        html (str): Conteúdo em HTML do relatório de vendas.

    Exceções Tratadas:
        Em caso de erro no envio do email, a exceção será capturada, 
        e um log de erro será impresso.
    """
    try:
        email_sender.send_email('Relatório de Vendas', html, email)
    except Exception as e:
        print(f"[LOG ERRO] Erro ao enviar email de relatório de vendas: {e}")


def enviar_arquivos(email, csvs_list: list[str], csvs_names: list[str]):
    """
    Envia um email contendo arquivos CSV como anexos.

    Args:
        email (str): Endereço de email do destinatário.
        csvs_list (list[str]): Lista de caminhos para os arquivos CSV a serem enviados.
        csvs_names (list[str]): Lista de nomes dos arquivos para exibição nos anexos.

    Exceções Tratadas:
        Em caso de erro no envio do email, a exceção será capturada, 
        e um log de erro será impresso.
    """
    try:
        email_sender.send_email_csvs(
            'Arquivos',
            criar_corpo_envio_arquivo_html(),
            email,
            csvs_list,
            csvs_names
        )
    except Exception as e:
        print(f"[LOG ERRO] Erro ao enviar email de arquivos: {e}")