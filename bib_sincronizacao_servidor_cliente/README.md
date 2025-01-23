# **sincronizacao_servidor_cliente**

A biblioteca sincronizacao_servidor_cliente é uma ferramenta que sincroniza dados do redis para o banco de dados Postgres

## **Instalação**

### **Instalação via Build**

O build está localizado no diretório `dist/`. Para instalá-lo, utilize:

bash
´´´
pip Install dist/sincronizacao_servidor_cliente-0.1.0-py3-none-any.whl

´´´
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

Após a instalação, aqui está um exemplo de como usar o `send_redis` para gerar e enviar dados ao Redis:

```python
from libary.sincronizacao import Sincronizacao

sincronizacao = Sincronizacao()
sincronizacao.run(10)
```



## **Build**

Para gerar um novo build, execute o seguinte comando no diretório raiz do projeto:

```bash
poetry build
```

Isso criará o pacote no formato `.whl` e `.tar.gz` no diretório `dist/`.