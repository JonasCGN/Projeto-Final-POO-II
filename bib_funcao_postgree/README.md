# **função_posttgree**

contem funções e classes responsáveis por interagir com o banco de dados PostgreSQL.

## **Instalação**

### **Instalação via Build**

```bash
pip install dist/funcao_postgree-0.1.0-py3-none-any.whl
```


### **Instalação para Desenvolvimento**

Se deseja modificar o código ou contribuir para o projeto, siga os passos abaixo:

1. Certifique-se de que o **Poetry** está instalado. Caso não esteja, instale com:
   ```bash
   pip install poetry
   ```

2. Inicie um novo ambiente virtual com o Poetry:
   ```bash
   poetry shell
   ```

3. Instale as dependências do projeto:
   ```bash
   poetry install
   ```

## **Como Usar**

As classes dentro da pasta função_postgree têm como objetivo facilitar a interação com o banco de dados PostgreSQL, permitindo a criação e manipulação das tabelas e dos dados. Para começar a usar, basta importar as classes necessárias e chamar seus métodos.

```python
rom src.funcao_postgree.bd_postgree_funcionario import BdFuncionario
from src.funcao_postgree.bd_postgree_pedido import BdPedido
from src.funcao_postgree.bd_postgree_produto import BdProduto
from src.funcao_postgree.bd_postgree_pedido_produto import BdPedidoProduto

# Inicializa a tabela de funcionários
bd_funcionario = BdFuncionario()
bd_funcionario.database_init()

# Inicializa a tabela de pedidos
bd_pedido = BdPedido()
bd_pedido.database_init()

# Inicializa a tabela de produtos
bd_produto = BdProduto()
bd_produto.database_init()

# Inicializa a tabela de pedidos-produtos
bd_pedido_produto = BdPedidoProduto()
bd_pedido_produto.database_init()
```

## **Build**

Para gerar um novo build, execute o seguinte comando no diretório raiz do projeto:

```bash
poetry build
```

Isso criará o pacote no formato `.whl` e `.tar.gz` no diretório `dist/`.
