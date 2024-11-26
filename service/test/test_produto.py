import pytest
from src.produto import Produto, GerenciarProdutos

class TestProduto:
    """
    Classe de testes para a classe Produto.
    Realiza verificações nos métodos de inicialização, conversão para string e carregamento de dados (método 'load').
    """

    @pytest.mark.parametrize("nome, preco", [("Coca-Cola", 5.00), ("Guaraná", 3.00)])
    def test_produto_initialization(self, nome, preco):
        """
        Testa a inicialização de um objeto Produto.

        Este teste verifica se os atributos 'nome' e 'preco' são definidos corretamente durante a criação do objeto.

        Cenários testados:
        - Produto com nome "Coca-Cola" e preço R$5,00.
        - Produto com nome "Guaraná" e preço R$3,00.

        Parâmetros:
        - nome: O nome do produto.
        - preco: O preço do produto.

        Comportamento esperado:
        - O objeto deve ser inicializado com os valores corretos para os atributos 'nome' e 'preco'.
        """
        produto = Produto(nome, preco)
        assert produto.nome == nome
        assert produto.preco == preco

    @pytest.mark.parametrize("nome, preco, expected_output", [
        ("Coca-Cola", 5.00, "Coca-Cola - R$5.00"),
        ("Guaraná", 3.00, "Guaraná - R$3.00")
    ])
    def test_produto_dump(self, nome, preco, expected_output):
        """
        Testa a representação em string de um objeto Produto.

        Este teste verifica se o método `__str__` retorna a string esperada, no formato 'nome - R$preco'.

        Cenários testados:
        - Produto com nome "Coca-Cola" e preço R$5,00.
        - Produto com nome "Guaraná" e preço R$3,00.

        Parâmetros:
        - nome: O nome do produto.
        - preco: O preço do produto.
        - expected_output: A string esperada para a representação do objeto.

        Comportamento esperado:
        - O método `__str__` deve retornar a string formatada corretamente.
        """
        produto = Produto(nome, preco)
        assert str(produto) == expected_output

    @pytest.mark.parametrize("data, expected_output", [
        ({"nome": "Coca-Cola", "preco": 5.00}, "Coca-Cola - R$5.00"),
        ({"nome": "Guaraná", "preco": 3.00}, "Guaraná - R$3.00")
    ])
    def test_produto_load(self, data, expected_output):
        """
        Testa o método 'load' de um objeto Produto.

        Este teste verifica se o método 'load' consegue carregar corretamente os dados de um dicionário,
        atribuindo os valores aos atributos 'nome' e 'preco'.

        Cenários testados:
        - Carregar um produto com nome "Coca-Cola" e preço R$5,00.
        - Carregar um produto com nome "Guaraná" e preço R$3,00.

        Parâmetros:
        - data: Dicionário contendo os dados do produto ('nome' e 'preco').
        - expected_output: A string esperada para a representação do objeto.

        Comportamento esperado:
        - O método 'load' deve atribuir corretamente os valores do dicionário aos atributos do objeto.
        - A representação em string do objeto deve corresponder à esperada.
        """
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
        """
        Testa o método '__str__' de um objeto Produto.

        Este teste verifica se o método '__str__' retorna a string formatada corretamente no formato 'nome - R$preco'.

        Cenários testados:
        - Produto com nome "Coca-Cola" e preço R$5,00.
        - Produto com nome "Guaraná" e preço R$3,00.

        Parâmetros:
        - nome: O nome do produto.
        - preco: O preço do produto.
        - expected_output: A string esperada para a representação do objeto.

        Comportamento esperado:
        - O método '__str__' deve retornar a string no formato correto.
        """
        produto = Produto(nome, preco)
        assert str(produto) == expected_output
