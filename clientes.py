from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configuração e conexão do banco (a conexão não está funcionando)
# app.config['MYSQL_USER'] = "dev"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "E$p@c02024!"
app.config['MYSQL_DB'] = "espacoautoestima"
app.config['MYSQL_HOST'] = "localhost"

mysql = MySQL(app)

@app.route('/')
def index():
    return "Seja bem-vindo!"

@app.route('/iniciar')
def iniciar():
    return render_template('cadastro-clientes.html')

# Criar rotas das operações básicas do banco (CRUD) de clientes, exceto DELETE
@app.route('/cadastrarCliente', methods=['POST'])
def adicionarCliente():
    if request.method == 'POST' and 'nome' in request.form and 'telefone' in request.form and 'email' in request.form and 'endereco' in request.form:
        nome = request.form['nome']
        telefone = request.form['telefone']
        email = request.form['email']
        endereco = request.form['endereco']

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO clientes(nome, telefone, email, endereco) VALUES (%s, %s, %s, %s)", (nome, telefone, email, endereco))
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

# Criar rotas das operações básicas do banco (CRUD) de profissionais, exceto DELETE
# @app.route('/cadastrarProfissionais')
# def cadastrarProfissional():
#     if request.method == 'POST' and 'nome' in request.form and 'especialidade' in request.form:
#         nome = request.form['nome']
#         especialidade = request.form['especializacao']
# Adicionar telefone e endereço

#         cursor = mysql.connection.cursor()
#         cursor.execute("INSERT INTO profissionais(nome, especialidade) VALUES(%s, %s)", (nome, especialidade))
#         mysql.connection.commit()
#         return redirect(url_for('success'))
#     return render_template('profissionais.html')

# Criar rotas das operações básicas do banco (CRUD) de agendamentos/consultas, exceto DELETE
# @app.route('/agendamento', methods=['POST', 'GET'])
# def agendamento():
#     if request.method == 'POST' and 'nome' in request.form and 'telefone' in request.form: #and 'nomep' in request.form and 'sessao' in request.form and 'horario' in request.form:
#         nome = request.form['nome']
#         #nomep = request.form['nomep']
#         telefone = request.form['telefone']
#         sessao = request.form['sessao']
#         # alterar campo na tabela do banco
#         horario = request.form['horario']
        
#         cursor = mysql.connection.cursor()
#         cursor.execute("INSERT INTO consulta(nome, telefone, sessao, horario) VALUES (%s, %s, %s, %s)", (nome, telefone, sessao, horario))
#         mysql.connection.commit()
#     return render_template('agendamento.html')

if __name__ == "__main__":
    app.run(debug=True)


