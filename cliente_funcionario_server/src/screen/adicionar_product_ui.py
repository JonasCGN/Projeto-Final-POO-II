from PyQt5.QtWidgets import (
    QMainWindow, QLabel, QLineEdit, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QMessageBox
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
        self.setGeometry(700, 600, 700, 600)  

        
        self.bg_label = QLabel(self)
        self.bg_label.setPixmap(QPixmap("../Tela base.jpg"))
        self.bg_label.setAlignment(Qt.AlignCenter)
        self.bg_label.setScaledContents(True)

      
        self.label_nome = QLabel("Nome do Produto:")
        self.label_nome.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        self.lineEdit_nome = QLineEdit()
        self.lineEdit_nome.setPlaceholderText("Digite o nome do produto")
        self.lineEdit_nome.setStyleSheet("background-color: white; color: black; border-radius: 5px; padding: 5px;")
        self.lineEdit_nome.setFixedSize(400, 30)
        self.lineEdit_nome.setAlignment(Qt.AlignCenter)
        
        self.label_preco = QLabel("Preço do Produto:")
        self.label_preco.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        self.lineEdit_preco = QLineEdit()
        self.lineEdit_preco.setPlaceholderText("Digite o preço")
        self.lineEdit_preco.setStyleSheet("background-color: white; color: black; border-radius: 5px; padding: 5px;")
        self.lineEdit_preco.setFixedSize(400, 30)
        self.lineEdit_preco.setAlignment(Qt.AlignCenter)

        self.label_disponibilidade = QLabel("Disponibilidade:")
        self.label_disponibilidade.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        self.comboBox_disponibilidade = QComboBox()
        self.comboBox_disponibilidade.setStyleSheet("""
            QComboBox {
                background-color: white;
                color: black;
                border-radius: 5px;
                padding: 5px;
            }
            QComboBox::item:hover {
                background-color: lightblue;
                color: black;
            }
        """)
        self.comboBox_disponibilidade.addItems(["Disponível", "Indisponível"])
        self.comboBox_disponibilidade.setFixedSize(400, 30)

        self.pushButton_confirm = QPushButton("Confirmar")
        self.pushButton_confirm.setStyleSheet(
            "background-color: black; color: white; border: 2px solid; border-radius: 10px; font-size: 18px;"
        )
        self.pushButton_confirm.setFixedSize(400, 30)
        self.pushButton_confirm.clicked.connect(self.inserir_valor)
        self.pushButton_confirm.clicked.connect(atualizar_produto)

        layout_central = QVBoxLayout()  
        layout_central.setContentsMargins(0, 0, 0, 0)  
       

        layout = QVBoxLayout() 
        layout.setContentsMargins(10, 20, 10, 20) 
        layout.setSpacing(15)  

       
        layout.addWidget(self.label_nome, alignment=Qt.AlignCenter)
        layout.addWidget(self.lineEdit_nome, alignment=Qt.AlignCenter)
        layout.addWidget(self.label_preco, alignment=Qt.AlignCenter)
        layout.addWidget(self.lineEdit_preco, alignment=Qt.AlignCenter)
        layout.addWidget(self.label_disponibilidade, alignment=Qt.AlignCenter)
        layout.addWidget(self.comboBox_disponibilidade, alignment=Qt.AlignCenter)
        layout.addWidget(self.pushButton_confirm, alignment=Qt.AlignCenter)

       
        layout_central.addStretch()  
        layout_central.addLayout(layout)  
        layout_central.addStretch()  

        
        container = QWidget(self)
        container.setLayout(layout_central)
        self.setCentralWidget(container)

    def resizeEvent(self, event):
        """
        Garante que a imagem de fundo seja redimensionada conforme a janela muda de tamanho.
        """
        self.bg_label.setGeometry(0, 0, self.width(), self.height())  
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
            if preco <= 0:
                raise ValueError("O preço deve ser maior que zero.")
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
