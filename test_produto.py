import pytest
from src.produto import Produto, GerenciarProdutos

class TestProduto():
    
    @pytest.mark.parametrize("nome, preco", [("Coca-Cola", 5.00), ("Guaraná", 3.00)])
    def test_produto_initialization(self, nome, preco):
        produto = Produto(nome, preco)
        assert produto.nome == nome
        assert produto.preco == preco

    @pytest.mark.parametrize("nome, preco, expected_output", [
        ("Coca-Cola", 5.00, "Coca-Cola - R$5.00"),
        ("Guaraná", 3.00, "Guaraná - R$3.00")
    ])
    
    def test_produto_dump(self, nome, preco, expected_output):
        produto = Produto(nome, preco)
        assert str(produto) == expected_output

    @pytest.mark.parametrize("data, expected_output", [
        ({"nome": "Coca-Cola", "preco": 5.00}, "Coca-Cola - R$5.00"),
        ({"nome": "Guaraná", "preco": 3.00}, "Guaraná - R$3.00")
    ])
    def test_produto_load(self, data, expected_output):
        produto = Produto()
        produto.load(data)
        
        assert produto.nome == data["nome"]
        assert produto.preco == data["preco"]
        
        assert str(produto) == expected_output

    @pytest.mark.parametrize("nome, preco, expected_output", [
        ("Coca-Cola", 5.00, "Coca-Cola - R$5.00"),
        ("Guaraná", 3.00, "Guaraná - R$3.00")
    ])
    def test_produto_str(self, nome, preco, expected_output):
        produto = Produto(nome, preco)
        assert str(produto) == expected_output

