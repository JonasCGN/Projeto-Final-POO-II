import unittest
from src.func.func_pedidos_desenvolvimento import remover_pedido_em_desenvolvimento, pedidos_em_desenvolvimento

class TestRemoverPedidoEmDesenvolvimento(unittest.TestCase):
    """
    Classe de testes para validar a funcionalidade de remoção de pedidos em desenvolvimento.
    """

    def setUp(self):
        """
        Configura o estado inicial da lista 'pedidos_em_desenvolvimento' antes de cada teste.
        """
        pedidos_em_desenvolvimento.clear()
        pedidos_em_desenvolvimento.append(("Produto: 1, Nome: Produto A, Categoria: Categoria A", 10))
        pedidos_em_desenvolvimento.append(("Produto: 2, Nome: Produto B, Categoria: Categoria B", 5))

    def test_remover_pedido_existente_quantidade_exata(self):
        """
        Testa a remoção completa de um pedido com a quantidade exata disponível.

        Cenário:
        - Pedido existe e a quantidade solicitada para remoção corresponde à disponível.

        Valida:
        - Se o pedido é completamente removido da lista.
        - Se a mensagem de sucesso é retornada.
        """
        result = remover_pedido_em_desenvolvimento("Produto: 1, Nome: Produto A, Categoria: Categoria A", 10)
        self.assertEqual(result, (True, "Pedido removido com sucesso"))
        self.assertNotIn(("Produto: 1, Nome: Produto A, Categoria: Categoria A", 10), pedidos_em_desenvolvimento)

    def test_remover_pedido_existente_quantidade_parcial(self):
        """
        Testa a remoção parcial de um pedido, reduzindo a quantidade disponível.

        Cenário:
        - Pedido existe e a quantidade solicitada é menor que a disponível.

        Valida:
        - Se a quantidade do pedido é atualizada corretamente.
        - Se a mensagem de sucesso é retornada.
        """
        result = remover_pedido_em_desenvolvimento("Produto: 2, Nome: Produto B, Categoria: Categoria B", 3)
        self.assertEqual(result, (True, "Pedido removido com sucesso"))
        self.assertIn(("Produto: 2, Nome: Produto B, Categoria: Categoria B", 2), pedidos_em_desenvolvimento)

    def test_remover_pedido_quantidade_maior_que_disponivel(self):
        """
        Testa o cenário em que a quantidade solicitada para remoção excede a quantidade disponível.

        Cenário:
        - Pedido existe, mas a quantidade solicitada é maior que a disponível.

        Valida:
        - Se o pedido permanece inalterado na lista.
        - Se a mensagem de erro apropriada é retornada.
        """
        result = remover_pedido_em_desenvolvimento("Produto: 1, Nome: Produto A, Categoria: Categoria A", 15)
        self.assertEqual(result, (False, "Quantidade maior que a disponível"))
        self.assertIn(("Produto: 1, Nome: Produto A, Categoria: Categoria A", 10), pedidos_em_desenvolvimento)

    def test_remover_pedido_nao_existente(self):
        """
        Testa o cenário em que o pedido solicitado para remoção não existe na lista.

        Cenário:
        - Pedido não está presente na lista.

        Valida:
        - Se a mensagem de erro apropriada é retornada.
        """
        result = remover_pedido_em_desenvolvimento("Produto: 3, Nome: Produto C, Categoria: Categoria C", 1)
        self.assertEqual(result, (False, "Pedido não encontrado"))
        
        
if __name__ == '__main__':
    unittest.main()