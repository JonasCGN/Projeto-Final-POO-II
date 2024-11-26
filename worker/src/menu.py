import json
from bd_postgres import DB_POSTGRES
import time
from produto import Produto, GerenciarProdutos


def inserir_pedido():         
        ids = input("Insira os IDs dos pedidos: ")
        pedidos = json.loads(ids)
        data = time.strftime("%Y-%m-%d")
        hora = time.strftime("%H:%M:%S")
        
        pedido_formatado = {
            "id": pedidos,
            "data": data,
            "hora": hora
        }
        
        return pedido_formatado

def menu(): 
    db = DB_POSTGRES()
    
    
    while True:
        print("\n----- MENU -----")
        print("1. Inserir Pedido")
        print("2. Buscar Pedido")
        print("3. Listar Todos os Pedidos")
        print("4. Sair")
        opcao = input("Escolha uma opcao")
        
        if opcao == '1': 
            gerenciador = GerenciarProdutos()
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
                print(f" pedido encontrado: {pedido}")
            else:
                print("Pedido encontrado ")
                
        elif opcao =='3':
            pedidos = db.get_all() 
            if pedidos:
                print("\nLista de Pedidos:")
                for pedido in pedidos:
                    print(pedido)
            else:
                print("Nenhum pedido encontrado.")

        elif opcao == '4':
            print("Saindo...")
            break

        else:
            print("Opção inválida, tente novamente.")

if __name__ == "__main__":
    menu()  