from cliente import Cliente

address = '127.0.0.1'
post = 9000

c1 = Cliente("Cliente1")
c2 = Cliente("Cliente2")

# Testar se um cliente pode ter um nome de usuário igual a outro cliente
def test_conectar():
    assert c1.conectar(address,post) == "connected: conectado!"
    assert c2.conectar(address,post) == "disconnected: Nome em uso!"

def test_enviar_pedido():
    assert c1.enviar_pedido("1") == '{"id": "1"}'
    assert c2.enviar_pedido("2") == '{"id": "2"}'
    assert c1.enviar_pedido("3") == '{"id": "3"}'
    assert c2.enviar_pedido("4") == '{"id": "4"}'
    assert c1.enviar_pedido("5") == '{"id": "5"}'