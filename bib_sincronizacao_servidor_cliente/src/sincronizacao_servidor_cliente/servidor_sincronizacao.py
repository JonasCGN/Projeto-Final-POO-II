"""
Módulo para implementação do servidor de sincronização.
"""

import socket
import threading
from typing import Callable

class ErroServidor(Exception):
    """
    Exceção para erros relacionados ao servidor de sincronização.
    """
    pass


class ServidorSincronizacao:
    """
    Classe para implementação do servidor de sincronização.
    """
    
    def __init__(self, host: str = "localhost", porta: int = 12345, tamanho_buffer: int = 1024) -> None:
        """
        Inicializa o servidor de sincronização.
        
        Args:
            host (str, optional): Endereço do servidor para conexão. Defaults to "localhost".
            porta (int, optional): Porta do servidor para conexão. Defaults to 12345.
            tamanho_buffer (int, optional): Tamanho do buffer para recebimento de mensagens. Defaults to 1024.
        """
        self.host = host
        self.porta = porta
        self.tamanho_buffer = tamanho_buffer
        self.servidor_socket = None
        self.executando = False
        self.manipuladores_clientes = []
        self.sockets_enderecos_clientes = []

    def iniciar(self, ao_receber_mensagem: Callable[[str, tuple], None]) -> None:
        """
        Inicia o servidor de sincronização.
        
        Args:
            ao_receber_mensagem (Callable[[str, tuple], None]): Função de callback para receber mensagens dos clientes.
        
        Raises:
            ErroServidor: O servidor já está em execução.
        """
        if self.executando:
            raise ErroServidor("O servidor já está em execução.")

        self.executando = True
        try:
            self._iniciar_servidor()
            self._aceitar_conexoes(ao_receber_mensagem)
        except Exception as e:
            raise ErroServidor(f"Erro ao iniciar o servidor: {e}")

    def _iniciar_servidor(self) -> None:
        """
        Inicia o servidor.
        """
        self.servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.servidor_socket.bind((self.host, self.porta))
        self.servidor_socket.listen()
        print(f"[LOG INFO] Servidor iniciado em {self.host}:{self.porta}...")

    def _aceitar_conexoes(self, ao_receber_mensagem: Callable) -> None:
        """
        Aceita conexões de clientes.
        
        Args:
            ao_receber_mensagem (Callable): Função de callback para receber mensagens dos clientes.
        """
        while self.executando:
            try:
                cliente_socket, endereco = self.servidor_socket.accept()
                print(f"[LOG INFO] Nova conexão de {endereco}")
                thread_handler = threading.Thread(
                    target=self._gerenciar_cliente,
                    args=(cliente_socket, endereco, ao_receber_mensagem),
                    daemon=True
                )
                thread_handler.start()
                self.manipuladores_clientes.append(thread_handler)
                self.sockets_enderecos_clientes.append((cliente_socket, endereco))
            except Exception as e:
                print(f"[LOG ERRO] Erro ao aceitar conexão: {e}")

    def parar(self) -> None:
        """
        Para o servidor de sincronização.
        """
        self.executando = False
        if self.servidor_socket:
            self._fechar_socket_servidor()
        self._aguardar_manipuladores_clientes()

    def _fechar_socket_servidor(self) -> None:
        """
        Fecha o socket do servidor.
        """
        try:
            self.servidor_socket.close()
            print("[LOG INFO] Servidor encerrado.")
        except Exception as e:
            print(f"[LOG ERRO] Erro ao fechar o servidor: {e}")

    def _aguardar_manipuladores_clientes(self) -> None:
        """
        Aguarda o término das threads de manipulação de clientes.
        """
        
        for manipulador in self.manipuladores_clientes:
            manipulador.join()

    def _gerenciar_cliente(self, cliente_socket: socket.socket, endereco: tuple, ao_receber_mensagem: Callable) -> None:
        """
        Gerencia a comunicação com um cliente.
        
        Args:
            cliente_socket (socket.socket): Socket do cliente.
            endereco (tuple): Endereço do cliente.
            ao_receber_mensagem (Callable): Função de callback para receber mensagens do cliente.
        """
        
        print(f"[LOG INFO] Thread iniciada para o cliente {endereco}")
        try:
            with cliente_socket:
                while self.executando:
                    self._receber_e_processar_mensagem(cliente_socket, endereco, ao_receber_mensagem)
                    
        except ConnectionError:
            print(f"[LOG INFO] Cliente {endereco} desconectou.")
        except Exception as e:
            print(f"[LOG ERRO] Erro na comunicação com o cliente {endereco}: {type(e).__name__} - {e}")
        finally:
            print(f"[LOG INFO] Thread finalizada para o cliente {endereco}")
        
        self.remover_cliente(endereco)

    def _receber_e_processar_mensagem(self, cliente_socket: socket.socket, endereco: tuple, ao_receber_mensagem: Callable) -> None:
        """
        Recebe e processa uma mensagem do cliente.
        
        Args:
            cliente_socket (socket.socket): Socket do cliente.
            endereco (tuple): Endereço do cliente.
            ao_receber_mensagem (Callable): Função de callback para receber mensagens do cliente.
        """
        
        dados = cliente_socket.recv(self.tamanho_buffer)
        if not dados:
            raise ConnectionError("Desconectado")

        mensagem = dados.decode("utf-8")
        print(f"[LOG INFO] Mensagem recebida de {endereco}: {mensagem}")
        ao_receber_mensagem(mensagem)
        
    def enviar_msg_para_todos_clientes(self, mensagem: str) -> None:
        """
        Envia uma mensagem para todos os clientes conectados.
        
        Args:
            mensagem (str): Mensagem a ser enviada.
        """
        
        for socket_endereco in self.sockets_enderecos_clientes:
            self._enviar_mensagem_para_cliente(socket_endereco[0], socket_endereco[1], mensagem)

    def _enviar_mensagem_para_cliente(self, cliente_socket: socket.socket, endereco: tuple, mensagem: str) -> None:
        """
        Envia uma mensagem para um cliente.
        
        Args:
            cliente_socket (socket.socket): Socket do cliente.
            endereco (tuple): Endereço do cliente.
            mensagem (str): Mensagem a ser enviada.
        """
        try:
            cliente_socket.sendall(mensagem.encode("utf-8"))
            print(f"[LOG INFO] Mensagem enviada para {endereco}: {mensagem}")
        except Exception as e:
            print(f"[LOG ERRO] Erro ao enviar mensagem para {endereco}: {type(e).__name__} - {e}")

    def remover_cliente(self, endereco: tuple) -> None:
        """
        Remove um cliente da lista de clientes.
        
        Args:
            endereco (tuple): Endereço do cliente a ser removido.
        """
        
        cliente_removido = False
        for socket_cliente, endereco_cliente in self.sockets_enderecos_clientes:
            if endereco_cliente == endereco:
                try:
                    socket_cliente.close()
                    print(f"[LOG INFO] Cliente {endereco_cliente} desconectado e removido.")
                    cliente_removido = True
                except Exception as e:
                    print(f"[LOG ERRO] Erro ao remover cliente {endereco_cliente}: {type(e).__name__} - {e}")
                finally:
                    self.sockets_enderecos_clientes.remove((socket_cliente, endereco_cliente))
                break
        
        if not cliente_removido:
            print(f"[LOG ERRO] Cliente {endereco} não encontrado para remoção.")
