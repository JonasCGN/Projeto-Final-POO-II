import threading
from PyQt5.QtWidgets import QMainWindow, QPushButton
from PyQt5 import uic
from src.func import enviar_mensagem_de_sincronizacao, iniciar_cliente_sincronizado
from PyQt5.QtCore import pyqtSignal, QObject

class SignalHandler(QObject):
    atualizar_signal = pyqtSignal()

class Home(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('src/screen/ui/home.ui', self)
        iniciar_cliente_sincronizado(self.logica_de_sincronizacao)
        
        self.btn_adicionar_pedido_aleatorio.clicked.connect(self.adicionar_pedido)
        self.show()

    def adicionar_pedido(self):
        enviar_mensagem_de_sincronizacao("sync")
    
    def logica_de_sincronizacao(self, msg):
        print(f"[LOG INFO] Inicinando logica de sincronizacao: {msg}")