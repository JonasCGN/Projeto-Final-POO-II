import unittest
from unittest.mock import patch, MagicMock
from src.func.func_produtos import atualizar_produto
import json

class TestFuncProdutos(unittest.TestCase):
    """
    Classe de testes para validar a funcionalidade de atualização de produtos.
    """

    @patch('src.func.func_produtos.bd_produto')
    def test_atualizar_produto_sucesso(self, mock_bd_produto):
        """
        Testa a atualização bem-sucedida de um produto.

        Simula:
        - O comportamento do banco de dados retornando `True` para indicar sucesso.

        Valida:
        - Se a função `atualizar_produto` chama o método `atualizar_produto` do banco de dados com os argumentos corretos.
        - Se o retorno da função `atualizar_produto` é `True`.

        Cenário:
        - Produto atualizado com sucesso.
        """
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
        """
        Testa a falha na atualização de um produto.

        Simula:
        - O comportamento do banco de dados retornando `False` para indicar falha.

        Valida:
        - Se a função `atualizar_produto` chama o método `atualizar_produto` do banco de dados com os argumentos corretos.
        - Se o retorno da função `atualizar_produto` é `False`.

        Cenário:
        - Falha ao atualizar o produto.
        """
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