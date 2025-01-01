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
from src.func.sincronizacao import close_server
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    autenticacao = Autenticacao()
    autenticacao.show()
    app.exec_()
    
    if autenticacao.autenticado:
        tela_principal = TelaPrincipalServer()
        tela_principal.show()
        app.exec_()
    
    close_server()