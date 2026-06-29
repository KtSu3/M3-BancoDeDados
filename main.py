import os
import mysql.connector
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# Conexao DB fallback
try:
    db = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME")
    )
    cursor = db.cursor()
except mysql.connector.Error as err:
    print(f"Erro de conexao: {err}")
    exit(1)

# --- MODULO: USUARIOS ---
def criar_usuario(nome, email, senha):
    # INSERT: Adiciona novo usuario
    try:
        cursor.execute("INSERT INTO Usuario (nome, email, senha) VALUES (%s, %s, %s)", (nome, email, senha))
        db.commit()
        print("Usuario criado com sucesso.")
    except Exception as e:
        print(f"Erro: {e}")

def ler_usuarios():
    # SELECT: Lista todos os usuarios
    cursor.execute("SELECT id_usuario, nome, email FROM Usuario")
    registros = cursor.fetchall()
    if not registros:
        print("Nenhum usuario encontrado.")
    for r in registros:
        print(f"ID: {r[0]} | Nome: {r[1]} | E-mail: {r[2]}")

def atualizar_usuario(id_usuario, novo_nome):
    # UPDATE: Altera o nome do usuario
    cursor.execute("UPDATE Usuario SET nome = %s WHERE id_usuario = %s", (novo_nome, id_usuario))
    db.commit()
    print("Usuario atualizado.")

def deletar_usuario(id_usuario):
    # DELETE: Remove o usuario (cascata para pastas e mensagens dependentes)
    try:
        cursor.execute("DELETE FROM Usuario WHERE id_usuario = %s", (id_usuario,))
        db.commit()
        print("Usuario deletado.")
    except Exception as e:
        print(f"Erro ao deletar: {e}")

# --- MODULO: PASTAS ---
def criar_pasta(nome, id_usuario):
    # INSERT: Adiciona pasta para um usuario
    try:
        cursor.execute("INSERT INTO Pasta (nome, id_usuario) VALUES (%s, %s)", (nome, id_usuario))
        db.commit()
        print("Pasta criada.")
    except Exception as e:
        print(f"Erro: {e}")

def ler_pastas():
    # SELECT: Lista pastas vinculadas aos seus donos
    sql = "SELECT p.id_pasta, p.nome, u.nome FROM Pasta p JOIN Usuario u ON p.id_usuario = u.id_usuario"
    cursor.execute(sql)
    for r in cursor.fetchall():
        print(f"ID Pasta: {r[0]} | Nome: {r[1]} | Dono: {r[2]}")

def deletar_pasta(id_pasta):
    # DELETE: Remove uma pasta
    cursor.execute("DELETE FROM Pasta WHERE id_pasta = %s", (id_pasta,))
    db.commit()
    print("Pasta deletada.")

# --- MODULO: MENSAGENS E E-MAILS ---
def enviar_email(assunto, corpo, id_remetente, id_pasta, id_destinatario, tipo_envio):
    # INSERT: Insere mensagem e cria vinculo de destinatario na mesma transacao
    try:
        # Insere a mensagem
        sql_msg = "INSERT INTO Mensagem (assunto, corpo, data_envio, id_remetente, id_pasta) VALUES (%s, %s, %s, %s, %s)"
        val_msg = (assunto, corpo, datetime.now(), id_remetente, id_pasta)
        cursor.execute(sql_msg, val_msg)
        
        id_mensagem = cursor.lastrowid
        
        # Insere o destinatario
        sql_dest = "INSERT INTO Destinatario (id_mensagem, id_usuario, tipo) VALUES (%s, %s, %s)"
        val_dest = (id_mensagem, id_destinatario, tipo_envio)
        cursor.execute(sql_dest, val_dest)
        
        db.commit()
        print("E-mail enviado com sucesso.")
    except Exception as e:
        db.rollback()
        print(f"Erro ao enviar e-mail: {e}")

def ler_caixa_entrada(id_usuario):
    # SELECT: Busca mensagens onde o usuario e destinatario
    sql = """
    SELECT m.id_mensagem, u.nome, m.assunto, m.data_envio, d.tipo 
    FROM Mensagem m 
    JOIN Destinatario d ON m.id_mensagem = d.id_mensagem 
    JOIN Usuario u ON m.id_remetente = u.id_usuario 
    WHERE d.id_usuario = %s
    """
    cursor.execute(sql, (id_usuario,))
    registros = cursor.fetchall()
    
    if not registros:
        print("Caixa de entrada vazia.")
        return
        
    for r in registros:
        print(f"Msg ID: {r[0]} | De: {r[1]} | Assunto: {r[2]} | Tipo: {r[4]} | Data: {r[3]}")

def deletar_mensagem(id_mensagem):
    # DELETE: Remove mensagem (cascata deleta da tabela Destinatario)
    cursor.execute("DELETE FROM Mensagem WHERE id_mensagem = %s", (id_mensagem,))
    db.commit()
    print("Mensagem deletada.")

# --- MENU INTERATIVO ---
def exibir_menu():
    while True:
        print("\n--- SISTEMA DE E-MAIL (CRUD COMPLETO) ---")
        print("[ USUARIOS ]")
        print("1. Listar Usuarios")
        print("2. Criar Usuario")
        print("3. Atualizar Nome do Usuario")
        print("4. Deletar Usuario")
        print("\n[ PASTAS ]")
        print("5. Listar Pastas")
        print("6. Criar Pasta")
        print("7. Deletar Pasta")
        print("\n[ MENSAGENS ]")
        print("8. Simular Envio de E-mail")
        print("9. Ver Caixa de Entrada")
        print("10. Deletar Mensagem")
        print("\n0. Sair")
        
        op = input("\nEscolha uma opcao: ")
        
        if op == '1':
            ler_usuarios()
        elif op == '2':
            n = input("Nome: ")
            e = input("E-mail: ")
            s = input("Senha: ")
            criar_usuario(n, e, s)
        elif op == '3':
            i = input("ID do Usuario: ")
            n = input("Novo Nome: ")
            atualizar_usuario(i, n)
        elif op == '4':
            i = input("ID do Usuario a deletar: ")
            deletar_usuario(i)
        elif op == '5':
            ler_pastas()
        elif op == '6':
            n = input("Nome da pasta: ")
            i = input("ID do dono: ")
            criar_pasta(n, i)
        elif op == '7':
            i = input("ID da Pasta a deletar: ")
            deletar_pasta(i)
        elif op == '8':
            rem = input("ID do Remetente: ")
            dest = input("ID do Destinatario: ")
            pst = input("ID da Pasta (ex: ID de 'Caixa de Entrada' ou 'Enviados'): ")
            ass = input("Assunto: ")
            msg = input("Corpo da mensagem: ")
            tipo = input("Tipo (PARA, CC, CCO): ").upper()
            enviar_email(ass, msg, rem, pst, dest, tipo)
        elif op == '9':
            usr = input("ID do usuario (Caixa de Entrada): ")
            ler_caixa_entrada(usr)
        elif op == '10':
            msg_id = input("ID da Mensagem a deletar: ")
            deletar_mensagem(msg_id)
        elif op == '0':
            print("Encerrando.")
            break
        else:
            print("Opcao invalida.")

if __name__ == "__main__":
    exibir_menu()
    cursor.close()
    db.close()
