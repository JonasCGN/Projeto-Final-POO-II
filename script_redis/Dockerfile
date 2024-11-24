# Use a imagem base do Python
FROM python:3.9-slim

# Define o diretório de trabalho no contêiner
WORKDIR /app

# Copia o arquivo de dependências para o contêiner
COPY requirements.txt /app/requirements.txt

# Instala as dependências do Python
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copia o restante dos arquivos
COPY . .

# Define o comando padrão para execução
CMD ["python", "app.py"]
