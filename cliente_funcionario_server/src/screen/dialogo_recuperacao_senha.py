
from PyQt5.QtWidgets import QDialog, QLineEdit, QComboBox, QDialogButtonBox, QMessageBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QBrush, QColor
from PyQt5 import uic
from src.func.func_sincronizacao import enviar_mensagem_de_sincronizacao_cliente
from src.func.func_autenticacao import recuperar_senha

class DialogoRecuperarSenha(QDialog):
    
    def __init__(self):
        super().__init__()
        uic.loadUi("src/screen/ui/dialogo_recuperacao_senha.ui", self)
        self.pushButton_enviar_email.clicked.connect(self.enviar_email)
    
    def enviar_email(self):
        email = self.lineEdit_email.text()
        if not email or "@" not in email:
            self.dialog("Email Inválido", "Esse email não é válido.")
            return
        
        enviar_mensagem_de_sincronizacao_cliente(f"Email_recuperacao: {email}")
        self.dialog()
        self.close()
      
    
    def dialog(self, title="Email Enviado", message="Email enviado com sucesso."):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec_()
        