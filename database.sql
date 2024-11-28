CREATE SCHEMA IF NOT EXISTS espacoautoestima;
USE espacoautoestima;

CREATE TABLE IF NOT EXISTS contas(
    id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nome_usuario VARCHAR(50),
    telefone VARCHAR(25),
    email VARCHAR(40),
    senha VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS clientes(
    id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY, 
    nome VARCHAR(45), 
    telefone VARCHAR(25), 
    email VARCHAR(40), 
    cpf VARCHAR(25)
);

CREATE TABLE IF NOT EXISTS profissionais(
    id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY, 
    nome VARCHAR(45), 
    telefone VARCHAR(25), 
    especialidade VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS procedimentos(
    id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY, 
    nome VARCHAR(45), 
    descricao VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS agendamento(
    id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nomeCliente VARCHAR(30),
    nomeProfissional VARCHAR(30),
    sessao BIGINT, 
    data date,
    horario time,
    clientes_id BIGINT, 
    profissionais_id BIGINT, 
    FOREIGN KEY (clientes_id) REFERENCES clientes(id), 
    FOREIGN KEY (profissionais_id) REFERENCES profissionais(id)
);

CREATE TABLE IF NOT EXISTS disponibilidade(
    id_disponibilidade BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    dia date, 
    hora time,
    profissionais_id BIGINT, 
    FOREIGN KEY (profissionais_id) REFERENCES profissionais(id) 
);

CREATE TABLE IF NOT EXISTS produtos(
    id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY, 
    nome VARCHAR(45), 
    data_validade date, 
    quantidade INT, 
    marca VARCHAR(20), 
    preco decimal(10, 2), 
    descricao VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS fornecedores(
    id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY, 
    nome VARCHAR(45), 
    telefone VARCHAR(20), 
    empresa VARCHAR(20)
);