from app import app
from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
import datetime as dt 
import time as tm

config = {
    'user': 'root', 
    'password': 'E$p@c02024!', 
    'host': 'localhost', 
    'database': 'espacoautoestima',
    'raise_on_warnings': True
}

@app.route('/agendamento', methods=['POST', 'GET'])
def realizar_agendamento():
    if request.method == 'POST':
        nome_cliente = request.form['nomec']
        nome_profissional = request.form['nomep']
        sessao = request.form['sessao']
        horario = request.form['horario']
        data = request.form['data']

        try:
            cnx = mysql.connector.connect(**config, buffered=True)
            cursor = cnx.cursor(dictionary=True)

            # Verifica se o profissional já tem um agendamento na mesma data e hora
            query_verificar_agendamento = """
                SELECT * FROM agendamento
                WHERE nomeProfissional = %s AND data = %s AND horario = %s
            """
            cursor.execute(query_verificar_agendamento, (nome_profissional, data, horario))
            agendamento_existe = cursor.fetchone()

            if agendamento_existe:
                flash('Este profissional já possui um agendamento nesta data e horário', 'warning')
                cursor.close()
                cnx.close()
                return redirect(url_for('realizar_agendamento'))

            # Verifica na tabela de disponibilidades no MySQL se possuem a data com o profissional disponível
            query_disponibilidade = """ 
                SELECT d.id_disponibilidade
                FROM disponibilidade d
                WHERE d.dia = %s AND d.hora = %s AND d.profissionais_id = (
                    SELECT id FROM profissionais WHERE nome = %s LIMIT 1
                )
            """
            
            cursor.execute(query_disponibilidade, (data, horario, nome_profissional))
            disponibilidade = cursor.fetchone()

            if not disponibilidade:
                flash('Horário não disponível para agendamento', 'error')
                cursor.close()
                cnx.close()
                return redirect(url_for('realizar_agendamento'))

            # Verifica se o cliente existe
            query_cliente = "SELECT id FROM clientes WHERE nome = %s"
            cursor.execute(query_cliente, (nome_cliente,))
            cliente = cursor.fetchone()
            if not cliente:
                flash('Cliente não encontrado.', 'error')
                cursor.close()
                cnx.close()
                return redirect(url_for('consultar_clientes'))

            # Verifica se o profissional existe
            query_profissional = "SELECT id FROM profissionais WHERE nome = %s"
            cursor.execute(query_profissional, (nome_profissional,))
            profissional = cursor.fetchone()
            if not profissional:
                flash('Profissional não encontrado', 'error')
                cursor.close()
                cnx.close()
                return redirect(url_for('consultar_profissionais'))

            # Insere o novo agendamento
            query_agendamento = """
                INSERT INTO agendamento(nomeCliente, nomeProfissional, sessao, data, horario, clientes_id, profissionais_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query_agendamento, (nome_cliente, nome_profissional, sessao, data, horario, cliente['id'], profissional['id']))

            # Realizar o commit da transação
            cnx.commit()
            flash('Agendamento realizado com sucesso!', 'success')
            cursor.close()
            cnx.close()
            return redirect(url_for('consultar_agendamentos'))

        except mysql.connector.Error as err:
            flash(f'Não foi possível agendar o cliente no momento: {err}', 'error')
            cursor.close()
            cnx.close()
            return redirect(url_for('realizar_agendamento'))

        finally:
            cursor.close()
            cnx.close()

    return render_template('cadastro-agendamento.html')

# Endpoint de listagem de agendamentos
@app.route('/agendamentos', methods=['POST', 'GET'])
def consultar_agendamentos():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM agendamento ORDER BY data ASC, horario ASC")
    agendamentos = cursor.fetchall()
    return render_template('agendamentos.html', agendamentos=agendamentos)

# Endpoint de atualização de agendamentos
@app.route('/agendamentos/<int:id>', methods=['POST', 'GET'])
def atualizar_agendamento(id):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    
    if request.method == 'POST':
        nome_cliente = request.form['nomec']
        nome_profissional = request.form['nomep']
        sessao = request.form['sessao']
        horario = request.form['horario']
        data = request.form['data']

        try:
            # Verifica se o profissional já tem um agendamento na mesma data e hora, exceto o atual
            query_verificar_agendamento = """
                SELECT * FROM agendamento
                WHERE nomeProfissional = %s AND data = %s AND horario = %s AND id != %s
            """
            cursor.execute(query_verificar_agendamento, (nome_profissional, data, horario, id))
            agendamento_existe = cursor.fetchone()

            if agendamento_existe:
                flash('Este profissional já possui um agendamento nesta data e horário', 'error')
                return redirect(url_for('consultar_agendamentos'))

            # Verifica na tabela de disponibilidade no MySQL se possuem a data com o profissional disponível
            query_disponibilidade = """ 
                SELECT d.id_disponibilidade
                FROM disponibilidade d
                INNER JOIN profissionais p ON p.id = d.profissionais_id 
                WHERE d.dia = %s AND d.hora = %s AND p.nome = %s
            """
            cursor.execute(query_disponibilidade, (data, horario, nome_profissional))
            disponibilidade = cursor.fetchone()

            if not disponibilidade:
                flash('Horário não disponível para agendamento', 'error')
                return redirect(url_for('consultar_agendamentos'))

            # Atualiza o agendamento
            query_agendamento = """
                UPDATE agendamento SET nomeCliente=%s, nomeProfissional=%s, sessao=%s, data=%s, horario=%s WHERE id=%s
            """
            cursor.execute(query_agendamento, (nome_cliente, nome_profissional, sessao, data, horario, id))
            
            # Realiza o commit da transação
            cnx.commit()
            flash('Consulta atualizada com sucesso!', 'success')

        except mysql.connector.Error as err:
            flash(f'Ocorreu um erro: {err}', 'error')
            cnx.rollback()  # Reverte qualquer mudança se ocorrer um erro
            
        finally:
            cursor.close()
            cnx.close()
        
        return redirect(url_for('consultar_agendamentos'))

    try:
        cursor.execute("SELECT * FROM agendamento WHERE id = %s", (id,))
        agendamento = cursor.fetchone()

    finally:
        cursor.close()
        cnx.close()
    
    return render_template('atualizar-agendamentos.html', agendamento=agendamento)

# Endpoint de cancelamento do agendamento/consulta
@app.route('/agendamento/<int:id>', methods=['POST', 'GET'])
def cancelar_agendamento(id):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    try: 
        query_verificar_agendamento = """
            SELECT * FROM agendamento WHERE id = %s
        """

        cursor.execute(query_verificar_agendamento, (id,))
        agendamento_existe = cursor.fetchone()

        if agendamento_existe: 
            query_agendamento = """
            DELETE FROM agendamento WHERE id=%s
            """
            cursor.execute(query_agendamento, (id,))
            cnx.commit()
            flash('Consulta cancelada com sucesso!', 'success')
        else:
            flash('Agendamento não encontrado', 'error')

    except mysql.connector.Error as err:
        flash(f'Ocorreu um erro: {err}', 'error')
        cnx.rollback()

    finally:
        cursor.close()
        cnx.close()
        
    return render_template('cadastro-agendamento.html')

# Endpoint de reagendamento de consulta
@app.route('/reagendamento/<int:id>', methods=['POST', 'GET'])
def reagendar_consulta(id):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    if request.method == 'POST':
        nome_profissional = request.form['nomep']
        horario = request.form['horario']
        data = request.form['data']

        try:
            query_verificar_agendamento = """
                    SELECT * FROM agendamento
                    WHERE nomeProfissional = %s AND data = %s AND horario = %s AND id != %s
            """
            cursor.execute(query_verificar_agendamento, (nome_profissional, data, horario, id))
            agendamento_existe = cursor.fetchone()

            if agendamento_existe:
                flash('Este profissional já possui um agendamento nesta data e horário', 'error')
                return redirect(url_for('consultar_agendamentos'))

            # Verifica na tabela de disponibilidade no MySQL se possuem a data com o profissional disponível
            query_disponibilidade = """ 
                SELECT d.id_disponibilidade
                FROM disponibilidade d
                INNER JOIN profissionais p ON p.id = d.profissionais_id 
                WHERE d.dia = %s AND d.hora = %s AND p.nome = %s
            """
            cursor.execute(query_disponibilidade, (data, horario, nome_profissional))
            disponibilidade = cursor.fetchone()

            if not disponibilidade:
                flash('Horário não disponível para agendamento', 'error')
                return redirect(url_for('consultar_agendamentos'))

            # Atualiza o agendamento
            query_agendamento = """
                UPDATE agendamento SET data=%s, horario=%s WHERE id=%s
            """
            cursor.execute(query_agendamento, (data, horario, id))
            
            # Realiza o commit da transação
            cnx.commit()
            flash('Consulta reagendada com sucesso!', 'success')

        except mysql.connector.Error as err:
            flash(f'Ocorreu um erro: {err}', 'error')
            cnx.rollback()  # Reverte qualquer mudança se ocorrer um erro
            
        finally:
            cursor.close()
            cnx.close()
        
        return redirect(url_for('consultar_agendamentos'))

    try:
        cursor.execute("SELECT * FROM agendamento WHERE id = %s", (id,))
        agendamento = cursor.fetchone()
    
    finally:
            cursor.close()
            cnx.close()
    
    return render_template('cadastro-reagendamento.html', id=id)