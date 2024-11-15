import socket
from threading import Thread
import json
from src.produto import produtos

BUFFER = 1024
HOST = "127.0.0.1"
PORT = 9000
NMR_CLIENTES = 1000

class User:
    def __init__(self, cliente_socket, cliente_addrs,user_name) -> None:
        self.cliente_socket: socket.socket = cliente_socket
        self.cliente_addrs = cliente_addrs
        self.name = user_name

class Servidor:

    def __init__(self):
        self.addr = (HOST, PORT)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._clientes: dict[str, User] = {}

    def init(self):
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(self.addr)
        self.server_socket.listen(NMR_CLIENTES)

    @property
    def clientes(self):
        return self._clientes

    def is_suport_connect(self):
        is_ok = True
        if len(self.clientes) >= NMR_CLIENTES:
            is_ok = False
        return is_ok

    def add_clientes(self, cliente_addrs, cliente_socket, user_name) -> bool:
        is_add = True
        if user_name in self.clientes:
            is_add = False
        else:
            self.clientes[user_name] = User(cliente_socket, cliente_addrs,user_name)
        return is_add

    def connect_user(self):
        client_socket, client_addr = self.server_socket.accept()
        name = client_socket.recv(BUFFER).decode()
        
        if not self.is_suport_connect():
            client_socket.send("disconnected: Servidor cheio!".encode())
            client_socket.close()
        else:
            if not (self.add_clientes(client_addr, client_socket, name)):
                client_socket.send("disconnected: Nome em uso!".encode())
                client_socket.close()
            else:
                print(f"Cliente {name} conectado.")
                client_socket.send("connected: conectado!".encode())
                Thread(target=self.handle_client, args=(self.clientes[name], name)).start()
    
    def handle_process(self, cliente_send: User, msg_recebida: str):
        if msg_recebida == 'LISTAR':
            str_produtos = ""
            for id, produto in produtos.items():
                str_produtos += f"{id} - {produto}\n"
            cliente_send.cliente_socket.send(str_produtos.encode())
            print(f"Enviado a lista de produtos para o cliente {cliente_send.cliente_addrs}.")
        elif msg_recebida == "QTD_PRODUTOS":
            cliente_send.cliente_socket.send(str(len(produtos)).encode())
            print(f"Enviado a quantidade de produtos para o cliente {cliente_send.cliente_addrs}.")
        else:
            msg_recebida = json.loads(msg_recebida)
            total = 0
            for id in msg_recebida["id"]:
                produto = produtos[int(id)]
                total += produto.preco
                print(f"Produto: {produto.nome} - R${produto.preco:.2f}")
            print(f"Total: R${total:.2f}")
            

    def handle_client(self, cliente_send: User, name_send):
        while True:
            try:
                msg_recebida: str = cliente_send.cliente_socket.recv(BUFFER).decode()
                
                if msg_recebida == f"{name_send}, exit" or msg_recebida == "":
                    raise ConnectionResetError
                
                self.handle_process(cliente_send, msg_recebida)

            except (ConnectionResetError, ConnectionAbortedError):
                print(f"Cliente {cliente_send.cliente_addrs} desconectado.")
                self.clientes.pop(name_send)
                break
            
            except json.JSONDecodeError:
                print(f"Erro ao decodificar a mensagem do cliente {cliente_send.cliente_addrs}.")
                break
