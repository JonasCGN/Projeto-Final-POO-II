"""
Módulo que contém a classe TelaPrincipalServer, que é a tela principal do servidor.
"""

from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QBrush, QColor
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5 import uic
from .editar_produto_ui import EditarProduto
from .adicionar_product_ui import AdicionarProducto
from .dialogo_exibir_pedido import DialogoExibirProduto
from src.func.func_pedido import get_utimos_1000_pedidos, editar_status_pedido
from src.func.sincronizacao import enviar_mensagem_de_sincronizacao_server, iniciar_servidor_sincronizado
from src.func.func_produtos import pegar_todos_itens_str, remover_produto, trocar_disponibilidade

class SignalHandler(QObject):
    """
    Classe que gerencia os sinais de atualização de produtos e pedidos.
    """
    atualizar_produto = pyqtSignal() 
    atualizar_pedido = pyqtSignal()


class TelaPrincipalServer(QMainWindow):
    """
    Classe que representa a tela principal do servidor.
    """
    
    def __init__(self) -> None:
        """
        Inicializa a tela principal do servidor, conectando os sinais, slots e inicializando as variáveis.
        e iniciando o servidor de sincronização.
        """
        
        super().__init__()
        uic.loadUi('src/screen/ui/tela_principal_server.ui', self)
        
        self.signal_handler = SignalHandler()
        self.signal_handler.atualizar_produto.connect(self.atualizar_lista_produto)
        self.signal_handler.atualizar_pedido.connect(self.atualizar_lista_pedido)
        
        iniciar_servidor_sincronizado(self.sync_tratament)
        
        self.init_vars()

        self.pushButton_adicionar_produto.clicked.connect(self.screen_add_product.show)
        self.pushButton_editar_produto.clicked.connect(self.abrir_editar_produto)
        self.pushButton_remover_produto.clicked.connect(self.remover_produto)
        self.pushButton_trocar_disponibilidade.clicked.connect(self.trocar_disponibilidade)
        self.actionAtualizar_dados_do_Cardapio.triggered.connect(self.atualizar_lista_produto)
        
        self.comboBox_status_do_pedido.setEnabled(False)
        self.lst_todos_pedidos.clicked.connect(self.status_pedido_selecionado)
        self.current_pedido_id = None 
        
        self.pushButton_exibir_pedido.clicked.connect(self.exibir_pedido)
        self.show()
    
    def status_pedido_selecionado(self) -> None:
        """
        Método que é chamado quando um pedido é selecionado na lista de pedidos.
        """
        try:
            self.comboBox_status_do_pedido.currentTextChanged.disconnect()
        except TypeError:
            pass
    
        selected_index = self.lst_todos_pedidos.selectedIndexes()
        
        if selected_index:
            self.comboBox_status_do_pedido.setEnabled(True)
            selected_item = self.lst_todos_pedidos.model().itemFromIndex(selected_index[0])
            item_text = selected_item.text()
            
            id = item_text.split(", ")[0].split(": ")[1]
            status = item_text.split(", ")[2].split(": ")[1]
        
            self.current_pedido_id = id
            
            self.comboBox_status_do_pedido.setCurrentText(status)
            self.comboBox_status_do_pedido.currentTextChanged.connect(self.editar_status_pedido)
        else:
            QMessageBox.warning(self, "Erro", "Selecione um pedido para editar.")
            
    def exibir_pedido(self) -> None:
        """
        Método que é chamado quando o botão de exibir pedido é clicado.
        """
        dialogo = DialogoExibirProduto(self.current_pedido_id)
        dialogo.exec()
        
    
    def editar_status_pedido(self) -> None:
        """
        Método que é chamado quando o status de um pedido é editado.
        """
        status = self.comboBox_status_do_pedido.currentText()
        editar_status_pedido(self.current_pedido_id, status)
        self.sync_tratament("sync_pedido")
        
    def init_vars(self) -> None:
        """
        Inicializa as variáveis da classe.
        """
        self.screen_add_product = AdicionarProducto(self.atualizar_lista_produto)
        self.screen_edit_product = EditarProduto(self.atualizar_lista_produto)
        self.atualizar_lista_produto()
        self.atualizar_lista_pedido()
        
    def sync_tratament(self, msg: str) -> None:
        """
        Método que é chamado quando uma mensagem de sincronização é recebida. O mesmo trata a mensagem e 
        atualiza a lista de produtos ou pedidos conforme necessário.
        """
        if msg == 'sync_produto':
            self.signal_handler.atualizar_produto.emit()
            enviar_mensagem_de_sincronizacao_server('sync_produto')
        elif msg == 'sync_pedido':
            self.signal_handler.atualizar_pedido.emit()
            enviar_mensagem_de_sincronizacao_server('sync_pedido')

    def atualizar_lista_produto(self) -> None:
        """
    '    Método que atualiza a lista de produtos.
        """
        print("[LOG INFO] Atualizando lista de produtos")
        model = QStandardItemModel()
        self.lst_todos_produtos.setModel(model)

        for entry in pegar_todos_itens_str():
            item = QStandardItem(entry)
            if "indisponível" in entry.split(", ")[3].split(": ")[1]:
                item.setBackground(QBrush(QColor(255, 0, 0)))
            model.appendRow(item)
            
        
    def abrir_editar_produto(self) -> None:
        """
        Método que é chamado quando o botão de editar produto é clicado.
        """
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
    
    def remover_produto(self) -> None:
        """
        Método que é chamado quando o botão de remover produto é clicado.
        """
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
                    self.sync_tratament("sync_produto")
                    
            except ValueError as e:
                QMessageBox.warning(self, "Erro", "Não foi possível extrair os dados do produto selecionado.")
        else:
            QMessageBox.warning(self, "Erro", "Selecione um produto para remover.")
    
    def trocar_disponibilidade(self) -> None:
        """
        Método que é chamado quando o botão de trocar disponibilidade é clicado.
        """
        selected_index = self.lst_todos_produtos.selectedIndexes()
        
        if selected_index:
            
            selected_item = self.lst_todos_produtos.model().itemFromIndex(selected_index[0])
            item_text = selected_item.text()

            id = item_text.split(', ')[0].split(": ")[1]
            print("[LOG INFO] Trocando disponibilidade")
            if trocar_disponibilidade(id):
                self.sync_tratament("sync_produto")
            else:
                QMessageBox.warning(self, "Erro", "Não foi possível trocar a disponibilidade do produto.")
        else:
            QMessageBox.warning(self, "Erro", "Selecione um produto para trocar a disponibilidade.")
    
    def atualizar_lista_pedido(self) -> None:
        """
        Método que atualiza a lista de pedidos.
        """
        
        print("[LOG INFO] Atualizando lista de pedidos")
        model = QStandardItemModel()
        self.lst_todos_pedidos.setModel(model)
        
        for pedido in get_utimos_1000_pedidos():
            item = QStandardItem(pedido)
            if "Pedido em andamento" in pedido.split(", ")[2].split(": ")[1]:
                item.setBackground(QBrush(QColor(255, 255, 0)))
            if "Pedido cancelado" in pedido.split(", ")[2].split(": ")[1]:
                item.setBackground(QBrush(QColor(255, 0, 0)))
            if "Pedido finalizado" in pedido.split(", ")[2].split(": ")[1]:
                item.setBackground(QBrush(QColor(0, 255, 0)))
            model.appendRow(item)

        