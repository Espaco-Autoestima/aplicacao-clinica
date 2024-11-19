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
@app.route('/cadastrarProfissional', methods=['POST', 'GET'])
def adicionarProfissional():
=======
@app.route('/cadastrar-profissionais', methods=['POST', 'GET'])
def adicionar_profissional():
>>>>>>> Stashed changes
    if request.method == 'POST' and 'nome' in request.form and 'telefone' in request.form and 'especialidade' in request.form:
        nome = request.form['nome']
        telefone = request.form['telefone']
        especialidade = request.form['especialidade']

        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        # Inserindo os dados no banco
        query = "INSERT INTO profissionais (nome, telefone, especialidade) VALUES (%s, %s, %s)"
        cursor.execute(query, (nome, telefone, especialidade))
        cnx.commit()
        cursor.close()
        cnx.close()
        return redirect('profissionais')
    
    return render_template('cadastro-profissionais.html')

@app.route('/profissionais', methods=['POST', 'GET'])
def consultarProfissional():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM profissionais")
    profissionais = cursor.fetchall()
    return render_template('profissionais.html', profissionais = profissionais)

# Busca de profissionais por telefone
<<<<<<< Updated upstream
@app.route('/pesquisarProfissional', methods=['POST'])
=======
@app.route('/pesquisar-profissionais', methods=['POST'])
>>>>>>> Stashed changes
def pesquisar_profissionais():
    try:
        telefone = request.form.get("pesquisa")
        
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor(dictionary=True)
            
        # Usando placeholders para evitar SQL Injection
        query = "SELECT * FROM profissionais WHERE telefone=%s"
        cursor.execute(query, (telefone,))
            
        resultados = cursor.fetchall()

        return render_template('profissionais.html', resultados = resultados)
        
    except mysql.connector.Error as err:
        return f"Tente novamente mais tarde: {err}", 500
        
    finally:
        cursor.close()
        cnx.close()

<<<<<<< Updated upstream
@app.route('/atualizarProfissional/<int:id>', methods=['POST', 'GET'])
def atualizarProfissional(id):
=======
@app.route('/atualizar-profissionais/<int:id>', methods=['POST', 'GET'])
def atualizar_profissional(id):
>>>>>>> Stashed changes
    if request.method == 'POST':
        nome = request.form['nome']
        telefone = request.form['telefone']
        especialidade = request.form['especialidade']

        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        query = "UPDATE profissionais SET nome=%s, telefone=%s, especialidade=%s WHERE id=%s"
        cursor.execute(query, (nome, telefone, especialidade, id))
        cnx.commit()
        cursor.close()
        cnx.close()
        return redirect(url_for('consultarProfissional'))
    
    # Carrega os dados do profissional para o formulário
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM profissionais WHERE id = %s", (id,))
    profissional = cursor.fetchone()
    cursor.close()
    cnx.close()

<<<<<<< Updated upstream
    return render_template('atualizar-profissionais.html', profissional = profissional)
=======
    return render_template('atualizar-profissionais.html', profissional = profissional)

@app.route('/excluir-profissionais/<int:id>', methods=['POST', 'GET'])
def deletar_profissional(id):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    try:
        query_verificar_profissional = """
            SELECT * FROM profissionais WHERE id = %s
        """

        cursor.execute(query_verificar_profissional, (id,))
        profissional_existe = cursor.fetchone()

        if profissional_existe:
            query_profissional = """
            DELETE FROM profissionais WHERE id = %s
            """
            cursor.execute(query_profissional, (id,))
            cnx.commit()
            flash('Profissional excluído com sucesso!', 'success')
        else:
            flash('Profissional não encontrado', 'error')

    except mysql.connector.Error as err:
        flash(f'Ocorreu um erro: {err}', 'error')
        cnx.rollback()

    finally:
        cursor.close()
        cnx.close()
        
    return render_template('cadastro-profissionais.html')
>>>>>>> Stashed changes
