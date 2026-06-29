-- Criação do Banco
CREATE DATABASE IF NOT EXISTS email_db;
USE email_db;

-- Criação das Tabelas
CREATE TABLE Usuario (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL
);

CREATE TABLE Pasta (
    id_pasta INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    id_usuario INT NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario) ON DELETE CASCADE
);

CREATE TABLE Mensagem (
    id_mensagem INT AUTO_INCREMENT PRIMARY KEY,
    assunto VARCHAR(255),
    corpo TEXT,
    data_envio DATETIME DEFAULT CURRENT_TIMESTAMP,
    id_remetente INT NOT NULL,
    id_pasta INT NOT NULL,
    FOREIGN KEY (id_remetente) REFERENCES Usuario(id_usuario),
    FOREIGN KEY (id_pasta) REFERENCES Pasta(id_pasta) ON DELETE CASCADE
);

CREATE TABLE Destinatario (
    id_mensagem INT NOT NULL,
    id_usuario INT NOT NULL,
    tipo VARCHAR(10) NOT NULL, -- 'PARA', 'CC', 'CCO'
    PRIMARY KEY (id_mensagem, id_usuario),
    FOREIGN KEY (id_mensagem) REFERENCES Mensagem(id_mensagem) ON DELETE CASCADE,
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario) ON DELETE CASCADE
);

-- População de Dados (Inserts)
INSERT INTO Usuario (nome, email, senha) VALUES 
('Kauã', 'kaua@univali.br', '12345'),
('Professor', 'prof@univali.br', 'abcde');

INSERT INTO Pasta (nome, id_usuario) VALUES 
('Caixa de Entrada', 1),
('Enviados', 1),
('Caixa de Entrada', 2);

INSERT INTO Mensagem (assunto, corpo, id_remetente, id_pasta) VALUES 
('Dúvida Trabalho', 'Professor, segue anexo.', 1, 2),
('Resposta', 'Recebido, Kauã.', 2, 1);

INSERT INTO Destinatario (id_mensagem, id_usuario, tipo) VALUES 
(1, 2, 'PARA'),
(2, 1, 'PARA');