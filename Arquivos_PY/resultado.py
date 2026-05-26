import Arquivos_PY.bancoDeDados as bd
import Arquivos_PY.gerenciamento as ger


def boletimUrna():
    ger.limpar()
    print("\n\t-- BOLETIM DE URNA --")
    bd.cursor.execute("SELECT c.nome, c.num_votacao, c.partido, COUNT(r.id_candidato) AS total_votos FROM candidatos c JOIN resultado r ON c.id_candidato = r.id_candidato GROUP BY c.id_candidato, c.nome, c.num_votacao, c.partido ORDER BY total_votos DESC LIMIT 1;")   
    ganhador = bd.cursor.fetchone()
    if ganhador is not None:
        print(f"\nCANDIDATO: {ganhador[0]}  |  NÚMERO: {ganhador[1]}  |  PARTIDO: {ganhador[2]}  |  TOTAL DE VOTOS: {ganhador[3]}")
    else:
        print("\nNenhum voto registrado.")
    input("\nAperte ENTER para continuar...")
    ger.limpar()

def votosPartidos():
    ger.limpar()
    print("\n\t-- VOTOS POR PARTIDO --")
    bd.cursor.execute("SELECT c.nome, COUNT(r.id_candidato) AS total_voto FROM candidatos c JOIN resultado r ON c.id_candidato = r.id_candidato GROUP BY c.id_candidato, c.nome")
    resultado = bd.cursor.fetchall()
    for candidato,votos in resultado:
        print(f"\nCADIDATO: {candidato}  |   VOTOS: {votos} ")
        
    input("\nAperte ENTER para continuar...")
    ger.limpar()  

def valIntegridade():
    ger.limpar()
    print("\n\t-- VALIDAÇÃO DA INTEGRIDADE --")
    bd.cursor.execute("SELECT COUNT(*) FROM eleitores WHERE status_voto = 1")
    eleitoresVotaram = bd.cursor.fetchone()[0]
    bd.cursor.execute("SELECT COUNT(*) FROM resultado")
    votosRealizados = bd.cursor.fetchone()[0]
    if eleitoresVotaram == votosRealizados:
        print("\nA ELEIÇÃO FOI INTEGRA.")
    
    else:
        print("\nERRO: A ELEIÇÃO NÃO FOI INTEGRA")

    input("\nAperte ENTER para continuar...")
    ger.limpar()
