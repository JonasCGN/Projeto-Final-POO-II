"""
Modulo principal do cliente, onde é feita a autenticação do usuário e a exibição da tela principal.
"""

import sys
from sincronizacao_servidor_cliente.cliente_sincronizacao import ErroCliente
from src.screen.autenticacao import Autenticacao
from PyQt5.QtWidgets import QApplication, QMessageBox 
from src.screen.home_cliente_ui import Home

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
