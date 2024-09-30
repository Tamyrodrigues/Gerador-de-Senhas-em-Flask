from flask import Flask, render_template_string, request
import bcrypt
import os
import string
import random

app = Flask(__name__)

def gerar_senha(tamanho=6):
    # Define os conjuntos de caracteres a serem usados
    letras_maiusculas = string.ascii_uppercase  # Letras maiúsculas (A-Z)
    numeros = string.digits                     # Números (0-9)
    caractere_especial = '*'                    # Caractere especial permitido
    # Se tamanho for maior que 6, limitamos a 6
    tamanho = min(tamanho, 6)

    # Garantir que a senha terá pelo menos um caractere de cada tipo
    senha = [
        random.choice(letras_maiusculas),      # Adiciona uma letra maiúscula
        random.choice(numeros),                 # Adiciona um número
        random.choice(caractere_especial)       # Adiciona o caractere especial
    ]

    # Preenche o restante da senha com caracteres aleatórios
    while len(senha) < tamanho:
        senha.append(random.choice(letras_maiusculas + numeros + caractere_especial))

    # Embaralha a senha para garantir que os caracteres não estejam em ordem fixa
    random.shuffle(senha)

    # Retorna a senha como uma string
    return ''.join(senha)


# Função para fazer o hash da senha
def hash_senha(senha):
    # Gera um sal aleatório
    salt = bcrypt.gensalt()
    # Hash da senha usando o sal
    senha_hash = bcrypt.hashpw(senha.encode('utf-8'), salt)
    return senha_hash

# HTML e CSS integrados
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gerador de Senhas</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
         :root {
            font-size: 62.5%;
        }
        
        body {
            font-size: 1.6rem;
            font-weight: 400;
            line-height: 1.6;
            font-family: Arial, sans-serif;
            background-color: #1d0b21;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        
        .container {
            background-color: transparent;
            border: 1px solid #fff;
            backdrop-filter: blur(2rem);
            padding: 3rem;
            border-radius: 0.8rem;
            max-width: 90%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        
        h1,
        h2,
        h5,
        h6 {
            text-align: center;
            color: #ffffff;
        }
        
        img {
            width: 35%;
        }
        
        .logo {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        
        label {
            display: block;
            margin: 10px 0 5px;
            color: #006375;
        }
        
        input[type="email"],
        input[type="submit"] {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border: 1px solid #006375;
            border-radius: 4px;
        }
        
        input[type="submit"] {
            background-color: #006375;
            color: #1d0b21;
            border: none;
            cursor: pointer;
        }
        
        input[type="submit"]:hover {
            background-color: #eef5ee;
        }
    </style>
</head>

<body>
    <div class="container">
        <div class="logo">
            <img src="./static/images/senha (1).png" alt="logo">
            <h1>Gerador de Senhas</h1>
        </div>
        <form method="post">
            <label for="email">Digite seu e-mail:</label>
            <input type="email" name="email" required>
            <input type="submit" value="Gerar Senha">
        </form>
        {% if senha %}
        <h2>Sua senha gerada é: <strong>{{ senha }}</strong></h2>
        <h5>O hash da sua senha é: <strong>{{ senha_hash }}</strong></h5>
        <h6>E-mail cadastrado: <strong>{{ email }}</strong></h6>
        {% endif %}
    </div>
</body>

</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    senha = None
    senha_hash = None
    email = None

    if request.method == 'POST':
        email = request.form['email']
        senha = gerar_senha()
        senha_hash = hash_senha(senha)

    return render_template_string(HTML_TEMPLATE, senha=senha, senha_hash=senha_hash, email=email)

if __name__ == '__main__':
    app.run(debug=True)
