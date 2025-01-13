import unittest
from unittest.mock import patch, MagicMock
from src.func.func_produtos import atualizar_produto
import json

class TestFuncProdutos(unittest.TestCase):

    @patch('src.func.func_produtos.bd_produto')
    def test_atualizar_produto_sucesso(self, mock_bd_produto):
        # Arrange
        mock_bd_produto.atualizar_produto.return_value = True
        product = {'nome': 'Produto Teste', 'preco': 100.0, 'disponivel': True}
        id_product = '1'

        # Act
        result = atualizar_produto(product, id_product)

        # Assert
        mock_bd_produto.atualizar_produto.assert_called_once_with(json.dumps(product), int(id_product))
        self.assertTrue(result)

    @patch('src.func.func_produtos.bd_produto')
    def test_atualizar_produto_falha(self, mock_bd_produto):
        # Arrange
        mock_bd_produto.atualizar_produto.return_value = False
        product = {'nome': 'Produto Teste', 'preco': 100.0, 'disponivel': True}
        id_product = '1'

        # Act
        result = atualizar_produto(product, id_product)

        # Assert
        mock_bd_produto.atualizar_produto.assert_called_once_with(json.dumps(product), int(id_product))
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()