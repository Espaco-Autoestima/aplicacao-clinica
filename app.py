from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configuração e conexão do banco (a conexão não está funcionando)
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'E$p@c02024!'
# app.config['MYSQL_ROOT_PASSWORD'] = 'E$p@c02024!'
app.config['MYSQL_DB'] = 'espacoautoestima'
app.config['MYSQL_HOST'] = '172.17.0.2'
# app.config['MYSQL_HOST'] = '172.17.0.1' -> IP do Gateway
# app.config['MYSQL_HOST'] = 'dockermysql5' -> Nome do container Docker criado

mysql = MySQL(app)

@app.route('/clientes', methods=['POST', 'GET'])
def cadastroClientes():
    nome = request.form['nome']
    telefone = request.form['telefone']

    if nome and telefone:
        connector = mysql.connect()
        cursor = connector.cursor()
        cursor.execute('INSERT INTO clientes (nome, telefone) VALUES (%s, %s)', (nome, telefone))
        connector.commit()
    return render_template('cadastro-clientes.html')

# @app.route('/profissionais')
# def cadastroProfissionais():
#     nome = request.form['nome']
#     especializacao = request.form['especializacao']

#     if nome and especializacao:
#         connector = mysql.connect()
#         cursor = connector.cursor()
#         cursor.execute('INSERT INTO clientes (nome, especializacao) VALUES (%s, %s)', (nome, especializacao))
#         connector.commit()
#     return render_template('cadastro-profissionais.html')

if __name__ == "__main__":
    app.run(debug=True)


