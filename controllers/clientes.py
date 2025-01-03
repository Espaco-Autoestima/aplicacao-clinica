from app import app
from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector

config = {
    'user': 'root', 
    'password': 'E$p@c02024!', 
    'host': 'localhost', 
    'database': 'espacoautoestima',
    'raise_on_warnings': True
}

@app.route('/cliente', methods=['POST', 'GET'])
def adicionar_cliente():
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

@app.route('/clientes', methods=['POST', 'GET'])
def consultar_clientes():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()
    return render_template('clientes.html', clientes = clientes)

# Busca de clientes por e-mail
@app.route('/pesquisar-cliente', methods=['POST'])
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

@app.route('/clientes/<int:id>', methods=['POST', 'GET'])
def atualizar_cliente(id):
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
        return redirect(url_for('consultar_clientes'))
    
    # Carrega os dados do cliente para o formulário
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM clientes WHERE id = %s", (id,))
    cliente = cursor.fetchone()
    cursor.close()
    cnx.close()

    return render_template('atualizar-clientes.html', cliente = cliente)

@app.route('/cliente/<int:id>', methods=['POST', 'GET'])
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
        
    return redirect(url_for('consultar_clientes'))