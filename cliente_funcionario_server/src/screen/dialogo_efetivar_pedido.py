from PyQt5.QtWidgets import QDialog, QLineEdit, QComboBox, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt

class DialogoEfetivarPedido(QDialog):
    """
    Classe que representa a tela de efetivação de um pedido.
    """
    def __init__(self):
        """
        Inicializa a tela de efetivação de um pedido.
        """
        super().__init__()

       
        self.setWindowTitle("Efetivar Pedido")
        self.setGeometry(700, 600, 700, 600)
        
        
        self.fundo_imagem = QLabel(self)
        self.fundo_imagem.setPixmap(QPixmap("../Tela base.jpg"))
        self.fundo_imagem.setScaledContents(True)  
        self.fundo_imagem.setGeometry(0, 0, self.width(), self.height())  
        
        
        self.label_titulo = QLabel("Efetivar Pedido", self)
        self.label_titulo.setFont(QFont("Arial", 20, QFont.Bold))
        self.label_titulo.setStyleSheet("color: white;")
        self.label_titulo.setAlignment(Qt.AlignCenter)

       
        self.label_numero_da_mesa = QLabel("Número da Mesa", self)
        self.label_numero_da_mesa.setFont(QFont("Arial", 10, QFont.Bold))
        self.label_numero_da_mesa.setStyleSheet("color: white;")
        self.numero_da_mesa = QLineEdit(self)
        self.numero_da_mesa.setStyleSheet("padding: 5px; border: 2px solid white; border-radius: 5px;")
        self.numero_da_mesa.setPlaceholderText("Digite o número da mesa")
        self.numero_da_mesa.setFixedWidth(400)
        self.numero_da_mesa.setFixedHeight(30)

      
        self.label_status_pedido = QLabel("Status do Pedido", self)
        self.label_status_pedido.setFont(QFont("Arial", 10, QFont.Bold))
        self.label_status_pedido.setStyleSheet("color: white;")
        self.status_pedido = QComboBox(self)
        self.status_pedido.setStyleSheet("padding: 5px; border: 2px solid white; border-radius: 5px;")
        self.status_pedido.addItems(["Pedido em andamento", "Entregar", "Pedido cancelado", "Pedido finalizado"])
        self.status_pedido.setFixedWidth(400)
        self.status_pedido.setFixedHeight(30)

        
        self.label_erro = QLabel("", self)
        self.label_erro.setFont(QFont("Arial", 10, QFont.Bold))
        self.label_erro.setStyleSheet("color: red;")

        
        self.pushButton_confirmar = QPushButton("Efetivar Pedido", self)
        self.pushButton_confirmar.setFixedWidth(400)
        self.pushButton_confirmar.setFixedHeight(30)
        self.pushButton_confirmar.setStyleSheet(
            "background-color: black; color: white; border: 2px solid white; border-radius: 5px; padding: 5px;"
        )
        self.pushButton_confirmar.clicked.connect(self.verificar_preenchimento)

    
        self.pushButton_cancelar = QPushButton("Cancelar", self)
        self.pushButton_cancelar.setFixedWidth(400)
        self.pushButton_cancelar.setFixedHeight(30)
        self.pushButton_cancelar.setStyleSheet(
            "background-color: #7FB4CB; color: white; border: 2px solid white; border-radius: 5px; padding: 5px;"
        )
        self.pushButton_cancelar.clicked.connect(self.reject)

        
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(8)
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label_titulo)
        self.layout.addWidget(self.label_numero_da_mesa)
        self.layout.addWidget(self.numero_da_mesa)
        self.layout.addWidget(self.label_status_pedido)
        self.layout.addWidget(self.status_pedido)
        self.layout.addWidget(self.label_erro)
        self.layout.addWidget(self.pushButton_confirmar)
        self.layout.addWidget(self.pushButton_cancelar)

        
        self.setLayout(self.layout)

    def verificar_preenchimento(self):
        """
        Verifica se o campo 'Número da mesa' foi preenchido corretamente.
        """
        if not self.numero_da_mesa.text().strip():
            self.numero_da_mesa.setStyleSheet("border: 2px solid red;")
            self.label_erro.setText("O campo 'Número da mesa' está vazio.")
            print("[LOG ERRO] O campo 'Número da mesa' está vazio.")
            return
        
        elif not self.numero_da_mesa.text().isdigit():
            self.numero_da_mesa.setStyleSheet("border: 2px solid red;")
            self.label_erro.setText("O campo 'Número da mesa' deve conter apenas números.")
            print("[LOG ERRO] O campo 'Número da mesa' deve conter apenas números.")
            return
        
        else:
            self.numero_da_mesa.setStyleSheet("border: 2px solid white;")
            self.label_erro.clear()
            numero_de_mesa = self.numero_da_mesa.text()  
            print(f"[LOG INFO] Pedido efetivado para a mesa {numero_de_mesa}")
            self.accept()
