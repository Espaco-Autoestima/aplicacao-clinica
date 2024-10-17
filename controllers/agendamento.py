from app import app
from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector

app = Flask(__name__)

app.secret_key = 'secret-key-ea'

# Configuração e conexão do banco de dados 
config = {
    'user': 'root', 
    'password': 'E$p@c02024!', 
    'host': 'localhost', 
    'database': 'espacoautoestima',
    'raise_on_warnings': True
}

@app.route('/realizarAgendamento', methods=['POST', 'GET'])
def realizar_agendamento():
    if request.method == 'POST':
        nome_cliente = request.form['nomec']
        nome_profissional = request.form['nomep']
        sessao = request.form['sessao']
        horario = request.form['horario']
        data = request.form['data']

        try:
            cnx = mysql.connector.connect(**config)
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
                flash('Horário não disponível para agendamento.', 'error')
                return redirect(url_for('realizar_agendamento'))

            # Verifica se o cliente existe
            query_cliente = "SELECT id FROM clientes WHERE nome = %s"
            cursor.execute(query_cliente, (nome_cliente,))
            cliente = cursor.fetchone()
            if not cliente:
                flash('Cliente não encontrado.', 'error')
                return redirect(url_for('consultarCliente'))

            # Verifica se o profissional existe
            query_profissional = "SELECT id FROM profissionais WHERE nome = %s"
            cursor.execute(query_profissional, (nome_profissional,))
            profissional = cursor.fetchone()
            if not profissional:
                flash('Profissional não encontrado', 'error')
                return redirect(url_for('consultarProfissional'))

            # Insere o novo agendamento
            query_agendamento = """
                INSERT INTO agendamento(nomeCliente, nomeProfissional, sessao, data, horario, clientes_id, profissionais_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query_agendamento, (nome_cliente, nome_profissional, sessao, data, horario, cliente['id'], profissional['id']))

            # Realizar o commit da transação
            cnx.commit()
            flash('Agendamento realizado com sucesso!', 'success')
            return redirect(url_for('consultar_agendamento'))

        except mysql.connector.Error as err:
            flash(f'Não foi possível agendar o cliente no momento: {err}', 'error')
            return redirect(url_for('realizar_agendamento'))

        finally:
            if cursor:
                cursor.close()
            if cnx:
                cnx.close()

    return render_template('cadastro-agendamento.html')

@app.route('/agendamentos', methods=['POST', 'GET'])
def consultar_agendamento():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM agendamento")
    agendamentos = cursor.fetchall()
    print("Agendamentos recuperados:", agendamentos)  # Log para verificar os agendamentos recuperados
    return render_template('agendamentos.html', agendamentos=agendamentos)

# Implementação da regra de negócio de atualizar agendamentos
@app.route('/atualizarAgendamentos/<int:id>', methods=['POST', 'GET'])
def atualizar_agendamento(id):
    if request.method == 'POST':
        nome_cliente = request.form['nomec']
        nome_profissional = request.form['nomep']
        sessao = request.form['sessao']
        horario = request.form['horario']
        data = request.form['data']
        data_hora = data + ' ' + horario + ':00'

        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        # Verifica se o profissional já tem um agendamento na mesma data e hora
        query_verificar_agendamento = """
            SELECT * FROM agendamento
            WHERE nomeProfissional = %s AND data = %s AND horario = %s
        """
        cursor.execute(query_verificar_agendamento, (nome_profissional, data_hora, id))
        agendamento_existe = cursor.fetchone()

        if agendamento_existe:
            return 'Este profissional já tem um agendamento nesta data e horário.'

        # Verifica na tabela de disponibilidades no MySQL se possuem a data com o profissional disponível
        query_disponibilidade = """ 
            SELECT d.id_disponibilidade
            FROM disponibilidade d
            INNER JOIN profissionais p ON
            p.id = d.profissionais_id 
            WHERE d.dia = %s AND d.hora = %s AND p.nome = %s
        """
        cursor.execute(query_disponibilidade, (data, horario, nome_profissional))
        disponibilidade = cursor.fetchone()

        if disponibilidade:
            # Horário não disponível
            return 'Horário não disponível para agendamento.'
        else:
            # Horário está disponível, então inserir na tabela de agendamento
            query_agendamento = """
                "UPDATE agendamento SET nomeCliente=%s, nomeProfissional=%s, sessao=%s, data=%s, horario=%s WHERE id=%s"
            """
            cursor.execute(query_agendamento, (nome_cliente, nome_profissional, sessao, data, horario))
            cnx.commit()
            print("Agendamento atualizado:", (nome_cliente, nome_profissional, sessao, data, horario))
            return redirect('agendamentos')
    
    return render_template('atualizar-agendamentos.html')

