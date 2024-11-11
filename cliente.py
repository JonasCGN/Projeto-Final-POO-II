import socket
import sys
import json

SERVER_POST = 9000
BUFFER = 1024
ADDRESS = "127.0.0.1"

class Cliente:

    def __init__(self):
        self.tcp_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name = ""
        
    def __call__(self):
        try:
            destination = (ADDRESS, SERVER_POST)
            self.tcp_connection.connect(destination)

            while True:
                self.name = input("Seu username: ")
                if self.name != "":
                    break

            self.tcp_connection.send(bytes(self.name, "utf-8"))
            self.escutar_resposta(self.tcp_connection)
            self.menu()

        except ConnectionError as error:
            print("Conexão encerrada\nErro:", error)
            sys.exit()

    def enviar_pedido(self, address):
        count = 1
        id_produtos = []

        while True:
            mensagem = input(f"(0 - Finalizar Pedido), id do Produto {count}: ")
            
            if mensagem == "":
                print("Insira o nome do produto que deseja comprar.")
            elif mensagem == "0":
                    pedido = {
                        "id": id_produtos
                    }
                    pedido = json.dumps(pedido)
                    print(pedido)
                    address.send(bytes(str(pedido), "utf-8"))
                    break
            elif not mensagem.isdigit():
                    print("Insira um id válido.")
            else:
                
                address.send(bytes("QTD_PRODUTOS", "utf-8"))
                resp = int(address.recv(BUFFER).decode())
                
                if int(mensagem) > resp or int(mensagem) < 1:
                    print("Insira um id válido.")
                else:
                    count += 1
                    id_produtos.append(mensagem)
    
    def escutar_resposta(self, address):
        try:
            address.settimeout(2)
            msg_recebida: str = address.recv(BUFFER).decode()

            if msg_recebida != "":
                print(msg_recebida)
        except (socket.timeout, OSError):
            pass
    
    def close_connection(self, address):
        address.send(bytes(f"{self.name}, exit", "utf-8"))
        address.close()

    def menu(self):
        while True:
            print("0 - Sair")
            print("1 - Enviar pedido")
            print("2 - Listar produtos")
            option = input("Opção: ")

            if option == "0":
                self.close_connection(self.tcp_connection)
                break
            elif option == "1":
                self.enviar_pedido(self.tcp_connection)
            elif option == "2":
                self.tcp_connection.send(bytes("LISTAR", "utf-8"))
                self.escutar_resposta(self.tcp_connection)
            else:
                print("Opção inválida")

if __name__ == "__main__":
    Cliente()()
