"""
Módulo para a implementação do cliente de sincronização.
"""

import socket
import threading
from typing import Callable


class ErroCliente(Exception):
    """
    Exceção para erros relacionados ao cliente de sincron
    """
    pass


class ClienteSincronizado:
    """
    Classe para implementação do cliente de sincronização.
    """
    
    def __init__(self, endereco: str = "localhost", porta: int = 12345, tamanho_buffer: int = 1024) -> None:
        """
        Inicializa o cliente de sincronização.

        Args:
            endereco (str, optional):  Endereço do servidor para conexão. Defaults to "localhost".
            porta (int, optional): Porta do servidor para conexão. Defaults to 12345.
            tamanho_buffer (int, optional): Tamanho do buffer para recebimento de mensagens. Defaults to 1024.
            
        """
        self.endereco = endereco
        self.porta = porta
        self.tamanho_buffer = tamanho_buffer
        self.soket_cliente = None
        self.executando = False
        self.thread_escuta = None

    def iniciar(self, ao_receber_mensagem: Callable[[str], None]):
        """
        Inicia a conexão com o servidor.

        Args:
            ao_receber_mensagem (Callable[[str], None]): Função de callback para receber mensagens do servidor.

        Raises:
            ErroCliente: O cliente já está conectado.
        """
        if self.executando:
            raise ErroCliente("O cliente já está conectado.")

        self.executando = True
        try:
            self.soket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.soket_cliente.connect((self.endereco, self.porta))
            print(f"[LOG INFO] Conectado ao servidor em {self.endereco}:{self.porta}")

            self.thread_escuta = threading.Thread(target=self._escutar, args=(ao_receber_mensagem,), daemon=True)
            self.thread_escuta.start()
        except Exception as e:
            self.executando = False
            raise ErroCliente(f"Erro ao conectar ao servidor: {e}")

    def _escutar(self, ao_receber_mensagem: Callable[[str], None]) -> None:
        """
        Função interna para escutar mensagens do servidor.

        Args:
            ao_receber_mensagem (Callable[[str], None]): Função de callback para receber mensagens do servidor.
        """
        try:
            while self.executando:
                try:
                    dados = self.soket_cliente.recv(self.tamanho_buffer)
                    if not dados:
                        print("[LOG INFO] Conexão com o servidor encerrada.")
                        break

                    mensagem = dados.decode("utf-8").strip()
                    print(f"[LOG INFO] Mensagem recebida do servidor: {mensagem}")
                    ao_receber_mensagem(mensagem)

                except ConnectionResetError:
                    print("[LOG ERRO] Conexão perdida com o servidor.")
                    break
                except Exception as e:
                    print(f"[LOG ERRO] Erro ao processar mensagem: {e}")
        finally:
            self.parar()

    def enviar_mensagem(self, mensagem: str) -> None:
        """
        Envia uma mensagem para o servidor.
        
        Args:
            mensagem (str): Mensagem a ser enviada.
        """
        if not self.executando or not self.soket_cliente:
            raise ErroCliente("O cliente não está conectado.")
        try:
            self.soket_cliente.sendall(mensagem.encode("utf-8"))
            print(f"[LOG INFO] Mensagem enviada: {mensagem}")
        except Exception as e:
            raise ErroCliente(f"Erro ao enviar mensagem: {e}")

    def parar(self) -> None:
        """
        Encerra a conexão com o servidor.
        """
        self.executando = False
        if self.soket_cliente:
            try:
                self.soket_cliente.close()
                print("[LOG INFO] Conexão encerrada.")
            except Exception as e:
                print(f"[LOG ERRO] Erro ao fechar a conexão: {e}")
