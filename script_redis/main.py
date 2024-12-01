"""
Este script realiza testes de conexão com um banco de dados Redis e insere um grande número de pedidos gerados dinamicamente.

Principais funcionalidades:
- Verificar a conexão com o Redis utilizando a classe DB_Redis.
- Gerar pedidos formatados como strings JSON usando a classe DicRequest.
- Inserir os pedidos no banco de dados Redis e atualizar o contador de inserções.

Constantes:
- `qtd_requests`: Define o número total de pedidos a serem gerados e inseridos no Redis.

Modo de uso:
Execute este script diretamente para iniciar o processo de teste e inserção de pedidos no Redis.
"""

import sys
import os
from src.bd import DB_Redis
from src.dic_request import DicRequest


"""
Este script é responsável por testar a conexão com um banco de dados Redis e inserir um grande número de pedidos gerados dinamicamente.
Classes:
    DB_Redis: Classe responsável por gerenciar a conexão e operações com o banco de dados Redis.
    DicRequest: Classe responsável por criar e formatar pedidos.
Constantes:
    qtd_requests (int): Número de pedidos a serem inseridos no banco de dados.
Funções:
    main: Função principal que executa o teste de conexão e insere os pedidos no banco de dados.
Uso:
    Execute este script diretamente para iniciar o processo de inserção de pedidos no banco de dados Redis.
"""

qtd_requests = 1_000_000

if __name__ == '__main__':
    db = DB_Redis()
    dic = DicRequest()

    db.test_connection()
    for _ in range(qtd_requests):
        pedido_string = dic.string_pedido(dic.criar_pedido())
        print(pedido_string)
        db.insert(db.get("qtd_inseridos"), pedido_string)
        db.increment("qtd_inseridos")
