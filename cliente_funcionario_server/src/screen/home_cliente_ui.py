"""
Módulo responsável por criar a tela principal do cliente.
"""

from PyQt5.QtWidgets import QMainWindow, QMessageBox, QDialog
from PyQt5 import uic
from src.screen.dialogo_exibir_pedido import DialogoExibirProduto
from src.screen.dialogo_efetivar_pedido import DialogoEfetivarPedido
from src.func.sincronizacao import enviar_mensagem_de_sincronizacao_cliente, iniciar_cliente_sincronizado
from src.func.func_pedidos_desenvolvimento import (
    pegar_pedidos_em_desenvolvimento_str,
    adicionar_pedido_em_desenvolvimento,
    remover_pedido_em_desenvolvimento
)
from src.func.func_pedido import inserir_pedido, get_utimos_1000_pedidos, transformar_lista_str_em_lista_tuple, editar_status_pedido
from src.func.func_produtos import pegar_todos_itens_str
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QBrush, QColor

class SignalHandler(QObject):
    """
    Classe que gerencia os sinais de atualização de produtos e pedidos.
    """
    atualizar_produto_signal = pyqtSignal()
    atualizar_pedido_signal = pyqtSignal()

class Home(QMainWindow):
    """
    Classe que representa a tela principal do cliente.
    """
    
    
    def __init__(self):
        """
        Inicializa a tela principal do cliente, conectando os sinais, slots e inicializando as variáveis.
        e iniciando o cliente de sincronização.
        """
        super().__init__()
        uic.loadUi('src/screen/ui/home.ui', self)
        

        self.comboBox_status_do_pedido.setEnabled(False)
        self.listView_list_pedidos.clicked.connect(self.status_pedido_selecionado)
        self.current_pedido_id = None 
        
        self.pushButton_exibir_pedido.clicked.connect(self.exibir_pedido)
        
        self.atualizar_lista_produto()
        self.atualizar_list_pedido()
        self.show()

    def atualizar_lista_produto(self):
        """
        Função para atualizar a lista de produtos.
        """
        model = QStandardItemModel()
        self.listView_cardapio.setModel(model)
        for entry in pegar_todos_itens_str():
            item = QStandardItem(entry)
            if "indisponível" == entry.split(", ")[3].split(": ")[1]:
                item.setBackground(QBrush(QColor(255, 0, 0)))
            model.appendRow(item)
        self.atualizar_pedido_desenvolvimento()
    
    def atualizar_list_pedido(self):
        """
        Função para atualizar a lista de pedidos.
        """
        model = QStandardItemModel()
        self.listView_list_pedidos.setModel(model)
        
        for pedido in get_utimos_1000_pedidos():
            item = QStandardItem(pedido)
            if "Pedido em andamento" in pedido.split(", ")[2].split(": ")[1]:
                item.setBackground(QBrush(QColor(255, 255, 0)))
            if "Pedido cancelado" in pedido.split(", ")[2].split(": ")[1]:
                item.setBackground(QBrush(QColor(255, 0, 0)))
            if "Pedido finalizado" in pedido.split(", ")[2].split(": ")[1]:
                item.setBackground(QBrush(QColor(0, 255, 0)))
            
            model.appendRow(item)
            

    def validar_quantidade(self, quantidade_input: str) -> int | None:
        """
        Função para validar a quantidade inserida.
        
        Args:
            quantidade_input (str): Quantidade inserida.
        
        Returns:
            int | None: Quantidade válida, ou None em caso de erro.
        """
        quantidade = quantidade_input.text()
        if not quantidade or not quantidade.isdigit():
            quantidade_input.setStyleSheet("border: 1px solid red")
            return None
        quantidade_input.setStyleSheet("")
        return int(quantidade)

    def adicionar_pedido_desenvolvimento(self) -> None:
        """
        Função para adicionar um pedido em desenvolvimento.
        """
        selected_index = self.listView_cardapio.selectedIndexes()
        if selected_index:
            quantidade = self.validar_quantidade(self.lineEdit_quantidade_inserir)
            if quantidade is None:
                QMessageBox.warning(self, "Aviso", "Quantidade inválida ou não inserida")
                return
            selected_item = self.listView_cardapio.model().itemFromIndex(selected_index[0])
            item_text = selected_item.text()
            confirm = adicionar_pedido_em_desenvolvimento(item_text, quantidade)
            if confirm[0]:
                self.atualizar_pedido_desenvolvimento()
            else:
                QMessageBox.warning(self, "Aviso", confirm[1])
        else:
            QMessageBox.warning(self, "Aviso", "Nenhum item selecionado")

    def remover_pedido_desenvolvimento(self) -> None:
        """
        Função para remover um pedido em desenvolvimento.
        """
        selected_index = self.listView_pedido_desenvolvimento.selectedIndexes()
        if selected_index:
            quantidade = self.validar_quantidade(self.lineEdit_quantidade_a_remover)
            if quantidade is None:
                QMessageBox.warning(self, "Aviso", "Quantidade inválida ou não inserida")
                return
            selected_item = self.listView_pedido_desenvolvimento.model().itemFromIndex(selected_index[0])
            item_text = selected_item.text()
            confirm = remover_pedido_em_desenvolvimento(item_text, quantidade)
            if confirm[0]:
                self.atualizar_pedido_desenvolvimento()
            else:
                QMessageBox.warning(self, "Aviso", confirm[1])
        else:
            QMessageBox.warning(self, "Aviso", "Nenhum item selecionado")

    def atualizar_pedido_desenvolvimento(self) -> None:
        """
        Função para atualizar a lista de pedidos em desenvolvimento.
        """
        pedidos_em_desenvolvimento = pegar_pedidos_em_desenvolvimento_str()
        produtos_disponiveis = self.get_produtos_disponiveis()
        
        model = QStandardItemModel()
        self.listView_pedido_desenvolvimento.setModel(model)
        
        for entry in pedidos_em_desenvolvimento:
            item = QStandardItem(entry)
            if entry.split(", ")[0].split(": ")[1] not in produtos_disponiveis:
                item.setBackground(QBrush(QColor(255, 0, 0)))
            model.appendRow(item)

    def get_produtos_disponiveis(self) -> list:
        """
        Função para obter os produtos disponíveis.
        
        Returns:
            list: Lista com os produtos disponíveis.
        """
        todos_itens = pegar_todos_itens_str()
        produtos_disponiveis = []
        
        for entry in todos_itens:
            partes = entry.split(", ")
            nome_produto = partes[0].split(": ")[1]
            status_produto = partes[3].split(": ")[1]
            if "disponível" == status_produto:
                produtos_disponiveis.append(nome_produto)
                
        return produtos_disponiveis

    def efetivar_pedido(self) -> None:
        """
        Função para efetivar um pedido.
        """
        produtos_disponiveis = self.get_produtos_disponiveis()
        pedidos_em_desenvolvimento = pegar_pedidos_em_desenvolvimento_str()
        
        if not pedidos_em_desenvolvimento:
            QMessageBox.warning(self, "Aviso", "Nenhum pedido em desenvolvimento")
            return
        
        for pedido in pedidos_em_desenvolvimento:
            if pedido.split(", ")[0].split(": ")[1] not in produtos_disponiveis:
                QMessageBox.warning(self, "Aviso", "Produto indisponível")
                return
            
        dialogo_confirmacao = DialogoEfetivarPedido()
        if dialogo_confirmacao.exec_() == QDialog.Accepted:
            numero_de_mesa = dialogo_confirmacao.lineEdit_numero_da_mesa.text()
            status = dialogo_confirmacao.comboBox_status.currentText()
            inserir_pedido(transformar_lista_str_em_lista_tuple(pedidos_em_desenvolvimento), numero_de_mesa, status)
            enviar_mensagem_de_sincronizacao_cliente("sync_pedido")
        else:
            QMessageBox.warning(self, "Aviso", "Pedido cancelado")
