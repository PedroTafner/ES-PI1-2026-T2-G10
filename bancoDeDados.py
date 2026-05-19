import mysql.connector # Conexão com o banco
import validacoes as v
import opcoes as o

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
        
def validarEleitor(texto, funcao):
    print(f"\n\t-- {texto} --")

    titulo_eleitor=int(input("\nDigite seu título de eleitor: "))
    valTitulo=v.validacaoTituloEleitor(titulo_eleitor)
    while valTitulo != True:
        o.limpar()
        print(f"\n\t-- {texto} --\n\n*ERRO: Título de eleitor inválido, digite novamente.")
        titulo_eleitor=int(input("\nDigite seu título de eleitor: "))
        valTitulo=v.validacaoTituloEleitor(titulo_eleitor)

    o.limpar()
    print(f"\n\t-- {texto} --")
    cpf=int(input("\nDigite os 4 primeiros dígitos do seu CPF: "))
    while len(str(cpf))<4 or len(str(cpf))>4:
        o.limpar()
        print(f"\n\t-- {texto} --\n\n*ERRO: Digite os 4 primeiros caracteres do seu CPF, tente novamente.")
        cpf=int(input("\nDigite os 4 primeiros dígitos do seu CPF: "))
    
    o.limpar()
    print(f"\n\t-- {texto} --")
    chave=input("\nDigite a sua chave de acesso: ")
    while len(str(chave))<7 or len(str(chave))>7:
        o.limpar()
        print(f"\n\t-- {texto} --\n\n*ERRO: A chave de acesso precisa ter 7 valores, tente novamente.")
        chave=input("\nDigite a sua chave de acesso: ")

    cursor.execute(f"SELECT titulo_eleitor,cpf,chave_acesso,mesario,status_voto FROM eleitores WHERE cpf LIKE '{cpf}%'")
    resultadoTC=cursor.fetchall()

    for titulo_eleitor,cpf,chaveValida,mesario,status_voto in resultadoTC:
        if funcao == 0:
            if chave == chaveValida:
                if mesario == 0:
                    input("\n*ERRO: Somente mesários podem abrir o sistema de votação.\n\nAperte ENTER para continuar...")
                    return
                    
                else:
                    if str(titulo_eleitor) and str(chave) in resultadoTC[0]:
                        return True
                    else:
                        input("\n*ERRO: Dados inválida, tente novamente\n\nAperte ENTER para continuar...")
                        return
            else:
                input("\n*ERRO: Chave de acesso inválida, tente novamente\n\nAperte ENTER para continuar...")
                return
            
        if funcao == 1:
            if status_voto == 1:
                input("\n*ERRO: Você já realizou seu foto.\n\nAperte ENTER para voltar...")
                o.arquivoTXT(0,0,'ALERTA: Tentativa de voto duplo')
                return
            
            else:
                o.limpar()
                print(f"-- {texto} --")
                listar_candidatos()

                voto = int(input("\nDigite para quem você vota: "))
                cursor.execute(f"SELECT id_canditado FROM candidatos WHERE num_votacao = {voto}")
                validacaoCandidato = cursor.fetchall() 

                while validacaoCandidato == None:
                    o.limpar()
                    print(f"\n\t-- {texto} --")
                    listar_candidatos()
                    voto = int(input("\nDigite para quem você vota: "))

                o.limpar()
                o.arquivoTXT(0,0,'SUCESSO: Voto realizado com sucesso.')
                cursor.execute(f"UPDATE eleitores SET status_voto = 1 WHERE cpf = {cpf}; UPDATE candidatos SET votos = votos + 1 WHERE num_votacao = {voto}") 
                conexao.commit()  
                print(f"\n\t-- {texto} --")
                input("\n*ATUALIZAÇÃO: Voto confirmado com sucesso.\n\nAperte ENTER para continuar...")
                return   

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

def listar_candidatos():
    cursor.execute("SELECT nome, num_votacao, partido FROM candidatos")
    for (nome, num_votacao, partido) in cursor.fetchall():
        return print(f"{num_votacao} - {partido} - {nome}")