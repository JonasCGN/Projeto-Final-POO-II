"""
Este módulo contém duas classes para gerenciar produtos em um estoque: `Produto` e `GerenciarProdutos`.

Classes:
    Produto: Representa um produto com atributos como nome, preço e quantidade.
    GerenciarProdutos: Gerencia um estoque de produtos, permitindo adicionar, listar, comprar e procurar produtos.

Execução:
    A classe `Produto` define os atributos do produto e métodos para manipular esses dados. 
    A classe `GerenciarProdutos` gerencia uma lista de produtos, permitindo várias operações de estoque.
"""

import json

class Produto:
    """
    classe:Produto
    Metodo: __init__
    o metodo __init__ é o construtor da classe Produto. ele é usado para inicializar uma nova instancia de um produto com as informações fornecidas.
    """
       
    def __init__(self, nome: str = None, preco: float = None, quantidade: int = None) -> None:
        
        """Parametros
    
        nome(str):para o nome do produto
        tipo esperado:str
        valor padrão:None
        
        preco(float):para o preço do produto.
        tipo esperado:float
        valor padrão:None
        
        quantidade(int):A quantidade de produto disponivel em estoque.
        tipo esperado:int
        valor padrão:None
        
        atributos criados: Os atributos criados são associados a instancia da classe de acordo com os argumentos fornecidos.
        
        self.nome:armazena o nome do produto
        self.preco:armazena o preço do produto.
        self.quantidade:armazena a quantidade do produto.
    """
        self.nome = nome
        self.preco = preco
        self.quantidade = quantidade
        
   
        
        

    def dump(self):
        """Método: dump
        O método dump é usado para converter os dados de uma instância da classe Produto em uma representação JSON.
        
        Parâmetros
        Este método não requer parâmetros adicionais além do padrão self, que representa a instância da classe.

        Retorno:str
        
        Retorna uma string no formato JSON contendo os atributos da instância (nome, preco, quantidade).
        
        Comportamento:
        Usa a função json.dumps para criar uma string JSON a partir de um dicionário com os valores dos atributos da instância (self.nome, self.preco, self.quantidade)."""
         
         
        return json.dumps({
           
            
            "nome": self.nome,
            "preco": self.preco,
            "quantidade": self.quantidade,
        })
        
    """O método dump retorna  os dados de uma instância da classe em uma string JSON, facilitando a exportação ou manipulação dos dados em formato estruturado."""

    def load(self, data: dict):
        
        """O método load é usado para carregar os dados de um dicionário para os atributos de uma instância da classe"""
        self.nome = data["nome"]
        self.preco = data["preco"]
        self.quantidade = data["quantidade"]
        

    def __str__(self) -> str:
        """Método: __str__
        O método  __str__ é usado para definir a representação em forma de string de uma instância da classe. Quando o objeto é convertido em uma string (por exemplo, com print), este método é chamado."""
        return f"{self.nome} - R${self.preco:.2f}"

class GerenciarProdutos:
    """
    Classe para gerenciar produtos em um estoque. Permite adicionar, listar, comprar, 
    salvar e carregar informações de produtos, além de buscar produtos pelo nome.

    Atributos:
        produtos (dict): Dicionário contendo os produtos. As chaves são os nomes dos 
        produtos e os valores são objetos da classe Produto.
    """
    def __init__(self):
        """
        Inicializa o gerenciador de produtos com um dicionário vazio.
        """
        self.produtos = {}

    def add_produto(self, produto: Produto, quantidade: int):
        """
        Adiciona um produto ao estoque ou atualiza a quantidade de um produto existente.

        Args:
            produto (Produto): Objeto do tipo Produto a ser adicionado ou atualizado.
            quantidade (int): Quantidade do produto a ser adicionada.

        Returno:
            bool, Sempre retorna True.
        """
        self.produtos[produto.nome] = produto
        self.produtos[produto.quantidade] = quantidade
        return True

    def listar_produtos(self):
        return [produto for produto in self.produtos.values()]
    

    def comprar_produto(self, nome: str, qtd: int) -> float:
        """
        Realiza a compra de um produto, retornando o custo total.

        Args:
            nome (str): Nome do produto a ser comprado.
            qtd (int): Quantidade do produto a ser comprada.

        Returno:
            float: O valor total da compra, calculado como preço do produto vezes a quantidade.
        """
        produto = self.produtos[nome]
        return produto.preco * qtd

    def dump(self):
        """
        Serializa o estoque de produtos para um formato JSON.

        Returno:
            str: String JSON representando o dicionário de produtos.
        """
        data = {}
        for key, value in self.produtos.items():
            data[key] = value.dump()
        return json.dumps(data)

    def load(self, data: dict):
        
        """
        Carrega produtos a partir de um dicionário de dados em formato JSON.

        Args:
            data (dict): Dicionário onde as chaves são os nomes dos produtos e os valores 
            são strings JSON representando os objetos Produto.
        """
        for key, value in data.items():
            produto = Produto()
            produto.load(json.loads(value))
            self.produtos[key] = produto

    def procurar_produto(self, nome: str) -> Produto:
        """
        Busca um produto pelo nome no estoque.

        Args:
            nome (str): Nome do produto a ser procurado.

        Returno:
            bool: Retorna True se o produto for encontrado; caso contrário, False.
        """
        return nome in self.produtos