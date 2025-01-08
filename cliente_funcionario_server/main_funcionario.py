"""
Módulo principal do servidor.
"""
from funcao_postgree.bd_postgree_base import Bd_Base
from dotenv import load_dotenv
import os

load_dotenv(".env")
Bd_Base(os.getenv('HOST_BD'), os.getenv('DATABASE'), os.getenv('USER_BD'), os.getenv('PASSWORD_BD'))

from src.screen.tela_principal_server_ui import TelaPrincipalServer
from src.screen.autenticacao import Autenticacao
from PyQt5.QtWidgets import QApplication
from src.func.sincronizacao import iniciar_cliente_sincronizado
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    tela_principal = TelaPrincipalServer()
    autenticacao = Autenticacao()
    
    try:
        iniciar_cliente_sincronizado(tela_principal.sync_tratament)
    except KeyboardInterrupt:
        print("Servidor encerrado.")
    except Exception as e:
        print(f"Erro ao iniciar o cliente sincronizado: {e}")
    
    # autenticacao.show()
    # app.exec_()
    
    # if autenticacao.autenticado:
    if True:
        tela_principal.show()
        app.exec_()
    