from flask import Flask, render_template, request, redirect, url_for
#from flask_mysqldb import MySQL
import mysql.connector

app = Flask(__name__)

# Configuração e conexão do banco (flask-mysqldb)
# app.config['MYSQL_USER'] = "root"
# app.config['MYSQL_PASSWORD'] = "E$p@c02024!"
# app.config['MYSQL_DB'] = "espacoautoestima"
# app.config['MYSQL_HOST'] = "localhost"

# mysql = MySQL(app)

config = {
    'user': 'root', 
    'password': 'E$p@c02024!', 
    'host': 'localhost', 
    'database': 'espacoautoestima',
    'raise_on_warnings': True
}

@app.route('/')
def index():
    return "Seja bem-vindo!"

@app.route('/iniciar')
def iniciar():
    return render_template('cadastro-clientes.html')

# Criar rotas das operações básicas do banco (CRUD) de clientes, exceto DELETE

@app.route('/cadastrarCliente', methods=['POST', 'GET'])
def adicionarCliente():
    if request.method == 'POST' and 'nome' in request.form and 'telefone' in request.form and 'email' in request.form:
        nome = request.form['nome']
        telefone = request.form['telefone']
        email = request.form['email']

        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        # Inserindo os dados no banco de dados
        query = "INSERT INTO clientes (nome, telefone, email) VALUES (%s, %s, %s)"
        cursor.execute(query, (nome, telefone, email))
        cnx.commit()
        cursor.close()
        cnx.close()
        return redirect('clientes')
    
    return render_template('cadastro-clientes.html')

@app.route('/clientes', methods=['POST', 'GET'])
def consultarCliente():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()
    return render_template('clientes.html', clientes = clientes)

@app.route('/atualizarCliente/<int:id>', methods=['POST', 'GET'])
def atualizarCliente(id):
    if request.method == 'POST':
        nome = request.form['nome']
        telefone = request.form['telefone']
        email = request.form['email']

        cnx = mysql.connection.cursor()
        cursor = cnx.cursor()
        query = "UPDATE clientes SET nome=%s, telefone=%s, email=%s WHERE id=%s"
        cursor.execute(query, (id, nome, telefone, email))
        cnx.commit()
        cursor.close()
        cnx.close()
        return redirect('clientes')
    return render_template('atualizar-clientes.html')

#Criar rotas das operações básicas do banco (CRUD) de profissionais, exceto DELETE
@app.route('/cadastrarProfissional', methods=['POST', 'GET'])
def cadastrarProfissional():
    if request.method == 'POST' and 'nome' in request.form and 'telefone' in request.form and 'especialidade' in request.form:
        nome = request.form['nome']
        telefone = request.form['telefone']
        especialidade = request.form['especialidade']

        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        # Inserindo os dados no banco de dados
        query = "INSERT INTO profissionais (nome, telefone, especialidade) VALUES (%s, %s, %s)"
        cursor.execute(query, (nome, telefone, especialidade))
        cnx.commit()
        cursor.close()
        cnx.close()
        return redirect('profissionais')
    
    return render_template('cadastro-profissionais.html')

@app.route('/profissionais', methods=['POST', 'GET'])
def consultarProfissional():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM profissionais")
    profissionais = cursor.fetchall()
    return render_template('profissionais.html', profissionais = profissionais)

@app.route('/atualizarProfissional/<int:id>', methods=['POST', 'GET'])
def atualizarProfissional(id):
    if request.method == 'POST':
        nome = request.form['nome']
        telefone = request.form['telefone']
        especialidade = request.form['especialidade']

        cnx = mysql.connection.cursor()
        cursor = cnx.cursor()
        query = "UPDATE profissionais SET nome=%s, telefone=%s, especialidade=%s WHERE id=%s"
        cursor.execute(query, (id, nome, telefone, especialidade))
        cnx.commit()
        cursor.close()
        cnx.close()
        return redirect('profissionais')
    return render_template('atualizar-profissionais.html')

if __name__ == "__main__":
    app.run(debug=True)


