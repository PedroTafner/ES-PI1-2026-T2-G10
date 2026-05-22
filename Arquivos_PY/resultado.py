import Arquivos_PY.bancoDeDados as bd
import Arquivos_PY.gerenciamento as ger


def boletimUrna():
    ger.limpar()
    print("\n\t-- BOLETIM DE URNA --")
    bd.cursor.execute("SELECT c.nome, c.num_votacao, c.partido, COUNT(r.id_candidato) AS total_votos FROM candidatos c JOIN resultado r ON c.id_candidato = r.id_candidato GROUP BY c.id_candidato, c.nome, c.num_votacao, c.partido ORDER BY total_votos DESC LIMIT 1;")   
    ganhador = bd.cursor.fetchone()
    print(f"CANDIDATO: {ganhador[0]} | NÚMERO: {ganhador[1]} | PARTIDO: {ganhador[2]} | TOTAL DE VOTOS: {ganhador[3]}")
    input("\nAperte ENTER para continuar...")
    ger.limpar()



def votosPartidos():
    ger.limpar()
    print("\n\t-- VOTOS POR PARTIDO --")
    bd.cursor.execute("SELECT c.nome, COUNT(r.id_candidato) AS total_voto FROM candidatos c JOIN resultado r ON c.id_candidato = r.id_candidato GROUP BY c.id_candidato, c.nome")
    resultado = bd.cursor.fetchall()
    for candidato,votos in resultado:
        print(f"\nCADIDATO:{candidato}  |   VOTOS: {votos} ")
        
    input("\nAperte ENTER para continuar...")
    ger.limpar()  


     



    
        
