

# Projeto-Final-POO-II

Um projeto desenvolvido em python para a realização da automação de um sistema de vendas de produtos de um restaurante. O projeto foi desenvolvido para a disciplina de Programação Orientada a Objetos II, ministrada pelo professor Lucas Bezerra, no curso de Sistemas de Informação da Universidade Federal do Piauí.

### 🚀 Inicializando

Siga as instruções abaixo para ter o projeto em execução localmente. 

### 📋 Pré-requisitos

Instalação do git para clonar o repositório. Caso não tenha, siga as instruções em - 📄 [Git](https://git-scm.com/).

```bash
git --version
# git version 2.32.0.windows.2
```

Certifique-se de ter o Python instalado. Se não tiver, siga as instruções em [PythonOrg](https://www.python.org/) para a instalação.

```bash
python --version
# Python 3.10
```

Também é possivel a utilização do docker para a execução do projeto. Para isso, siga as instruções em [Docker](https://www.docker.com/).

```bash
docker --version
# Docker version 27.3.1, build ce12230
```


### 🔧 Implantação

1. 🌀 Clone o repositório para a sua máquina local:
   
```bash
git clone https://github.com/JonasCGN/Projeto-Final-POO-II
```

2. 📂 Navegue até o diretório do projeto:
   
```bash
cd Projeto-Final-POO-II
```

3. 🐍 Crie um ambiente virtual e ative-o:

> Windows

```bash
python -m venv venv
./venv\Scripts\activate.sh
```

> Linux

```bash
python3 -m venv venv
./venv/bin/activate
```

### 🚀 Usage

Agora o projeto está configurado. Você pode executá-lo com os seguintes comandos:

#### Inicialização do banco de dados

> Inicialização do banco de dados
```bash
docker-compose up --build
```

#### Executação de cada projeto separadamente

> Execução do servidor
```bash
make server
```

> Execução do cliente
```bash
make client
```
Comandos para Sátiro 

@cd cliente_funcionario_server && export DISPLAY=:0 && export QT_QPA_PLATFORM=xcb && python3 main_funcionario.py