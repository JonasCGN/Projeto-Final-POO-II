from PyQt5.QtWidgets import QMainWindow, QListView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5 import uic
from .add_product import AddProduct
from src.func import get_all_itens_str


class Home(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('src/screen/ui/home.ui', self)
        self.init_vars()
        self.pushButton_adicionar_produto.clicked.connect(self.screen_add_product.show)
        self.show()

    def init_vars(self):
        self.screen_add_product = AddProduct(self.atualizar_lista_pedidos)
        self.atualizar_lista_pedidos()

    def atualizar_lista_pedidos(self):
        print("Atualizando lista de produtos...")
        
        model = QStandardItemModel()
        self.lst_todos_pedidos.setModel(model)

        for entry in get_all_itens_str():
            item = QStandardItem(entry)
            model.appendRow(item)
