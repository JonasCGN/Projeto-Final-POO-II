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
        if not produtos:
            print("não chegou o pedido aqui")
            return None
        pedido = {
            "id": produtos,
            "data": time.strftime("%Y-%m-%d"),
            "hora": time.strftime("%H:%M:%S")
        }
        
        try: 
            pedido_json = json.dumps(pedido)
            self.tcp_connection.send(pedido_json.encode("utf-8"))
            print("Pedido enviado com sucesso")
        except Exception as e: 
            print("Erro ao enviar pedido")
            return None
        return pedido
    
    def menu_enviar_pedido(self):
        count = 1
        id_produtos = []

        while True:
            mensagem = input(f"(0 - Finalizar Pedido), id do Produto {count}: ")
            
            #validar entrada 
            if not mensagem: 
               print("insira o id do produto que deseja comprar")
               continue
            if mensagem =="0": 
                if count ==1:
                    print("Pedido invalido. Nenhum produto add")
                    return None
                else: 
                    print("finalizando pedido hehhe")
                    break
            if not mensagem.isdigit(): 
                print("insira um id valido(numero)")
                continue
            # ver o numero de produtos que tem 
            try:
                self.tcp_connection.send(b"QTD_PRODUTOS")
                resposta = self.tcp_connection.recv(self.buffer_size).decode("utf-8")
                
                if not resposta.isdigit(): 
                    print("erro ao obter a quant de produtos")
                    continue
                
                qtd_produtos = int(resposta)
                produto_id = int(mensagem)
                
                if produto_id < 1 or produto_id > qtd_produtos:
                        print(f"Insira um ID válido (1 a {qtd_produtos}).")
                        continue
                #add produto ao pedido 
                id_produtos.append(produto_id)
                print(f"Produto {produto_id} adicionado ao pedido")
                count += 1 
            except Exception as e: 
                print(f"erro na comunicação com o server: {e}")
                return None
        return self.enviar_pedido(id_produtos)
            
            
    
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
                self.menu_enviar_pedido()
            elif option == "2":
                self.tcp_connection.send(bytes("LISTAR", "utf-8"))
                self.escutar_resposta()
            else:
                print("Opção inválida")

