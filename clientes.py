from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configuração e conexão do banco (a conexão não está funcionando)
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "E$p@c02024!"
app.config['MYSQL_DB'] = "espacoautoestima"
app.config['MYSQL_HOST'] = "172.17.0.2"

mysql = MySQL(app)

@app.route('/')
def index():
    return "Seja bem-vindo!"

@app.route('/iniciar')
def iniciar():
    return render_template('cadastro-clientes.html')

# Criar rotas das operações básicas do banco (CRUD)
@app.route('/clientes/cadastrar', methods=['POST'])
def adicionarCliente():
    if request.method == 'POST' and 'nome' in request.form and 'telefone' in request.form:
        nome = request.form['nome']
        telefone = request.form['telefone']

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO clientes(nome, telefone) VALUES (%s, %s)", (nome, telefone))
        mysql.connection.commit()
        return redirect(url_for('success'))
    return render_template('clientes.html')

@app.route('/clientes', methods=['GET'])
def consultarCliente():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()
    return render_template('clientes.html', clientes = clientes)

@app.route('/clientes/atualizar/<int:id>', methods=['POST'])
def atualizarCliente(id):
    if request.method == 'POST':
        nome = request.form['nome']
        telefone = request.form['telefone']

        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE clientes SET nome=%s, telefone=%s WHERE id=%s", (nome, telefone, id))
        mysql.connection.commit()
        return redirect(url_for('success'))
    return render_template('clientes.html')

@app.route('/clientes/deletar/<int:id>')
def deletarCliente():
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM clientes WHERE id=%s", (id))
    mysql.connection.commit()
    return render_template('clientes.html')

@app.route('/profissionais/cadastrar')
def cadastrarProfissional():
    if request.method == 'POST' and 'nome' in request.form and 'especializacao' in request.form:
        nome = request.form['nome']
        especializacao = request.form['especializacao']

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO profissionais(nome, especializacao) VALUES(%s, %s)", (nome, especializacao))
        mysql.connection.commit()
        return redirect(url_for('success'))
    return render_template('profissionais.html')

if __name__ == "__main__":
    app.run(debug=True)


