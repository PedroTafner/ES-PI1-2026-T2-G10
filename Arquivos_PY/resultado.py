import Arquivos_PY.bancoDeDados as bd
import Arquivos_PY.gerenciamento as ger


def boletimUrna():
    ger.limpar()
    print("\n\t-- BOLETIM DE URNA --\n")
    bd.cursor.execute("SELECT c.nome, COUNT(r.id_candidato) AS total_votos FROM candidatos c JOIN resultado r ON c.id_candidato = r.id_candidato GROUP BY c.id_candidato, c.nome ORDER BY c.nome")   
    candidatos = bd.cursor.fetchall()
    
    if candidatos:
        for nome, votos in candidatos:
            if nome != 'Voto Nulo':
                print(f"Candidato: {nome} | Total de Votos: {votos}")
            else:
                print(f"Votos Nulos: {votos}")

        bd.cursor.execute("SELECT c.nome, c.num_votacao, c.partido, COUNT(r.id_candidato) AS total_votos FROM candidatos c JOIN resultado r ON c.id_candidato = r.id_candidato GROUP BY c.id_candidato, c.nome, c.num_votacao, c.partido ORDER BY total_votos DESC LIMIT 1;")   
        ganhador = bd.cursor.fetchone()

        if ganhador[0] == 'Voto Nulo':
            print("\nNão houve vencedor, pois houve mais votos nulos.")
        else:
            print(f"\nVencedor: {ganhador[0]}  |  N.º {ganhador[1]}  |  Partido: {ganhador[2]}  |  Total de Votos: {ganhador[3]}")
        
        input("\nAperte ENTER para continuar...")

    else:
        print("\nNenhum voto registrado.")

    ger.limpar()

def votosPartidos():
    ger.limpar()
    print("\n\t-- VOTOS POR PARTIDO --")
    bd.cursor.execute("SELECT c.partido, COUNT(r.id_candidato) AS total_voto FROM candidatos c JOIN resultado r ON c.id_candidato = r.id_candidato GROUP BY c.id_candidato, c.partido")
    resultado = bd.cursor.fetchall()
    for partido,votos in resultado:
        if partido != 'Nulo':
            print(f"\nPartido: {partido} | Votos: {votos} ")
        else:
            print(f"\nVotos nulos: {votos}")
        
    input("\nAperte ENTER para continuar...")
    ger.limpar()  

def valIntegridade():
    ger.limpar()
    print("\n\t-- VALIDAÇÃO DA INTEGRIDADE --")
    bd.cursor.execute("SELECT COUNT(*) FROM eleitores WHERE status_voto = 1")
    eleitoresVotaram = bd.cursor.fetchone()[0]
    bd.cursor.execute("SELECT COUNT(*) FROM resultado")
    votosRealizados = bd.cursor.fetchone()[0]

    print(f"\nVotos computados: {votosRealizados}\nEleitores que votaram: {eleitoresVotaram}")
    if eleitoresVotaram == votosRealizados:
        print("\n*SUCESSO: A Eleição foi integra.")
    
    else:
        print("\n*ERRO: A Eleição não foi integra")

    input("\nAperte ENTER para continuar...")
    ger.limpar()

def estatistica_comparecimento():
    ger.limpar()
    print("\n\t-- ESTATÍSTICA DE COMPARECIMENTO --")

    #  quantas pessoas votaram e percentual
    bd.cursor.execute("SELECT COUNT(*) FROM eleitores")
    total_eleitores = bd.cursor.fetchone()[0]

    bd.cursor.execute("SELECT COUNT(*) FROM eleitores WHERE status_voto = 1")
    total_votaram = bd.cursor.fetchone()[0]

    if total_eleitores == 0:
        print("Nenhum eleitor cadastrado!")
        return

    percentual = (total_votaram / total_eleitores) * 100

    print(f"Total de eleitores: {total_eleitores}")
    print(f"Total que votaram: {total_votaram}")
    print(f"Percentual de comparecimento: {percentual:.2f}%")
    input("\nAperte ENTER para retornar...")
    ger.limpar()