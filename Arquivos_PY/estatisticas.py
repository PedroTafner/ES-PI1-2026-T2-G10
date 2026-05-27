# Estatiscas de comparecimento

def estatistica_comparecimento(cursor):
    print("\n--- ESTATÍSTICA DE COMPARECIMENTO ---")

    #  quantas pessoas votaram e percentual
    cursor.execute("SELECT COUNT(*) FROM eleitores")
    total_eleitores = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM eleitores WHERE status_voto = 'Já Votou'")
    total_votaram = cursor.fetchone()[0]

    if total_eleitores == 0:
        print("Nenhum eleitor cadastrado!")
        return

    percentual = (total_votaram / total_eleitores) * 100

    print(f"Total de eleitores aptos: {total_eleitores}")
    print(f"Total que votaram: {total_votaram}")
    print(f"Percentual de comparecimento: {percentual:.2f}%")



