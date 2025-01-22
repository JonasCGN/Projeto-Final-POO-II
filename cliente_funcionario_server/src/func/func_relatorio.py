import random
import pandas as pd
import numpy as np
from datetime import datetime 
from email_functions.email_sand import EmailSender

from funcao_postgree.bd_postgree_base import Bd_Base
from funcao_postgree.bd_postgree_pedido_produto import BdPedidoProduto
from funcao_postgree.bd_postgree_pedido import BdPedido
from funcao_postgree.bd_postgree_produto import BdProduto
from dotenv import load_dotenv
import os

load_dotenv(".env")
Bd_Base(os.getenv('HOST_BD'), os.getenv('DATABASE'), os.getenv('USER_BD'), os.getenv('PASSWORD_BD'))

bd_produto = BdProduto()
bd_pedido = BdPedido()
bd_pedido_produto = BdPedidoProduto()

def criar_csv():
    """
    Cria arquivos CSV com os dados de pedidos, produtos e produtos relacionados aos pedidos.

    Esta função obtém os dados necessários de três tabelas (pedidos, produtos e produtos pedidos) e 
    grava esses dados em arquivos CSV (pedidos.csv, produtos.csv, produtos_pedidos.csv).
    """
    text_pedidos_csv = bd_pedido.get_pedidos_csv()
    text_produtos_csv = bd_produto.get_produto_csv()
    text_produtos_pedidos_csv = bd_pedido_produto.get_pedidos_produto_csv()
    
    with open("pedidos.csv", "w") as file:
        file.write(text_pedidos_csv)
    with open("produtos.csv", "w") as file:
        file.write(text_produtos_csv)
    with open("produtos_pedidos.csv", "w") as file:
        file.write(text_produtos_pedidos_csv)
        
def remover_csv():
    """
    Remove os arquivos CSV criados anteriormente.

    Após a criação e leitura dos arquivos CSV, essa função exclui os arquivos 
    pedidos.csv, produtos.csv e produtos_pedidos.csv do sistema.
    """
    os.remove("pedidos.csv")
    os.remove("produtos.csv")
    os.remove("produtos_pedidos.csv")


def carregar_dados():
    """
    Carrega os dados de pedidos, produtos e produtos pedidos a partir de arquivos CSV.

    A função cria os arquivos CSV, carrega os dados em DataFrames pandas, 
    e remove os arquivos após o uso.

    Retorna:
        df_pedidos (DataFrame): Dados sobre os pedidos.
        df_produtos (DataFrame): Dados sobre os produtos.
        df_produtos_pedidos (DataFrame): Relacionamento entre pedidos e produtos.
    """
    criar_csv()
    df_pedidos = pd.read_csv("pedidos.csv")
    df_produtos = pd.read_csv("produtos.csv")
    df_produtos_pedidos = pd.read_csv("produtos_pedidos.csv")
    remover_csv()
    
    print("Dados carregados com sucesso.")
    print("Pedidos:", df_pedidos.shape)
    print("Produtos:", df_produtos.shape)
    print("Produtos_Pedidos:", df_produtos_pedidos.shape)
    
    return df_pedidos, df_produtos, df_produtos_pedidos

def mesclar_e_limpar(df1, df2, chave_esquerda, chave_direita, sufixos=("", "_y")):
    """
    Realiza a mesclagem de dois DataFrames com base nas chaves fornecidas e remove colunas duplicadas.

    A função mescla dois DataFrames com base nas chaves de junção e remove as colunas
    duplicadas adicionadas pela operação de mesclagem.

    Args:
        df1 (DataFrame): Primeiro DataFrame para mesclagem.
        df2 (DataFrame): Segundo DataFrame para mesclagem.
        chave_esquerda (str): Coluna de junção do primeiro DataFrame.
        chave_direita (str): Coluna de junção do segundo DataFrame.
        sufixos (tuple): Sufixos a serem adicionados às colunas duplicadas (padrão: "", "_y").

    Retorna:
        DataFrame: DataFrame mesclado e limpo.
    """
    mesclado = df1.merge(df2, left_on=chave_esquerda, right_on=chave_direita, suffixes=sufixos)
    return mesclado.loc[:, ~mesclado.columns.str.endswith("_y")]

def preprocessar_dados(df_pedidos, df_produtos, df_produtos_pedidos):
    """
    Realiza o pré-processamento dos dados de pedidos, produtos e produtos pedidos.

    Essa função adiciona novas colunas aos dados de pedidos (como mês, hora, dia da semana, etc.) 
    e realiza a mesclagem entre os DataFrames de pedidos, produtos e produtos pedidos.

    Args:
        df_pedidos (DataFrame): Dados de pedidos.
        df_produtos (DataFrame): Dados de produtos.
        df_produtos_pedidos (DataFrame): Relacionamento entre pedidos e produtos.

    Retorna:
        tuple: DataFrames atualizados de pedidos, produtos e produtos pedidos.
    """
    df_pedidos["data_hora"] = pd.to_datetime(df_pedidos["data_hora"])
    df_pedidos["mes"] = df_pedidos["data_hora"].dt.month
    df_pedidos["dia_semana"] = df_pedidos["data_hora"].dt.dayofweek
    df_pedidos["hora"] = df_pedidos["data_hora"].dt.hour
    df_pedidos["data"] = df_pedidos["data_hora"].dt.date
    df_pedidos["semana"] = df_pedidos["data_hora"].dt.isocalendar().week
    df_pedidos["trimestre"] = df_pedidos["data_hora"].dt.quarter

    df_produtos_pedidos = mesclar_e_limpar(df_produtos_pedidos, df_produtos, "produto_id", "id")
    df_produtos_pedidos = mesclar_e_limpar(df_produtos_pedidos, df_pedidos, "pedido_id", "id")
    return df_pedidos, df_produtos, df_produtos_pedidos

def calcular_totais(df_pedidos, df_produtos, df_produtos_pedidos):
    """
    Calcula os totais de vendas com base nos dados de pedidos, produtos e produtos pedidos.

    A função calcula o total geral de vendas e também o total de vendas agrupado por 
    diferentes critérios como produto, mês, dia da semana, hora, etc.

    Args:
        df_pedidos (DataFrame): Dados de pedidos.
        df_produtos (DataFrame): Dados de produtos.
        df_produtos_pedidos (DataFrame): Relacionamento entre pedidos e produtos.

    Retorna:
        dict: Dicionário com os totais de vendas por diferentes critérios.
    """
    total_vendas = df_produtos_pedidos["preco_pago"].sum()
    totais = {
        "total_vendas": total_vendas,
        "total_vendas_produto": df_produtos_pedidos.groupby("nome")["preco_pago"].sum(),
        "total_vendas_mes": df_produtos_pedidos.groupby("mes")["preco_pago"].sum(),
        "total_vendas_dia_semana": df_produtos_pedidos.groupby("dia_semana")["preco_pago"].sum(),
        "total_vendas_hora": df_produtos_pedidos.groupby("hora")["preco_pago"].sum(),
        "total_vendas_status": df_produtos_pedidos.groupby("status")["preco_pago"].sum(),
        "total_vendas_mesa": df_produtos_pedidos.groupby("mesa")["preco_pago"].sum(),
        "total_vendas_data": df_produtos_pedidos.groupby("data")["preco_pago"].sum(),
        "total_vendas_semana": df_produtos_pedidos.groupby("semana")["preco_pago"].sum(),
        "total_vendas_trimestre": df_produtos_pedidos.groupby("trimestre")["preco_pago"].sum(),
    }
    return totais

def dataframe_para_html(df, cabeçalhos_personalizados=None):
    """
    Converte um DataFrame para uma tabela HTML formatada.

    Essa função converte um DataFrame pandas para um código HTML que representa 
    uma tabela com as devidas formatações CSS aplicadas.

    Args:
        df (DataFrame): DataFrame a ser convertido.
        cabeçalhos_personalizados (dict, opcional): Dicionário de cabeçalhos personalizados.

    Retorna:
        str: Código HTML representando a tabela.
    """
    if cabeçalhos_personalizados:
        df = df.rename(columns=cabeçalhos_personalizados)
    
    # Adiciona classes CSS para uma melhor formatação de tabelas
    return df.to_html(
        classes='table styled-table',
        escape=False,
        index=False,
        justify='center',
        border=1,
        sparsify=True,
        
    )

def gerar_html(totais):
    """
    Gera o HTML do relatório de vendas, incluindo totais e tabelas formatadas.

    A função monta um relatório em HTML com base nos totais de vendas calculados 
    e converte os dados em tabelas formatadas.

    Args:
        totais (dict): Dicionário contendo os totais de vendas por diversos critérios.

    Retorna:
        str: Código HTML completo do relatório de vendas.
    """
    cabeçalhos_personalizados_pedidos = {
        "data_hora": "Data e Hora",
        "mes": "Mês",
        "dia_semana": "Dia da Semana",
        "hora": "Hora",
        "data": "Data",
        "semana": "Semana",
        "trimestre": "Trimestre"
    }

    html = f"""
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Relatório de Vendas</title>
      <style>
      body {{
        font-family: Arial, sans-serif;
        margin: 20px;
        background-color: #f4f4f9;
        color: #333;
        width: 1300px;
      }}
      h1 {{
        text-align: center;
        color: #2c3e50;
      }}
      h2 {{
        color: #2980b9;
        margin-top: 20px;
      }}
      table.styled-table {{
        width: 100%;
        border-collapse: collapse;
        margin: 20px 0;
        font-size: 18px;
        text-align: left;
      }}
      table.styled-table th {{
        background-color: #2980b9;
        color: #fff;
        padding: 10px;
      }}
      table.styled-table td {{
        padding: 8px;
        text-align: center;
      }}
      table.styled-table tr:nth-child(even) {{
        background-color: #f2f2f2;
      }}
      table.styled-table tr:hover {{
        background-color: #ddd;
      }}
      .footer {{
        margin-top: 40px;
        font-size: 14px;
        color: #aaa;
      }}
      </style>
    </head>
    <body>
      <div class="container">
      <h1>Relatório de Vendas</h1>
      <h2>Total de Vendas</h2>
      <p>Total de vendas: R${totais["total_vendas"]:.2f}</p>
    """
    for chave, dado in totais.items():
        if isinstance(dado, pd.Series) or isinstance(dado, pd.DataFrame):
            html += f"""
            <h2>Total de Vendas por {chave.replace("_", " ").title()}</h2>
            {dataframe_para_html(dado.reset_index(), cabeçalhos_personalizados=cabeçalhos_personalizados_pedidos)}
            """
    html += """
      <div class="footer">
        <p>&copy; 2025 Relatório de Vendas - Todos os direitos reservados.</p>
      </div>
      </div>
    </body>
    </html>
    """
    return html

def gerar_relatorio() -> str:
    """
    Gera o relatório completo de vendas.

    A função carrega os dados, realiza o pré-processamento, calcula os totais 
    de vendas e gera o relatório em formato HTML.

    Retorna:
        str: Código HTML do relatório de vendas.
    """
    df_pedidos, df_produtos, df_produtos_pedidos = carregar_dados()
    df_pedidos, df_produtos, df_produtos_pedidos = preprocessar_dados(df_pedidos, df_produtos, df_produtos_pedidos)
    totais = calcular_totais(df_pedidos, df_produtos, df_produtos_pedidos)
    html = gerar_html(totais)
    return html

# from email_functions.email_sand import EmailSender
# from dotenv import load_dotenv
# from os import getenv

# load_dotenv(".env")
# email_sender = EmailSender(getenv('EMAIL'), getenv('PASSWORD'))


# def principal():
#     df_pedidos, df_produtos, df_produtos_pedidos = carregar_dados()
#     df_pedidos, df_produtos, df_produtos_pedidos = preprocessar_dados(df_pedidos, df_produtos, df_produtos_pedidos)
#     totais = calcular_totais(df_pedidos, df_produtos, df_produtos_pedidos)
#     html = gerar_html(totais)
#     email_sender.send_email("Relatório de Vendas", html, "kaua.sbc@gmail.com")
  
# if __name__ == "__main__":
#     principal()
