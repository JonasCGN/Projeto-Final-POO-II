import psycopg2
import csv


# Configurações de conexão
conn = psycopg2.connect(
  dbname='database_postgres',
  user='root',
  password='root',
  host='localhost',
  port='5432'
)

# Comandos SQL e arquivos de destino
commands = [
  ("SELECT * FROM pedido", '/home/user/workspace/jonas/Projeto-Final-POO-II/testando/pedido.csv'),
  ("SELECT * FROM produto", '/home/user/workspace/jonas/Projeto-Final-POO-II/testando/produto.csv'),
  ("SELECT * FROM produto_pedido", '/home/user/workspace/jonas/Projeto-Final-POO-II/testando/produto_pedido.csv')
]

# Função para exportar dados para CSV
def export_to_csv(query, file_path):
  with conn.cursor() as cursor:
    cursor.execute(query)
    rows = cursor.fetchall()
    headers = [desc[0] for desc in cursor.description]
    
    with open(file_path, 'w', newline='') as f:
      writer = csv.writer(f)
      writer.writerow(headers)
      writer.writerows(rows)

# Executa os comandos
for query, file_path in commands:
  print(f'Exportando dados para {file_path}')
  print(f'Comando SQL: {query}')
  export_to_csv(query, file_path)

# Fecha a conexão
conn.close()