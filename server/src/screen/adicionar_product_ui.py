from typing import Callable
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5 import uic
from src.func import inserir_produto, enviar_mensagem_de_sincronizacao



class AdicionarProducto(QMainWindow):
    def __init__(self, atualizar_product: Callable):
        super().__init__()
        uic.loadUi('src/screen/ui/add_product.ui', self)
        
        self.pushButton_confim.clicked.connect(self.inserir_valor)
        self.pushButton_confim.clicked.connect(atualizar_product)

    def clear_line_edit(self):
        self.lineEdit_nome.clear()
        self.lineEdit_quantidade.clear()
        self.lineEdit_preco.clear()

    def inserir_valor(self):
        try:
            nome = self.lineEdit_nome.text()
            quantidade = self.lineEdit_quantidade.text()
            preco = self.lineEdit_preco.text()

            if not nome:
                raise ValueError("O nome do produto não pode estar vazio.")
            if not quantidade.isdigit():
                raise ValueError("A quantidade deve ser um número inteiro.")
            if not preco.replace('.', '', 1).isdigit():
                raise ValueError("O preço deve ser um número válido.")

            quantidade = int(quantidade)
            preco = float(preco)
            produto = {"nome": nome, "quantidade": quantidade, "preco": preco}

            if inserir_produto(produto):
                QMessageBox.information(self, "Sucesso", "Produto inserido com sucesso!")
                enviar_mensagem_de_sincronizacao("sync")
                self.clear_line_edit()
            else:
                QMessageBox.warning(self, "Erro", "Verifique sua conexão com a internet e o produto que está inserindo.")

        except ValueError as e:
            QMessageBox.warning(self, "Erro", str(e))

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao inserir produto: {str(e)}")
