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
