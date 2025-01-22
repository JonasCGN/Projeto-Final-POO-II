import unittest
from src.func.func_pedido import transformar_lista_str_em_lista_tuple

class TestFuncPedido(unittest.TestCase):
    """
    Classe de testes para validar a funcionalidade de transformação de listas de strings em listas de tuplas.
    """

    def test_transformar_lista_str_em_lista_tuple_sucesso(self):
        """
        Testa a transformação bem-sucedida de uma lista de strings em uma lista de tuplas.

        Cenário:
        - A entrada contém strings formatadas corretamente.
        - Cada string é transformada em uma tupla contendo: ID, Preço e Quantidade.

        Valida:
        - Se a saída corresponde à lista de tuplas esperada.
        """
        lista = [
            "ID: 1, Nome: Produto1, Preço: 10.5, Quantidade: 2",
            "ID: 2, Nome: Produto2, Preço: 20.0, Quantidade: 1"
        ]
        esperado = [
            ("1", 10.5, 2),
            ("2", 20.0, 1)
        ]
        resultado = transformar_lista_str_em_lista_tuple(lista)
        self.assertEqual(resultado, esperado)

    def test_transformar_lista_str_em_lista_tuple_lista_vazia(self):
        """
        Testa o comportamento da função ao receber uma lista vazia como entrada.

        Cenário:
        - A entrada é uma lista vazia.
        - A saída esperada é uma lista vazia.

        Valida:
        - Se a função retorna uma lista vazia.
        """
        lista = []
        esperado = []
        resultado = transformar_lista_str_em_lista_tuple(lista)
        self.assertEqual(resultado, esperado)

    def test_transformar_lista_str_em_lista_tuple_formato_incorreto(self):
        """
        Testa o comportamento da função ao receber strings em formatos incorretos.

        Cenário:
        - A entrada contém strings onde as informações estão incompletas ou mal formatadas.
        - A função deve lançar uma exceção do tipo IndexError.

        Valida:
        - Se a exceção `IndexError` é lançada corretamente.
        """
        lista = [
            "ID: 1, Nome: Produto1, Preço: 10.5",
            "ID: 2, Nome: Produto2, Quantidade: 1"
        ]
        with self.assertRaises(IndexError):
            transformar_lista_str_em_lista_tuple(lista)

if __name__ == '__main__':
    unittest.main()