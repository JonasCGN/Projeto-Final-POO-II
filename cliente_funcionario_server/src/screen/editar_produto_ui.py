from typing import Callable, Tuple
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
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
        self.setGeometry(500, 300, 500, 450)  # Aumentei a altura para acomodar o espaçamento

        # Widget principal
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Layout principal
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 30, 20, 10)

        # Imagem de fundo
        self.fundo_label = QLabel(self)
        layout.setContentsMargins(20, 70, 20, 10)
        self.fundo_label.setPixmap(QPixmap("/root/Projeto-Final-POO-II/Tela base.jpg"))
        self.fundo_label.setScaledContents(True)
        self.fundo_label.setGeometry(0, 0, self.width(), self.height())
        self.fundo_label.lower()

        # Título
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

        # ID do produto
        self.label_id = QLabel("Id do produto: ", self)
        self.label_id.setStyleSheet(
            """
            color: white;
            font-size: 16px;
            """
        )
        layout.addWidget(self.label_id)

        # Campo para o nome do produto
        self.lineEdit_nome = QLineEdit(self)
        self.lineEdit_nome.setPlaceholderText("Nome do Produto")
        self.lineEdit_nome.setStyleSheet(
            """
            background-color: transparent;
            color: white;
            border: 2px solid white;
            border-radius: 5px;
            padding: 10px;
            font-size: 16px;
            """
        )
        layout.addWidget(self.lineEdit_nome)

        # Campo para o preço do produto
        self.lineEdit_preco = QLineEdit(self)
        self.lineEdit_preco.setPlaceholderText("Preço do Produto")
        self.lineEdit_preco.setStyleSheet(
            """
            background-color: transparent;
            color: white;
            border: 2px solid white;
            border-radius: 5px;
            padding: 10px;
            font-size: 16px;
            """
        )
        layout.addWidget(self.lineEdit_preco)

        # ComboBox para disponibilidade
        self.comboBox_disponibilidade = QComboBox(self)
        self.comboBox_disponibilidade.addItems(["Disponível", "Indisponível"])
        self.comboBox_disponibilidade.setStyleSheet(
            """
            background-color: transparent;
            color: white;
            border: 2px solid white;
            border-radius: 5px;
            padding: 5px;
            font-size: 16px;
            """
        )
        layout.addWidget(self.comboBox_disponibilidade)

        # Ajuste de espaçamento entre os campos e o botão
        layout.addStretch(2)

        # Botão para confirmar
        self.pushButton_confim = QPushButton("Confirmar", self)
        self.pushButton_confim.setStyleSheet(
            """
            background-color: black;
            color: white;
            border: 2px solid white;
            border-radius: 5px;
            padding: 10px;
            font-size: 16px;
            """
        )
        layout.addWidget(self.pushButton_confim, alignment=Qt.AlignCenter)

        # Conectar o botão ao método
        self.pushButton_confim.clicked.connect(self.editar_valor)
        self.pushButton_confim.clicked.connect(atualizar_product)

        # Ajuste do layout final
        layout.addStretch(1)

    def start_values(self, values_start: Tuple[str, str, str, str]):
        """
        Inicia os valores da tela de edição de produto.
        """
        self.id, nome, preco, disponivel = values_start
        self.label_id.setText(f"Id do produto: {self.id}")
        self.lineEdit_nome.setText(nome)
        self.comboBox_disponibilidade.setCurrentText("Disponível" if disponivel == "disponível" else "Indisponível")
        self.lineEdit_preco.setText(preco)

    def editar_valor(self):
        """
        Edita o valor do produto.
        """
        try:
            nome = self.lineEdit_nome.text()
            preco = self.lineEdit_preco.text()
            disponivel = self.comboBox_disponibilidade.currentText()

            if not nome:
                raise ValueError("O nome do produto não pode estar vazio.")
            if not preco.replace('.', '', 1).isdigit():
                raise ValueError("O preço deve ser um número válido.")

            disponivel = disponivel == "Disponível"

            preco = float(preco)
            produto = {"nome": nome, "disponivel": disponivel, "preco": preco}

            if atualizar_produto(produto, self.id):
                QMessageBox.information(self, "Sucesso", "Produto editado!")
                enviar_mensagem_de_sincronizacao_server("sync_produto")
                print("[LOG INFO] Produto editado com sucesso!")
                self.close()
            else:
                QMessageBox.warning(self, "Erro", "Verifique sua conexão com a internet e o produto que está inserindo.")

        except ValueError as e:
            QMessageBox.warning(self, "Erro", str(e))

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao inserir produto: {str(e)}")
