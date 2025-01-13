import random
import pandas as pd
import numpy as np
from datetime import datetime 
from email_functions.email_sand import EmailSender

def carregar_dados():
    df_pedidos = pd.read_csv("pedido.csv")
    df_produtos = pd.read_csv("produto.csv")
    df_produtos_pedidos = pd.read_csv("produto_pedido.csv")
    return df_pedidos, df_produtos, df_produtos_pedidos

def mesclar_e_limpar(df1, df2, chave_esquerda, chave_direita, sufixos=("", "_y")):
    mesclado = df1.merge(df2, left_on=chave_esquerda, right_on=chave_direita, suffixes=sufixos)
    return mesclado.loc[:, ~mesclado.columns.str.endswith("_y")]

def preprocessar_dados(df_pedidos, df_produtos, df_produtos_pedidos):
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

from email_functions.email_sand import EmailSender
from dotenv import load_dotenv
from os import getenv

load_dotenv(".env")
email_sender = EmailSender(getenv('EMAIL'), getenv('PASSWORD'))


def principal():
    df_pedidos, df_produtos, df_produtos_pedidos = carregar_dados()
    df_pedidos, df_produtos, df_produtos_pedidos = preprocessar_dados(df_pedidos, df_produtos, df_produtos_pedidos)
    totais = calcular_totais(df_pedidos, df_produtos, df_produtos_pedidos)
    html = gerar_html(totais)
    email_sender.send_email("Relatório de Vendas", html, "jonasbo66@gmail.com")
  

if __name__ == "__main__":
    principal()
