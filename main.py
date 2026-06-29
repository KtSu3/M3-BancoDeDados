import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

db = mysql.connector.connect(
    host=os.getenv("EXAMPLE_DB_HOST"),
    user=os.getenv("EXAMPLE_DB_USER"),
    password=os.getenv("EXAMPLE_DB_PASS"),
    database=os.getenv("EXAMPLE_DB_NAME")
)
cursor = db.cursor()

# --- CRUD USUÁRIO ---
def criar_usuario(nome, email, senha):
    # Insere um novo usuário
    cursor.execute("INSERT INTO Usuario (nome, email, senha) VALUES (%s, %s, %s)", (nome, email, senha))
    db.commit()

def ler_usuarios():
    # Busca e exibe todos os usuários
    cursor.execute("SELECT * FROM Usuario")
    for row in cursor.fetchall():
        print(row)

def atualizar_usuario(id_usuario, novo_nome):
    # Atualiza o nome de um usuário específico
    cursor.execute("UPDATE Usuario SET nome = %s WHERE id_usuario = %s", (novo_nome, id_usuario))
    db.commit()

def deletar_usuario(id_usuario):
    # Remove um usuário pelo ID
    cursor.execute("DELETE FROM Usuario WHERE id_usuario = %s", (id_usuario,))
    db.commit()

# --- CRUD PASTA ---
def criar_pasta(nome, id_usuario):
    # Cria nova pasta atrelada a um usuário
    cursor.execute("INSERT INTO Pasta (nome, id_usuario) VALUES (%s, %s)", (nome, id_usuario))
    db.commit()

def ler_pastas():
    # Retorna todas as pastas
    cursor.execute("SELECT * FROM Pasta")
    for row in cursor.fetchall():
        print(row)

def atualizar_pasta(id_pasta, novo_nome):
    # Renomeia uma pasta
    cursor.execute("UPDATE Pasta SET nome = %s WHERE id_pasta = %s", (novo_nome, id_pasta))
    db.commit()

def deletar_pasta(id_pasta):
    # Remove uma pasta
    cursor.execute("DELETE FROM Pasta WHERE id_pasta = %s", (id_pasta,))
    db.commit()

# --- CRUD MENSAGEM ---
def criar_mensagem(assunto, corpo, id_remetente, id_pasta):
    # Insere mensagem em uma pasta
    cursor.execute("INSERT INTO Mensagem (assunto, corpo, id_remetente, id_pasta) VALUES (%s, %s, %s, %s)", 
                   (assunto, corpo, id_remetente, id_pasta))
    db.commit()

def ler_mensagens():
    # Busca todas as mensagens
    cursor.execute("SELECT * FROM Mensagem")
    for row in cursor.fetchall():
        print(row)

def atualizar_mensagem(id_mensagem, novo_assunto):
    # Altera o assunto da mensagem
    cursor.execute("UPDATE Mensagem SET assunto = %s WHERE id_mensagem = %s", (novo_assunto, id_mensagem))
    db.commit()

def deletar_mensagem(id_mensagem):
    # Exclui uma mensagem
    cursor.execute("DELETE FROM Mensagem WHERE id_mensagem = %s", (id_mensagem,))
    db.commit()

# --- TESTES DE EXECUÇÃO ---
if __name__ == "__main__":
    print("=== Lendo Usuários Iniciais ===")
    ler_usuarios()
    
    print("\n=== Testando Inserção ===")
    criar_usuario("Novo User", "novo@teste.com", "senha123")
    ler_usuarios()
    
    # Fechando conexão
    cursor.close()
    db.close()