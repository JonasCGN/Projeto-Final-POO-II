import unittest
from src.func.func_pedidos_desenvolvimento import remover_pedido_em_desenvolvimento, pedidos_em_desenvolvimento

class TestRemoverPedidoEmDesenvolvimento(unittest.TestCase):

    def setUp(self):
        pedidos_em_desenvolvimento.clear()
        pedidos_em_desenvolvimento.append(("Produto: 1, Nome: Produto A, Categoria: Categoria A", 10))
        pedidos_em_desenvolvimento.append(("Produto: 2, Nome: Produto B, Categoria: Categoria B", 5))

    def test_remover_pedido_existente_quantidade_exata(self):
        result = remover_pedido_em_desenvolvimento("Produto: 1, Nome: Produto A, Categoria: Categoria A", 10)
        self.assertEqual(result, (True, "Pedido removido com sucesso"))
        self.assertNotIn(("Produto: 1, Nome: Produto A, Categoria: Categoria A", 10), pedidos_em_desenvolvimento)

    def test_remover_pedido_existente_quantidade_parcial(self):
        result = remover_pedido_em_desenvolvimento("Produto: 2, Nome: Produto B, Categoria: Categoria B", 3)
        self.assertEqual(result, (True, "Pedido removido com sucesso"))
        self.assertIn(("Produto: 2, Nome: Produto B, Categoria: Categoria B", 2), pedidos_em_desenvolvimento)

    def test_remover_pedido_quantidade_maior_que_disponivel(self):
        result = remover_pedido_em_desenvolvimento("Produto: 1, Nome: Produto A, Categoria: Categoria A", 15)
        self.assertEqual(result, (False, "Quantidade maior que a disponível"))
        self.assertIn(("Produto: 1, Nome: Produto A, Categoria: Categoria A", 10), pedidos_em_desenvolvimento)

    def test_remover_pedido_nao_existente(self):
        result = remover_pedido_em_desenvolvimento("Produto: 3, Nome: Produto C, Categoria: Categoria C", 1)
        self.assertEqual(result, (False, "Pedido não encontrado"))

if __name__ == '__main__':
    unittest.main()