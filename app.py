from flask import Flask, request, render_template, redirect, url_for, flash, session
import json
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Necessário para usar flash messages e sessões

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pop_up')
def pop_up():
    return render_template('pop_up.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        confirmar_senha = request.form['confirmar_senha']

        if senha != confirmar_senha:
            #flash('Senhas não coincidem!', 'error')
            return redirect(url_for('pop_up'))

        dados = {
            'nome': nome,
            'email': email,
            'senha': senha
        }

        with open('cadastros.json', 'a') as file:
            json.dump(dados, file)
            file.write('\n')

        flash('Cadastro realizado com sucesso!', 'success')
        return redirect(url_for('index'))

    return render_template('cadastro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        if not os.path.exists('cadastros.json'):
            #flash('Nenhum usuário cadastrado!', 'error')
            return redirect(url_for('login'))

        with open('cadastros.json', 'r') as file:
            usuarios = file.readlines()

        for usuario in usuarios:
            dados = json.loads(usuario)
            if dados['email'] == email and dados['senha'] == senha:
                session['user'] = dados['nome']  # Armazena o nome do usuário na sessão
                flash(f'Bem-vindo, {dados["nome"]}!', 'success')
                return redirect(url_for('index'))

        flash('E-mail ou senha incorretos!', 'error')
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Você saiu com sucesso!', 'success')
    return redirect(url_for('index'))

@app.route('/usuarios')
def usuarios():
    if 'user' not in session:
        flash('Por favor, faça login para acessar esta página.', 'error')
        return redirect(url_for('login'))

    if not os.path.exists('cadastros.json'):
        usuarios = []
    else:
        with open('cadastros.json', 'r') as file:
            usuarios = [json.loads(line) for line in file]

    return render_template('usuarios.html', usuarios=usuarios)

@app.route('/contatos')
def contatos():
    return render_template('contatos.html')

if __name__ == '__main__':
    app.run(debug=True)

if __name__ == '__main__':
    app.run(debug=True)

