from src.produto import Produto, GerenciarProdutos
import pytest

class TestGerenciarProduto():
    
    p1 = Produto("Coca-Cola", 5.00)
    p2 = Produto("Pepsi", 4.00)
    p3 = Produto("Guaraná", 3.00)
    p4 = Produto("Fanta", 2.00)
    p5 = Produto("Sprite", 1.00)
    
    @pytest.fixture
    def gp(self):
        return GerenciarProdutos()
    
    @pytest.mark.parametrize("nome, preco", [("Coca-Cola", 5.00), ("Guaraná", 3.00)])
    def test_adicionar_produto(self, nome, preco, gp: GerenciarProdutos):
        gp.add_produto(Produto(nome, preco))
        assert gp.produtos[nome].nome == nome
        assert gp.produtos[nome].preco == preco

    @pytest.mark.parametrize("nome, preco, qtd, expected_output", [
        ("Coca-Cola", 5.00, 2, 2 * 5),
        ("Guaraná", 3.00, 3, 3 * 3)
    ])
    def test_compra(self, nome, preco, qtd, expected_output, gp: GerenciarProdutos):
        gp.add_produto(Produto(nome, preco))
        assert gp.comprar_produto(nome, qtd) == expected_output
        
    @pytest.mark.parametrize("nome, preco, expected_output", [
        ("Coca-Cola", 5.00, True),
        ("Guaraná", 3.00, False)
    ])
    def test_procura(self, nome, preco, expected_output, gp: GerenciarProdutos):
      if expected_output == True:
        gp.add_produto(Produto(nome, preco))
        
      assert gp.procurar_produto(nome) == expected_output

    @pytest.mark.parametrize("nome, preco", [("Coca-Cola", 5.00), ("Guaraná", 3.00)])
    def test_listar_produtos(self, nome, preco, gp: GerenciarProdutos):
        gp.add_produto(Produto(nome, preco))
        assert gp.listar_produtos() == [gp.produtos[nome]]