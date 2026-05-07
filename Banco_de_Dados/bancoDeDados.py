import mysql.connector
# Conexão com o banco
conexao = mysql.connector.connect(
host='localhost',
user='root',
password='Zxxyf1',
database='pi1_2026'
)
cursor = conexao.cursor()

def inserir_eleitores(nome, titulo_eleitor,cpf, mesario, chave_acesso, status_voto=0):
    sql = "INSERT INTO eleitores (nome, titulo_eleitor,cpf, mesario, chave_acesso, status_voto) VALUES (%s, %s, %s, %s, %s, %s)"
    valores = (nome, titulo_eleitor,cpf, mesario, chave_acesso, status_voto)
    cursor.execute(sql, valores)
    conexao.commit()

def listar_usuarios():
    cursor.execute("SELECT id, nome, titulo_eleitor,cpf, mesario, chave_acesso FROM eleitores")
    for (id, nome, titulo_eleitor, cpf, mesario, chave_acesso) in cursor.fetchall():
        print(f"ID: {id}, Nome: {nome}, Titulo Eleitor: {titulo_eleitor}, cpf {cpf}, mesario {mesario}, Chave de Acesso: {chave_acesso}")