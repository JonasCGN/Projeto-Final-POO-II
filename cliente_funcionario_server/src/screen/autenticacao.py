from PyQt5.QtWidgets import (
    QMainWindow, QLabel, QLineEdit, QPushButton, QMessageBox,
    QVBoxLayout, QHBoxLayout, QWidget, QStackedWidget
)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt

from src.func.func_autenticacao import inserir_funcionario, validar_acesso
from src.screen.dialogo_recuperacao_senha import DialogoRecuperarSenha

class Autenticacao(QMainWindow):
    """
    Classe que representa a tela de autenticação do sistema.
    """
    def __init__(self):
        """
        Inicializa a tela de autenticação do sistema.
        """
        super().__init__()
        self.autenticado = False

        self.setWindowTitle("HOME")
        self.setGeometry(900, 800, 900, 800)

        self.widget_central = QWidget(self)
        self.setCentralWidget(self.widget_central)

        self.layout_principal = QVBoxLayout(self.widget_central)
        self.layout_principal.setAlignment(Qt.AlignCenter)
        
        self.fundo_label = QLabel(self)
        self.fundo_label.setGeometry(0, 0, 900, 900)
        self.fundo_label.setScaledContents(True)
        self.fundo_label.setPixmap(QPixmap("../Tela base.jpg"))
        self.fundo_label.lower()


        # Criar o QStackedWidget para alternar entre as telas de login e cadastro
        self.stacked_widget = QStackedWidget(self)
        self.layout_principal.addWidget(self.stacked_widget)

        # Tela de Login
        self.tela_login = self.criar_tela_login()
        self.stacked_widget.addWidget(self.tela_login)

        # Tela de Cadastro
        self.tela_cadastro = self.criar_tela_cadastro()
        self.stacked_widget.addWidget(self.tela_cadastro)

        # Definir a tela inicial como a tela de login
        self.stacked_widget.setCurrentWidget(self.tela_cadastro)

    def criar_tela_login(self):
        """
        Cria a interface de login.
        """
        tela_login = QWidget()

        layout_login = QVBoxLayout()
        layout_login.setAlignment(Qt.AlignCenter)

        self.label_titulo = QLabel("Bem-vindo(a) de volta!", tela_login)
        self.label_titulo.setFont(QFont("Arial", 20, QFont.Bold))
        self.label_titulo.setAlignment(Qt.AlignCenter)
        self.label_titulo.setStyleSheet("color: white;")

        self.label_usuario = QLabel("USUÁRIO", tela_login)
        self.label_usuario.setStyleSheet("color: white;")
        self.label_usuario.setFont(QFont("Arial", 14, QFont.Bold))

        self.lineEdit_usuario_login = QLineEdit(tela_login)
        self.lineEdit_usuario_login.setStyleSheet("padding: 5px; border: 2px solid white; border-radius: 5px;")
        self.lineEdit_usuario_login.setPlaceholderText("Digite seu usuário")
        self.lineEdit_usuario_login.setFixedWidth(400)
        self.lineEdit_usuario_login.setFixedHeight(40)
        
        self.label_senha = QLabel("SENHA", tela_login)
        self.label_senha.setStyleSheet("color: white;")
        self.label_senha.setFont(QFont("Arial", 14, QFont.Bold))

        self.lineEdit_senha_login = QLineEdit(tela_login)
        self.lineEdit_senha_login.setEchoMode(QLineEdit.Password)
        self.lineEdit_senha_login.setStyleSheet("padding: 5px; border: 2px solid white; border-radius: 5px;")
        self.lineEdit_senha_login.setPlaceholderText("Digite sua senha")
        self.lineEdit_senha_login.setFixedWidth(400)
        self.lineEdit_senha_login.setFixedHeight(40)

        self.pushButton_login = QPushButton("ENTRAR", tela_login)
        self.pushButton_login.setFixedWidth(400)
        self.pushButton_login.setFixedHeight(60)
        self.pushButton_login.setStyleSheet(
            "background-color: black; color: white; border: 2px solid white; border-radius: 5px; padding: 5px; margin-bottom: 10px;\
            margin-top: 10px;"
        )
        self.pushButton_login.clicked.connect(self.validar_acesso_login)
        
        self.pushButton_recuperar_login = QPushButton("Esqueceu sua senha? Clique aqui", tela_login)
        self.pushButton_recuperar_login.setStyleSheet("color: white; border: none; text-align: center;")
        self.pushButton_recuperar_login.clicked.connect(self.recuperar_senha)

        self.pushButton_cadastro = QPushButton("Não tem cadastro ? Clique aqui!!", tela_login)
        self.pushButton_cadastro.setStyleSheet("color: white; border: none; text-align: center;")
        self.pushButton_cadastro.clicked.connect(self.mudar_para_cadastro)

        layout_login.addWidget(self.label_titulo)
        layout_login.addWidget(self.label_usuario)
        layout_login.addWidget(self.lineEdit_usuario_login)
        layout_login.addWidget(self.label_senha)
        layout_login.addWidget(self.lineEdit_senha_login)
        layout_login.addWidget(self.pushButton_login)
        layout_login.addWidget(self.pushButton_recuperar_login)
        layout_login.addWidget(self.pushButton_cadastro)

        tela_login.setLayout(layout_login)
        return tela_login

    def criar_tela_cadastro(self):
        """
        Cria a interface de cadastro.
        """
        tela_cadastro = QWidget()

        layout_cadastro = QVBoxLayout()
        layout_cadastro.setAlignment(Qt.AlignCenter)

        self.label_titulo_cadastro = QLabel("Cadastro de Usuário", tela_cadastro)
        self.label_titulo_cadastro.setFont(QFont("Arial", 20, QFont.Bold))
        self.label_titulo_cadastro.setStyleSheet("color: white;")

        self.label_usuario_cadastro = QLabel("Usuário", tela_cadastro)
        self.label_usuario_cadastro.setStyleSheet("color: white;")
        self.lineEdit_usuario_cadastro = QLineEdit(tela_cadastro)
        self.lineEdit_usuario_cadastro.setStyleSheet("padding: 5px; border: 2px solid white; border-radius: 5px;")
        self.lineEdit_usuario_cadastro.setPlaceholderText("Digite o nome de usuário")
        self.lineEdit_usuario_cadastro.setFixedWidth(400)
        self.lineEdit_usuario_cadastro.setFixedHeight(40)

        self.label_email_cadastro = QLabel("Email", tela_cadastro)
        self.label_email_cadastro.setStyleSheet("color: white;")
        self.lineEdit_email_cadastro = QLineEdit(tela_cadastro)
        self.lineEdit_email_cadastro.setStyleSheet("padding: 5px; border: 2px solid white; border-radius: 5px;")
        self.lineEdit_email_cadastro.setPlaceholderText("Digite seu email")
        self.lineEdit_email_cadastro.setFixedWidth(400)
        self.lineEdit_email_cadastro.setFixedHeight(40)

        self.label_senha_cadastro = QLabel("Senha", tela_cadastro)
        self.label_senha_cadastro.setStyleSheet("color: white;")
        self.lineEdit_senha_cadastro = QLineEdit(tela_cadastro)
        self.lineEdit_senha_cadastro.setEchoMode(QLineEdit.Password)
        self.lineEdit_senha_cadastro.setStyleSheet("padding: 5px; border: 2px solid white; border-radius: 5px;")
        self.lineEdit_senha_cadastro.setPlaceholderText("Digite sua senha")
        self.lineEdit_senha_cadastro.setFixedWidth(400)
        self.lineEdit_senha_cadastro.setFixedHeight(40)

        self.label_confirm_senha_cadastro = QLabel("Confirme a senha", tela_cadastro)
        self.label_confirm_senha_cadastro.setStyleSheet("color: white;")
        self.lineEdit_confirm_senha_cadastro = QLineEdit(tela_cadastro)
        self.lineEdit_confirm_senha_cadastro.setEchoMode(QLineEdit.Password)
        self.lineEdit_confirm_senha_cadastro.setStyleSheet("padding: 5px; border: 2px solid white; border-radius: 5px;")
        self.lineEdit_confirm_senha_cadastro.setPlaceholderText("Confirme sua senha")
        self.lineEdit_confirm_senha_cadastro.setFixedWidth(400)
        self.lineEdit_confirm_senha_cadastro.setFixedHeight(40)

        self.pushButton_cadastrar = QPushButton("Cadastrar", tela_cadastro)
        self.pushButton_cadastrar.setFixedWidth(400)
        self.pushButton_cadastrar.setFixedHeight(40)
        self.pushButton_cadastrar.setStyleSheet(
            "background-color: black; color: white; border: 2px solid white; border-radius: 5px; padding: 5px;"
        )
        self.pushButton_cadastrar.clicked.connect(self.validar_cadastro)

        self.pushButton_voltar = QPushButton("Voltar", tela_cadastro)
        self.pushButton_voltar.setFixedWidth(400)
        self.pushButton_voltar.setFixedHeight(40)
        self.pushButton_voltar.setStyleSheet(
            "background-color: #7FB4CB; color: white; border: 2px solid white; border-radius: 5px; padding: 5px;"
        )
        self.pushButton_voltar.clicked.connect(self.mudar_para_login)

        layout_cadastro.addWidget(self.label_titulo_cadastro)
        layout_cadastro.addWidget(self.label_usuario_cadastro)
        layout_cadastro.addWidget(self.lineEdit_usuario_cadastro)
        layout_cadastro.addWidget(self.label_email_cadastro)
        layout_cadastro.addWidget(self.lineEdit_email_cadastro)
        layout_cadastro.addWidget(self.label_senha_cadastro)
        layout_cadastro.addWidget(self.lineEdit_senha_cadastro)
        layout_cadastro.addWidget(self.label_confirm_senha_cadastro)
        layout_cadastro.addWidget(self.lineEdit_confirm_senha_cadastro)
        layout_cadastro.addWidget(self.pushButton_cadastrar)
        layout_cadastro.addWidget(self.pushButton_voltar)

        tela_cadastro.setLayout(layout_cadastro)
        return tela_cadastro

    def mudar_para_cadastro(self):
        """Muda para a tela de cadastro."""
        self.stacked_widget.setCurrentWidget(self.tela_cadastro)

    def mudar_para_login(self):
        """Muda para a tela de login."""
        self.stacked_widget.setCurrentWidget(self.tela_login)

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
        usuario = self.lineEdit_usuario_cadastro.text()
        email = self.lineEdit_email_cadastro.text()
        senha = self.lineEdit_senha_cadastro.text()
        confirmar_senha = self.lineEdit_confirm_senha_cadastro.text()

        if senha != confirmar_senha:
            self.show_error("As senhas não coincidem. Tente novamente.")
            return

        if len(usuario) < 4 or len(senha) < 4:
            self.show_error("Usuário e senha devem ter pelo menos 4 caracteres.")
            return

        if not email or "@" not in email:
            self.show_error("Email inválido. Tente novamente.")
            return

        if inserir_funcionario({"usuario": usuario, "email": email, "senha": senha}):
            QMessageBox.information(self, "Sucesso", "Cadastro realizado com sucesso!")
            self.autenticado = True
            self.close()
        else:
            self.show_error("Erro ao cadastrar usuário. Tente novamente.")

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
        msg_box.setWindowTitle("Erro")
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()
