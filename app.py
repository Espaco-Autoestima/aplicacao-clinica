import os
from flask import Flask, render_template, json, request
from flaskext.mysql import MySQL 

app = Flask(__name__)

# Configuração e conexão do banco
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'E$p@c02024!'
# Criar database
app.config['MYSQL_DATABASE_DB'] = ''
app.config['MYSQL_DATABASE_HOST'] = ''

mysql.init_app(app)

# def cadastro():
#     return render_template('cadastro.html')


