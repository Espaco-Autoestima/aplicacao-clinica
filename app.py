from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
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

@app.route('/')
def index():
    return render_template('cadastro-agendamento.html')

# Rotas de login de usuários
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'email' in request.form and 'senha' in request.form:
        email = request.form['email']
        senha = request.form['senha']
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        # Selecionando os dados no banco
        query = "SELECT * FROM contas WHERE email = %s AND senha = %s"
        cursor.execute(query, (email, senha))
        conta = cursor.fetchone()
        # Verifica se existe a conta. Se existir, redireciona para a home
        if conta:
            session['loggedin'] = True
            session['id'] = conta[0]
            session['email'] = conta[1]
            return redirect(url_for('home'))
        else:
            # Caso a conta não exista ou se algum dado estiver incorreto
            flash("E-mail ou senha incorretos", "danger")

    return render_template('login.html')

# Rota de cadastro de usuários
@app.route('/signup', methods=['POST', 'GET'])
def signUp():
    if request.method == 'POST' and 'nome' in request.form and 'telefone' in request.form and 'email' in request.form and 'senha' in request.form:
        nome = request.form['nome']
        telefone = request.form['telefone']
        email = request.form['email']
        senha = request.form['senha']

        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        # Selecionando os dados no banco
        query = "SELECT * FROM contas WHERE email = %s and senha = %s"
        cursor.execute(query, (email, senha))
        conta = cursor.fetchone()
        # Verifica se existe a conta. Se existir, redireciona para a home
        if conta:
            session['loggedin'] = True
            session['id'] = conta[0]
            flash("E-mail já existe", "danger")
        else:
            # Inserindo os dados no banco
            query = "INSERT INTO contas (nome_usuario, telefone, email, senha) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (nome, telefone, email, senha))
            cnx.commit()
            cursor.close()
            cnx.close()
            flash("Conta criada com sucesso!", "success")
            return redirect(url_for('login'))
    
    return render_template('cadastro.html')

# Página inicial apenas para usuários logados
@app.route('/home')
def home():
    if 'loggedin' in session:
        return render_template('home.html', email=session['email'])
    return redirect(url_for('login'))

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

# Busca de clientes por e-mail
@app.route('/pesquisarCliente', methods=['POST'])
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

@app.route('/atualizarCliente/<int:id>', methods=['POST', 'GET'])
def atualizarCliente(id):
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

    return render_template('atualizar-clientes.html', cliente = cliente)

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

# Busca de profissionais por telefone
@app.route('/pesquisarProfissional', methods=['POST'])
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

@app.route('/atualizarProfissional/<int:id>', methods=['POST', 'GET'])
def atualizarProfissional(id):
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

    return render_template('atualizar-profissionais.html', profissional = profissional)

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

# Busca de fornecedores por telefone 
@app.route('/pesquisarFornecedor', methods=['POST'])
def pesquisar_fornecedores():
    try:
        telefone = request.form.get("pesquisa")
        
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor(dictionary=True)
            
        # Usando placeholders para evitar SQL Injection
        query = "SELECT * FROM fornecedores WHERE telefone=%s"
        cursor.execute(query, (telefone,))
            
        resultados = cursor.fetchall()

        return render_template('fornecedores.html', resultados = resultados)
        
    except mysql.connector.Error as err:
        return f"Tente novamente mais tarde: {err}", 500
        
    finally:
        cursor.close()
        cnx.close()

@app.route('/atualizarFornecedor/<int:id>', methods=['POST', 'GET'])
def atualizarFornecedor(id):
    if request.method == 'POST':
        nome = request.form['nome']
        telefone = request.form['telefone']
        empresa = request.form['empresa']

        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        query = "UPDATE fornecedores SET nome=%s, telefone=%s, empresa=%s WHERE id=%s"
        cursor.execute(query, (nome, telefone, empresa, id))
        cnx.commit()
        cursor.close()
        cnx.close()
        return redirect(url_for('consultarFornecedor'))

    # Carrega os dados do fornecedor para o formulário
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM fornecedores WHERE id = %s", (id,))
    fornecedor = cursor.fetchone()
    cursor.close()
    cnx.close()

    return render_template('atualizar-fornecedores.html', fornecedor = fornecedor)

# Regras de negócio de produtos
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

# Regras de negócio de agendamento
@app.route('/realizarAgendamento', methods=['POST', 'GET'])
def realizar_agendamento():
    if request.method == 'POST' and 'nomec' in request.form and 'nomep' in request.form and 'sessao' in request.form and 'horario' in request.form and 'data' in request.form: 
        nome_cliente = request.form['nomec']
        nome_profissional = request.form['nomep']
        sessao = request.form['sessao']
        horario = request.form['horario']
        data = request.form['data']

        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        # Verifica se o profissional já tem um agendamento na mesma data e hora
        query_verificar_agendamento = """
            SELECT * FROM agendamento
            WHERE nomeProfissional = %s AND data = %s AND horario = %s
        """
        cursor.execute(query_verificar_agendamento, (nome_profissional, data, horario))
        agendamento_existe = cursor.fetchone()

        if agendamento_existe:
            return 'Este profissional já tem um agendamento nesta data e horário.'

        # Verifica na tabela de disponibilidades no MySQL se possuem a data com o profissional disponível
        query_disponibilidade = """ 
            SELECT d.id_disponibilidade
            FROM disponibilidade d
            WHERE d.dia = %s AND d.hora = %s AND d.profissionais_id = (SELECT id FROM profissionais WHERE nome = %s)
        """
        cursor.execute(query_disponibilidade, (data, horario, nome_profissional))
        disponibilidade = cursor.fetchone()

        if disponibilidade:
            # Horário não disponível
            return 'Horário não disponível para agendamento.'
        else:
            # Horário está disponível, então inserir na tabela de agendamento
            query_cliente = "SELECT id FROM clientes WHERE nome = %s"
            cursor.execute(query_cliente, (nome_cliente,))
            cliente = cursor.fetchone()
            if not cliente:
                return 'Cliente não encontrado.'

            query_profissional = "SELECT id FROM profissionais WHERE nome = %s"
            cursor.execute(query_profissional, (nome_profissional,))
            profissional = cursor.fetchone()
            if not profissional:
                return 'Profissional não encontrado.'

            query_agendamento = """
                INSERT INTO agendamento(nomeCliente, nomeProfissional, sessao, data, horario, clientes_id, profissionais_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query_agendamento, (nome_cliente, nome_profissional, sessao, data, horario, cliente[0], profissional[0]))
            cnx.commit()
            print("Agendamento inserido:", (nome_cliente, nome_profissional, sessao, data, horario))
            return redirect('agendamentos')

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

if __name__ == "__main__":
    app.run(debug=True)