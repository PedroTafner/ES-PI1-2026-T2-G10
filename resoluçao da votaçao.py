
from database.conexao_SQL import criar_conexao

# FUNÇÕES DE RELATÓRIO E MONITORAMENTO

def status_sistema():
    print("\n" + "="*50)
    print("[SISTEMA] Inicializando Urna Eletrônica...")
    print("[INFO] Conexão com o banco de dados estabelecida.")
    print("[INFO] Todos os módulos carregados com sucesso.")
    print("="*50)


def boletim_urna(cursor):
    print("\n" + "-"*50)
    print("             BOLETIM DE URNA - GERAL            ")
    print("-"*50)

    # Lista candidatos em ordem alfabética com votos
    cursor.execute("SELECT id, nome, numero, partido, total_votos FROM candidatos ORDER BY nome ASC")
    candidatos = cursor.fetchall()

    if not candidatos:
        print("[-] Nenhum candidato cadastrado no sistema!")
        print("-"*50)
        return

    print(f"{'Nome do Candidato':<22} | {'Nº':<5} | {'Partido':<8} | {'Votos':<6}")
    print("-" * 50)
    
    for cand in candidatos:
        print(f"{cand[1]:<22} | {cand[2]:<5} | {cand[3]:<8} | {cand[4]:<6}")

    # Responsável por buscar o vencedor atual
    cursor.execute("SELECT id, nome, numero, partido, total_votos FROM candidatos ORDER BY total_votos DESC LIMIT 1")
    vencedor = cursor.fetchone()

    print("\n" + "-"*50)
    print("                   VENCEDOR                     ")
    print("-"*50)
    
    if vencedor and vencedor[4] > 0:
        print(f" > Candidato Eleito: {vencedor[1]}")
        print(f" > Número Eleitoral: {vencedor[2]}")
        print(f" > Partido Político: {vencedor[3]}")
        print(f" > Total de Votos  : {vencedor[4]} votos computados")
    elif vencedor and vencedor[4] == 0:
        print("[!] Existem candidatos, mas todos estão com 0 votos.")
    else:
        print("[-] Não há dados de votação para eleger um vencedor.")
    print("-"*50)


def votos_por_partido(cursor):
    print("\n" + "-"*50)
    print("               VOTOS POR PARTIDO                ")
    print("-"*50)

    cursor.execute("SELECT partido, SUM(total_votos) FROM candidatos GROUP BY partido ORDER BY partido ASC")
    partidos = cursor.fetchall()

    if not partidos or partidos[0][0] is None:
        print("[-] Nenhum voto registrado para partidos até o momento!")
        print("-"*50)
        return

    print(f"{'Legenda/Partido':<20} | {'Total de Votos Acumulados':<25}")
    print("-" * 50)
    for part in partidos:
        print(f"{part[0]:<20} | {part[1]:<25}")
    print("-"*50)


def estatistica_comparecimento(cursor):
    print("\n" + "-"*50)
    print("          ESTATÍSTICA DE COMPARECIMENTO         ")
    print("-"*50)

    cursor.execute("SELECT COUNT(*) FROM eleitores")
    total_eleitores = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM eleitores WHERE status_voto = 'Já Votou'")
    total_votaram = cursor.fetchone()[0]

    if total_eleitores == 0:
        print("[-] Nenhum eleitor cadastrado na base de dados!")
        print("-"*50)
        return

    percentual_comp = (total_votaram / total_eleitores) * 100
    percentual_abst = 100 - percentual_comp
    abstencoes = total_eleitores - total_votaram

    print(f" • Total de eleitores aptos     : {total_eleitores}")
    print(f" • Total de eleitores que votaram: {total_votaram}")
    print(f" • Total de abstenções (faltas) : {abstencoes}")
    print(f" • Percentual de comparecimento : {percentual_comp:.2f}%")
    print(f" • Percentual de abstenção      : {percentual_abst:.2f}%")
    print("-"*50)


def validacao_integridade(cursor):
    print("\n" + "-"*50)
    print("            AUDITORIA E INTEGRIDADE             ")
    print("-"*50)

    cursor.execute("SELECT COUNT(*) FROM votos")
    total_votos_urna = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM eleitores WHERE status_voto = 'Já Votou'")
    total_ja_votou = cursor.fetchone()[0]

    print(f" -> Contagem de votos físicos na Urna    : {total_votos_urna}")
    print(f" -> Registro de eleitores que confirmaram: {total_ja_votou}")
    print("-" * 50)

    if total_votos_urna == total_ja_votou:
        print("[OK] Sucesso! Urna auditada e 100% íntegra.")
    else:
        print("[CRÍTICO] ALERTA DE FRAUDE OU INCONSISTÊNCIA!")
        print("[SISTEMA] Os votos da urna não batem com o fluxo de eleitores.")
    print("-"*50)

# INTERAÇÕES DO USUÁRIO (CADASTROS E SIMULAÇÃO)

def cadastrar_candidato(cursor, conexao):
    print("\n" + "="*50)
    print("             CADASTRO DE CANDIDATO              ")
    print("="*50)
    nome = input("Nome do candidato: ").strip()
    if not nome:
        print("[-] Erro: Nome inválido!")
        return
        
    try:
        numero = int(input("Número do candidato (ex: 22, 13, 45): "))
    except ValueError:
        print("[-] Erro: O número precisa ser um algarismo inteiro!")
        return

    partido = input("Sigla do Partido (ex: PT, PL, PSDB): ").strip().upper()
    
    try:
        # Usando placeholders '%s' padrão do mysql-connector
        cursor.execute(
            "INSERT INTO candidatos (nome, numero, partido, total_votos) VALUES (%s, %s, %s, 0)",
            (nome, numero, partido)
        )
        conexao.commit()
        print(f"[+] {nome} registrado com sucesso sob o número {numero}!")
    except Exception as e:
        print(f"[-] Erro ao salvar candidato: {e}")


def cadastrar_eleitor(cursor, conexao):
    print("\n" + "="*50)
    print("              CADASTRO DE ELEITOR               ")
    print("="*50)
    nome = input("Nome completo do eleitor: ").strip()
    if not nome:
        print("[-] Erro: Nome inválido!")
        return
        
    titulo = input("Número do Título de Eleitor: ").strip()
    if not titulo:
        print("[-] Erro: Título inválido!")
        return
    
    try:
        cursor.execute(
            "INSERT INTO eleitores (nome, titulo, status_voto) VALUES (%s, %s, 'Apto')",
            (nome, titulo)
        )
        conexao.commit()
        print(f"[+] Eleitor {nome} cadastrado e habilitado para votar!")
    except Exception as e:
        print(f"[-] Erro ao salvar eleitor: {e}")


def zeradesima_sistema(cursor, conexao):
    print("\n" + "!"*50)
    print("  ATENÇÃO: VOCÊ ESTÁ PRESTES A LIMPAR O SISTEMA!  ")
    print("!"*50)
    confirmar = input("Deseja executar a ZERADÉSIMA? Todos os votos sumirão (S/N): ").strip().upper()
    
    if confirmar == 'S':
        try:
            cursor.execute("UPDATE candidatos SET total_votos = 0")
            cursor.execute("DELETE FROM votos")
            cursor.execute("UPDATE eleitores SET status_voto = 'Apto'")
            conexao.commit()
            print("[✔️] ZERADÉSIMA EXECUTADA! Banco de dados limpo para votação.")
        except Exception as e:
            print(f"[-] Erro ao redefinir sistema: {e}")
    else:
        print("[*] Operação abortada pelo administrador.")


# LOOP PRINCIPAL DO MENU (WHILE + IF/ELIF)

def menu_principal():
    conexao = criar_conexao()
    if not conexao:
        print("[-] Não foi possível rodar o sistema devido a falhas no Banco de Dados.")
        return
        
    cursor = conexao.cursor()
    status_sistema()
    
    # Controle do loop 'while'
    rodando = True
    while rodando:
        print("\n" + "═"*45)
        print("          SISTEMA DE GESTÃO ELEITORAL          ")
        print("═"*45)
        print(" [1] Boletim de Urna (Geral e Vencedor)")
        print(" [2] Estatística de Votos por Partido")
        print(" [3] Indicadores de Comparecimento")
        print(" [4] Auditoria de Integridade da Urna")
        print(" " + "─"*41)
        print(" [5] Cadastrar Novo Candidato")
        print(" [6] Cadastrar Novo Eleitor")
        print(" [7] Executar Zeradésima (Zerar Urna)")
        print(" " + "─"*41)
        print(" [8] Fechar e Sair do Programa")
        print("═"*45)
        
        opcao = input("Selecione uma opção (1-8): ").strip()
        
        if opcao == "1":
            boletim_urna(cursor)
        elif opcao == "2":
            votos_por_partido(cursor)
        elif opcao == "3":
            estatistica_comparecimento(cursor)
        elif opcao == "4":
            validacao_integridade(cursor)
        elif opcao == "5":
            cadastrar_candidato(cursor, conexao)
        elif opcao == "6":
            cadastrar_eleitor(cursor, conexao)
        elif opcao == "7":
            zeradesima_sistema(cursor, conexao)
        elif opcao == "8":
            print("\n[DESCONECTANDO] Finalizando sessões do SQL...")
            print("[DESCONECTANDO] Aplicação encerrada com sucesso.")
            rodando = False  # Para o While
        else:
            print(f"\n[!] Erro: '{opcao}' não é uma opção válida. Tente de 1 a 8.")
            
    # Fecha os canais de comunicação com segurança
    cursor.close()
    conexao.close()


if __name__ == "__main__":
    menu_principal()

    