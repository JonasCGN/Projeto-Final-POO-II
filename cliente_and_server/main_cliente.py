"""
Modulo principal do cliente, onde é feita a autenticação do usuário e a exibição da tela principal.
"""

from funcao_postgree.bd_postgree_base import Bd_Base
from dotenv import load_dotenv
import os

load_dotenv(".env")
Bd_Base(os.getenv('HOST_BD'), os.getenv('DATABASE'), os.getenv('USER_BD'), os.getenv('PASSWORD_BD'))

import sys
from sincronizacao_servidor_cliente.cliente_sincronizacao import ErroCliente
from src.screen.autenticacao import Autenticacao
from PyQt5.QtWidgets import QApplication, QMessageBox 
from src.screen.home_cliente_ui import Home
from funcao_postgree.bd_postgree_base import Bd_Base
from dotenv import load_dotenv
import os

load_dotenv(".env")
Bd_Base(os.getenv('HOST_BD'), os.getenv('DATABASE'), os.getenv('USER_BD'), os.getenv('PASSWORD_BD'))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    autenticacao = Autenticacao()
    autenticacao.show()
    app.exec_()
    
    if autenticacao.autenticado:
        try:
            window = Home()
            window.show()
            app.exec_()
        except ErroCliente as e:
            QMessageBox.critical(None, "ERROR", "Impossível conectar ao servidor.")
