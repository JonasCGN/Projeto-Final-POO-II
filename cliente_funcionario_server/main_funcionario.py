"""
Módulo principal do servidor.
"""
from funcao_postgree.bd_postgree_base import Bd_Base
from dotenv import load_dotenv
import os

load_dotenv(".env")
Bd_Base(os.getenv('HOST_BD'), os.getenv('DATABASE'), os.getenv('USER_BD'), os.getenv('PASSWORD_BD'))

from src.screen.tela_principal_server_ui import TelaPrincipalServer
from src.screen.autenticacao import Autenticacao
from PyQt5.QtWidgets import QApplication, QMessageBox
from src.func.func_sincronizacao import iniciar_cliente_sincronizado
import sys


app = QApplication(sys.argv)
tela_principal = TelaPrincipalServer()
autenticacao = Autenticacao()

def sync_tratament(msg: str) -> None:
    """
    Método que é chamado quando uma mensagem de sincronização é recebida. O mesmo trata a mensagem e 
    atualiza a lista de produtos ou pedidos conforme necessário.
    """
    if msg == 'sync_produto':
        tela_principal.signal_handler.atualizar_produto.emit()
    elif msg == 'sync_pedido':
        tela_principal.signal_handler.atualizar_pedido.emit()
    elif msg == 'server_down':
        QMessageBox.critical(None, "Erro", "Servidor desconectado.")
        app.quit()
        

if __name__ == "__main__":
    
    try:
        iniciar_cliente_sincronizado(sync_tratament)
        
        autenticacao.show()
        app.exec_()
        
        if autenticacao.autenticado:
            tela_principal.show()
            app.exec_()
    except KeyboardInterrupt:
        print("Servidor encerrado.")
    except Exception as e:
        print(f"Erro ao iniciar o cliente sincronizado: {e}")
    
    