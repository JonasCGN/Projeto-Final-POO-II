from typing import Callable, Tuple
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont
from src.func.func_produtos import atualizar_produto
from src.func.func_sincronizacao import enviar_mensagem_de_sincronizacao_server


class EditarProduto(QMainWindow):
    """
    Classe que representa a tela de edição de um produto.
    """

    def __init__(self, atualizar_product: Callable):
        """
        Inicializa a tela de edição de um produto.
        """
        super().__init__()
        self.setWindowTitle("Editar Produto")
        self.setGeometry(500, 300, 500, 400)
        

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

      
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(40, 60, 20, 10)

      
        self.fundo_label = QLabel(self)
        self.fundo_label.setPixmap(QPixmap("../Tela base.jpg"))
        self.fundo_label.setScaledContents(True)
        self.fundo_label.setGeometry(0, 0, self.width(), self.height())
        self.fundo_label.lower()

  
        self.lbl_titulo = QLabel("Editar Produto", self)
        self.lbl_titulo.setStyleSheet(
            """
            color: white;
            font-size: 20px;
            font-weight: bold;
            """
        )
        self.lbl_titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.lbl_titulo)

      
        self.label_id = QLabel("Id do produto: ", self)
        self.label_id.setStyleSheet(
            """
            color: white;
            font-size: 16px;
            """
        )
        layout.addWidget(self.label_id)

        self.lineEdit_nome = QLineEdit(self)
        self.lineEdit_nome.setStyleSheet("padding: 5px; border: 2px solid white; border-radius: 5px;")
        self.lineEdit_nome.setPlaceholderText("Nome do Produto")
        self.lineEdit_nome.setFixedWidth(400)  # largura
        self.lineEdit_nome.setFixedHeight(30)  # altura
        layout.addWidget(self.lineEdit_nome)

        self.lineEdit_preco = QLineEdit(self)
        self.lineEdit_preco.setPlaceholderText("Preço do Produto")
        self.lineEdit_preco.setStyleSheet(
            """
            padding: 5px; border: 2px solid white; border-radius: 5px;
            """
        )
        self.lineEdit_preco.setFixedWidth(400)  # largura
        self.lineEdit_preco.setFixedHeight(30)  # altura
        layout.addWidget(self.lineEdit_preco)

    
        self.comboBox_disponibilidade = QComboBox(self)
        self.comboBox_disponibilidade.addItems(["Disponível", "Indisponível"])
        self.comboBox_disponibilidade.setStyleSheet(
            """
            padding: 5px; border: 2px black; border-radius: 5px;
            """
        )
        self.comboBox_disponibilidade.setFixedWidth(400)  # largura
        self.comboBox_disponibilidade.setFixedHeight(30)  # altura
        layout.addWidget(self.comboBox_disponibilidade)

        self.pushButton_confirmar = QPushButton("Confirmar", self)
        self.pushButton_confirmar.setStyleSheet(
            """
            padding: 5px;
            border: 2px solid white;
            border-radius: 5px;
            background-color: black;
            color: white;
            font-size: 14px;
            """
        )
        self.pushButton_confirmar.setFixedWidth(200)
        self.pushButton_confirmar.setFixedHeight(30)
        layout.addWidget(self.pushButton_confirmar, alignment=Qt.AlignCenter)

       
        self.pushButton_confirmar.clicked.connect(self.editar_valor)
        self.pushButton_confirmar.clicked.connect(atualizar_product)

       
        layout.addStretch(1)

    def start_values(self, values_start: Tuple[str, str, str, str]):
        """
        Inicia os valores da tela de edição de produto.
        """
        self.id, nome, preco, disponivel = values_start
        self.label_id.setText(f"Id do produto: {self.id}")
        self.lineEdit_nome.setText(nome)
        self.lineEdit_preco.setText(preco)
        self.comboBox_disponibilidade.setCurrentText("Disponível" if disponivel.lower() == "disponível" else "Indisponível")

    def editar_valor(self):
        """
        Edita o valor do produto.
        """
        try:
            nome = self.lineEdit_nome.text()
            preco = self.lineEdit_preco.text()
            disponivel = self.comboBox_disponibilidade.currentText()

            if not nome.strip():
                raise ValueError("O nome do produto não pode estar vazio.")
            if not preco.replace('.', '', 1).isdigit():
                raise ValueError("O preço deve ser um número válido.")

            disponivel = disponivel == "Disponível"
            preco = float(preco)
            produto = {"nome": nome, "disponivel": disponivel, "preco": preco}

            if atualizar_produto(produto, self.id):
                QMessageBox.information(self, "Sucesso", "Produto editado com sucesso!")
                enviar_mensagem_de_sincronizacao_server("sync_produto")
                self.close()
            else:
                QMessageBox.warning(self, "Erro", "Falha ao editar. Verifique a conexão ou os dados inseridos.")

        except ValueError as e:
            QMessageBox.warning(self, "Erro", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro inesperado: {str(e)}")
