import Arquivos_PY.validacoes as val
import Arquivos_PY.gerenciamento as ger
import Arquivos_PY.votacao as vot
import Arquivos_PY.criptografia as c
import Arquivos_PY.descriptografia as d
import mysql.connector # Conexão com o banco
import datetime # Biblioteca para pegar o tempo e data certa da ocorrência de tal fato

conexao = mysql.connector.connect(
host='localhost',
user='root',
password='Zxxyf1',
database='pi1_2026'
)
cursor = conexao.cursor()


def inserir_eleitores(nome, titulo_eleitor,cpf, mesario, chave_acesso, status_voto=0):
    
    """
    Insere os dados de um novo eleitor no banco de dados após passarem pelas validações.

    Args:
        nome (str): Nome do eleitor.
        titulo_eleitor (int): Número validado do título de eleitor.
        cpf (str): CPF criptografado do eleitor.
        mesario (int): 1 se atuará como mesário, 0 caso contrário.
        chave_acesso (str): Chave de acesso única e criptografada.

    Returns:
        Nenhum valor é retornado (None).
    """

    sql = "INSERT INTO eleitores (nome, titulo_eleitor,cpf, mesario, chave_acesso, status_voto) VALUES (%s, %s, %s, %s, %s, %s)"
    valores = (nome, titulo_eleitor,cpf, mesario, chave_acesso, status_voto)
    cursor.execute(sql, valores)
    conexao.commit()

def listar_usuarios(): 
    
    """
    Exibe todos os eleitores cadastrados ordenados alfabeticamente.
    Descriptografa o CPF para exibição na tela .

    Args:
        Não recebe parâmetros de entrada.

    Returns:
        Nenhum valor é retornado (None).
    """

    cursor.execute("SELECT nome, cpf FROM eleitores ORDER BY nome")
        
    for (nome, cpf) in cursor.fetchall():
        cpf = d.descriptografia(0,cpf)
        print(f"Nome: {nome}\tCPF: {cpf}")

def buscarEleitor(nome): 
    
    """
    Realiza uma busca e exibe os eleitores cujo nome contenha o termo pesquisado.

    Args:
        nome (str): O trecho do nome ou nome completo a ser buscado.

    Returns:
        Nenhum valor é retornado (None).
    """

    cursor.execute(f"SELECT nome, cpf, mesario FROM eleitores WHERE nome LIKE '%{nome}%' ORDER BY nome")
    resultado = cursor.fetchall()

    for (nome,  cpf, mesario) in resultado:
        cpf = d.descriptografia(0,cpf)
        if resultado == None:
            break

        if mesario == 1:
            print(f"Nome: {nome}\tCPF: {cpf}\tMesário: Sim")

        else:
            print(f"Nome: {nome}\tCPF: {cpf}\tMesário: Não")                          

def removerEleitor(chave): 
    
    """
    Remove um eleitor do banco de dados através de sua chave de acesso.

    Args:
        chave (str): A chave de acesso criptografada correspondente ao eleitor.

    Returns:
        int: O número de linhas afetadas pela deleção (0 se não encontrou, 1 se removeu).
    """

    cursor.execute(f"DELETE FROM eleitores WHERE chave_acesso = '{chave}'")
    conexao.commit()
    resultadoDEL = cursor.rowcount
    return resultadoDEL
    
def inserir_candidato(nome,num_vot,partido): 
    
    """
    Registra um novo candidato na tabela de candidatos do banco de dados.

    Args:
        nome (str): O nome de urna do candidato.
        num_vot (int): O número eleitoral único do candidato.
        partido (str): O nome do partido.

    Returns:
        Nenhum valor é retornado (None).
    """

    sql = "INSERT INTO candidatos (nome,num_votacao,partido) VALUES (%s, %s, %s)"
    valores = (nome,num_vot,partido)
    cursor.execute(sql, valores)
    conexao.commit()

def buscar_eleitorCandidato(nome): 
    
    """
    Verifica se existe um eleitor com o nome informado.

    Args:
        nome (str): O nome a ser verificado no banco.

    Returns:
        bool: Retorna True se o eleitor existir, False caso contrário.
    """

    cursor.execute(f"SELECT nome FROM eleitores WHERE nome LIKE '{nome}' ORDER BY nome")
    resultado = cursor.fetchall()
    for nome in resultado:
        if resultado == None:
            return False
        else:
            return True
    return False

def buscar_statusVoto(nome):
    
    """
    Consulta o status_voto de um eleitor.

    Args:
        nome (str): O nome do eleitor.

    Returns:
        int: Retorna o status atual (0 para não votou, 1 para já votou).
    """

    cursor.execute(f"SELECT status_voto FROM eleitores WHERE nome LIKE '%{nome}%'")
    return cursor.fetchall()[0][0]

def zeresima(): 
    
    """
    Zera os votos de todos os candidatos e o status de voto dos eleitores para iniciar a eleição, 
    imprimindo a zerésima provando que não há votos computados.

    Args:
        Não recebe parâmetros de entrada.

    Returns:
        Nenhum valor é retornado (None).
    """

    cursor.execute(f"UPDATE eleitores SET status_voto = 0")
    conexao.commit()
    cursor.execute("SELECT nome, num_votacao, partido FROM candidatos")
    for (nome, num_votacao, partido) in cursor.fetchall():
        if nome != "Voto Nulo":
            print(f"{num_votacao} | {nome} - ({partido}) | Total de Votos: 0")
    return

def listar_candidatos(): 
    
    """
    Exibe uma listagem de todos os candidatos e seus partidos e números.

    Args:
        Não recebe parâmetros de entrada.

    Returns:
        Nenhum valor é retornado (None).
    """

    cursor.execute("SELECT nome, num_votacao, partido FROM candidatos ORDER BY nome")
    for (nome, num_votacao, partido) in cursor.fetchall():
        print(f"{num_votacao}\t{nome}\t{partido}")

def votoRealizado(voto,cpfValido,texto):

    """
    Registra um voto na urna. Altera o status do eleitor, gera o protocolo 
    criptografado e salva a escolha associada ao ID do candidato na tabela de resultados.

    Args:
        voto (int): O número do candidato escolhido.
        cpfValido (str): O CPF criptografado do eleitor que realizou o voto.
        texto (str): O menu atual para exibição visual.

    Returns:
        Nenhum valor é retornado (None).
    """

    ger.limpar()
    protocolo = vot.gerador_protocolo(voto)
    print(f"\n\t-- {texto} --")
    input(f"\n*ATUALIZAÇÃO: Voto confirmado com sucesso.\nSeu protocolo de votação é {protocolo}\n\nAperte ENTER para continuar...")
    protocolo = c.criptografia(2,protocolo)
    vot.arquivoTXT(0,'SUCESSO: Voto realizado com sucesso.')
    cursor.execute(f"UPDATE eleitores SET status_voto = status_voto + 1 WHERE cpf = '{cpfValido}'")
    conexao.commit()
    cursor.execute(f"SELECT id_candidato FROM candidatos WHERE num_votacao = {voto}")
    id_candidato = cursor.fetchone()[0]
    horario = datetime.datetime.now()
    cursor.execute("INSERT INTO resultado (protocolo_votacao, horario_votacao, id_candidato) VALUES (%s, %s, %s)",(protocolo, horario, id_candidato))
    conexao.commit()
    ger.limpar()

def votoNulo(cpfValido,texto): 
    
    """
    Registra um voto nulo na urna. Altera o status do eleitor, gera o protocolo 
    criptografado e salva a escolha associada ao ID do 'Voto Nulo' na tabela de resultados Se 'Voto Nulo' não 
    existir no banco de dados, a função a cria automaticamente.

    Args:
        cpfValido (str): O CPF criptografado do eleitor.
        texto (str): O contexto/menu atual para exibição visual.

    Returns:
        Nenhum valor é retornado (None).
    """

    ger.limpar()
    cursor.execute("SELECT id_candidato FROM candidatos WHERE nome = 'Voto Nulo'")
    resultado = cursor.fetchone()

    if resultado == None:
        id_nulo = None
        cursor.execute("INSERT INTO candidatos(nome,partido, num_votacao) values(%s,%s,%s)", ("Voto Nulo", "Nulo", 0))
        conexao.commit()
        cursor.execute("SELECT id_candidato FROM candidatos WHERE nome = 'Voto Nulo'")
        id_nulo= cursor.fetchone()[0]
    else:
        id_nulo = resultado[0]
     
    protocolo = vot.gerador_protocolo(id_nulo)
    print(f"\n\t-- {texto} --")
    input(f"\n*ATUALIZAÇÃO: Voto confirmado com sucesso.\nSeu protocolo de votação é {protocolo}\n\nAperte ENTER para continuar...")
    protocolo = c.criptografia(2,protocolo)
    vot.arquivoTXT(0,'SUCESSO: Voto realizado com sucesso.')
    cursor.execute(f"UPDATE eleitores SET status_voto = status_voto + 1 WHERE cpf = '{cpfValido}'")
    conexao.commit()
    horario = datetime.datetime.now()
    cursor.execute("INSERT INTO resultado (protocolo_votacao, horario_votacao, id_candidato) VALUES (%s, %s, %s)",(protocolo, horario, id_nulo))
    conexao.commit()
    ger.limpar()

def somarVotos(): 
    
    """
    Calcula o total de votos por candidato na tabela de resultados.

    Args:
        Não recebe parâmetros de entrada.

    Returns:
        soma: Retorna o total de votos agrupado.
    """

    cursor.execute(f"SELECT c.nome, COUNT(r.id_candidato) AS total_votos FROM candidatos c JOIN resultado r ON c.id_candidato = r.id_candidato GROUP BY c.id_candidato, c.nome;")
    soma = cursor.fetchone()
    return soma