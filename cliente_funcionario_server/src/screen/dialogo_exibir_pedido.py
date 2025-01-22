from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel, QScrollArea
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
        self.setGeometry(600, 500, 600, 500)

        # Layout principal
        layout = QVBoxLayout(self)
        
        layout.setContentsMargins(10, 90, 20, 10) 

        # Fundo
        self.fundo_label = QLabel(self)
        self.fundo_label.setPixmap(QPixmap("../Tela base.jpg"))
        self.fundo_label.setScaledContents(True)
        self.fundo_label.setGeometry(0, 0, self.width(), self.height())
        self.fundo_label.lower()

        # Área de rolagem para os produtos
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("background: transparent; border: none;")

        self.scroll_content = QLabel(self)
        self.scroll_content.setStyleSheet(
            """
            color: white;
            font-size: 16px;
            """
        )
        self.scroll_content.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.scroll_content.setWordWrap(True)

        self.scroll_area.setWidget(self.scroll_content)
        layout.addWidget(self.scroll_area)

        # Botão Sair
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

        self.prencher_campos(id_pedido)

    def prencher_campos(self, id_pedido: int):
        """
        Preenche os campos da tela de exibição de um pedido em formato de texto contínuo,
        incluindo o total geral de todos os produtos.
        """
        produtos = get_produtos_do_pedido(id_pedido)

        texto_produtos = ""
        total_geral = 0

        for produto in produtos:
            total_item = produto['preco_pago'] * produto['quantidade']
            total_geral += total_item

            texto_produtos += (
                f"Id: {produto['produto_id']}\n"
                f"Nome: {produto['nome']}\n"
                f"Quantidade: {produto['quantidade']}\n"
                f"Preço unitário: R$ {produto['preco_pago']:.2f}\n"
                f"TOTAL: R$ {total_item:.2f}\n"
                "----------------------------------------\n"
            )

        texto_produtos += f"\nTOTAL GERAL: R$ {total_geral:.2f}\n"

        # Atualiza o conteúdo do QLabel dentro da área de rolagem
        self.scroll_content.setText(texto_produtos)
