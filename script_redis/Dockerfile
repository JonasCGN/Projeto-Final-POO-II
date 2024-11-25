# Use a imagem base do Python
FROM python:3.9-slim

# Define o diretório de trabalho no contêiner
WORKDIR /app

<<<<<<< HEAD
# Copia o arquivo de dependências para o contêiner
COPY requirements.txt /app/requirements.txt
=======
# Copia o código do worker para o contêiner
COPY . .
>>>>>>> origin/satiro

# Instala as dependências do Python
RUN pip install --no-cache-dir -r /app/requirements.txt

<<<<<<< HEAD
<<<<<<< HEAD
# Copia o restante dos arquivos
COPY . .

# Define o comando padrão para execução
CMD ["python", "app.py"]
=======
=======
# Define a variável de ambiente
ENV HOST_TO_REDIS=redis

>>>>>>> origin/dev_KauaHen
# Comando padrão para executar o worker
CMD ["python", "main.py"]
>>>>>>> origin/satiro
