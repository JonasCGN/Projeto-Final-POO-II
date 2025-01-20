"""
Módulo que contém a classe TelaPrincipalServer, que é a tela principal do servidor.
"""

from PyQt5.QtWidgets import QMainWindow, QMessageBox, QDialog
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QBrush, QColor, QImage, QIcon, QPixmap
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5 import uic

from src.screen.dialogo_trocar_senha import DialogoTrocarSenha
from src.screen.dialogo_efetivar_pedido import DialogoEfetivarPedido
from src.func.func_pedidos_desenvolvimento import adicionar_pedido_em_desenvolvimento, finalizar_pedido_em_desenvolvimento, pegar_pedidos_em_desenvolvimento_str, remover_pedido_em_desenvolvimento
from .editar_produto_ui import EditarProduto
from src.screen.adicionar_product_ui import AdicionarProduto
from .dialogo_exibir_pedido import DialogoExibirProduto
from src.func.func_pedido import get_utimos_1000_pedidos, editar_status_pedido, inserir_pedido, transformar_lista_str_em_lista_tuple
from src.func.func_sincronizacao import enviar_mensagem_de_sincronizacao_cliente
from src.func.func_produtos import pegar_todos_itens_str, remover_produto, trocar_disponibilidade
from src.func.func_autenticacao import carregar_credenciais

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
        
        self.init_vars()

        self.pushButton_adicionar_produto.clicked.connect(self.screen_add_product.show)
        self.pushButton_editar_produto.clicked.connect(self.abrir_editar_produto)
        self.pushButton_remover_produto.clicked.connect(self.remover_produto)
        self.pushButton_trocar_disponibilidade.clicked.connect(self.trocar_disponibilidade)
        self.pushButton_adicionar_ao_pedido.clicked.connect(self.adicionar_pedido_desenvolvimento)
        self.pushButton_remover_pedido_temporario.clicked.connect(self.remover_pedido_desenvolvimento)
        self.pushButton_efetivar_pedido.clicked.connect(self.efetivar_pedido)
        self.actionAtualizar_dados_do_Cardapio.triggered.connect(self.atualizar_lista_produto)
        self.actionAtualizar_dados_dos_pedidos.triggered.connect(self.atualizar_lista_pedido)
        self.actionEnviar_Relatorio_Email.triggered.connect(self.enviar_relatorio_email)
        self.actionEnviar_banco_de_dados_Email.triggered.connect(self.enviar_banco_de_dados_email)
        self.actionTrocar_senha.triggered.connect(self.trocar_senha)
        
        self.comboBox_status_do_pedido.setEnabled(False)
        self.lst_todos_pedidos.clicked.connect(self.status_pedido_selecionado)
        self.current_pedido_id = None 
        
        self.pushButton_exibir_pedido.clicked.connect(self.exibir_pedido)
    
    def enviar_relatorio_email(self) -> None:
        email,_  = carregar_credenciais()
        if not email:
            QMessageBox.warning(self, "Aviso", "Email não encontrado")
            return
        enviar_mensagem_de_sincronizacao_cliente(f"enviar_relatorio: {email}")
    
    def enviar_banco_de_dados_email(self) -> None:
        email, _ = carregar_credenciais()
        if not email:
            QMessageBox.warning(self, "Aviso", "Email não encontrado")
            return
        enviar_mensagem_de_sincronizacao_cliente(f"enviar_arquivos: {email}")

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
            numero_de_mesa = dialogo_confirmacao.numero_da_mesa.text()  # Corrigido
            status = dialogo_confirmacao.status_pedido.currentText()
            if(inserir_pedido(transformar_lista_str_em_lista_tuple(pedidos_em_desenvolvimento), numero_de_mesa, status)):
                enviar_mensagem_de_sincronizacao_cliente("sync_pedido")
                finalizar_pedido_em_desenvolvimento()
                self.atualizar_pedido_desenvolvimento()
            else:
                QMessageBox.warning(self, "Aviso", "Aconteceu um problema ao efetivar, verifique sua conecção")
        else:
            QMessageBox.warning(self, "Aviso", "Pedido cancelado")
            
    def trocar_senha(self) -> None:
        """
        Função para trocar a senha do usuário.
        """
        dialogo = DialogoTrocarSenha()
        dialogo.exec()
    
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
        enviar_mensagem_de_sincronizacao_cliente("sync_pedido")
        
        
    def init_vars(self) -> None:
        """
        Inicializa as variáveis da classe.
        """
        self.screen_add_product = AdicionarProduto(self.atualizar_lista_produto)
        self.screen_edit_product = EditarProduto(self.atualizar_lista_produto)
        self.atualizar_lista_produto()
        self.atualizar_lista_pedido()
    
    def adicionar_cor_item(self, cor: QColor, item: QStandardItem) -> QIcon:
        """
        Função para adicionar uma cor a um item.
        
        Args:
            cor (QColor): Cor a ser adicionada.
        
        Returns:
            QIcon: Ícone com a cor adicionada.
        """
        img = QImage(10, 10, QImage.Format_ARGB32)
        img.fill(cor)
        icon = QIcon(QPixmap.fromImage(img))
        item.setIcon(icon)
        return icon

    def atualizar_lista_produto(self) -> None:
        """
        Método que atualiza a lista de produtos.
        """
        pegar_todos_itens_str_cache = pegar_todos_itens_str()
        
        print("[LOG INFO] Atualizando listas de produtos e cardápio")

        model_produtos = QStandardItemModel()
        model_cardapio = QStandardItemModel()

        for entry in pegar_todos_itens_str_cache:
            item = QStandardItem(entry)
            color = QColor(255, 0, 0) if "indisponível" == entry.split(", ")[3].split(": ")[1] else QColor(0, 255, 0)
            self.adicionar_cor_item(color, item)
            
            model_produtos.appendRow(item)
            model_cardapio.appendRow(QStandardItem(item))
        
        self.lst_todos_produtos.setModel(model_produtos)
        self.listView_cardapio.setModel(model_cardapio)
        
        self.atualizar_pedido_desenvolvimento()
        
    def atualizar_pedido_desenvolvimento(self) -> None:
        """
        Função para atualizar a lista de pedidos em desenvolvimento.
        """
        print("[LOG INFO] Atualizando lista de pedidos em desenvolvimento")
        
        pedidos_em_desenvolvimento = pegar_pedidos_em_desenvolvimento_str()
        produtos_disponiveis = self.get_produtos_disponiveis()
        
        model = QStandardItemModel()
        self.listView_pedido_desenvolvimento.setModel(model)

        for entry in pedidos_em_desenvolvimento:
            produto = entry.split(", ")[0].split(": ")[1]
            color = QColor(255, 0, 0) if produto not in produtos_disponiveis else QColor(0, 255, 0)
            item = QStandardItem(entry)
            self.adicionar_cor_item(color, item)
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
                    enviar_mensagem_de_sincronizacao_cliente("sync_produto")
                    
                    
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
                enviar_mensagem_de_sincronizacao_cliente("sync_produto")
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
            status = pedido.split(", ")[2].split(": ")[1]

            if "Pedido em andamento" in status:
                self.adicionar_cor_item(QColor(255, 255, 0), item)  # Amarelo para "em andamento"
            elif "Pedido cancelado" in status:
                self.adicionar_cor_item(QColor(255, 0, 0), item)  # Vermelho para "cancelado"
            elif "Pedido finalizado" in status:
                self.adicionar_cor_item(QColor(0, 255, 0), item)  # Verde para "finalizado"
            elif "Entregar" in status:
                self.adicionar_cor_item(QColor(0, 0, 255), item)  # Azul para "entregar"
            
            model.appendRow(item)

        