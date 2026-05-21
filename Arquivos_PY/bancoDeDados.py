import mysql.connector # Conexão com o banco
import Arquivos_PY.validacoes as val
import Arquivos_PY.gerenciamento as ger
import Arquivos_PY.votacao as vot
import datetime

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

def removerEleitor(cpf): #FUNÇÃO PARA EXECUTAR NO BANCO DE DADOS A REMOÇÃO DE CERTO ELEITOR
    cursor.execute(f"DELETE FROM eleitores WHERE cpf= {cpf}")
    conexao.commit()
    resultadoDEL = cursor.rowcount
    return resultadoDEL
    
def inserir_candidato(nome,num_vot,partido): #FUNÇÃO PARA EXECUTAR NO BANCO DE DADOS A ADICAÇÃO DE UM CERTO CANDIDATO
    sql = "INSERT INTO candidatos (nome,num_votacao,partido, votos) VALUES (%s, %s, %s, 0)"
    valores = (nome,num_vot,partido)
    cursor.execute(sql, valores)
    conexao.commit()

def buscar_eleitorCandidato(nome): #VERIFICA NO BANCO DE DADOS SE UM ELEITOR EXISTE
    cursor.execute(f"SELECT nome FROM eleitores WHERE nome LIKE '{nome}'")
    resultado = cursor.fetchall()
    for nome in resultado:
        if resultado == None:
            return False
        else:
            return True
    return False

def buscar_statusVoto(nome): #BUSCA NO BANCO DE DADOS SE UM ELEITOR JA VOTOU
    cursor.execute(f"SELECT status_voto FROM eleitores WHERE nome LIKE '%{nome}%'")
    return cursor.fetchall()[0][0]

def zeresima(): #ZERA VOTOS DE CANDIDATOS E O STATUS DE VOTO DO ELEITOR PARA REINICIAR A ELEIÇÃO
    cursor.execute(f"UPDATE eleitores SET status_voto = 0")
    conexao.commit()
    cursor.execute("SELECT nome, num_votacao, partido FROM candidatos")
    for (nome, num_votacao, partido) in cursor.fetchall():
        print(f"{num_votacao} - {nome} | {partido}: votos = 0")
    return

def listar_candidatos(): #LISTA TODOS OS CANDIDATOS DISPONÍVEIS NO BANCO DE DADOS
    cursor.execute("SELECT nome, num_votacao, partido FROM candidatos")
    for (nome, num_votacao, partido) in cursor.fetchall():
        print(f"{num_votacao} - {partido} - {nome}")
    return

def votoRealizado(voto,cpfValido,texto):
    ger.limpar()
    protocolo = vot.gerador_protocolo(voto)
    vot.arquivoTXT(0,'SUCESSO: Voto realizado com sucesso.')
    cursor.execute(f"UPDATE eleitores SET status_voto = status_voto + 1 WHERE cpf = {cpfValido}")
    conexao.commit()
    cursor.execute(f"SELECT id_candidato FROM candidatos WHERE num_votacao = {voto}")
    id_candidato = cursor.fetchone()[0]
    horario = datetime.datetime.now()
    cursor.execute("INSERT INTO resultado (protocolo_votacao, horario_votacao, id_candidato) VALUES (%s, %s, %s)",(protocolo, horario, id_candidato))
    conexao.commit()
    print(f"\n\t-- {texto} --")
    input(f"\n*ATUALIZAÇÃO: Voto confirmado com sucesso.\nSeu protocolo de votação é {protocolo}\n\nAperte ENTER para continuar...")
    ger.limpar()

def votoNulo(cpfValido,texto):
    ger.limpar()
    protocolo = vot.gerador_protocolo(2)
    vot.arquivoTXT(0,'SUCESSO: Voto realizado com sucesso.')
    cursor.execute(f"UPDATE eleitores SET status_voto = status_voto + 1 WHERE cpf = {cpfValido}")
    conexao.commit()
    horario = datetime.datetime.now()
    cursor.execute("INSERT INTO resultado (protocolo_votacao, horario_votacao, id_candidato) VALUES (%s, %s, %s)",(protocolo, horario, 2))
    conexao.commit()
    print(f"\n\t-- {texto} --")
    input(f"\n*ATUALIZAÇÃO: Voto confirmado com sucesso.\nSeu protocolo de votação é {protocolo}\n\nAperte ENTER para continuar...")
    ger.limpar()
