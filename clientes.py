from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configuração e conexão do banco
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
@app.route('/cadastrarCliente', methods=['POST', 'GET'])
def adicionarCliente():
    if request.method == 'POST' and 'nome' in request.form and 'telefone' in request.form and 'email' in request.form:
        nome = request.form['nome']
        telefone = request.form['telefone']
        email = request.form['email']

        conn = mysql.connection.cursor()
        conn.execute("INSERT INTO clientes(nome, telefone, email) VALUES (%s, %s, %s)", (nome, telefone, email))
        mysql.connection.commit()
        return redirect('clientes.html')
    return render_template('cadastro-clientes.html')

@app.route('/clientes', methods=['POST', 'GET'])
def consultarCliente():
    conn = mysql.connection.cursor()
    conn.execute("SELECT * FROM clientes")
    clientes = conn.fetchall()
    return render_template('clientes.html', clientes = clientes)

@app.route('/atualizarClientes/<int:id>', methods=['POST', 'GET'])
def atualizarCliente(id):
    if request.method == 'POST':
        nome = request.form['nome']
        telefone = request.form['telefone']
        email = request.form['email']

        conn = mysql.connection.cursor()
        conn.execute("UPDATE clientes SET nome=%s, telefone=%s, email=%s WHERE id=%s", (nome, telefone, email, id))
        mysql.connection.commit()
        return redirect('atualizar-cliente')
    return render_template('clientes.html')

# Criar rotas das operações básicas do banco (CRUD) de profissionais, exceto DELETE
# @app.route('/cadastrarProfissionais')
# def cadastrarProfissional():
#     if request.method == 'POST' and 'nome' in request.form and 'especialidade' in request.form:
#         nome = request.form['nome']
#         especialidade = request.form['especializacao']
# Adicionar telefone e endereço

#         conn = mysql.connection.cursor()
#         conn.execute("INSERT INTO profissionais(nome, especialidade) VALUES(%s, %s)", (nome, especialidade))
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
        
#         conn = mysql.connection.cursor()
#         conn.execute("INSERT INTO consulta(nome, telefone, sessao, horario) VALUES (%s, %s, %s, %s)", (nome, telefone, sessao, horario))
#         mysql.connection.commit()
#     return render_template('agendamento.html')

if __name__ == "__main__":
    app.run(debug=True)


