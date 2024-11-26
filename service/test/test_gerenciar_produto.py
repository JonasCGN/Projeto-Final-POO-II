from src.produto import Produto, GerenciarProdutos
import pytest

class TestGerenciarProduto():
    """
    Classe de teste para validar as funcionalidades do sistema de gerenciamento de produtos.
    """

    
    p1 = Produto("Coca-Cola", 5.00)
    p2 = Produto("Pepsi", 4.00)
    p3 = Produto("Guaraná", 3.00)
    p4 = Produto("Fanta", 2.00)
    p5 = Produto("Sprite", 1.00)
    
    @pytest.fixture
    def gp(self):
        """
        Método auxiliar para criar uma instância de GerenciarProdutos.

        Returno:
            GerenciarProdutos: Nova instância de GerenciarProdutos.
        """
        return GerenciarProdutos()
    
    @pytest.mark.parametrize("nome, preco", [("Coca-Cola", 5.00), ("Guaraná", 3.00)])
    def test_adicionar_produto(self, nome, preco, gp: GerenciarProdutos):
        """
        Testa o método add_produto para verificar se o produto é adicionado corretamente.

        Args:
            nome (str): Nome do produto a ser adicionado.
            preco (float): Preço do produto a ser adicionado.
            gp (GerenciarProdutos): Instância do gerenciador de produtos.
        """
        gp.add_produto(Produto(nome, preco))
        assert gp.produtos[nome].nome == nome
        assert gp.produtos[nome].preco == preco

    @pytest.mark.parametrize("nome, preco, qtd, expected_output", [
        ("Coca-Cola", 5.00, 2, 2 * 5),
        ("Guaraná", 3.00, 3, 3 * 3)
    ])
    def test_compra(self, nome, preco, qtd, expected_output, gp: GerenciarProdutos):
        """
        Testa o método comprar_produto para validar o cálculo do custo total.

        Args:
            nome (str): Nome do produto a ser comprado.
            preco (float): Preço unitário do produto.
            qtd (int): Quantidade do produto a ser comprado.
            expected_output (float): Valor esperado para a compra.
            gp (GerenciarProdutos): Instância do gerenciador de produtos.
        """
        gp.add_produto(Produto(nome, preco))
        assert gp.comprar_produto(nome, qtd) == expected_output
        
    @pytest.mark.parametrize("nome, preco, expected_output", [
        ("Coca-Cola", 5.00, True),
        ("Guaraná", 3.00, False)
    ])
    def test_procura(self, nome, preco, expected_output, gp: GerenciarProdutos):
        """
        Testa o método procurar_produto para verificar se o produto está no sistema.

        Args:
            nome (str): Nome do produto a ser procurado.
            preco (float): Preço do produto (usado apenas para adição quando esperado True).
            expected_output (bool): Resultado esperado da busca (True se o produto existe).
            gp (GerenciarProdutos): Instância do gerenciador de produtos.
        """
        if expected_output == True:
            gp.add_produto(Produto(nome, preco))
            
        assert gp.procurar_produto(nome) == expected_output

    @pytest.mark.parametrize("nome, preco", [("Coca-Cola", 5.00), ("Guaraná", 3.00)])
    def test_listar_produtos(self, nome, preco, gp: GerenciarProdutos):
        """
        Testa o método listar_produtos para validar a listagem correta dos produtos.

        Args:
            nome (str): Nome do produto a ser adicionado.
            preco (float): Preço do produto a ser adicionado.
            gp (GerenciarProdutos): Instância do gerenciador de produtos.
        """
        gp.add_produto(Produto(nome, preco))
        assert gp.listar_produtos() == [gp.produtos[nome]]