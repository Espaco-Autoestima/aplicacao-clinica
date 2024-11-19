from app import app
from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector

app.secret_key = 'secret-key-ea'

# Configuração e conexão do banco de dados 
config = {
    'user': 'root', 
    'password': 'E$p@c02024!', 
    'host': 'localhost', 
    'database': 'espacoautoestima',
    'raise_on_warnings': True
}

<<<<<<< Updated upstream
@app.route('/cadastrarCliente', methods=['POST', 'GET'])
def adicionarCliente():
=======
@app.route('/cadastrar-clientes', methods=['POST', 'GET'])
def adicionar_cliente():
>>>>>>> Stashed changes
    if request.method == 'POST' and 'nome' in request.form and 'telefone' in request.form and 'email' in request.form and 'cpf' in request.form:
        nome = request.form['nome']
        telefone = request.form['telefone']
        email = request.form['email']
        cpf = request.form['cpf']

        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        # Inserindo os dados no banco
        query = "INSERT INTO clientes (nome, telefone, email, cpf) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (nome, telefone, email, cpf))
        cnx.commit()
        cursor.close()
        cnx.close()
        return redirect('clientes')
    
    return render_template('cadastro-clientes.html')

<<<<<<< Updated upstream
@app.route('/clientes', methods=['POST', 'GET'])
def consultarCliente():
=======
@app.route('/clientes', methods=['GET'])
def consultar_clientes():
>>>>>>> Stashed changes
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()
    return render_template('clientes.html', clientes = clientes)

# Busca de clientes por e-mail
<<<<<<< Updated upstream
@app.route('/pesquisarCliente', methods=['POST'])
=======
@app.route('/pesquisar-clientes', methods=['POST´p'])
>>>>>>> Stashed changes
def pesquisar_clientes():
    try:
        email = request.form.get("pesquisa")
        
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor(dictionary=True)
            
        # Usando placeholders para evitar SQL Injection
        query = "SELECT * FROM clientes WHERE email=%s"
        cursor.execute(query, (email,))
            
        resultados = cursor.fetchall()

        return render_template('clientes.html', resultados = resultados)
        
    except mysql.connector.Error as err:
        return f"Tente novamente mais tarde: {err}", 500
        
    finally:
        cursor.close()
        cnx.close()

<<<<<<< Updated upstream
@app.route('/atualizarCliente/<int:id>', methods=['POST', 'GET'])
def atualizarCliente(id):
=======
@app.route('/atualizar-clientes/<int:id>', methods=['POST', 'GET', 'PUT'])
def atualizar_cliente(id):
>>>>>>> Stashed changes
    if request.method == 'POST':
        nome = request.form.get('nome')
        telefone = request.form.get('telefone')
        email = request.form.get('email')
        cpf = request.form.get('cpf')

        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        query = "UPDATE clientes SET nome=%s, telefone=%s, email=%s, cpf=%s WHERE id=%s"
        cursor.execute(query, (nome, telefone, email, cpf, id))
        cnx.commit()
        cursor.close()
        cnx.close()
        return redirect(url_for('consultarCliente'))
    
    # Carrega os dados do cliente para o formulário
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM clientes WHERE id = %s", (id,))
    cliente = cursor.fetchone()
    cursor.close()
    cnx.close()

<<<<<<< Updated upstream
    return render_template('atualizar-clientes.html', cliente = cliente)
=======
    return render_template('atualizar-clientes.html', cliente = cliente)

@app.route('/deletar-clientes/<int:id>', methods=['POST', 'GET'])
def deletar_cliente(id):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    
    try:
        query_verificar_cliente = """
            SELECT * FROM clientes WHERE id = %s
        """

        cursor.execute(query_verificar_cliente, (id,))
        cliente_existe = cursor.fetchone()

        if cliente_existe:
            query_verificar_agendamento = "SELECT * FROM agendamento WHERE clientes_id = %s"
            cursor.execute(query_verificar_agendamento, (id,))
            agendamento_existe = cursor.fetchone()

            if agendamento_existe:
                flash('Não é possível excluir o cliente porque ele possui agendamentos associados', 'error')
            else: 
                query_cliente = """
                DELETE FROM clientes WHERE id = %s 
                """
                cursor.execute(query_cliente, (id,))
                cnx.commit()
                flash('Cliente excluído com sucesso!', 'success')
        else:
            flash('Cliente não encontrado', 'error')
        
    except mysql.connector.Error as err:
        flash(f'Ocorreu um erro: {err}', 'error')
        cnx.rollback()

    finally:
        cursor.close()
        cnx.close()
        
    return render_template('cadastro-clientes.html')
>>>>>>> Stashed changes
