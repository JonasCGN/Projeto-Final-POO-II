"""
Script: cliente.py
Descrição: Este script define a classe Cliente, responsável por estabelecer uma conexão TCP com um servidor, listar produtos disponíveis e enviar pedidos de compra.

Funcionalidades:
- Conectar ao servidor.
- Listar produtos disponíveis.
- Enviar pedidos de compra.
- Interagir por meio de um menu.

Requisitos:
- Python 3.x
- Módulos padrão: socket, json, sys, time

Como usar:
1. Inicie o script.
2. Quando solicitado, insira seu nome de usuário.
3. O menu de opções será exibido:
   - 0: Sair e encerrar a conexão.
   - 1: Enviar um pedido ao servidor.
   - 2: Listar produtos disponíveis no servidor.
4. Para enviar um pedido, insira os IDs dos produtos.
5. Para sair, selecione a opção 0.
"""
import socket
import sys
import json
import time

SERVER_POST = 9000
BUFFER = 1024
ADDRESS = "127.0.0.1"

class Cliente:
    """
    Classe que representa um cliente que interage com um servidor TCP.
    
    Atributos:
        name (str): O nome do cliente, usado para identificá-lo.
        tcp_connection (socket.socket): A conexão TCP do cliente com o servidor.
        buffer_size (int): O tamanho do buffer de recepção de dados.
    """
    

    def __init__(self, name = '', tcp_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)):
        """
        Construtor da classe Cliente.

        Parâmetros:
            name (str): O nome do cliente, usado para identificá-lo.
            tcp_connection (socket.socket): A conexão TCP do cliente com o servidor.
            buffer_size (int): O tamanho do buffer de recepção de dados.

        Retorna:    
            Nenhum.
            
        """
        self.tcp_connection = tcp_connection
        self.name = name
      
        
    def __call__(self):
        """
         Método que inicia a conexão do cliente com o servidor e executa o menu de interação com o servidor.

         Parâmetros:
            Nenhum.
        
        Retorna:
            Uma string com a resposta do servidor.
         """

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
        """
         Método que estabelece uma conexão com um servidor TCP.

        Este método conecta o cliente ao servidor especificado por meio do endereço IP e da porta. 
        Após estabelecer a conexão, o nome do cliente é enviado ao servidor e o método 
        aguarda a resposta utilizando `escutar_resposta`.

        Parâmetros:
            address (str): O endereço IP do servidor.
            server_port (int): A porta do servidor.

        Retorna:
            str: A resposta recebida do servidor após a conexão.
        
        Comportamento:
            1. Estabelece uma conexão com o servidor especificado.
            2. Envia o nome do cliente para o servidor.
            3. Retorna a resposta do servidor, capturada pelo método `escutar_resposta`.


        """
        self.tcp_connection.connect((address,server_post))
        self.tcp_connection.send(bytes(self.name, "utf-8"))
        return self.escutar_resposta()
   
        
    def enviar_pedido(self, produtos):
        """
            Método responsável por enviar um pedido ao servidor.

            Este método formata os dados do pedido em um dicionário, incluindo os IDs dos produtos, 
            a data e a hora da solicitação. Em seguida, os dados são convertidos para o formato JSON 
            e enviados ao servidor através de uma conexão TCP.

            Parâmetros:
                produtos (list): Lista contendo os IDs dos produtos que compõem o pedido.

            Retorna:
                dict: Um dicionário com os dados do pedido caso o envio seja bem-sucedido.
                None: Retorna `None` caso não seja possível enviar o pedido ou se a lista de produtos estiver vazia.

            Comportamento:
                1. Verifica se a lista de produtos está vazia.
                2. Cria um dicionário contendo:
                    - "id": Lista de IDs dos produtos.
                    - "data": Data atual no formato "YYYY-MM-DD".
                    - "hora": Hora atual no formato "HH:MM:SS".
                3. Converte o dicionário para uma string JSON e o envia ao servidor.
                4. Retorna o dicionário do pedido em caso de sucesso ou `None` em caso de erro.

            Exceções Tratadas:
                - Exception: Captura qualquer erro durante a conversão ou envio do JSON, exibe uma mensagem 
                de erro e retorna `None`.
        """
        if not produtos:
            print("não chegou o pedido aqui")
            return None
        ids = json.loads(produtos)
        pedido = {
            "id": ids,
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
        """
        Método responsável por executar o menu de envio de pedidos ao servidor.

        O método permite que o usuário insira os IDs dos produtos que deseja comprar. 
        Ele solicita repetidamente IDs de produtos até que o usuário insira `0`, 
        indicando a finalização do pedido. Durante o processo, o método realiza 
        validações das entradas e se comunica com o servidor para garantir a validade dos IDs.

        Parâmetros:
            Nenhum.

        Retorna:
            dict: Um dicionário contendo os dados do pedido caso produtos tenham sido adicionados.
            None: Retorna `None` caso o usuário não adicione nenhum produto ou em caso de erro.
        
        Comportamento:
            1. Solicita IDs de produtos ao usuário, validando se as entradas são números.
            2. Comunica-se com o servidor para obter a quantidade total de produtos disponíveis.
            3. Garante que os IDs informados estão no intervalo válido (1 até a quantidade máxima de produtos).
            4. Adiciona os IDs válidos a uma lista de produtos.
            5. Retorna os produtos selecionados ao final ou exibe mensagens informativas em caso de erro.

        Exceções Tratadas:
            - Exception: Captura erros de comunicação com o servidor e retorna `None` com uma mensagem de erro.
        """
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

        """
        Método que escuta a resposta do servidor.

        Este método aguarda uma mensagem do servidor através da conexão TCP. Ele define 
        um timeout para evitar bloqueios indefinidos e retorna a mensagem recebida.

        Parâmetros:
            Nenhum.

        Retorna:
            str: A mensagem recebida do servidor.
            None: Caso nenhuma mensagem seja recebida ou ocorra uma exceção.

        Comportamento:
            1. Define um timeout de 2 segundos para a conexão TCP.
            2. Tenta receber e decodificar a mensagem do servidor.
            3. Se a mensagem recebida não for vazia, exibe-a no console.
            4. Ignora exceções relacionadas a timeout ou falhas de conexão sem encerrar o programa.

        Exceções Tratadas:
            - `socket.timeout`: Caso o tempo limite de espera seja excedido.
            - `OSError`: Para erros gerais relacionados à comunicação via socket.

        Observações:
            - Caso nenhuma mensagem seja recebida ou ocorra um erro, o método retornará `None`.

        """

        try:
            self.tcp_connection.settimeout(2)
            msg_recebida: str = self.tcp_connection.recv(BUFFER).decode()

            if msg_recebida != "":
                print(msg_recebida)
        except (socket.timeout, OSError):
            pass
        
        return msg_recebida
    
    def close_connection(self):
        """
        Método que fecha a conexão do cliente com o servidor.

        Este método envia uma mensagem ao servidor indicando que o cliente está encerrando 
        a conexão e, em seguida, fecha a conexão TCP.

        Parâmetros:
            Nenhum.

        Comportamento:
            1. Envia uma mensagem formatada com o nome do cliente e o comando "exit" ao servidor.
            2. Fecha a conexão TCP utilizando `close()`.

        Observações:
            - É importante garantir que o método seja chamado quando o cliente não 
            precisar mais se comunicar com o servidor, para evitar conexões abertas desnecessárias.
            - Caso o envio da mensagem falhe, o fechamento da conexão ainda será realizado.
        
        """

        self.tcp_connection.send(bytes(f"{self.name}, exit", "utf-8"))
        self.tcp_connection.close()

    def menu(self):
        """
        Método que apresenta o menu principal para o cliente.

        Este método exibe opções para interação com o servidor, como envio de pedidos e listagem de produtos, 
        permitindo ao cliente escolher ações específicas. O loop continua até que a opção de sair seja selecionada.

        Parâmetros:
            Nenhum.

        Comportamento:
            1. Exibe as opções disponíveis no menu:
                - 0: Sair e encerrar a conexão.
                - 1: Enviar um pedido ao servidor.
                - 2: Listar os produtos disponíveis no servidor.
            2. Solicita a entrada do usuário para selecionar uma opção.
            3. Executa a ação correspondente com base na opção escolhida:
                - "0": Chama `close_connection` para encerrar a conexão e finaliza o loop.
                - "1": Chama `menu_enviar_pedido` para iniciar o processo de envio de pedido.
                - "2": Envia o comando "LISTAR" ao servidor e chama `escutar_resposta` para exibir a resposta.
            4. Trata entradas inválidas exibindo uma mensagem de erro.

        Observações:
            - A opção "LISTAR" depende de uma implementação no servidor que responde ao comando com a lista de produtos.

        Exemplo de Uso:
            cliente.menu()
        """


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

