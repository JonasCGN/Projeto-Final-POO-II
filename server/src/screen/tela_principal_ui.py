from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5 import uic
from .editar_produto_ui import EditarProduto
from .adicionar_product_ui import AdicionarProducto
from src.func.sincronizacao import enviar_mensagem_de_sincronizacao, iniciar_servidor_sincronizado
from src.func.func_produtos import pegar_todos_itens_str, remover_produto, trocar_disponibilidade

class SignalHandler(QObject):
    atualizar_signal = pyqtSignal() 


class TelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('src/screen/ui/tela_principal.ui', self)
        
        self.signal_handler = SignalHandler()
        self.signal_handler.atualizar_signal.connect(self.atualizar_lista_produto)
        
        iniciar_servidor_sincronizado(self.sync_tratament)
        
        self.init_vars()

        self.pushButton_adicionar_produto.clicked.connect(self.screen_add_product.show)
        self.pushButton_editar_produto.clicked.connect(self.abrir_editar_produto)
        self.pushButton_remover_produto.clicked.connect(self.remover_produto)
        self.pushButton_trocar_disponibilidade.clicked.connect(self.trocar_disponibilidade)
        self.actionAtualizar_dados_do_Cardapio.triggered.connect(self.atualizar_lista_produto)
        
        self.show()
    

    def init_vars(self):
        self.screen_add_product = AdicionarProducto(self.atualizar_lista_produto)
        self.screen_edit_product = EditarProduto(self.atualizar_lista_produto)
        self.atualizar_lista_produto()
        
    def sync_tratament(self, msg):
        if msg == 'sync':
            self.signal_handler.atualizar_signal.emit()
            enviar_mensagem_de_sincronizacao('sync')

    def atualizar_lista_produto(self):
        print("[LOG INFO] Atualizando lista de produtos")
        model = QStandardItemModel()
        self.lst_todos_produtos.setModel(model)

        for entry in pegar_todos_itens_str():
            item = QStandardItem(entry)
            model.appendRow(item)
            
        
    def abrir_editar_produto(self):
        selected_index = self.lst_todos_produtos.selectedIndexes()
        
        if selected_index:
            selected_item = self.lst_todos_produtos.model().itemFromIndex(selected_index[0])
            item_text = selected_item.text()

            try:
                id, nome, preco, status = item_text.split(', ')
                id, nome, preco, status = (id.split(": ")[1], nome.split(": ")[1], preco.split(": ")[1], status.split(": ")[1])
                
                self.screen_edit_product.start_values((id, nome, preco, status))
                self.screen_edit_product.show()
            except ValueError as e:
                QMessageBox.warning(self, "Erro", "Não foi possível extrair os dados do produto selecionado.")
        else:
            QMessageBox.warning(self, "Erro", "Selecione um produto para editar.")
    
    def remover_produto(self):
        selected_index = self.lst_todos_produtos.selectedIndexes()
        
        if selected_index:
            selected_item = self.lst_todos_produtos.model().itemFromIndex(selected_index[0])
            item_text = selected_item.text()

            try:
                remove = False
                id = item_text.split(', ')[0].split(": ")[1]
                if QMessageBox.question(
                    self, "Remover produto", "Tem certeza que deseja remover o produto?",
                    QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
                    remove = True
                
                if remove:
                    print("[LOG INFO] Removendo produto")
                    remover_produto(id)
                    self.sync_tratament("sync")
                    
            except ValueError as e:
                QMessageBox.warning(self, "Erro", "Não foi possível extrair os dados do produto selecionado.")
        else:
            QMessageBox.warning(self, "Erro", "Selecione um produto para remover.")
    
    def trocar_disponibilidade(self):   
        selected_index = self.lst_todos_produtos.selectedIndexes()
        
        if selected_index:
            
            selected_item = self.lst_todos_produtos.model().itemFromIndex(selected_index[0])
            item_text = selected_item.text()

            id = item_text.split(', ')[0].split(": ")[1]
            print("[LOG INFO] Trocando disponibilidade")
            if trocar_disponibilidade(id):
                self.sync_tratament("sync")
            else:
                QMessageBox.warning(self, "Erro", "Não foi possível trocar a disponibilidade do produto.")
        else:
            QMessageBox.warning(self, "Erro", "Selecione um produto para trocar a disponibilidade.")
        