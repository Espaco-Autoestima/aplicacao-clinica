from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Configuração e conexão do banco de dados 
config = {
    'user': 'root', 
    'password': 'E$p@c02024!', 
    'host': 'localhost', 
    'database': 'espacoautoestima',
    'raise_on_warnings': True
}

@app.route('/')
def index():
    return render_template('cadastro-clientes.html')

# Rotas das operações básicas do banco (CRUD) de clientes, exceto DELETE
@app.route('/cadastrarCliente', methods=['POST', 'GET'])
def adicionarCliente():
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
def consultarCliente():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()
    return render_template('clientes.html', clientes = clientes)

@app.route('/atualizarCliente/<int:id>', methods=['POST', 'GET'])
def atualizarCliente(id):
    if request.method == 'POST':
        nome = request.form['nome']
        telefone = request.form['telefone']
        email = request.form['email']
        cpf = request.form['cpf']

        cnx = mysql.connection.cursor()
        cursor = cnx.cursor()
        query = "UPDATE clientes SET nome=%s, telefone=%s, email=%s, cpf=%s WHERE id=%s"
        cursor.execute(query, (id, nome, telefone, email, cpf))
        cnx.commit()
        cursor.close()
        cnx.close()
        return redirect('clientes')
    
    return render_template('atualizar-clientes.html')

# Rotas das operações básicas do banco (CRUD) de profissionais, exceto DELETE
@app.route('/cadastrarProfissional', methods=['POST', 'GET'])
def adicionarProfissional():
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

@app.route('/atualizarProfissional/<int:id>', methods=['POST', 'GET'])
def atualizarProfissional(id):
    if request.method == 'POST':
        nome = request.form['nome']
        telefone = request.form['telefone']
        especialidade = request.form['especialidade']

        cnx = mysql.connection.cursor()
        cursor = cnx.cursor()
        query = "UPDATE profissionais SET nome=%s, telefone=%s, especialidade=%s WHERE id=%s"
        cursor.execute(query, (id, nome, telefone, especialidade))
        cnx.commit()
        cursor.close()
        cnx.close()
        return redirect('profissionais')
    
    return render_template('atualizar-profissionais.html')

# Rotas das operações básicas do banco (CRUD) de fornecedores, exceto DELETE
@app.route('/cadastrarFornecedor', methods=['POST', 'GET'])
def adicionarFornecedor():
    if request.method == 'POST' and 'nome' in request.form and 'telefone' in request.form and 'empresa' in request.form:
        nome = request.form['nome']
        telefone = request.form['telefone']
        empresa = request.form['empresa']

        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        # Inserindo os dados no banco
        query = "INSERT INTO fornecedores (nome, telefone, empresa) VALUES (%s, %s, %s)"
        cursor.execute(query, (nome, telefone, empresa))
        cnx.commit()
        cursor.close()
        cnx.close()
        return redirect('fornecedores')
    
    return render_template('cadastro-fornecedores.html')

@app.route('/fornecedores', methods=['POST', 'GET'])
def consultarFornecedor():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM fornecedores")
    fornecedores = cursor.fetchall()
    return render_template('fornecedores.html', fornecedores = fornecedores)

@app.route('/atualizarFornecedor/<int:id>', methods=['POST', 'GET'])
def atualizarFornecedor(id):
    if request.method == 'POST':
        nome = request.form['nome']
        telefone = request.form['telefone']
        empresa = request.form['empresa']

        cnx = mysql.connection.cursor()
        cursor = cnx.cursor()
        query = "UPDATE fornecedores SET nome=%s, telefone=%s, empresa=%s WHERE id=%s"
        cursor.execute(query, (id, nome, telefone, empresa))
        cnx.commit()
        cursor.close()
        cnx.close()
        return redirect('fornecedores')

    return render_template('atualizar-fornecedores.html')

# Regras de negócio de produtos
@app.route('/cadastrarProduto', methods=['POST', 'GET'])
def adicionarProduto():
    if request.method == 'POST' and 'nome' in request.form and 'data-validade' in request.form and 'quantidade' in request.form and 'marca' in request.form and 'preco' in request.form and 'descricao' in request.form:
        produto = request.form['nome']
        dataValidade = request.form['data-validade']
        quantidade = request.form['quantidade']
        marca = request.form['marca']
        preco = request.form['preco']
        descricao = request.form['descricao']

        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        # Inserindo dados no banco 
        query = "INSERT INTO Produtos (nome, data_validade, quantidade, marca, preco, descricao) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (produto, dataValidade, quantidade, marca, preco, descricao))
        cnx.commit()
        cursor.close()
        cnx.close()
        return redirect('produtos')
    
    return render_template('cadastro-produtos.html')

@app.route('/produtos', methods=['POST', 'GET'])
def consultarProduto():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM Produtos")
    produtos = cursor.fetchall()
    return render_template('produtos.html', produtos = produtos)

@app.route('/atualizarProduto', methods=['POST', 'GET'])
def atualizarProduto(id):
    if request.method == 'POST':
        produto = request.form['nome']
        dataValidade = request.form['data-validade']
        quantidade = request.form['quantidade']
        marca = request.form['marca']
        preco = request.form['preco']
        descricao = request.form['descricao']

        cnx = mysql.connection.cursor()
        cursor = cnx.cursor()
        query = "UPDATE produtos SET nome=%s, data_validade=%s, quantidade=%s, marca=%s, preco=%s, descricao=%s WHERE id=%s"
        cursor.execute(query, (id, produto, dataValidade, quantidade, marca, preco, descricao))
        cnx.commit()
        cursor.close()
        cnx.close()
        return redirect('produtos')
    
    return render_template('atualizar-produtos.html')

# Regras de negócio de agendamento
@app.route('/realizarAgendamento', methods=['POST', 'GET'])
def agendar_consulta():
    if request.method == 'POST' and 'nomec' in request.form and 'nomep' in request.form and 'sessao' in request.form and 'horario' in request.form and 'data' in request.form: 
        nome_cliente = request.form['nomec']
        nome_profissional = request.form['nomep']
        sessao = request.form['sessao']
        horario = request.form['horario']
        data = request.form['data']
        data_hora = data + ' ' + horario + ':00'

        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        # Verificar se o profissional já tem um agendamento na mesma data e hora
        query_verificar_agendamento = """
            SELECT * FROM Agendamento
            WHERE nomeProfissional = %s AND dataHora = %s
        """
        cursor.execute(query_verificar_agendamento, (nome_profissional, data_hora))
        agendamento_existe = cursor.fetchone()

        if agendamento_existe:
            return 'Este profissional já tem um agendamento nesta data e horário.'

        # Verificar na tabela de disponibilidades no MySQL se possuem a data com o profissional disponível
        query_disponibilidade = """ 
            SELECT d.Id_disponibilidade
            FROM Disponibilidade d
            INNER JOIN profissionais p ON
            p.profissionais_id = d.profissionais_id 
            WHERE d.Dia = %s AND d.Hora = %s AND p.nome = %s
        """
        cursor.execute(query_disponibilidade, (data, horario, nome_profissional))
        disponibilidade = cursor.fetchone()

        if disponibilidade:
            # Horário não disponível
            return 'Horário não disponível para agendamento.'
        else:
            # Horário está disponível, então inserir na tabela de agendamento
            query_agendamento = """
                INSERT INTO Agendamento (nomeCliente, nomeProfissional, sessao, dataHora, clientes_id, profissionais_id)
                VALUES (%s, %s, %s, %s, (SELECT clientes_id FROM clientes WHERE nome = %s), (SELECT profissionais_id FROM profissionais WHERE nome = %s))
            """
            cursor.execute(query_agendamento, (nome_cliente, nome_profissional, sessao, data_hora, nome_cliente, nome_profissional))
            cnx.commit()
            print("Agendamento inserido:", (nome_cliente, nome_profissional, sessao, data_hora, nome_cliente, nome_profissional))
            return redirect('agendamentos')

    return render_template('cadastro-agendamento.html')

@app.route('/agendamentos', methods=['GET'])
def consultar_agendamento():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM Agendamento")
    agendamentos = cursor.fetchall()
    print("Agendamentos recuperados:", agendamentos)  # Log para verificar os agendamentos recuperados
    return render_template('agendamentos.html', agendamentos=agendamentos)

# Implementação da regra de negócio de atualizar agendamentos

# Regras de negócio de consultas

if __name__ == "__main__":
    app.run(debug=True)