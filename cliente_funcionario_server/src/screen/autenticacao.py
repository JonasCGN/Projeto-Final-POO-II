from PyQt5.QtWidgets import (
    QMainWindow, QLabel, QLineEdit, QPushButton, QMessageBox, 
    QVBoxLayout, QHBoxLayout, QWidget
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
        self.setWindowTitle("HOME")
        self.setGeometry(700, 600, 700, 600)  

        # Widget central
        self.widget_central = QWidget(self)
        self.setCentralWidget(self.widget_central)

        # Layout principal
        self.layout_principal = QVBoxLayout(self.widget_central)
        self.layout_principal.setAlignment(Qt.AlignCenter)
        
        # Espaço reservado para o fundo
        self.fundo_label = QLabel(self)
        self.fundo_label.setGeometry(0, 0, 900, 900)  
        self.fundo_label.setScaledContents(True)
        self.fundo_label.setPixmap(QPixmap("/root/Projeto-Final-POO-II/Tela base.jpg"))  

        # Título principal
        self.label_titulo = QLabel("Bem-vindo(a) de volta!", self)
        self.label_titulo.setGeometry(50,50, 200, 50)
        self.label_titulo.setFont(QFont("Arial", 20, QFont.Bold))
        self.label_titulo.setAlignment(Qt.AlignCenter)
        self.label_titulo.setStyleSheet("color: white;")
           
        #  campo usuario
        self.label_usuario = QLabel("USUÁRIO", self)
        self.label_usuario.setGeometry(50, 400, 400, 50)
        self.label_usuario.setStyleSheet("color: white;")
        self.label_usuario.setFont(QFont("Arial", 14, QFont.Bold))  
        self.label_usuario.setAlignment(Qt.AlignCenter)
        
        self.lineEdit_usuario_login = QLineEdit(self)
        self.lineEdit_usuario_login.setStyleSheet("padding: 5px; border: 2px solid white; border-radius: 5px;")
        self.lineEdit_usuario_login.setPlaceholderText("Digite seu usuário")
        self.lineEdit_usuario_login.setFixedWidth(400)  # largura 
        self.lineEdit_usuario_login.setFixedHeight(30)  # altura

        # Campo de senha
        self.label_senha = QLabel("SENHA", self)
        
        self.label_senha.setGeometry(50, 400, 400, 50)
        self.label_senha.setStyleSheet("color: white;")
        self.label_senha.setFont(QFont("Arial", 14, QFont.Bold)) 
        self.label_senha.setAlignment(Qt.AlignCenter)
        
         
        self.lineEdit_senha_login = QLineEdit(self)
        self.lineEdit_senha_login.setEchoMode(QLineEdit.Password)
        self.lineEdit_senha_login.setStyleSheet("padding: 5px; border: 2px solid white; border-radius: 5px;")
        self.lineEdit_senha_login.setPlaceholderText("Digite sua senha")
        self.lineEdit_senha_login.setFixedWidth(400)  
        self.lineEdit_senha_login.setFixedHeight(30) 
        

        # Botão Entrar
        self.pushButton_login = QPushButton("ENTRAR", self)
        self.pushButton_login.setFixedWidth(400)
        self.pushButton_login.setFixedHeight(30)
        self.pushButton_login.setStyleSheet(
            "background-color: black; color: white; border: 2px solid white; border-radius: 5px; padding: 5px;"
        )
        self.pushButton_login.clicked.connect(self.validar_acesso_login)
       
        
        # Link para recuperar senha
        self.pushButton_recuperar_login = QPushButton("Esqueceu sua senha? Clique aqui", self)
        self.pushButton_recuperar_login.setStyleSheet("color: white; border: none; text-align: center;")
        self.pushButton_recuperar_login.clicked.connect(self.recuperar_senha)

        # Botão de cadastro
        self.pushButton_cadastro = QPushButton("Cadastro", self)
        self.pushButton_cadastro.setFixedWidth(400)
        self.pushButton_cadastro.setFixedHeight(30)
        self.pushButton_cadastro.setStyleSheet(
            "background-color: white; color: black; border: 2px solid black; border-radius: 5px; padding: 5px;"
        )
        self.pushButton_cadastro.clicked.connect(self.abrir_tela_cadastro)
       
       
        # Layout principal
        self.layout_principal = QVBoxLayout()
        self.layout_principal.setSpacing(10)
        self.layout_principal.setAlignment(Qt.AlignCenter)

        self.layout_principal.addWidget(self.label_titulo)
        self.layout_principal.addWidget(self.label_usuario)
        self.layout_principal.addWidget(self.lineEdit_usuario_login)
        self.layout_principal.addWidget(self.label_senha)
        self.layout_principal.addWidget(self.lineEdit_senha_login)
        self.layout_principal.addWidget(self.pushButton_login)
        self.layout_principal.addWidget(self.pushButton_recuperar_login)
        self.layout_principal.addWidget(self.pushButton_cadastro)

        # Widget central
        self.widget_central = QWidget()
        self.widget_central.setLayout(self.layout_principal)
        self.setCentralWidget(self.widget_central)

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

    def abrir_tela_cadastro(self):
        """
        Função que será chamada ao clicar no botão de Cadastro.
        Abre a tela de cadastro.
        """
        self.tela_cadastro = CadastroTela()
        self.tela_cadastro.show()

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

class CadastroTela(QMainWindow):
    """
    Classe para a tela de cadastro.
    """
    def __init__(self):
        """
        Inicializa a tela de cadastro.
        """
        super().__init__()
        self.setWindowTitle("Cadastro de Usuário")
        self.setGeometry(700, 600, 700, 600)  

        # Fundo da tela
        self.fundo_label = QLabel(self)
        self.fundo_label.setGeometry(0, 0, 900, 900) 
        self.fundo_label.setScaledContents(True)
        self.fundo_label.setPixmap(QPixmap("/root/Projeto-Final-POO-II/Tela base.jpg"))

        # Título principal
        self.label_titulo = QLabel("Cadastro de Usuário", self)
        self.label_titulo.setGeometry(50,50, 400, 50)
        self.label_titulo.setFont(QFont("Arial", 20, QFont.Bold))
        self.label_titulo.setAlignment(Qt.AlignCenter)
        self.label_titulo.setStyleSheet("color: white;")

        # Campo de usuário
        self.label_usuario = QLabel("Usuário", self)
        self.label_usuario.setAlignment(Qt.AlignCenter)
        self.label_usuario.setFont(QFont("Arial", 10, QFont.Bold)) 
        self.label_usuario.setStyleSheet("color: white;")
        self.lineEdit_usuario = QLineEdit(self)
        self.lineEdit_usuario.setStyleSheet("padding: 5px; border: 2px solid white; border-radius: 5px;")
        self.lineEdit_usuario.setPlaceholderText("Digite o nome de usuário")
        self.lineEdit_usuario.setFixedWidth(400)  # largura 
        self.lineEdit_usuario.setFixedHeight(30)
        
      
        # Campo de email
        self.label_email = QLabel("Email", self)
        self.label_email.setStyleSheet("color: white;")
        self.label_email.setFont(QFont("Arial", 10, QFont.Bold)) 
        self.label_email.setAlignment(Qt.AlignCenter)
        self.lineEdit_email = QLineEdit(self)
        self.lineEdit_email.setStyleSheet("padding: 5px; border: 2px solid white; border-radius: 5px;")
        self.lineEdit_email.setPlaceholderText("Digite seu email")
        self.lineEdit_email.setFixedWidth(400)  # largura 
        self.lineEdit_email.setFixedHeight(30)

        # Campo de senha
        self.label_senha = QLabel("Senha", self)
        self.label_senha.setStyleSheet("color: white;")
        self.label_senha.setFont(QFont("Arial", 10, QFont.Bold)) 
        self.label_senha.setAlignment(Qt.AlignCenter)
        self.lineEdit_senha = QLineEdit(self)
        self.lineEdit_senha.setEchoMode(QLineEdit.Password)
        self.lineEdit_senha.setStyleSheet("padding: 5px; border: 2px solid white; border-radius: 5px;")
        self.lineEdit_senha.setPlaceholderText("Digite sua senha")
        self.lineEdit_senha.setFixedWidth(400)  # largura 
        self.lineEdit_senha.setFixedHeight(30)

        # Campo de confirmação de senha
        self.label_confirm_senha = QLabel("Confirme a senha", self)
        self.label_confirm_senha.setFont(QFont("Arial", 10, QFont.Bold)) 
        self.label_confirm_senha.setStyleSheet("color: white;")
        self.label_confirm_senha.setAlignment(Qt.AlignCenter)
        self.lineEdit_confirm_senha = QLineEdit(self)
        self.lineEdit_confirm_senha.setEchoMode(QLineEdit.Password)
        self.lineEdit_confirm_senha.setStyleSheet("padding: 5px; border: 2px solid white; border-radius: 5px;")
        self.lineEdit_confirm_senha.setPlaceholderText("Confirme sua senha")
        self.lineEdit_confirm_senha.setFixedWidth(400)  # largura 
        self.lineEdit_confirm_senha.setFixedHeight(30)

        # Botão de cadastro
        self.pushButton_cadastrar = QPushButton("Cadastrar", self)
        self.pushButton_cadastrar.setFixedWidth(400)
        self.pushButton_cadastrar.setFixedHeight(30)
        self.pushButton_cadastrar.setStyleSheet(
            "background-color: black; color: white; border: 2px solid white; border-radius: 5px; padding: 5px;"
        )

        self.pushButton_cadastrar.clicked.connect(self.validar_cadastro)

        # Botão de voltar
        self.pushButton_voltar = QPushButton("Voltar", self)
        self.pushButton_voltar.setFixedWidth(400)
        self.pushButton_voltar.setFixedHeight(30)
        self.pushButton_voltar.setStyleSheet(
            "background-color: #7FB4CB; color: white; border: 2px solid white; border-radius: 5px; padding: 5px;"
        )
        self.pushButton_voltar.setFixedSize(100, 40)  # Tamanho menor para o botão
        self.pushButton_voltar.clicked.connect(self.fechar_tela_cadastro)

        # Layout de cadastro
        self.layout_cadastro = QVBoxLayout()
        self.layout_cadastro.setSpacing(10)
        self.layout_cadastro.setAlignment(Qt.AlignCenter)

        self.layout_cadastro.addWidget(self.label_titulo)
        self.layout_cadastro.addWidget(self.label_usuario)
        self.layout_cadastro.addWidget(self.lineEdit_usuario)
        self.layout_cadastro.addWidget(self.label_email)
        self.layout_cadastro.addWidget(self.lineEdit_email)
        self.layout_cadastro.addWidget(self.label_senha)
        self.layout_cadastro.addWidget(self.lineEdit_senha)
        self.layout_cadastro.addWidget(self.label_confirm_senha)
        self.layout_cadastro.addWidget(self.lineEdit_confirm_senha)
        self.layout_cadastro.addWidget(self.pushButton_cadastrar)

        # Layout do botão "Voltar"
        self.layout_voltar = QHBoxLayout()
        self.layout_voltar.setAlignment(Qt.AlignLeft)  # Coloca no canto inferior esquerdo
        self.layout_voltar.addWidget(self.pushButton_voltar)
        
        # Layout principal
        self.layout_principal = QVBoxLayout()
        self.layout_principal.addLayout(self.layout_cadastro)
        self.layout_principal.addLayout(self.layout_voltar)

        # Widget central
        self.widget_central = QWidget()
        self.widget_central.setLayout(self.layout_principal)
        self.setCentralWidget(self.widget_central)

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

        if inserir_funcionario({"usuario": usuario, "email": email, "senha": senha}):
            QMessageBox.information(self, "Sucesso", "Cadastro realizado com sucesso!")
            self.close()
        else:
            self.show_error("Erro ao cadastrar usuário. Tente novamente.")

    def fechar_tela_cadastro(self):
        """
        Fecha a tela de cadastro e retorna à tela anterior (autenticação).
        """
        self.close()

    def show_error(self, message: str):
        """
        Exibe uma mensagem de erro na tela.
        """
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("Erro de Cadastro")
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()