from typing import Callable, Tuple
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5 import uic
from src.func import atualizar_produto, enviar_mensagem_de_sincronizacao


class EditarProduto(QMainWindow):
    def __init__(self, atualizar_product: Callable):
        super().__init__()
        uic.loadUi('src/screen/ui/editar_product.ui', self)
        self.pushButton_confim.clicked.connect(self.editar_valor)
        self.pushButton_confim.clicked.connect(atualizar_product)
      
    def start_values(self, values_start: Tuple[str, str, str, str]):
        self.id, nome, preco, quantidade = values_start
        self.label_id.setText(f"Id do pedido: {self.id}")
        self.lineEdit_nome.setText(nome)
        self.lineEdit_quantidade.setText(quantidade)
        self.lineEdit_preco.setText(preco)

    def editar_valor(self):
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

            if atualizar_produto(produto, self.id):
                QMessageBox.information(self, "Sucesso", "Produto editado!")
                enviar_mensagem_de_sincronizacao("sync")
                print("[LOG INFO] Produto editado com sucesso!")
            else:
                QMessageBox.warning(self, "Erro", "Verifique sua conexão com a internet e o produto que está inserindo.")

        except ValueError as e:
            QMessageBox.warning(self, "Erro", str(e))

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao inserir produto: {str(e)}")
