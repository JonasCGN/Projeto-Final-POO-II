"""
Módulo de autenticação do sistema.
"""

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from src.func.func_autenticacao import  inserir_funcionario, validar_acesso
from src.screen.dialogo_recuperacao_senha import DialogoRecuperarSenha

class Autenticacao(QMainWindow):
    """
    Classe que representa a tela de autenticação do sistema
    """
    
    def __init__(self):
        """
        Inicializa a tela de autenticação do sistema
        """
        super().__init__()
        uic.loadUi('src/screen/ui/autenticacao.ui', self)
        self.autenticado = False 
        self.pushButton_login.clicked.connect(self.validar_acesso_login)
        self.pushButton_recuperar_login.clicked.connect(self.recuperar_senha)
        self.pushButton_cadrastro.clicked.connect(self.validar_cadastro)
    
    def validar_acesso_login(self):
        """
        Valida o acesso do usuário.
        """
        usuario = self.lineEdit_usuario_login.text()
        senha = self.lineEdit_senha_login.text()
        
        if not usuario or not senha:
            self.show_error("Usuário e senha são obrigatórios.")
            return

        if not validar_acesso(usuario, senha):
            self.show_error("Usuário ou senha inválidos.")
            return
    
        self.autenticado = True
        self.close()
    
    def validar_cadastro(self):
        """
        Valida o cadastro do usuário.
        """
        usuario = self.lineEdit_usuario.text()
        email = self.lineEdit_email.text()
        senha = self.lineEdit_senha.text()
        confirmar_senha = self.lineEdit_confirm_senha.text()
        
        if senha != confirmar_senha:
            self.show_error("As senhas não coincidem. Tente novamente.")
            return
        
        if len(usuario) < 4 or len(senha) < 4:
            self.show_error("Usuário e senha devem ter pelo menos 4 caracteres.")
            return
        
        if not email or "@" not in email:
            self.show_error("Email inválido. Tente novamente.")
            return
        
        print(f"[LOG INFO] Cadastro realizado {usuario}, {email}, {senha}")
        inserir_funcionario({"usuario": usuario, "email": email, "senha": senha})
        QMessageBox.information(self, "Sucesso", "Cadastro realizado com sucesso!")
        
        self.autenticado = True
        self.close()
            
    def recuperar_senha(self):
        """
        Recupera a senha do usuário.
        """
        dialogo = DialogoRecuperarSenha()
        dialogo.exec_()
        
        
    def show_error(self, message: str):
        """
        Exibe uma mensagem de erro na tela. 
        """
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("Erro de Autenticação")
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()
