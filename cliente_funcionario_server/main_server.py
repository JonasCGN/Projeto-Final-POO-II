from funcao_postgree.bd_postgree_base import Bd_Base
from dotenv import load_dotenv
import os

load_dotenv(".env")
Bd_Base(os.getenv('HOST_BD'), os.getenv('DATABASE'), os.getenv('USER_BD'), os.getenv('PASSWORD_BD'))

from src.func.func_autenticacao import recuperar_senha
from src.func.func_sincronizacao import close_server, enviar_mensagem_de_sincronizacao_server, iniciar_servidor_sincronizado
from src.func.func_email import enviar_email_recuperacao_de_conta, enviar_relatorio_vendas, enviar_arquivos
from src.func.func_relatorio import gerar_relatorio, criar_csv, remover_csv


def sync_tratament(msg: str) -> str | None:
  if msg == "server_down":
    raise KeyboardInterrupt
  
  elif msg.startswith("Email_recuperacao: "):
    email = msg.split("Email_recuperacao: ")[1]
    print(f"[LOG INFO] Solicitação de recuperação de conta para o email '{email}'.")
    valor = recuperar_senha(email)
    if valor is not False:
      enviar_email_recuperacao_de_conta(email, *valor)
      print(f"[LOG INFO] Email de recuperação de conta enviado para '{email}'.")
      
  elif msg.startswith("enviar_relatorio: "):
    print(f"[LOG INFO] Solicitação de envio de relatório de vendas.")
    email = msg.split("enviar_relatorio: ")[1]
    html = gerar_relatorio()
    enviar_relatorio_vendas(email, html)
    print(f"[LOG INFO] Relatório de vendas enviado para '{email}'.")
    
  elif msg.startswith("enviar_arquivos: "):
    print(f"[LOG INFO] Solicitação de envio de arquivos.")
    email = msg.split("enviar_arquivos: ")[1]
    criar_csv()
    csvs_list = ["pedidos.csv", "produtos.csv", "produtos_pedidos.csv"]
    enviar_arquivos(email, csvs_list, csvs_list)
    remover_csv()
    print(f"[LOG INFO] Arquivos enviados para '{email}'.")

  else:
    print(f"[LOG INFO] Mensagem '{msg}' está sendo repassada para os clientes.")
    enviar_mensagem_de_sincronizacao_server(msg)  
  

if __name__ == "__main__":
  try:
    iniciar_servidor_sincronizado(sync_tratament)
  except KeyboardInterrupt:
    print("Servidor encerrado.")
  except Exception as e:
    print(f"Erro ao iniciar o servidor: {e}") 
    
  close_server()
  