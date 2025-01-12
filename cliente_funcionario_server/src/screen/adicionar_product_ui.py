from PyQt5.QtWidgets import (
    QMainWindow, QLabel, QLineEdit, QComboBox, QPushButton, QVBoxLayout, QWidget, QMessageBox
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from typing import Callable
from src.func.func_produtos import inserir_produto
from src.func.func_sincronizacao import enviar_mensagem_de_sincronizacao_server


class AdicionarProduto(QMainWindow):
    """
    Classe que representa a tela de adição de um produto.
    """

    def __init__(self, atualizar_produto: Callable):
        """
        Inicializa a tela de adição de um produto.
        """
        super().__init__()
        self.setWindowTitle("Adicionar Produto")
        self.setGeometry(100, 100, 300, 200)

        # Criando os widgets
        self.label_nome = QLabel("Nome do Produto:")
        self.lineEdit_nome = QLineEdit()

        self.label_preco = QLabel("Preço do Produto:")
        self.lineEdit_preco = QLineEdit()

        self.label_disponibilidade = QLabel("Disponibilidade:")
        self.comboBox_disponibilidade = QComboBox()
        self.comboBox_disponibilidade.addItems(["Disponível", "Indisponível"])

        self.pushButton_confirm = QPushButton("Confirmar")
        self.pushButton_confirm.clicked.connect(self.inserir_valor)
        self.pushButton_confirm.clicked.connect(atualizar_produto)

        # Adicionando a imagem de fundo
        self.bg_label = QLabel(self)
        self.bg_label.setPixmap(QPixmap("/root/Projeto-Final-POO-II/Tela base.jpg"))  
        self.bg_label.setAlignment(Qt.AlignCenter)
        self.bg_label.setScaledContents(True)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label_nome)
        layout.addWidget(self.lineEdit_nome)
        layout.addWidget(self.label_preco)
        layout.addWidget(self.lineEdit_preco)
        layout.addWidget(self.label_disponibilidade)
        layout.addWidget(self.comboBox_disponibilidade)
        layout.addWidget(self.pushButton_confirm)

        # Definindo o widget central
        container = QWidget(self)
        container.setLayout(layout)
        self.setCentralWidget(container)

    def resizeEvent(self, event):
        """
        Garante que a imagem de fundo seja redimensionada conforme a janela muda de tamanho.
        """
        self.bg_label.setGeometry(0, 0, self.width(), self.height())  # Ajusta para o tamanho da janela
        super().resizeEvent(event)

    def clear_values(self):
        """
        Limpa os valores dos campos da tela de adição de produto.
        """
        self.lineEdit_nome.clear()
        self.lineEdit_preco.clear()
        self.comboBox_disponibilidade.setCurrentText("Disponível")

    def inserir_valor(self):
        """
        Insere o valor do produto.
        """
        try:
            nome = self.lineEdit_nome.text()
            preco = self.lineEdit_preco.text()
            status = self.comboBox_disponibilidade.currentText()

            if not nome:
                raise ValueError("O nome do produto não pode estar vazio.")
            if not preco.replace('.', '', 1).isdigit():
                raise ValueError("O preço deve ser um número válido.")

            preco = float(preco)
            produto = {"nome": nome, "preco": preco, "disponivel": status == "Disponível"}

            if inserir_produto(produto):  
                QMessageBox.information(self, "Sucesso", "Produto inserido com sucesso!")
                enviar_mensagem_de_sincronizacao_server("sync_produto")  
                print("[LOG INFO] Produto inserido com sucesso!")
                self.clear_values()
                self.close()
            else:
                QMessageBox.warning(self, "Erro", "Verifique sua conexão com a internet e o produto que está inserindo.")

        except ValueError as e:
            QMessageBox.warning(self, "Erro", str(e))

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao inserir produto: {str(e)}")
