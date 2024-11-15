from produto import Produto, GerenciarProdutos

p1 = Produto("Coca-Cola", 5.00)
p2 = Produto("Pepsi", 4.00)
p3 = Produto("Guaraná", 3.00)
p4 = Produto("Fanta", 2.00)
p5 = Produto("Sprite", 1.00)

gp = GerenciarProdutos()

def test_aducionar_produto():
    assert gp.add_produto(p1) == True
    assert gp.add_produto(p2) == True
    assert gp.add_produto(p3) == True
    assert gp.add_produto(p4) == True
    assert gp.add_produto(p5) == True

def test_compra():
    assert gp.comprar_produto("Coca-Cola", 2) == 10.00
    assert gp.comprar_produto("Pepsi", 2) == 8.00
    
def test_procura():
    assert gp.procurar_produto("Coca-Cola") == True
    assert gp.procurar_produto("Suco") == False
    
def test_listar_produtos():
    assert gp.listar_produtos() == [p1, p2, p3, p4, p5]