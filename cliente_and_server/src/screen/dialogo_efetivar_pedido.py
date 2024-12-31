"""
Módulo que contém a classe DialogoEfetivarPedido
"""

from PyQt5.QtWidgets import QDialog, QLineEdit, QComboBox, QDialogButtonBox
from PyQt5 import uic

class DialogoEfetivarPedido(QDialog):
    """
    Classe que representa a tela de efetivação de um pedido
    """
    def __init__(self):
        """
        Inicializa a tela de efetivação de um pedido
        """
        super().__init__()
        uic.loadUi("src/screen/ui/diago_inserir.ui", self) 

        self.numero_da_mesa = self.findChild(QLineEdit, "lineEdit_numero_da_mesa")
        self.status_pedido = self.findChild(QComboBox, "comboBox_status")
        self.buttonBox = self.findChild(QDialogButtonBox, "buttonBox")

        self.buttonBox.accepted.disconnect()
        self.buttonBox.accepted.connect(self.verificar_preenchimento)
        self.buttonBox.rejected.connect(self.reject)
        
    def verificar_preenchimento(self):
        """
        Verifica se o campo 'Número da mesa' foi preenchido corretamente.
        """
        if not self.numero_da_mesa.text().strip():
            self.numero_da_mesa.setStyleSheet("border: 1px solid red;")
            print("[LOG ERRO] O campo 'Número da mesa' está vazio.")
            return
        
        elif not self.numero_da_mesa.text().isdigit():
            self.numero_da_mesa.setStyleSheet("border: 1px solid red;")
            print("[LOG ERRO] O campo 'Número da mesa' deve conter apenas números.")
            return
        
        else:
          self.numero_da_mesa.setStyleSheet("")
          print(f"[LOG INFO] Pedido efetivado para a mesa {self.numero_da_mesa.text()}")
          self.accept()
          
