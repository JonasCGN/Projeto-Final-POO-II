# email_funcions

A biblioteca **email_functions** é uma coleção de funções e classes projetadas para facilitar o envio de e-mails com conteúdos dinâmicos e anexos. Inclui funcionalidades como a criação de corpos de e-mail para recuperação de senha, envio de arquivos em formato HTML e gerenciamento do envio de e-mails usando o servidor SMTP do Gmail.


# Instalação

# Instalação via Build

   O build está localizado no diretório `dist/`. Para instalá-lo, utilize:

   ```bash
  pip install dist/email_functions-0.1.0-py3-none-any.whl
   ```

# Instalação para Desenvolvimento

   Se deseja modificar o código ou contribuir para o projeto, siga os passos abaixo:

   1-Certifique-se de que o Poetry está instalado. Caso não tenha o Poetry instalado, você pode instalar com o comando:
   
   ```bash
   pip install poetry
   ```

   2-Inicie um novo ambiente virtual com o Poetry:

   ```bash
   poetry shell
   ```


   3-Instale as dependências do projeto:
   
   ```bash
   poetry install
   ```


# Como Usar


O email_functions  inclui várias funcionalidades para enviar e-mails de recuperação de conta, gerar e enviar relatórios, além de sincronizar dados entre Redis e Postgres. 

# Exemplo: Enviar um e-mail de recuperação de conta

```python
from src.email_functions.email_def_body import criar_corpo_email_recupercao_de_conta_html
from src.email_functions.email_sand import EmailSender

#Criando corpo do e-mail com usuário e senha
usuario = "usuario_teste"
senha = "nova_senha"
corpo_email = criar_corpo_email_recupercao_de_conta_html(usuario, senha)

#enviando email
email_sender = EmailSender(email="seu_email@gmail.com", password="sua_senha")
email_sender.send_email(subject="Recuperação de Conta", body=corpo_email, to="destinatario@example.com")

```

# Parâmetros do Método `run`

num_threads (int): Especifica o número de threads para o processamento paralelo. Esse parâmetro permite controlar o nível de paralelismo durante a execução, acelerando o processamento quando for adequado



# Testes

Para garantir que o sistema esteja funcionando corretamente, a biblioteca inclui testes automatizados. Eles estão localizados no diretório `/tests`.
