"""
Este módulo gerencia pedidos de produtos utilizando um banco de dados PostgreSQL.

Funções:
    inserir_pedido: Solicita ao usuário a inserção de IDs de pedidos e retorna um dicionário com os pedidos, data e hora.
    menu: Exibe um menu interativo para gerenciar pedidos de produtos. O menu permite:
        1. Inserir um novo pedido.
        2. Buscar um pedido existente pelo ID.
        3. Listar todos os pedidos.
        4. Sair do programa.

Dependências:
    - DB_POSTGRES: Classe responsável pela interação com o banco de dados PostgreSQL.
    - GerenciarProdutos: Classe responsável por gerenciar os produtos disponíveis.
    - Produto: Classe que representa um produto.
    - json: Módulo utilizado para converter o pedido em formato JSON antes de inseri-lo no banco de dados.
    - time: Módulo utilizado para formatar data e hora de inserção dos pedidos.

A execução do programa começa ao chamar a função `menu()`, que permanece em execução até que o usuário escolha a opção 
de sair.
"""

import json
from libary.bd_postgres import DB_POSTGRES
import time
from libary.produto import Produto, GerenciarProdutos


def inserir_pedido():
    """
    Solicita ao usuário a inserção dos IDs dos pedidos, formata a data e hora atuais,
    e retorna um dicionário com os pedidos, data e hora.
    Returns:
        dict: Um dicionário contendo os pedidos, data e hora no seguinte formato:
            {
                "pedidos": [list]: Lista de pedidos inseridos pelo usuário,
                "data": str: Data atual no formato "YYYY-%m:%d",
                "hora": str: Hora atual no formato "HH:%M:%S"
    """
    ids = input("Insira os IDs dos pedidos: ")
    pedidos = [json.loads(ids)]
    data = time.strftime("%Y-%m:%d")
    hora = time.strftime("%H:%M:%S")

    pedido_formatado = {
        "pedidos": pedidos,
        "data": data,
        "hora": hora
    }

    return pedido_formatado


def menu():
    """
    Exibe um menu interativo para gerenciar pedidos de produtos.
    O menu permite ao usuário:
    1. Inserir um novo pedido.
    2. Buscar um pedido existente pelo ID.
    3. Listar todos os pedidos.
    4. Sair do programa.
    Funções:
    - Inserir Pedido: Lista os produtos disponíveis e permite ao usuário inserir um novo pedido no banco de dados.
    - Buscar Pedido: Solicita o ID do pedido e exibe os detalhes do pedido correspondente, se encontrado.
    - Listar Todos os Pedidos: Exibe uma lista de todos os pedidos armazenados no banco de dados.
    - Sair: Encerra o programa.
    O menu continua a ser exibido até que o usuário escolha a opção de sair.
    Exceções:
    - Exibe mensagens de erro apropriadas se ocorrerem problemas ao inserir ou buscar pedidos no banco de dados.
    - Valida a entrada do usuário para garantir que uma opção válida seja selecionada.
    Dependências:
    - DB_POSTGRES: Classe responsável pela interação com o banco de dados PostgreSQL.
    - GerenciarProdutos: Classe responsável por gerenciar os produtos disponíveis.
    - Produto: Classe que representa um produto.
    - json: Módulo utilizado para converter o pedido em formato JSON antes de inseri-lo no banco de dados.
    """
    db = DB_POSTGRES()
    gerenciador = GerenciarProdutos()
    produtos = {
        1: Produto("Coca-Cola", 5.00, 6),
        2: Produto("Pepsi", 4.00, 1),
        3: Produto("Guaraná", 3.00, 7),
        4: Produto("Fanta", 2.00, 4),
        5: Produto("Sprite", 1.00, 1),
    }

    gerenciador.produtos = produtos

    while True:
        print("\n----- MENU -----")
        print("1. Inserir Pedido")
        print("2. Buscar Pedido")
        print("3. Listar Todos os Pedidos")
        print("4. Sair")
        opcao = input("Escolha uma opcao")

        if opcao == '1':
            produtos = gerenciador.listar_produtos()

            for produto in produtos:
                print(produto)

            pedido = inserir_pedido()
            pedido_json = json.dumps(pedido)

            if db.insert(pedido_json):
                print("Peido inserido com suscesso!")
            else:
                print("erro ao inserir no banco de dados")

        elif opcao == '2':
            id_pedido = int(input("Digite o id do pedido que deseja buscar "))
            pedido = db.get(id_pedido)
            if pedido:
                print(f"Pedido encontrado:", pedido[0], pedido[1], pedido[2], pedido[3])
            else:
                print("Pedido nao encontrado ")

        elif opcao == '3':
            pedidos = db.get_all()
            if pedidos:
                print("\nLista de Pedidos:")
                for id, pedido, data, hora in pedidos:
                    print("Id:", id, "Pedido:", pedido, "Data:", data, "Hora:", hora)
            else:
                print("Nenhum pedido encontrado.")

        elif opcao == '4':
            print("Saindo...")
            break

        else:
            print("Opção inválida, tente novamente.")


if __name__ == "__main__":
    menu()
