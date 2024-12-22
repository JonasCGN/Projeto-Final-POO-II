import threading
from PyQt5.QtWidgets import QMainWindow, QPushButton
from PyQt5 import uic
from src.func.sincronizacao import enviar_mensagem_de_sincronizacao, iniciar_cliente_sincronizado
from src.func.func_produtos import pegar_todos_itens_str
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtGui import QStandardItemModel, QStandardItem

class SignalHandler(QObject):
    atualizar_signal = pyqtSignal() 

class Home(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('src/screen/ui/home.ui', self)
        
        self.signal_handler = SignalHandler()
        self.signal_handler.atualizar_signal.connect(self.atualizar_lista_produto)
        
        iniciar_cliente_sincronizado(self.logica_de_sincronizacao)
        
        self.init_vars()
        self.show()
        
    def init_vars(self):
        self.atualizar_lista_produto()

    def logica_de_sincronizacao(self, msg):
        print(f"[LOG INFO] Iniciando lógica de sincronização: {msg}")
        if msg == "sync":
            print("[LOG INFO] Atualizando")
            self.signal_handler.atualizar_signal.emit()
    
    def atualizar_lista_produto(self):
        print("[LOG INFO] Atualizando lista de produtos")
        model = QStandardItemModel()
        self.listView_cardapio.setModel(model)

        for entry in pegar_todos_itens_str():
            item = QStandardItem(entry)
            model.appendRow(item)
