
"""
Este módulo gerencia a conexão com o banco de dados PostgreSQL e operações relacionadas a pedidos.
Classes:
    DB_POSTGRES: Classe responsável pela conexão com o PostgreSQL e gerenciamento de pedidos.

Execução:
    A classe DB_POSTGRES realiza a conexão com o banco de dados, inicializa a tabela de pedidos, insere novos pedidos,
    consulta pedidos existentes e executa transações.
"""

from typing import Union
import psycopg2  # type: ignore
from time import sleep
import os
import json
from datetime import datetime


class DB_POSTGRES:
    '''
    Classe DB_POSTGRES para gerenciar a conexão e operações com um banco de dados PostgreSQL.
    Métodos:
        __init__:
            Inicializa a conexão com o banco de dados PostgreSQL. Tenta conectar repetidamente até obter sucesso.
        database_init:
            Inicializa a tabela 'gerencia_pedidos' no banco de dados, se ela não existir.
        test_connection:
            Testa a conexão com o banco de dados PostgreSQL e retorna True se a conexão for bem-sucedida, 
            caso contrário, retorna False.
        insert:
            Insere um pedido no banco de dados.
                pedido (str): Pedido em formato JSON.
        get:
            Retorna um pedido específico do banco de dados com base no ID fornecido.
                id (int): ID do pedido a ser consultado.
        get_all:
            Retorna todos os pedidos do banco de dados.
        commit:
            Realiza o commit das transações pendentes no banco de dados.
   '''

    def __init__(self) -> None:
        """
        Inicializa uma instância da classe e tenta conectar ao banco de dados PostgreSQL.

        Este método tenta continuamente estabelecer uma conexão com o banco de dados PostgreSQL
        usando as credenciais fornecidas. Se a conexão falhar, ele espera 2 segundos antes de tentar novamente.

        Variáveis de ambiente:
            HOST_TO_POSTGRES: O endereço do host do PostgreSQL (padrão: 'localhost').

        Exceções:
            psycopg2.OperationalError: Lançada se não for possível conectar ao PostgreSQL.

        Saída:
            Mensagem de sucesso ao conectar ao PostgreSQL ou mensagem de erro e tentativa de reconexão.
        """
        while True:
            try:
                post_host = os.getenv('HOST_TO_POSTGRES', 'localhost')
                self.post_client = psycopg2.connect(host=post_host, database='database-postgres',
                                                    user='root', password='root')
                print(f"Conectado ao PostgreSQL em {post_host}...")
                break
            except psycopg2.OperationalError:
                print("Não foi possível conectar ao PostgreSQL. Tentando novamente em 2 segundos...")
                sleep(2)
                continue

        self.cursor_inserct = self.post_client.cursor()

    def database_init(self) -> None:
        """
        Inicializa a tabela 'gerencia_pedidos' no banco de dados PostgreSQL.
        A tabela 'gerencia_pedidos' possui as seguintes colunas:
        - id: Chave primária do tipo SERIAL.
        - pedidos: Array de inteiros que não pode ser nulo.
        - data: Data do pedido que não pode ser nula.
        - hora: Hora do pedido que não pode ser nula.
        Em caso de sucesso, uma mensagem de confirmação será impressa.
        Em caso de falha, uma mensagem de erro será impressa com a descrição da exceção.
        A conexão com o banco de dados é fechada no bloco 'finally' e a transação é confirmada após a execução do
        comando.
        Raises:
            Exception: Se ocorrer um erro durante a criação da tabela.
        """
        try:
            executar = self.post_client.cursor()
            executar.execute("""
                CREATE TABLE IF NOT EXISTS gerencia_pedidos (
                    id SERIAL PRIMARY KEY,
                    pedidos INTEGER[] NOT NULL,
                    data DATE NOT NULL,
                    hora TIME NOT NULL
                );
            """)
            
            self.commit()
            print("Tabela inicializada com sucesso!")
        except Exception as e:
            print(f"Não foi possível criar a tabela: {e}")

    def test_connection(self) -> bool:
        """
        Testa a conexão com o banco de dados PostgreSQL.
        Tenta criar um cursor e executar um comando SQL para obter a versão do PostgreSQL.
        Se a conexão for bem-sucedida, imprime a versão do PostgreSQL e retorna True.
        Caso contrário, imprime uma mensagem de erro e retorna False.
        Returns:
            bool: True se a conexão for bem-sucedida, False caso contrário.
        """
        retorno = False
        try:
            executar = self.post_client.cursor()

            executar.execute("SELECT version();")
            versao = executar.fetchone()

            print(f"Conectado ao PostgreSQL. Versão: {versao}")
            retorno = True
        except Exception as e:
            print(f"Não foi possível conectar ao PostgreSQL: {e}")
        finally:
            if executar:
                executar.close()

        return retorno

    def insert(self, pedido: str) -> bool:
        retorno = False
        try:
            pedido = json.loads(pedido)
            data_datetime = datetime.strptime(pedido['data'], '%Y-%m:%d').date()

            query = """
                INSERT INTO gerencia_pedidos (pedidos, data, hora) 
                VALUES (%s, %s, %s)
            """
            valores = [pedido['pedidos'], data_datetime, pedido['hora']]
            self.cursor_de_insercao.execute(query, valores)

            retorno = True
        except Exception as e:
            print(f"Erro ao inserir dados: {e}")
            self.post_client.rollback()

        return retorno

    def get(self, id: int) -> Union[tuple, None]:
        """
        Recupera um registro da tabela 'gerencia_pedidos' com base no ID fornecido.
        Args:
            id (int): O ID do registro a ser recuperado.
        Returns:
            tuple: Uma tupla contendo os dados do registro, ou None se ocorrer um erro.
        Raises:
            Exception: Se ocorrer um erro durante a consulta ao banco de dados.
        """
        try:
            executar = self.post_client.cursor()
            executar.execute("SELECT * FROM gerencia_pedidos WHERE id = %s;", [id])
            resultado = executar.fetchone()

            return resultado
        except Exception as e:
            print(f"Erro ao consultar dados: {e}")
            return None

    def get_all(self) -> Union[list, None]:
        """
        Recupera todos os registros da tabela 'gerencia_pedidos' no banco de dados PostgreSQL.
        Retorna:
            list: Uma lista de tuplas contendo todos os registros da tabela 'gerencia_pedidos'.
            None: Se ocorrer um erro durante a consulta.
        Exceções:
            Exception: Captura qualquer exceção que ocorra durante a execução da consulta SQL e imprime uma mensagem
            de erro.
        """
        try:
            executar = self.post_client.cursor()
            executar.execute("SELECT * FROM gerencia_pedidos;")

            resultados = executar.fetchall()
            print("Dados consultados com sucesso!")

            return resultados
        except Exception as e:
            print(f"Erro ao consultar dados: {e}")
            return None
    
    def start_cursor(self) -> None:
        """
        Inicia um novo cursor para executar operações no banco de dados PostgreSQL.
        """
        self.cursor_de_insercao = self.post_client.cursor()
    
    def close_cursor(self) -> None:
        """
        Fecha o cursor atual e descarta todas as operações pendentes.
        """
        self.cursor_de_insercao.close()


    def commit(self) -> None:
        """
        Confirma as transações pendentes no banco de dados PostgreSQL.

        Este método envia todas as operações pendentes para o banco de dados,
        garantindo que todas as alterações sejam salvas permanentemente.

        Raises:
            Exception: Se ocorrer um erro durante a confirmação das transações.
        """
        self.post_client.commit()
