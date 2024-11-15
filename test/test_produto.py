import unittest
from src.produto import Produto

class TestProduto(unittest.TestCase):

    def test_produto_initialization(self):
        produto = Produto("Coca-Cola", 5.00)
        self.assertEqual(produto.nome, "Coca-Cola")
        self.assertEqual(produto.preco, 5.00)

    def test_produto_dump(self):
        produto = Produto("Coca-Cola", 5.00)
        expected_output = '{"nome": "Coca-Cola", "preco": 5.0}'
        self.assertEqual(produto.dump(), expected_output)

    def test_produto_load(self):
        produto = Produto()
        data = {"nome": "Pepsi", "preco": 4.00}
        produto.load(data)
        self.assertEqual(produto.nome, "Pepsi")
        self.assertEqual(produto.preco, 4.00)

    def test_produto_str(self):
        produto = Produto("Guaraná", 3.00)
        self.assertEqual(str(produto), "Guaraná - R$3.00")

if __name__ == '__main__':
    unittest.main()