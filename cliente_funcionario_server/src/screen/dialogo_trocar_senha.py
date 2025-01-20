from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel, QMessageBox, QLineEdit
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from src.func.func_pedido import get_produtos_do_pedido
from src.func.func_autenticacao import trocar_senha


class DialogoTrocarSenha(QDialog):
    """
    Classe que representa a tela de exibição de um pedido.
    """

    def __init__(self):
        """
        Inicializa a tela de exibição de um pedido.
        """
        super().__init__()
        uic.loadUi("src/screen/ui/trocar_senha.ui", self)
        self.pushButton_trocar_senha.clicked.connect(self.trocar_senha)
        
    def trocar_senha(self):
        """
        Método que troca a senha do usuário.
        """
        retorno = trocar_senha(self.lineEdit_senha.text())
        if retorno:
            QMessageBox.information(self, "Sucesso", f"Senha trocada com sucesso.")
        else:
            QMessageBox.critical(self, "Erro", "Erro ao trocar a senha.")
        self.close()
        
        
