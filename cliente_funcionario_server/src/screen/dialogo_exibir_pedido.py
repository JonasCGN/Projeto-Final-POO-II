from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from src.func.func_pedido import get_produtos_do_pedido


class DialogoExibirProduto(QDialog):
    """
    Classe que representa a tela de exibição de um pedido.
    """

    def __init__(self, id_pedido: int):
        """
        Inicializa a tela de exibição de um pedido.
        """
        super().__init__()
        self.setWindowTitle("Exibir Produtos do Pedido")
        self.setGeometry(500, 400, 500, 400)

       
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 20, 20, 10)

        
        self.fundo_label = QLabel(self)
        self.fundo_label.setPixmap(QPixmap("/root/Projeto-Final-POO-II/Tela base.jpg"))
        self.fundo_label.setScaledContents(True)
        self.fundo_label.setGeometry(0, 0, self.width(), self.height())
        self.fundo_label.lower()

       
        self.lbl_produtos = QLabel(self)
        self.lbl_produtos.setStyleSheet(
            """
            color: white;
            font-size: 16px;
            """
        )
        self.lbl_produtos.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.lbl_produtos.setWordWrap(True)
        layout.addStretch(1)  
        layout.addWidget(self.lbl_produtos)

        
        self.prencher_campos(id_pedido)

       
        self.pushButton_exit = QPushButton("Sair", self)
        self.pushButton_exit.setFixedWidth(200)
        self.pushButton_exit.setFixedHeight(40)
        self.pushButton_exit.setStyleSheet(
            """
            background-color: black;
            color: white;
            border: 2px solid white;
            border-radius: 5px;
            padding: 5px;
            """
        )
        layout.addStretch(1) 
        layout.addWidget(self.pushButton_exit, alignment=Qt.AlignCenter)

        
        self.pushButton_exit.clicked.connect(self.accept)

       
        self.setLayout(layout)

    def prencher_campos(self, id_pedido: int):
        """
        Preenche os campos da tela de exibição de um pedido em formato de texto contínuo.
        """
        
        produtos = get_produtos_do_pedido(id_pedido)

       
        texto_produtos = ""
        for produto in produtos:
            texto_produtos += (
                f"Id: {produto['produto_id']}\n"
                f"Nome: {produto['nome']}\n"
                f"Quantidade: {produto['quantidade']}\n"
                f"Preço unitário: R$ {produto['preco_pago']:.2f}\n"
                "----------------------------------------\n"
            )

        
        self.lbl_produtos.setText(texto_produtos)
