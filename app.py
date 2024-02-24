from flask import Flask
from flask_mysqldb import MySQL 

app = Flask(__name__)

# Configuração e conexão do banco

# api.secret_key = 'you secret key' (manter comentado temporariamente)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
# app.config["MYSQL_DB"] = "database"

mysql = MySQL(app)

