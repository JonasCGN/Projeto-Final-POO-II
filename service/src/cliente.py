import socket
import sys
import json
import time

SERVER_POST = 9000
BUFFER = 1024
ADDRESS = "127.0.0.1"

class Cliente:

    def __init__(self, name = '', tcp_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)):
        self.tcp_connection = tcp_connection
        self.name = name
      
        
    def __call__(self):
        try:
            destination = (ADDRESS, SERVER_POST)
            self.tcp_connection.connect(destination)

            while True:
                self.name = input("Seu username: ")
                if self.name != "":
                    break

            self.tcp_connection.send(bytes(self.name, "utf-8"))
            self.escutar_resposta()
            self.menu()

        except ConnectionError as error:
            print("Conexão encerrada\nErro:", error)
            sys.exit()

    def conectar(self, address,server_post):
        self.tcp_connection.connect((address,server_post))
        self.tcp_connection.send(bytes(self.name, "utf-8"))
        return self.escutar_resposta()
        
    def enviar_pedido(self, produtos):
        pedido = {
            "id": produtos,
            "data": time.strftime(),
            "hora": time.strftime()
        }
        
        if len(pedido) != 0:
            pedido = json.dumps(pedido)
            self.tcp_connection.send(bytes(str(pedido), "utf-8"))

        return pedido
    
    def menu_enviar_pedido(self):
        count = 1
        id_produtos = []

        while True:
            mensagem = input(f"(0 - Finalizar Pedido), id do Produto {count}: ")
            
            
            if mensagem == "":
                print("Insira o id do produto que deseja comprar.")
            elif mensagem == "0":
                    if count == 1:
                        print("Comanda inválido, reiniciando pedido.")
                        break
                    
                    pedido = {
                        "id": id_produtos,
                    }
                    
                    pedido = json.dumps(pedido)
                    print(pedido)
                    self.tcp_connection.send(bytes(str(pedido), "utf-8"))
                    break
            elif not mensagem.isdigit():
                    print("Insira um id válido.")
            else:
                self.tcp_connection.send(bytes("QTD_PRODUTOS", "utf-8"))
                resp = int(self.tcp_connection.recv(BUFFER).decode())
                
                if int(mensagem) > resp or int(mensagem) < 1:
                    print("Insira um id válido.")
                else:
                    count += 1
                    id_produtos.append(mensagem)
    
    def escutar_resposta(self):
        try:
            self.tcp_connection.settimeout(2)
            msg_recebida: str = self.tcp_connection.recv(BUFFER).decode()

            if msg_recebida != "":
                print(msg_recebida)
        except (socket.timeout, OSError):
            pass
        
        return msg_recebida
    
    def close_connection(self):
        self.tcp_connection.send(bytes(f"{self.name}, exit", "utf-8"))
        self.tcp_connection.close()

    def menu(self):
        while True:
            print("0 - Sair")
            print("1 - Enviar pedido")
            print("2 - Listar produtos")
            option = input("Opção: ")

            if option == "0":
                self.close_connection()
                break
            elif option == "1":
                self.enviar_pedido()
            elif option == "2":
                self.tcp_connection.send(bytes("LISTAR", "utf-8"))
                self.escutar_resposta()
            else:
                print("Opção inválida")

