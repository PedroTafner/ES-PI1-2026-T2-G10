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

    cursor.execute("SELECT  nome, titulo_eleitor,cpf, mesario, chave_acesso FROM eleitores")
    for (nome, titulo_eleitor, cpf, mesario, chave_acesso) in cursor.fetchall():
            print(f"Nome: {nome}, CPF: {cpf}")

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
                return input("\n*ERRO: Somente mesários podem abrir o sistema de votação.\n\nAperte ENTER para continuar...")
                
            else:
                if str(titulo_eleitor) and str(chave) in resultadoTC[0]:
                    return True
                else:
                    return input("\n*ERRO: Dados inválida, tente novamente\n\nAperte ENTER para continuar...")
        else:
            return input("\n*ERRO: Chave de acesso inválida, tente novamente\n\nAperte ENTER para continuar...")
        

def removerEleitor(cpf):
    cursor.execute(f"DELETE FROM eleitores WHERE cpf= {cpf}")
    resultadoDEL = cursor.rowcount
    return resultadoDEL
    
def inserir_candidato(nome,num_vot,partido):
    sql = "INSERT INTO candidatos (nome,num_votacao,partido) VALUES (%s, %s, %s)"
    valores = (nome,num_vot,partido)
    cursor.execute(sql, valores)
    conexao.commit()

def buscar_eleitorCandidato(nome):
    cursor.execute(f"SELECT nome FROM eleitores WHERE nome LIKE '{nome}'")
    resultado = cursor.fetchall()
    for nome in resultado:
        if resultado == None:
            return False
        else:
            return True
    return False

def buscar_statusVoto(nome):
    cursor.execute(f"SELECT status_voto FROM eleitores WHERE nome LIKE '%{nome}%'")
    return cursor.fetchall()[0][0]


def zerezima():
    cursor.execute(f"UPDATE eleitores SET status_voto = 0")


def listar_candidatos_zerezima():

    cursor.execute("SELECT nome, num_votacao, partido FROM candidatos")
    for (nome, num_votacao, partido) in cursor.fetchall():
            print(f"Nome: {nome}, Numero de Votação: {num_votacao}, Partido: {partido} ")

    
