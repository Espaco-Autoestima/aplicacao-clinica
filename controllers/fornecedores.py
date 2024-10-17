from app import app
from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector

app = Flask(__name__)

app.secret_key = 'secret-key-ea'

# Configuração e conexão do banco de dados 
config = {
    'user': 'root', 
    'password': 'E$p@c02024!', 
    'host': 'localhost', 
    'database': 'espacoautoestima',
    'raise_on_warnings': True
}

@app.route('/cadastrarFornecedor', methods=['POST', 'GET'])
def adicionarFornecedor():
    if request.method == 'POST' and 'nome' in request.form and 'telefone' in request.form and 'empresa' in request.form:
        nome = request.form['nome']
        telefone = request.form['telefone']
        empresa = request.form['empresa']

        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        # Inserindo os dados no banco
        query = "INSERT INTO fornecedores (nome, telefone, empresa) VALUES (%s, %s, %s)"
        cursor.execute(query, (nome, telefone, empresa))
        cnx.commit()
        cursor.close()
        cnx.close()
        return redirect('fornecedores')
    
    return render_template('cadastro-fornecedores.html')

@app.route('/fornecedores', methods=['POST', 'GET'])
def consultarFornecedor():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM fornecedores")
    fornecedores = cursor.fetchall()
    return render_template('fornecedores.html', fornecedores = fornecedores)

# Busca de fornecedores por telefone 
@app.route('/pesquisarFornecedor', methods=['POST'])
def pesquisar_fornecedores():
    try:
        telefone = request.form.get("pesquisa")
        
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor(dictionary=True)
            
        # Usando placeholders para evitar SQL Injection
        query = "SELECT * FROM fornecedores WHERE telefone=%s"
        cursor.execute(query, (telefone,))
            
        resultados = cursor.fetchall()

        return render_template('fornecedores.html', resultados = resultados)
        
    except mysql.connector.Error as err:
        return f"Tente novamente mais tarde: {err}", 500
        
    finally:
        cursor.close()
        cnx.close()

@app.route('/atualizarFornecedor/<int:id>', methods=['POST', 'GET'])
def atualizarFornecedor(id):
    if request.method == 'POST':
        nome = request.form['nome']
        telefone = request.form['telefone']
        empresa = request.form['empresa']

        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        query = "UPDATE fornecedores SET nome=%s, telefone=%s, empresa=%s WHERE id=%s"
        cursor.execute(query, (nome, telefone, empresa, id))
        cnx.commit()
        cursor.close()
        cnx.close()
        return redirect(url_for('consultarFornecedor'))

    # Carrega os dados do fornecedor para o formulário
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM fornecedores WHERE id = %s", (id,))
    fornecedor = cursor.fetchone()
    cursor.close()
    cnx.close()

    return render_template('atualizar-fornecedores.html', fornecedor = fornecedor)