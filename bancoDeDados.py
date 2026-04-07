import mysql.connector
# Conexão com o banco
conexao = mysql.connector.connect(
host='localhost',
user='root',
password='Zxxyf1',
database='pi1_2026'
)
cursor = conexao.cursor()

def inserir_eleitores(nome, titulo_eleitor,cpf, mesario):
    sql = "INSERT INTO eleitores (nome, titulo_eleitor,cpf, mesario) VALUES (%s, %s)"
    valores = (nome, titulo_eleitor,cpf, mesario)
    cursor.execute(sql, valores)
    conexao.commit()

def listar_usuarios():
        cursor.execute("SELECT id, nome, titulo_eleitor,cpf, mesario FROM eleitores")
    for (id, nome, titulo_eleitor, cpf, mesario) in cursor.fetchall():
        print(f"ID: {id}, Nome: {nome}, Titulo Eleitor: {titulo_eleitor}, cpf {cpf}, mesario {mesario}")