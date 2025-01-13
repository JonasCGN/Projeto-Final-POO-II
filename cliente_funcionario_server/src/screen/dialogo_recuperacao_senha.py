from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from src.func.func_sincronizacao import enviar_mensagem_de_sincronizacao_cliente


class DialogoRecuperarSenha(QDialog):
    """
    Classe para a tela de recuperação de senha.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Recuperar Senha")
        self.setGeometry(500, 300, 500, 300)

        # Layout principal
        layout = QVBoxLayout(self)

        # Ajusta as margens do layout (esquerda, topo, direita, baixo)
        layout.setContentsMargins(20, 70, 20, 10)

        # Imagem de fundo
        self.fundo_label = QLabel(self)
        self.fundo_label.setPixmap(QPixmap("/root/Projeto-Final-POO-II/Tela base.jpg"))
        self.fundo_label.setScaledContents(True)
        self.fundo_label.setGeometry(0, 0, self.width(), self.height())
        self.fundo_label.lower()

        # Título
        self.lbl_titulo = QLabel("Recuperar Senha", self)
        self.lbl_titulo.setStyleSheet(
            """
            color: white;
            font-size: 20px;
            font-weight: bold;
            """
        )
        self.lbl_titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.lbl_titulo)

        # Campo de entrada para o email
        self.lineEdit_email = QLineEdit(self)
        self.lineEdit_email.setPlaceholderText("Digite seu email")
        self.lineEdit_email.setStyleSheet(
            """
            background-color: transparent;
            color: white;
            border: 2px solid white;
            border-radius: 5px;
            padding: 10px;
            font-size: 16px;
            """
        )
        layout.addWidget(self.lineEdit_email)

        # Botão para enviar o email
        self.pushButton_enviar_email = QPushButton("Enviar Email", self)
        self.pushButton_enviar_email.setFixedHeight(40)
        self.pushButton_enviar_email.setStyleSheet(
            """
            background-color: black;
            color: white;
            border: 2px solid white;
            border-radius: 5px;
            padding: 5px;
            """
        )
        layout.addWidget(self.pushButton_enviar_email, alignment=Qt.AlignCenter)

        # Conectar o botão ao método
        self.pushButton_enviar_email.clicked.connect(self.enviar_email)

        # Ajusta o layout
        layout.addStretch(1)
        self.setLayout(layout)

    def enviar_email(self):
        """
        Método para enviar o email de recuperação de senha.
        """
        email = self.lineEdit_email.text()
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
