from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
from src.func.func_sincronizacao import enviar_mensagem_de_sincronizacao_cliente


class DialogoRecuperarSenha(QDialog):
    """
    Classe para a tela de recuperação de senha.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Recuperar Senha")
        self.setGeometry(550, 300, 550, 300)

        layout = QVBoxLayout(self)

        layout.setContentsMargins(20, 70, 20, 10)
       
        layout.setSpacing(30)  

        self.fundo_label = QLabel(self)
        self.fundo_label.setPixmap(QPixmap("../Tela base.jpg"))
        self.fundo_label.setScaledContents(True)
        self.fundo_label.setGeometry(0, 0, self.width(), self.height())
        self.fundo_label.lower()
        
        self.lbl_titulo = QLabel("Recuperar Senha", self)
        self.lbl_titulo.setFont(QFont("Arial", 14, QFont.Bold))
        self.lbl_titulo.setStyleSheet("color: white;")
        self.lbl_titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.lbl_titulo)

        self.lineEdit_usuario_login = QLineEdit(self)
        self.lineEdit_usuario_login.setStyleSheet("padding: 5px; border: 2px solid white; border-radius: 5px;")
        self.lineEdit_usuario_login.setPlaceholderText("Digite seu E-mail")
        self.lineEdit_usuario_login.setFixedWidth(400)  # largura
        self.lineEdit_usuario_login.setFixedHeight(30)  # altura
        layout.addWidget(self.lineEdit_usuario_login, alignment=Qt.AlignCenter)
        
        self.pushButton_enviar_email = QPushButton("Enviar Email", self)
        self.pushButton_enviar_email.setStyleSheet(
            """
            padding: 5px;
            border: 2px solid white;
            border-radius: 5px;
            background-color: black;
            color: white;
            font-size: 14px;
            """
        )
        self.pushButton_enviar_email.setFixedWidth(200)
        self.pushButton_enviar_email.setFixedHeight(30)
        layout.addWidget(self.pushButton_enviar_email, alignment=Qt.AlignCenter)

        
        self.pushButton_enviar_email.clicked.connect(self.enviar_email)

        
        layout.addStretch(1)
        self.setLayout(layout)

    def enviar_email(self):
        """
        Método para enviar o email de recuperação de senha.
        """
        email = self.lineEdit_usuario_login.text()  
        if not email or "@" not in email:
            self.exibir_mensagem("Email Inválido", "Esse email não é válido.")
            return

        enviar_mensagem_de_sincronizacao_cliente(f"Email_recuperacao: {email}")
        self.exibir_mensagem("Email Enviado", "Email enviado com sucesso.")
        self.close()

    def exibir_mensagem(self, titulo, mensagem):
        """
        Exibe uma mensagem em uma caixa de diálogo.
        """
        msg = QMessageBox(self)
        msg.setWindowTitle(titulo)
        msg.setText(mensagem)
        msg.exec_()
