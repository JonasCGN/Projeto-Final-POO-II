"""
Modulo responsável pela adiministração do banco de dados dos funcionários.
"""

import random
import string
from .bd_postgree_base import Bd_Base
from typing import Tuple, Union
import json
from passlib.hash import pbkdf2_sha256 # type: ignore

class BdFuncionario(Bd_Base):
    """
    Classe para manipulação de dados da tabela funcionario no banco de dados PostgreSQL
    """

    def __init__(self, host: str = 'localhost', database: str = 'database-postgres', user: str = 'root', password: str = 'root') -> None:
        """
        Inicializa a conexão com o banco de dados, e cria a tabela funcionario caso não exista.
        """ 
        super().__init__(host, database, user, password)
        self.database_init()

    def database_init(self) -> None:
        """
        Inicia a estrutura do banco de dados, criando a tabela funcionario caso não exista.
        """
        try:
            cursor = self.get_cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS funcionario (
                    id SERIAL PRIMARY KEY,
                    usuario VARCHAR(255) UNIQUE,
                    senha VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL
                );
            """)

            self.commit()
        except Exception as e:
            print(f"[LOG ERRO] Não foi possível criar a tabela: {e}")
        finally:
            cursor.close()

    def _format_from_inserct(self, funcionario: str) -> dict:
        """
        Formata os dados para inserção no banco de dados.

        Args:
            funcionario (str): Dados do funcionario em formato JSON.

        Returns:
            dict: Dicionário com os dados formatados.
        """
        valor =  json.loads(funcionario)
        valor["senha"] = pbkdf2_sha256.hash(valor["senha"])
        return (valor['usuario'], valor["senha"], valor["email"])

    def insert_funcionario(self, funcionario: str) -> bool:
        """
        Insere um funcionario no banco de dados.
        
        Args:
            funcionario (str): Dados do funcionario em formato JSON.
        
        Returns:
            bool: True se a inserção foi bem sucedida, False caso contrário.
        """
        retorno = True
        try:
            valor = self._format_from_inserct(funcionario)
            query = """
                INSERT INTO funcionario (usuario, senha, email)
                VALUES (%s, %s, %s)
            """
            cursor = self.get_cursor()
            cursor.execute(query, valor)
            self.commit()
            
        except Exception as e:
            print("[LOG ERRO] Erro ao inserir funcionario: ", e)
            self.post_client.rollback()
            retorno = False
        finally:
            cursor.close()

        return retorno

    def validar_acesso(self, usuario: str, senha: str) -> bool:
        """
        Valida o acesso de um funcionario no banco de dados.
        
        Args:
            usuario (str): Nome de usuario do funcionario.
            senha (str): Senha do funcionario.
        
        Returns:
            bool: True se o acesso foi validado, False caso contrário.
        """
        
        retorno = False
        try:
            query = """
                SELECT * FROM funcionario 
                WHERE usuario = %s
            """
            cursor = self.get_cursor()
            cursor.execute(query, (usuario,))
            resultado = cursor.fetchone()
            
            if resultado:
                retorno = pbkdf2_sha256.verify(senha, resultado[2])  
               
            
        except Exception as e:
            print("[LOG ERRO] Erro ao validar acesso: ", e)
        finally:
            cursor.close()

        return retorno

    def recuperar_senha_usuario(self, email: str) -> Union[Tuple[str, str], bool]:
        """
        Gera uma nova senha para um funcionário e atualiza no banco.
        
        Args:
            email (str): Email do funcionário.
        
        Returns:
            Union[str, bool]: Nova senha gerada se o funcionário for encontrado, False caso contrário.
        """
        
        nova_senha = ''.join(random.choices(string.ascii_letters + string.digits, k=8))  # Gera senha aleatória de 8 caracteres
        hash_senha = pbkdf2_sha256.hash(nova_senha)
        retorno = False

        try:
            query_select = """
                SELECT * FROM funcionario
                WHERE email = %s
            """
            query_update = """
                UPDATE funcionario
                SET senha = %s
                WHERE email = %s
            """
            cursor = self.get_cursor()
            cursor.execute(query_select, (email,))
            resultado = cursor.fetchone()
            
            if resultado:
                cursor.execute(query_update, (hash_senha, email))
                self.commit() 
                retorno = (resultado[1], nova_senha)
            
        except Exception as e:
            print("[LOG ERRO] Erro ao recuperar senha: ", e)
        finally:
            if cursor:
                cursor.close()

        return retorno

