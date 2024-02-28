from flask import Flask, render_template, json, request
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configuração e conexão do banco
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'E$p@c02024!'
app.config['MYSQL_DATABASE_DB'] = ''
app.config['MYSQL_DATABASE_HOST'] = ''

mysql = MySQL(app)

# def cadastro():
#     return render_template('cadastro.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)


