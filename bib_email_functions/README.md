# email_funcion

A biblioteca Pack Work é uma ferramenta projetada para gerenciar o envio e a sincronização de dados entre o Redis e o Postgres. Através de funcionalidades como recuperação de senhas, envio de relatórios e arquivos, e sincronização eficiente, o Pack Work oferece uma solução prática e escalável para a integração de dados.

# Instalação

# Instalação via Build

   O build está localizado no diretório `dist/`. Para instalá-lo, utilize:

   ```bash
   pip install dist/email_function.whl
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


O Pack Work inclui várias funcionalidades para enviar e-mails de recuperação de conta, gerar e enviar relatórios, além de sincronizar dados entre Redis e Postgres. 

# Exemplo: Enviar um e-mail de recuperação de conta

```python
from src.email_functions.email_def_body import criar_corpo_email_recupercao_de_conta_html
from src.email_functions.email_sand import EmailSender

Criando corpo do e-mail com usuário e senha
usuario = "usuario_teste"
senha = "nova_senha"
corpo_email = criar_corpo_email_recupercao_de_conta_html(usuario, senha)


email_sender = EmailSender(email="seu_email@gmail.com", password="sua_senha")
email_sender.send_email(subject="Recuperação de Conta", body=corpo_email, to="destinatario@example.com")

```

# Parâmetros do Método `run`

**`num_threads`** *(int)*: Número de threads para processamento paralelo.



# Testes

Para garantir que o sistema esteja funcionando corretamente, a biblioteca inclui testes automatizados. Eles estão localizados no diretório `/tests`.
