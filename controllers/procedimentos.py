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

@app.route('/cadastrarProcedimento', methods=['POST', 'GET'])
def adicionarProcedimento():
    if request.method == 'POST' and 'procedimento' in request.form and 'descricao' in request.form:
        nome = request.form['procedimento']
        descricao = request.form['descricao']

        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        # Inserindo dados no banco
        query = "INSERT INTO procedimentos (nome, descricao) VALUES (%s, %s)"
        cursor.execute(query, (nome, descricao))
        cnx.commit()
        cursor.close()
        cnx.close()
        return redirect('procedimentos')
    
    return render_template('cadastro-procedimentos.html')

@app.route('/procedimentos', methods=['POST', 'GET'])
def consultarProcedimento():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM procedimentos")
    procedimentos = cursor.fetchall()
    return render_template('procedimentos.html', procedimentos = procedimentos)

# Pesquisar procedimentos pelo nome
@app.route('/pesquisarProcedimento', methods=['POST'])
def pesquisar_procedimentos():
    try:
        nome = request.form.get("pesquisa")

        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor(dictionary=True)

        # Usando placeholders para evitar SQL Injection
        query = "SELECT * FROM procedimentos WHERE nome LIKE %s"
        cursor.execute(query, (f"%{nome}%",))

        resultados = cursor.fetchall()

        return render_template('procedimentos.html', resultados = resultados)
    
    except mysql.connector.Error as err:
        return f"Tente novamente mais tarde: {err}", 500
    
    finally:
        cursor.close()
        cnx.close()

@app.route('/atualizarProcedimento/<int:id>', methods=['POST', 'GET'])
def atualizarProcedimento(id):
    if request.method == 'POST':
        nome = request.form['procedimento']
        descricao = request.form['descricao']

        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        query = "UPDATE procedimentos SET nome=%s, descricao=%s WHERE id=%s"
        cursor.execute(query, (nome, descricao, id))
        cnx.commit()
        cursor.close()
        cnx.close()
        return redirect(url_for('consultarProcedimento'))
    
    # Carrega os dados do procedimento para o formulário
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM procedimentos WHERE id = %s", (id,))
    procedimentoList = cursor.fetchone()
    cursor.close()
    cnx.close()

    return render_template('atualizar-procedimentos.html', procedimento = procedimentoList)

@app.route('/deletar-procedimento/<int:id>', methods=['POST', 'GET'])
def deletar_procedimento(id):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    try:
        query_verificar_procedimento = """
            SELECT * FROM procedimentos WHERE id = %s
        """

        cursor.execute(query_verificar_procedimento, (id,))
        procedimento_existe = cursor.fetchone()

        if procedimento_existe:
            query_procedimento = """
            DELETE FROM procedimentos WHERE id = %s
            """

            cursor.execute(query_procedimento, (id,))
            cnx.commit()
            flash('Procedimento excluído com sucesso!', 'success')
        else:
            flash('Procedimento não encontrado', 'error')

    except mysql.connector.Error as err:
        flash(f'Ocorreu um erro: {err}', 'error')
        cnx.rollback()

    finally:
        cursor.close()
        cnx.close()
        
    return render_template('cadastro-procedimentos.html')