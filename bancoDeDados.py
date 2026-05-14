import mysql.connector # Conexão com o banco

conexao = mysql.connector.connect(
host='localhost',
user='root',
password='Zxxyf1',
database='pi1_2026'
)
cursor = conexao.cursor()

def inserir_eleitores(nome, titulo_eleitor,cpf, mesario, chave_acesso, status_voto=0): #FUNÇÃO QUE INSERE DADOS NO BANCO DE DADOS VIA CONEXÃO MYSQL
    sql = "INSERT INTO eleitores (nome, titulo_eleitor,cpf, mesario, chave_acesso, status_voto) VALUES (%s, %s, %s, %s, %s, %s)"
    valores = (nome, titulo_eleitor,cpf, mesario, chave_acesso, status_voto)
    cursor.execute(sql, valores)
    conexao.commit()

def listar_usuarios(): #FUNÇÃO QUE LISTA INFORMAÇÕES DOS ELEITORES
    cursor.execute("SELECT id, nome, titulo_eleitor,cpf, mesario, chave_acesso FROM eleitores")
    for (id, nome, titulo_eleitor, cpf, mesario, chave_acesso) in cursor.fetchall():
        print(f"ID: {id}, Nome: {nome}, Titulo Eleitor: {titulo_eleitor}, cpf {cpf}, mesario {mesario}, Chave de Acesso: {chave_acesso}")

def buscarEleitor(nome): #FUNÇÃO QUE BUSCA E MOSTRA OS ELEITORES FILTRADOS
    
    cursor.execute(f"SELECT nome, cpf, mesario FROM eleitores WHERE nome LIKE '%{nome}%'")

    resultado = cursor.fetchall()

    for (nome,  cpf, mesario) in resultado:
        if resultado == None:
            break
        if mesario == 1:
            print(f"Nome: {nome}, Cpf: {cpf}, Mesario: Sim")
        else:
            print(f"Nome: {nome}, Cpf: {cpf}, Mesario: Não")
        
def validarEleitor(titulo_eleitor,Chave,cpf):
    cursor.execute(f"SELECT titulo_eleitor,cpf,chave_acesso,mesario FROM eleitores WHERE cpf LIKE '{cpf}%'")
    resultadoTC=cursor.fetchall()

    for titulo_eleitor,cpf,chave,mesario in resultadoTC:
        if chave == Chave:
            if mesario == 0:
                print("\n\tErro! Mesários não podem abrir o sistema de votação.")
                return
            else:
                if str(titulo_eleitor) and str(chave) in resultadoTC[0]:
                    return True
                else:
                    return False
        else:
            print("\n\tErro! Chave de acesso errada, tente novamente.")
            return
    