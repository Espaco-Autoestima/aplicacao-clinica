from app import app
from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime
import mysql.connector

config = {
    'user': 'root', 
    'password': 'E$p@c02024!', 
    'host': 'localhost', 
    'database': 'espacoautoestima',
    'raise_on_warnings': True
}

@app.route('/cadastrarProduto', methods=['POST', 'GET'])
def adicionarProduto():
    if request.method == 'POST' and 'sku' in request.form and 'nome' in request.form and 'data-validade' in request.form and 'quantidade' in request.form and 'marca' in request.form and 'preco' in request.form and 'descricao' in request.form:
        codigo_sku = request.form['sku']
        produto = request.form['nome']
        dataValidade = request.form['data-validade']
        quantidade = request.form['quantidade']
        marca = request.form['marca']
        preco = request.form['preco']
        descricao = request.form['descricao']

        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        # Inserindo dados no banco 
        query = "INSERT INTO produtos (nome, data_validade, quantidade, marca, preco, descricao, sku) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (produto, dataValidade, quantidade, marca, preco, descricao, codigo_sku))
        cnx.commit()
        cursor.close()
        cnx.close()
        return redirect('produtos')
    
    return render_template('cadastro-produtos.html')

@app.route('/produtos', methods=['POST', 'GET'])
def consultarProduto():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()
    return render_template('produtos.html', produtos = produtos)

# Busca de produtos por nome
@app.route('/pesquisarProduto', methods=['POST'])
def pesquisar_produtos():
    try:
        sku = request.form.get("pesquisa")

        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor(dictionary=True)

        query = "SELECT * FROM produtos WHERE sku=%s"
        cursor.execute(query, (sku,))

        resultados = cursor.fetchall()

        return render_template('produtos.html', resultados = resultados)
    
    except mysql.connector.Error as err:
        return f"Tente novamente mais tarde: {err}", 500

    finally:
        cursor.close()
        cnx.close() 

@app.route('/atualizarProduto/<int:id>', methods=['POST', 'GET'])
def atualizarProduto(id):
    if request.method == 'POST':
        codigo_sku = request.form['sku']
        produto = request.form['nome']
        dataValidade = request.form['data-validade']
        quantidade = request.form['quantidade']
        marca = request.form['marca']
        preco = request.form['preco']
        descricao = request.form['descricao']

        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        query = """
            UPDATE produtos 
            SET nome=%s, data_validade=%s, quantidade=%s, marca=%s, preco=%s, descricao=%s, sku=%s 
            WHERE id=%s
        """
        cursor.execute(query, (produto, dataValidade, quantidade, marca, preco, descricao, codigo_sku, id))
        cnx.commit()
        cursor.close()
        cnx.close()
        return redirect(url_for('consultarProduto'))
    
    # Carrega os dados do produto para o formulário
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM produtos WHERE id = %s", (id,))
    produto = cursor.fetchone()
    cursor.close()
    cnx.close()

    return render_template('atualizar-produtos.html', produto = produto)

@app.route('/deletar-produto/<int:id>', methods=['POST', 'GET'])
def deletar_produto(id):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    try:
        query_verificar_produto = """
            SELECT * FROM produtos WHERE id = %s
        """

        cursor.execute(query_verificar_produto, (id,))
        produto_existe = cursor.fetchone()

        if produto_existe:
            query_produto = """
            DELETE FROM produtos WHERE id = %s
            """
            cursor.execute(query_produto, (id,))
            cnx.commit()
            flash('Produto excluído com sucesso', 'success')
        else:
            flash('Produto não encontrado', 'error')
    
    except mysql.connector.Error as err:
        flash(f'Ocorreu um erro: {err}', 'error')
        cnx.rollback()

    finally:
        cursor.close()
        cnx.close()
        
    return render_template('cadastro-produtos.html')