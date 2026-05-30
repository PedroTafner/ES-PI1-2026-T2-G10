import Arquivos_PY.bancoDeDados as bd
import Arquivos_PY.gerenciamento as ger


def boletimUrna(): # FUNÇÃO PARA MOSTRAR O BOLETIM DE URNA NO RESULTADO DA VOTAÇÃO
    ger.limpar()
    print("\n\t-- BOLETIM DE URNA --\n")

    # AQUI ELE SELECIONA TODOS OS CANDIDATOS E, ATRAVÉS DO JOIN, ELE CONECTA ID_CANDIDATO NA TABELA RESULTADO, CONTABILIZANDO SEUS VOTOS
    bd.cursor.execute("SELECT c.nome, COUNT(r.id_candidato) AS total_votos FROM candidatos c JOIN resultado r ON c.id_candidato = r.id_candidato GROUP BY c.id_candidato, c.nome ORDER BY c.nome") 
    candidatos = bd.cursor.fetchall()
    
    if candidatos:
        votosNulos=0 # SE HOUVER RESULTADO, ELE MOSTRA INICIALMENTE TODOS OS CANDIDATOS E QUANTOS VOTOS RECEBEU
        for nome, votos in candidatos:
            if nome != 'Voto Nulo':
                print(f"Candidato: {nome} | Total de Votos: {votos}")
            else:
                votosNulos = votos

        if votosNulos > 0: # CASO HÁ VOTOS NULOS, ELE É MOSTRADO
            print(f"Votos nulos: {votosNulos}")

        # AQUI É SELECIONADO O CANDIDATO VENCEDOR PELA QUANTIDADE DE VOTOS RECEBIDOS
        bd.cursor.execute("SELECT c.nome, c.num_votacao, c.partido, COUNT(r.id_candidato) AS total_votos FROM candidatos c JOIN resultado r ON c.id_candidato = r.id_candidato GROUP BY c.id_candidato, c.nome, c.num_votacao, c.partido ORDER BY total_votos DESC LIMIT 1;")   
        ganhador = bd.cursor.fetchone()

        if ganhador[0] == 'Voto Nulo': # CASO O VENCEDOR SEJA O VOTO NULO, UM AVISO É MOSTRADO DIZENDO QUE NÃO HÁ VENCEDOR
            print("\n* Não houve vencedor, pois houve mais votos nulos.")

        else: # CASO NÃO SEJA VOTO NULO, É MOSTRADO O SEU NOME, NÚMERO DE VOTAÇÃO, PARTIDO E O SEU TOTAL DE VOTOS
            print(f"\n* Vencedor:\n\t{ganhador[1]} | {ganhador[0]} - ({ganhador[2]}) | Total de Votos: {ganhador[3]}")
        
        input("\nAperte ENTER para continuar...")

    else: # SE NÃO HOUVER RESULTADO DISPONÍVEL, UM ALERTA APARECE DIZENDO QUE NÃO HÁ VOTOS
        print("*STATUS: Nenhum voto registrado.")
        input("\nAperte ENTER para retornar...")

    ger.limpar()

def votosPartidos(): # FUNÇÃO PARA MOSTRAR A QUANTIDADE DE VOTOS POR PARTIDO
    ger.limpar()
    print("\n\t-- VOTOS POR PARTIDO --\n")
    
    bd.cursor.execute("""
        SELECT c.partido, COUNT(r.id_candidato) AS total_voto_partido 
        FROM candidatos c 
        JOIN resultado r ON c.id_candidato = r.id_candidato 
        GROUP BY c.partido 
        ORDER BY total_voto_partido DESC
    """)
    resultado = bd.cursor.fetchall()

    votoNulo = 0  # Variável para guardar os votos nulos se eles existirem

    if resultado: # CASO TENHA VOTOS REGISTRADOS
        for partido, votos in resultado:
            if partido != 'Nulo':
                print(f"• Partido: {partido} | Votos: {votos}")
            else:
                votoNulo = votos  # Guarda a quantidade de nulos que já veio no SELECT
        
        # Se houver votos nulos (maior que 0), mostra no final por organização visual
        if votoNulo > 0:
            print(f"• Votos nulos: {votoNulo}")

    else: # CASO NÃO TENHA VOTOS REGISTRADOS
        print("*STATUS: Nenhum voto registrado.")
        
    input("\nAperte ENTER para continuar...")
    ger.limpar()

def valIntegridade(): # FUNÇÃO PARA VERIFICAR SE A ELEIÇÃO REALIZADA FOI INTEGRA OU NÃO
    ger.limpar()
    print("\n\t-- VALIDAÇÃO DA INTEGRIDADE --")
    bd.cursor.execute("SELECT COUNT(*) FROM eleitores WHERE status_voto = 1")
    eleitoresVotaram = bd.cursor.fetchone()[0]
    bd.cursor.execute("SELECT COUNT(*) FROM resultado")
    votosRealizados = bd.cursor.fetchone()[0]

    if votosRealizados: # CASO TENHA VOTOS REGISTRADOS, ELE MOSTRA A QUANTIDADES DE VOTOS COMPUTADOS, A QUANTIDADE DE ELEITORES QUE VOTARAM E DETERMINA SE, ATRAVÉS DESSAS INFORMAÇÕES, A VOTAÇÃO FOI INTEGRA OU NÃO
        print(f"\n• Votos computados: {votosRealizados}\n• Eleitores que votaram: {eleitoresVotaram}")

        if eleitoresVotaram == votosRealizados: # CASO FOI
            print("\n*SUCESSO: A Eleição foi integra.")
        
        else: # CASO NÃO
            print("\n*ERRO: A Eleição não foi integra")

    else: # CASO NÃO TENHA VOTOS REGISTRADO, UM AVISO É MOSTRADO EXPLICANDO
        print("\n*STATUS: Nenhum voto registrado.")

    input("\nAperte ENTER para continuar...")
    ger.limpar()

def estatistica_comparecimento(): # FUNÇÃO PARA MOSTRAR A ESTATÍSTICA DE COMPARECIMENTO DA VOTAÇÃO REALIZADA
    ger.limpar()
    print("\n\t-- ESTATÍSTICA DE COMPARECIMENTO --")

    #  quantas pessoas votaram e percentual
    bd.cursor.execute("SELECT COUNT(*) FROM eleitores")
    total_eleitores = bd.cursor.fetchone()[0]

    bd.cursor.execute("SELECT COUNT(*) FROM eleitores WHERE status_voto = 1")
    total_votaram = bd.cursor.fetchone()[0]

    if total_votaram: # CASO TENHA VOTOS COMPUTADOS, O TOTAL DE ELEITORES REGISTRADOS, O TOTAL QUE VOTOU E O PERCENTUAL DE COMPARECIMENTO É MOSTRADO
        print(f"\n• Total de eleitores: {total_eleitores}")
        print(f"• Total que votaram: {total_votaram}")
        percentual = (total_votaram / total_eleitores) * 100
        print(f"• Percentual de comparecimento: {percentual:.2f}%")

    else: # CASO NÃO TENHA VOTOS COMPUTADOS, UM AVISO É MOSTRADO EXPLICANDO
        print("\n*STATUS: Nenhum voto registrado.")
    input("\nAperte ENTER para retornar...")
    ger.limpar()