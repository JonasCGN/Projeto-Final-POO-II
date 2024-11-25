import psycopg2

import sys
import os

# Adicione o diretório do pacote ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))


from script_redis.src.produtos_mock import Produto, Pedido

class DB_POSTGRES:
    
    def __init__(self):
        self.post_client = psycopg2.connect(host='localhost', database='database-postgres',
        user='root', password='root')
    
    def database_init(self):
        try:
            executar = self.post_client.cursor()
            executar.execute("""
                CREATE TABLE IF NOT EXISTS gerencia_pedidos (
                    id SERIAL PRIMARY KEY,
                    pedidos JSONB NOT NULL
                );
            """)
            
            print("Tabela inicializada com sucesso!")
        except Exception as e:
            print(f"Não foi possível criar a tabela: {e}")
        finally:
            if executar:
                executar.close()
            
        self.post_client.commit()
    
    def set_initial_values(self):
        executar = self.post_client.cursor()
        
        self.qtd_removidos = self.get('qtd_removidos')
        self.qtd_inseridos = self.get('qtd_inseridos')

        if self.qtd_removidos is None:
            self.insert('qtd_removidos', 0)

        if self.qtd_inseridos is None:
            self.insert('qtd_inseridos', 0)

        self.commit()
    
    def test_connection(self):
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
    
    def insert(self, pedido: Pedido):
        executar = self.post_client.cursor()
        
        executar.execute("""
                INSERT INTO gerencia_pedidos (pedidos) 
                VALUES (%s);
            """, [pedido.dump()])
        
        self.commit()

        print("Dados inseridos com sucesso!")
        
        if executar:
            executar.close()

    def increment(self, key):
        self.post_client.incr(key)

    def decrement(self, key):
        self.post_client.decr(key)

    def get(self,key):
        executar = self.post_client.cursor()
        executar.execute("SELECT * FROM gerencia_pedidos;")
        return executar.fetchall()

    def get_all(self):
        try:
            executar = self.post_client.cursor()
            executar.execute("SELECT * FROM gerencia_pedidos;")
            
            resultados = executar.fetchall()
            print("Dados consultados com sucesso!")
            
            return resultados
        except Exception as e:
            print(f"Erro ao consultar dados: {e}")
            return None
    
    def commit(self):
        self.post_client.commit()