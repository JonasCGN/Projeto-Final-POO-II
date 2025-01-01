import unittest
from src.func.func_pedido import transformar_lista_str_em_lista_tuple

class TestFuncPedido(unittest.TestCase):

    def test_transformar_lista_str_em_lista_tuple_sucesso(self):
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
        lista = []
        esperado = []
        resultado = transformar_lista_str_em_lista_tuple(lista)
        self.assertEqual(resultado, esperado)

    def test_transformar_lista_str_em_lista_tuple_formato_incorreto(self):
        lista = [
            "ID: 1, Nome: Produto1, Preço: 10.5",
            "ID: 2, Nome: Produto2, Quantidade: 1"
        ]
        with self.assertRaises(IndexError):
            transformar_lista_str_em_lista_tuple(lista)

if __name__ == '__main__':
    unittest.main()