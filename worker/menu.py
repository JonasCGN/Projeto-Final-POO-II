import json
from src.bd_postgres import DB_POSTGRES
import time
from src.produto import Produto, GerenciarProdutos


def inserir_pedido():         
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
                
        elif opcao =='2': 
            id_pedido = int(input("Digite o id do pedido que deseja buscar "))
            pedido = db.get(id_pedido)
            if pedido:
                print(f"Pedido encontrado:", pedido[0], pedido[1], pedido[2], pedido[3])
            else:
                print("Pedido nao encontrado ")
                
        elif opcao =='3':
            pedidos = db.get_all() 
            if pedidos:
                print("\nLista de Pedidos:")
                for id,pedido,data,hora in pedidos:
                    print("Id:",id,"Pedido:",pedido,"Data:",data,"Hora:",hora)
            else:
                print("Nenhum pedido encontrado.")

        elif opcao == '4':
            print("Saindo...")
            break

        else:
            print("Opção inválida, tente novamente.")

if __name__ == "__main__":
    menu()  