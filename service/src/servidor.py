import socket
from threading import Thread
import json
from src.produto import produtos

BUFFER = 1024
HOST = "127.0.0.1"
PORT = 9000
NMR_CLIENTES = 1000

class User:
    """
    Classe que representa um usuário conectado ao servidor.

    Atributos:
    cliente_socket: socket.socket
        O socket do cliente conectado.
    cliente_addrs: tuple
        O endereço do cliente conectado.
    name: str
        O nome do usuário.
    
    """

    def __init__(self, cliente_socket, cliente_addrs,user_name) -> None:

        """
        Construtor da classe User.

        Parâmetros:
            cliente_socket (socket.socket): O socket associado ao cliente.
            cliente_addrs (tuple): O endereço do cliente (IP, porta).
            user_name (str): O nome do usuário.

        Retorna:
            None.
        """
        
        self.cliente_socket: socket.socket = cliente_socket
        self.cliente_addrs = cliente_addrs
        self.name = user_name

class Servidor:
    """
    Classe que representa o servidor.

    Esta classe implementa as funcionalidades de um servidor TCP que gerencia conexões de múltiplos clientes,
    processa mensagens enviadas pelos clientes e mantém um controle das conexões ativas.

    Atributos:
        addr (tuple): O endereço do servidor, no formato (HOST, PORT).
        server_socket (socket.socket): O socket do servidor para escutar conexões.
        _clientes (dict[str, User]): Dicionário que mapeia o nome de cada usuário ao seu respectivo objeto User.
    """

    def __init__(self):
        """
        Construtor da classe Servidor.

        Inicializa o endereço do servidor, o socket e um dicionário para armazenar os clientes conectados.
        """
        self.addr = (HOST, PORT)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._clientes: dict[str, User] = {}

    def init(self):
        """
        Inicializa o servidor, configurando o socket para reutilizar o endereço, vinculando-o ao endereço especificado
        e iniciando a escuta para conexões.

        Parâmetros:
            Nenhum.

        Retorna:
            None.
        """
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(self.addr)
        self.server_socket.listen(NMR_CLIENTES)

    @property
    def clientes(self):
        """
        Propriedade para acessar o dicionário de clientes conectados.

        Retorna:
            dict[str, User]: O dicionário de clientes conectados.
        """
        return self._clientes

    def is_suport_connect(self):
        """
        Verifica se o servidor suporta novas conexões com base no limite máximo de clientes.

        Retorna:
            bool: True se o servidor pode aceitar novas conexões, False caso contrário.
        """
        return len(self.clientes) < NMR_CLIENTES

    def add_clientes(self, cliente_addrs, cliente_socket, user_name) -> bool:
        """
        Adiciona um novo cliente ao dicionário de clientes conectados.

        Parâmetros:
            cliente_addrs (tuple): O endereço do cliente (IP, porta).
            cliente_socket (socket.socket): O socket do cliente.
            user_name (str): O nome do cliente.

        Retorna:
            bool: True se o cliente foi adicionado com sucesso, False se o nome já estiver em uso.
        """
        if user_name in self.clientes:
            return False
        self.clientes[user_name] = User(cliente_socket, cliente_addrs, user_name)
        return True

    def connect_user(self):
        """
        Aceita uma nova conexão de cliente, verifica se o servidor suporta a conexão e gerencia nomes duplicados.

        Retorna:
            None.
        """
        client_socket, client_addr = self.server_socket.accept()
        name = client_socket.recv(BUFFER).decode()

        if not self.is_suport_connect():
            client_socket.send("disconnected: Servidor cheio!".encode())
            client_socket.close()
        elif not self.add_clientes(client_addr, client_socket, name):
            client_socket.send("disconnected: Nome em uso!".encode())
            client_socket.close()
        else:
            print(f"Cliente {name} conectado.")
            client_socket.send("connected: conectado!".encode())
            Thread(target=self.handle_client, args=(self.clientes[name], name)).start()

    def handle_process(self, cliente_send: User, msg_recebida: str):
        """
        Processa as mensagens enviadas pelos clientes e executa a ação correspondente.

        Parâmetros:
            cliente_send (User): O cliente que enviou a mensagem.
            msg_recebida (str): A mensagem recebida do cliente.

        Retorna:
            None.
        """
        if msg_recebida == 'LISTAR':
            str_produtos = "\n".join([f"{id} - {produto}" for id, produto in produtos.items()])
            cliente_send.cliente_socket.send(str_produtos.encode())
            print(f"Enviado a lista de produtos para o cliente {cliente_send.cliente_addrs}.")
        elif msg_recebida == "QTD_PRODUTOS":
            cliente_send.cliente_socket.send(str(len(produtos)).encode())
            print(f"Enviado a quantidade de produtos para o cliente {cliente_send.cliente_addrs}.")
        else:
            try:
                pedido = json.loads(msg_recebida)
                total = sum(produtos[int(id)].preco for id in pedido["id"])
                for id in pedido["id"]:
                    print(f"Produto: {produtos[int(id)].nome} - R${produtos[int(id)].preco:.2f}")
                print(f"Total: R${total:.2f}")
            except json.JSONDecodeError:
                print(f"Erro ao decodificar a mensagem do cliente {cliente_send.cliente_addrs}.")

    def handle_client(self, cliente_send: User, name_send):
        """
        Gerencia as mensagens recebidas de um cliente específico até que a conexão seja encerrada.

        Parâmetros:
            cliente_send (User): O cliente que está sendo gerenciado.
            name_send (str): O nome do cliente.

        Retorna:
            None.
        """
        while True:
            try:
                msg_recebida = cliente_send.cliente_socket.recv(BUFFER).decode()
                if msg_recebida == f"{name_send}, exit" or not msg_recebida:
                    raise ConnectionResetError
                self.handle_process(cliente_send, msg_recebida)
            except (ConnectionResetError, ConnectionAbortedError):
                print(f"Cliente {cliente_send.cliente_addrs} desconectado.")
                self.clientes.pop(name_send, None)
                break
            except json.JSONDecodeError:
                print(f"Erro ao decodificar a mensagem do cliente {cliente_send.cliente_addrs}.")
                break