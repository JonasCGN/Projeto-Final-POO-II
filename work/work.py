from psycopg2.pool import ThreadedConnectionPool
from faker import Faker
from concurrent.futures import ThreadPoolExecutor
import os

# Configurações do banco de dados
DB_CONFIG = {
    'dbname': 'database_postgres',
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'port': '5432'
}

fake = Faker()
NUM_CORES = os.cpu_count()
NUM_THREADS_IO = NUM_CORES * 2

connection_pool = ThreadedConnectionPool(1, NUM_CORES, **DB_CONFIG)

# Funções auxiliares
def executar_query(query, params=None, fetch=False):
    """Executa uma query no banco de dados com suporte a transações."""
    with connection_pool.getconn() as conn:
        try:
            with conn.cursor() as cur:
                if params and isinstance(params[0], tuple):  # Verifica se é uma lista de tuplas
                    cur.executemany(query, params)
                else:
                    cur.execute(query, params)
                if fetch:
                    return cur.fetchall()
                conn.commit()
        except Exception as e:
            print(f"Erro: {e}")
            conn.rollback()
        finally:
            connection_pool.putconn(conn)

# Criação de tabelas
def criar_tabelas():
    queries = [
        """
        CREATE TABLE IF NOT EXISTS funcionario (
            id SERIAL PRIMARY KEY,
            usuario VARCHAR(255) UNIQUE,
            senha VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Pedido (
            id SERIAL PRIMARY KEY,
            mesa INT NOT NULL,
            status VARCHAR(255) NOT NULL,
            data_hora TIMESTAMP NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Produto (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(255) UNIQUE,
            preco DECIMAL(10, 2) NOT NULL,
            disponivel BOOLEAN DEFAULT TRUE
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Produto_Pedido (
            id SERIAL PRIMARY KEY,
            pedido_id INT NOT NULL,
            produto_id INT NOT NULL,
            quantidade INT NOT NULL,
            preco_pago DECIMAL(10, 2) NOT NULL,
            FOREIGN KEY (pedido_id) REFERENCES Pedido (id) ON DELETE CASCADE,
            FOREIGN KEY (produto_id) REFERENCES Produto (id) ON DELETE CASCADE
        );
        """
    ]
    for query in queries:
        executar_query(query)

# Geração de dados - Pedidos
def gerar_dados_pedidos(qtd_pedido):
    """Gera uma lista de dados fictícios para a tabela Pedido."""
    return [
        (
            fake.random_int(1, 10),
            fake.random_element(["Pedido em andamento", "Entregar", "Pedido cancelado", "Pedido finalizado"]),
            fake.date_time_this_year()
        )
        for _ in range(qtd_pedido)
    ]

# Geração de dados - Pedido_Produto
def gerar_dados_pedido_produto(qtd_pedido_produto, qtd_pedido, qtd_produto):
    """
    Gera dados fictícios para a tabela Produto_Pedido. 
    Considera os pedidos já inseridos e os novos a serem inseridos.
    """
    pedidos_inseridos = executar_query("SELECT COUNT(*) FROM Pedido", fetch=True)[0][0]
    
    if pedidos_inseridos == 0:
        print("Nenhum pedido inserido no banco de dados.")
        return []
    
    return [
        (
            fake.random_int(1, pedidos_inseridos),
            fake.random_int(1, qtd_produto),
            fake.random_int(1, 10),
            fake.random_int(10, 100)
        )
        for _ in range(qtd_pedido_produto)
    ]


# Inserção de dados
def inserir_dados(funcionarios=None, pedidos=None, produtos=None, pedidos_produtos=None):
    if funcionarios:
        executar_query("INSERT INTO funcionario (usuario, senha, email) VALUES (%s, %s, %s)", funcionarios)
    if pedidos:
        executar_query("INSERT INTO Pedido (mesa, status, data_hora) VALUES (%s, %s, %s)", pedidos)
    if produtos:
        executar_query("INSERT INTO Produto (nome, preco, disponivel) VALUES (%s, %s, %s)", produtos)
    if pedidos_produtos:
        executar_query(
            "INSERT INTO Produto_Pedido (pedido_id, produto_id, quantidade, preco_pago) VALUES (%s, %s, %s, %s)", 
            pedidos_produtos
        )

if __name__ == "__main__":
    try:
        print("Criando as tabelas...")
        criar_tabelas()
        
        print("Inserindo dados iniciais...")
        nomes_produtos = [
            "Pizza", "Hamburguer", "Cachorro-quente", "Coxinha", "Pastel",
            "Pão de queijo", "Tapioca", "Cuscuz", "Bolo", "Brigadeiro",
            "Café", "Suco", "Refrigerante", "Água", "Cerveja",
            "Vinho", "Whisky", "Vodka", "Tequila", "Licor"
        ]
        nomes_funcionarios = ["Jonas", "Satiro", "Kauã", "Walison"]
        produtos_iniciais = [(nome, fake.random_int(10, 100), True) for nome in nomes_produtos]
        funcionarios_iniciais = [(nome, fake.password(), f"{nome.lower()}@gmail.com") for nome in nomes_funcionarios]
        inserir_dados(funcionarios=funcionarios_iniciais, produtos=produtos_iniciais)

        print("Gerando dados fictícios...")
        qtd_pedido = 1_000
        qtd_pedido_produto = 50_000

        print("Gerando dados para a tabela Pedido...")
        dados_pedido = gerar_dados_pedidos(qtd_pedido)

        print("Inserindo dados em massa...")
        with ThreadPoolExecutor(max_workers=NUM_THREADS_IO) as executor:
            if dados_pedido:
                executor.submit(inserir_dados, pedidos=dados_pedido)

        print("Gerando dados para a tabela Produto_Pedido...")
        dados_pedido_produto = gerar_dados_pedido_produto(qtd_pedido_produto, qtd_pedido, len(nomes_produtos))
        
        with ThreadPoolExecutor(max_workers=NUM_THREADS_IO) as executor:
            if dados_pedido_produto:
                executor.submit(inserir_dados, pedidos_produtos=dados_pedido_produto)

    except KeyboardInterrupt:
        print("\nInterrompido pelo usuário.")
    finally:
        connection_pool.closeall()
        print("Conexões fechadas.")
