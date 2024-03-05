from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configuração e conexão do banco (a conexão não está funcionando)
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "E$p@c02024!"
app.config['MYSQL_DB'] = "espacoautoestima"
app.config['MYSQL_HOST'] = "172.17.0.2"

mysql = MySQL(app)

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