from psycopg2.pool import ThreadedConnectionPool
from faker import Faker
from concurrent.futures import ThreadPoolExecutor
import os

# dbname='database_postgres',
# user='root',
# password='root',
# host='localhost',
# port='5432'

# Configurações do banco de dados
db_config = {
    'dbname': 'Database_BD2',
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'port': '5432'
}


fake = Faker()

# Criação do pool de conexões para I/O-bound
num_cores = os.cpu_count()  # Número de núcleos da CPU
num_threads_cpu = num_cores  # Número de threads CPU-bound
num_threads_io = num_cores * 2  # Número de threads I/O-bound
qtd_por_thread = 1_000  # Quantidade de dados por thread

# Criação do pool de conexões
connection_pool = ThreadedConnectionPool(1, num_threads_io, **db_config)

# Função para criar a tabela no banco de dados


def criar_tabela():
    """Cria a tabela Usuario, se não existir."""
    conn = connection_pool.getconn()
    cur = conn.cursor()

    cur.execute("""
                CREATE TABLE IF NOT EXISTS funcionario (
                    id SERIAL PRIMARY KEY,
                    usuario VARCHAR(255) UNIQUE,
                    senha VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL UNIQUE
                );
            """)

    cur.execute("""
                CREATE TABLE IF NOT EXISTS Pedido (
                    id SERIAL PRIMARY KEY,
                    mesa INT NOT NULL,
                    status VARCHAR(255) NOT NULL,
                    data_hora TIMESTAMP NOT NULL
                );
            """)

    cur.execute("""
                CREATE TABLE IF NOT EXISTS Produto (
                    id SERIAL PRIMARY KEY,
                    nome VARCHAR(255) UNIQUE,
                    preco DECIMAL(10, 2) NOT NULL,
                    disponivel BOOLEAN DEFAULT TRUE
                );
            """)

    cur.execute("""
                CREATE TABLE IF NOT EXISTS Produto_Pedido (
                    id SERIAL PRIMARY KEY,
                    pedido_id INT NOT NULL,
                    produto_id INT NOT NULL,
                    quantidade INT NOT NULL,
                    preco_pago DECIMAL(10, 2) NOT NULL,
                    FOREIGN KEY (pedido_id) REFERENCES Pedido (id) ON DELETE CASCADE,
                    FOREIGN KEY (produto_id) REFERENCES Produto (id) ON DELETE CASCADE
                );
            """)

    conn.commit()
    cur.close()
    connection_pool.putconn(conn)

# Função para inserir dados no banco usando uma conexão do pool


def inserir_dados_pool(dados_funcionario, dados_pedido, dados_produto, dados_pedido_produto):
    """Insere dados no banco usando uma conexão do pool."""
    # conn = connection_pool.getconn()
    # try:
    #     cur = conn.cursor()
    #     cur.executemany("""
    #         INSERT INTO my_table (nome, idade, descricao_tsv, texto, data)
    #         VALUES (%s, %s, to_tsvector(%s), %s, %s)
    #     """, dados)
    #     conn.commit()
    #     cur.close()
    # except Exception as e:
    #     print(f"Erro ao inserir dados: {e}")
    #     conn.rollback()
    # finally:
    #     connection_pool.putconn(conn)

    conn = connection_pool.getconn()
    cur = conn.cursor()
    try:
        cur.executemany("""
            INSERT INTO funcionario (usuario, senha, email)
            VALUES (%s, %s, %s)
        """, dados_funcionario)

        cur.executemany("""
            INSERT INTO Pedido (mesa, status, data_hora)
            VALUES (%s, %s, %s)
        """, dados_pedido)

        cur.executemany("""
            INSERT INTO Produto (nome, preco, disponivel)
            VALUES (%s, %s, %s)
        """, dados_produto)

        cur.executemany("""
            INSERT INTO Produto_Pedido (pedido_id, produto_id, quantidade, preco_pago)
            VALUES (%s, %s, %s, %s)
        """, dados_pedido_produto)

        conn.commit()
    except Exception as e:
        print(f"Erro ao inserir dados: {e}")
        conn.rollback()
    finally:
        cur.close()
        connection_pool.putconn(conn)

# Função para gerar dados com Faker (CPU-bound)
def pegar_qtd_produto() -> int:
    conn = connection_pool.getconn()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM Produto")
    qtd_produto = cur.fetchone()[0]
    cur.close()
    connection_pool.putconn(conn)
    return qtd_produto

def pegar_qtd_pedido() -> int:
    conn = connection_pool.getconn()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM Pedido")
    qtd_pedido = cur.fetchone()[0]
    cur.close()
    connection_pool.putconn(conn)
    return qtd_pedido
  

def get_preco_produto(produto_id: int) -> float:
    conn = connection_pool.getconn()
    cur = conn.cursor()
    cur.execute("SELECT preco FROM Produto WHERE id = %s", (produto_id,))
    preco = cur.fetchone()[0]
    cur.close()
    connection_pool.putconn(conn)
    return preco
  


def gerar_dados(qtd_funcionario, qtd_pedido, qtd_produto, qtd_pedido_produto):
    """Gera dados usando Faker para inserção no banco."""

    # elementos = []
    # for _ in range(qtd):
    #     description = fake.text()
    #     elementos.append((fake.name(), fake.random_int(
    #         0, 100), description, description, fake.date()))
    # return elementos

    dados_funcionario = [(fake.user_name(), fake.password(), fake.email())
                         for _ in range(qtd_funcionario)]
    dados_pedido = [(fake.random_int(1, 10), fake.random_element(["Pedido em andamento", "Entregar",
                     "Pedido cancelado", "Pedido finalizado"]), fake.date_time_this_year()) for _ in range(qtd_pedido)]
    dados_produto = [(fake.word(), fake.random_int([10, 1000]), fake.boolean())
                     for _ in range(qtd_produto)]
    dados_pedido_produto = [(fake.random_int(pegar_qtd_pedido()), fake.random_int(pegar_qtd_produto()), fake.random_int(), 

# Função para gerenciar a geração e inserção dos dados em paralelo


def inserir_infinitamente():
    """Insere dados infinitamente utilizando dois pools de threads."""
    with ThreadPoolExecutor(max_workers=num_threads_cpu) as executor_cpu, ThreadPoolExecutor(max_workers=num_threads_io) as executor_io:
        while True:
            # Gera os dados utilizando as threads CPU-bound
            futuros_dados = [executor_cpu.submit(
                gerar_dados, qtd_por_thread) for _ in range(num_threads_io)]
            dados = [futuro.result() for futuro in futuros_dados]

            # Envia os dados para o banco usando as threads I/O-bound
            futuros_insercao = [executor_io.submit(
                inserir_dados_pool, dados[i]) for i in range(num_threads_io)]
            for futuro in futuros_insercao:
                try:
                    futuro.result()  # Espera a inserção ser concluída
                except Exception as e:
                    print(f"Erro na inserção de dados: {e}")


if __name__ == "__main__":
    try:
        print("Criando a Tabela...")
        criar_tabela()
        # print("Iniciando inserções em massa...")
        # inserir_infinitamente()
    except KeyboardInterrupt:
        print("\nInterrompido pelo usuário.")
    finally:
        # Fecha todas as conexões do pool
        if connection_pool:
            connection_pool.closeall()
        print("Conexões fechadas.")
