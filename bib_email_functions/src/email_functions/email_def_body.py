
def criar_corpo_email_recupercao_de_conta_html(usuario, senha):
    corpo_email = f"""
    <html>
    <head>
      <style>
      body {{
        font-family: Arial, sans-serif;
      }}
      .container {{
        padding: 20px;
        border: 1px solid #ccc;
        border-radius: 10px;
        width: 80%;
        margin: 0 auto;
      }}
      .header {{
        background-color: #f2f2f2;
        padding: 10px;
        text-align: center;
        border-bottom: 1px solid #ccc;
      }}
      .content {{
        margin-top: 20px;
      }}
      .footer {{
        margin-top: 20px;
        text-align: center;
        font-size: 12px;
        color: #777;
      }}
      </style>
    </head>
    <body>
      <div class="container">
      <div class="header">
        <h2>Recuperação de Conta</h2>
      </div>
      <div class="content">
        <p>Ola, <strong>{usuario}</strong></p>
        <p>Sua nova senha é: <strong>{senha}</strong></p>
      </div>
      <div class="footer">
        <p>Atenciosamente,</p>
        <p>Equipe de suporte</p>
      </div>
      </div>
    </body>
    </html>
    """
    return corpo_email

def criar_corpo_envio_arquivo_html():
    corpo_email = f"""
    <html>
    <head>
      <style>
      body {{
        font-family: Arial, sans-serif;
      }}
      .container {{
        padding: 20px;
        border: 1px solid #ccc;
        border-radius: 10px;
        width: 80%;
        margin: 0 auto;
      }}
      .header {{
        background-color: #f2f2f2;
        padding: 10px;
        text-align: center;
        border-bottom: 1px solid #ccc;
      }}
      .content {{
        margin-top: 20px;
      }}
      .footer {{
        margin-top: 20px;
        text-align: center;
        font-size: 12px;
        color: #777;
      }}
      </style>
    </head>
    <body>
      <div class="container">
      <div class="header">
        <h2>Envio de Arquivos</h2>
      </div>
      <div class="content">
        <p>Segue em anexo os arquivos solicitados.</p>
      </div>
      <div class="footer">
        <p>Atenciosamente,</p>
        <p>Equipe de suporte</p>
      </div>
      </div>
    </body>
    </html>
    """
    return corpo_email