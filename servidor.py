#  Implementação de um chat básico:
#  ○ Deve ter no mínimo 3 clientes;
#  ○ Deverá ter dois códigos diferentes, o do servidor e do cliente;
#  ○ O Cliente terá um menu onde ele irá escolher o que ele deseja fazer:
# ■ Escutar até receber uma mensagem, depois ele volta para o menu;
#  ■ Apenas escutar mensagens e mostrar na tela;
#  ■ Sair.
#  ■ Mandar mensagem para 1 cliente informando a qual cliente que ele deseja mandar a
# mensagem;
#  ■ Enviar mensagem e escutar a resposta e depois voltar ao menu;
#  ○ O servidor deverá censurar mensagens indevidas (as palavras são definidas pelo grupo).
#  ○ Caso o cliente mande 3 mensagens indevidas no período de 1 minuto, ele deve ser banido e as
# mensagens dele não serão mais transmitidas.
import socket
import datetime

BUFFER = 1024
HOST = "192.168.1.15"
PORT = 9000
NMR_CLIENTES = 1000
class Cliente:
    def __init__(self, cliente_socket, cliente_addrs,user_name) -> None:
        self.cliente_socket: socket.socket = cliente_socket
        self.cliente_addrs = cliente_addrs
        self.name = user_name

class Servidor:

    def __init__(self):
        self.addr = (HOST, PORT)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._clientes: dict[str, Cliente] = {}

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

    def __add_clientes(self, cliente_addrs, cliente_socket, user_name) -> bool:
        is_add = True
        if user_name in self.clientes:
            is_add = False
        else:
            self.clientes[user_name] = Cliente(cliente_socket, cliente_addrs,user_name)
        return is_add

    def connect_user(self):
        client_socket, client_addr = self.server_socket.accept()
        name = client_socket.recv(BUFFER).decode()

        if not self.is_suport_connect():
            client_socket.send("disconnected: Servidor cheio!".encode())
            client_socket.close()

        else:
            if not (self.__add_clientes(client_addr, client_socket, name)):
                client_socket.send("disconnected: Nome em uso!".encode())
                client_socket.close()
            else:
                print(f"Cliente {name} conectado.")
                client_socket.send("connected: conectado!".encode())

if __name__ == "__main__":
    servidor = Servidor()
    servidor.init()

    while True:
        if servidor.is_suport_connect():
            print("Adicione um cliente para continuar")
            servidor.connect_user()
            continue

        try:
            for name, cliente in servidor.clientes.items():
                servidor.handle_client(cliente, name)
        except RuntimeError:
            print("Alerta: Um cliente foi desconectado.")
