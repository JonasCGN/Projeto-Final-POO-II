from PyQt5.QtWidgets import QMainWindow, QMessageBox, QDialog
from PyQt5 import uic
from src.screen.dialogo_efetivar_pedido import DialogoEfetivarPedido
from src.func.sincronizacao import enviar_mensagem_de_sincronizacao, iniciar_cliente_sincronizado
from src.func.func_pedidos_desenvolvimento import pegar_pedidos_em_desenvolvimento_str, adicionar_pedido_em_desenvolvimento, remover_pedido_em_desenvolvimento, finalizar_pedido_em_desenvolvimento
from src.func.func_produtos import pegar_todos_itens_str
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QBrush, QColor

class SignalHandler(QObject):
    atualizar_produto_signal = pyqtSignal() 

class Home(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('src/screen/ui/home.ui', self)
        
        self.signal_handler = SignalHandler()
        self.signal_handler.atualizar_produto_signal.connect(self.atualizar_lista_produto)
        
        iniciar_cliente_sincronizado(self.logica_de_sincronizacao)
        
        self.pushButton_adicionar_ao_pedido.clicked.connect(self.adicionar_pedido_desenvolvimento)
        self.pushButton_remover_pedido_temporario.clicked.connect(self.remover_pedido_desenvolvimento)
        self.pushButton_efetivar_pedido.clicked.connect(self.efetivar_pedido)
        
        self.init_vars()
        self.show()
        
    def init_vars(self):
        self.atualizar_lista_produto()

    def logica_de_sincronizacao(self, msg):
        print(f"[LOG INFO] Iniciando lógica de sincronização: {msg}")
        if msg == "sync_produto":
            print("[LOG INFO] Atualizando Produtos")
            self.signal_handler.atualizar_produto_signal.emit()
        elif msg == "sync_pedido":
            print("[LOG INFO] Atualizando pedidos")
            
    def atualizar_lista_produto(self):
        print("[LOG INFO] Atualizando lista de produtos")
        model = QStandardItemModel()
        self.listView_cardapio.setModel(model)

        for entry in pegar_todos_itens_str():
            item = QStandardItem(entry)
            if "indisponível" in entry.split(", ")[3].split(": ")[1]:
                item.setBackground(QBrush(QColor(255, 0, 0)))
            model.appendRow(item)
        
        self.atualizar_pedido_desenvolvimento()
        
    
    def adicionar_pedido_desenvolvimento(self):
        print("[LOG INFO] Adicionando pedido em desenvolvimento")
        
        # Lógica para adicionar pedido em desenvolvimento
        selected_index = self.listView_cardapio.selectedIndexes()
        
        if selected_index:
            qtd_inser = self.lineEdit_quantidade_inserir.text()
            
            if not qtd_inser:
                print("[LOG INFO] Quantidade não inserida")
                self.lineEdit_quantidade_inserir.setStyleSheet("border: 1px solid red")
                QMessageBox.warning(self, "Aviso", "Quantidade não inserida")
                return
            
            if not qtd_inser.isdigit():
                print("[LOG INFO] Quantidade inválida")
                self.lineEdit_quantidade_inserir.setStyleSheet("border: 1px solid red")
                QMessageBox.warning(self, "Aviso", "Quantidade inválida (deve ser um número inteiro)")
                return
    
            self.lineEdit_quantidade_inserir.setStyleSheet("")
        
            selected_item = self.listView_cardapio.model().itemFromIndex(selected_index[0])
            item_text = selected_item.text()
            confirm = adicionar_pedido_em_desenvolvimento(item_text, int(qtd_inser))
            if confirm[0]:
                self.atualizar_pedido_desenvolvimento()
                
            else:
                print("[LOG ERRO] Pedido não adicionado")
                QMessageBox.warning(self, "Aviso", confirm[1])
                
        else:
            print("[LOG INFO] Nenhum item selecionado")
            QMessageBox.warning(self, "Aviso", "Nenhum item selecionado")
    
    def remover_pedido_desenvolvimento(self):
        
        selected_index = self.listView_pedido_desenvolvimento.selectedIndexes()
        
        
        if selected_index:
            selected_item = self.listView_pedido_desenvolvimento.model().itemFromIndex(selected_index[0])
            item_text = selected_item.text()
            
            qtd_remover = self.lineEdit_quantidade_a_remover.text()
            
            if not qtd_remover:
                print("[LOG INFO] Quantidade não inserida")
                self.lineEdit_quantidade_a_remover.setStyleSheet("border: 1px solid red")
                QMessageBox.warning(self, "Aviso", "Quantidade não inserida")
                return
            
            if not qtd_remover.isdigit():
                print("[LOG INFO] Quantidade inválida")
                self.lineEdit_quantidade_a_remover.setStyleSheet("border: 1px solid red")
                QMessageBox.warning(self, "Aviso", "Quantidade inválida (deve ser um número inteiro)")
                return
            
            self.lineEdit_quantidade_a_remover.setStyleSheet("")
            
            confirm = remover_pedido_em_desenvolvimento(item_text, int(qtd_remover))
            if confirm[0]:
                self.atualizar_pedido_desenvolvimento()
            else:
                print("[LOG INFO] Pedido não removido")
                QMessageBox.warning(self, "Aviso", confirm[1])
        else:
            print("[LOG INFO] Nenhum item selecionado")
            QMessageBox.warning(self, "Aviso", "Nenhum item selecionado")
            
    def atualizar_pedido_desenvolvimento(self):
        print("[LOG INFO] Atualizando lista de pedidos em desenvolvimento")
        model = QStandardItemModel()
        self.listView_pedido_desenvolvimento.setModel(model)
        
        pedidos_em_desenvolvimento = pegar_pedidos_em_desenvolvimento_str()
        cardapio = pegar_todos_itens_str()
        produto_disp = [entry.split(", ")[0].split(": ")[1] for entry in cardapio if "disponível" == entry.split(", ")[3].split(": ")[1]]
        
        for entry in pedidos_em_desenvolvimento:
            id_pedido = entry.split(", ")[0].split(": ")[1]
            
            if not id_pedido in produto_disp:
                item = QStandardItem(entry)
                item.setBackground(QBrush(QColor(255, 0, 0)))
                model.appendRow(item)
            else:
                item = QStandardItem(entry)
                model.appendRow(item)

    def efetivar_pedido(self):
        
        # Pegar o cardápio
        cardapio = pegar_todos_itens_str()
        produto_disp = [entry.split(", ")[0].split(": ")[1] for entry in cardapio if "disponível" == entry.split(", ")[3].split(": ")[1]]
        
        # Pegar os pedidos em desenvolvimento
        pedidos_em_desenvolvimento = pegar_pedidos_em_desenvolvimento_str()
        
        if not pedidos_em_desenvolvimento:
            print("[LOG INFO] Nenhum pedido em desenvolvimento")
            QMessageBox.warning(self, "Aviso", "Nenhum pedido em desenvolvimento")
            return
    
        for pedido in pedidos_em_desenvolvimento:
            id_pedido = pedido.split(", ")[0].split(": ")[1]
            
            if not id_pedido in produto_disp:
                print("[LOG INFO] Produto indisponível")
                QMessageBox.warning(self, "Aviso", "Produto indisponível")
                return
        

        self.dialogo_confirmacao = DialogoEfetivarPedido()
        if self.dialogo_confirmacao.exec_() == QDialog.Accepted:
            print("[LOG INFO] Efetivando pedido")
            print("[LOG INFO] Pedido efetivado para a mesa", self.dialogo_confirmacao.lineEdit_numero_da_mesa.text())
            
            enviar_mensagem_de_sincronizacao("sync_pedido")
            
            # finalizar_pedido_em_desenvolvimento()
            # self.atualizar_pedido_desenvolvimento()
        else:
            print("[LOG INFO] Pedido cancelado")
        
        