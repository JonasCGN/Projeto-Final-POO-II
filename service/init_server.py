from src.servidor import Servidor
"""
Este módulo inicializa o servidor e aguarda conexões de usuários.
Classes:
    Servidor: Classe responsável por gerenciar o servidor.
Funções:
    Nenhuma
Execução:
    Se este módulo for executado diretamente, ele irá:
    1. Criar uma instância da classe Servidor.
    2. Inicializar o servidor.
    3. Entrar em um loop infinito aguardando conexões de usuários.
"""

if __name__ == "__main__":
    servidor = Servidor()
    servidor.init()
    while True:
        servidor.connect_user()