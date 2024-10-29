from app import app
from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector

config = {
    'user': 'root', 
    'password': 'E$p@c02024!', 
    'host': 'localhost', 
    'database': 'espacoautoestima',
    'raise_on_warnings': True
}

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'email' in request.form and 'senha' in request.form:
        email = request.form['email']
        senha = request.form['senha']
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        # Selecionando os dados no banco
        query = "SELECT * FROM contas WHERE email = %s AND senha = %s"
        cursor.execute(query, (email, senha))
        conta = cursor.fetchone()

        # Verifica se a conta existe. Se sim, redireciona para a home
        if conta:
            session['loggedin'] = True
            session['id'] = conta[0]
            session['email'] = conta[1]
            session['senha'] = conta[2]
            return redirect(url_for('home'))
        else:
            # Caso não exista ou se algum dado esteja incorreto
            flash("E-mail ou senha incorretos", "danger")

    return render_template('login.html')

@app.route('/signup', methods=['POST', 'GET'])
def signUp():
    if request.method == 'POST' and 'nome' in request.form and 'telefone' in request.form and 'email' in request.form and 'senha' in request.form:
        nome = request.form['nome']
        telefone = request.form['telefone']
        email = request.form['email']
        senha = request.form['senha']

        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        # Selecionando os dados no banco
        query = "SELECT * FROM contas WHERE email = %s and senha = %s"
        cursor.execute(query, (email, senha))
        conta = cursor.fetchone()
        # Verifica se existe a conta. Se existir, redireciona para a home
        if conta:
            session['loggedin'] = True
            session['id'] = conta[0]
            flash("Uma conta com esse e-mail já criada. Clique para fazer login", "warning")
        else:
            # Inserindo os dados no banco
            query = "INSERT INTO contas (nome_usuario, telefone, email, senha) VALUES (%s, %s, %s, %s)"
        
            cursor.execute(query, (nome, telefone, email, senha))
            cnx.commit()
            cursor.close()
            cnx.close()
            flash("Conta criada com sucesso!", "success")
            return redirect(url_for('login'))
    
    return render_template('cadastro.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('login')

# @app.route('/apagar-conta/<int:id>', methods=['POST', 'GET'])
# def apagar_conta(id):
#     cnx = mysql.connector.connect(**config)
#     cursor = cnx.cursor()

#     try:
#         if conta:
#             session['loggedin'] = True
#             session['id'] = conta[0]
#             query = "DELETE FROM contas WHERE id = %s"
#             cursor.execute(query, (id,))
#             cnx.commit()
#             cursor.close()
#             cnx.close()
#             flash("Conta excluída com sucesso!", "success")
#             return redirect(url_for('signUp', contas=contas))
        
#     except mysql.connector.Error as err:
#         flash(f'Ocorreu um erro: {err}', 'error')
#         cnx.rollback()

#     finally:
#         cursor.close()
#         cnx.close()

# Exibe a página inicial apenas para usuários logados
@app.route('/home')
def home():
    if 'loggedin' in session:
        return render_template('home.html', email=session['email'])
    return redirect(url_for('login'))