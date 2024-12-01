"""
Módulo: servidor_inicializa.py
Descrição: Este módulo inicializa o servidor e aguarda conexões de usuários.

Classes:
    Servidor: Classe responsável por gerenciar o servidor. Contém métodos para inicializar o servidor, conectar usuários e gerenciar clientes.

Funções:
    Nenhuma função adicional é definida neste módulo, apenas a execução direta de um servidor.

Execução:
    Se este módulo for executado diretamente, ele realizará as seguintes ações:
    1. Criará uma instância da classe Servidor.
    2. Inicializará o servidor chamando o método 'init()'.
    3. Entrará em um loop infinito aguardando conexões de usuários, chamando o método 'connect_user()' para cada novo usuário.
"""
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