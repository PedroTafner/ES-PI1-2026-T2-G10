import Arquivos_PY.bancoDeDados as bd
import Arquivos_PY.resultado as res
import Arquivos_PY.criptografia as c
import Arquivos_PY.descriptografia as d
import Arquivos_PY.validacoes as val
import Arquivos_PY.gerenciamento as ger

import random as r
import os
import datetime
permicao = 0


def opcao_votacao(): # OPÇÃO VOTAÇÃO
    limpar()
    opcao=0
    while opcao != 4:
        print("\n\t-- VOTAÇÃO --")
        print("\n1 - Abrir Sistema de Votação")
        print("2 - Auditoria do Sistema de Votação")
        print("3 - Resultado da Votação")
        print("4 - Voltar para o Menu Principal")

        opcao=int(input("\nEscolha uma opção: "))
        match opcao:
            case 1: #OPÇÃO ABRIR SISTEMA DE VOTAÇÃO
                abertura()

            case 2: #OPÇÃO AUDITORIA DO SISTEMA DE VOTAÇÃO
                auditoria()

            case 3: #OPÇÃO RESULTADO DA VOTAÇÃO
                resultado()

            case 4: #OPÇÃO SAIR
                limpar()
                return
            
            case _: #OPÇÃO INVÁLIDA
                limpar()

def abertura(): # OPÇÃO ABERTURA DE SISTEMA DE VOTAÇÃO
    limpar()
    
    permicao = ger.verificacao_existencia(0) # VERIFICA SE HÁ ELEITORES CADASTRADOS NO SISTEMA
    if permicao == False: # SE NÃO, A ABERTURA DE VOTAÇÃO É INTERROMPIDA
        print("\n\t-- ABERTURA DE SISTEMA DE VOTAÇÃO --")
        input("\n*ERRO: Não há eleitores cadastrados.\n\nAperte ENTER para retornar...")
        limpar()
        return
    
    permicao = ger.verificacao_existencia(1) # VERIFICA SE HÁ CANDIDATOS CADASTRADOS NO SISTEMA
    if permicao == False: # SE NÃO, A ABERTURA DE VOTAÇÃO É INTERROMPIDA
        print("\n\t-- ABERTURA DE SISTEMA DE VOTAÇÃO --")
        input("\n*ERRO: Não há candidatos cadastrados.\n\nAperte ENTER para retornar...")
        limpar()
        return
        
    validacao = val.validarEleitor('ABERTURA DE SISTEMA DE VOTAÇÃO', 0) # VERIFICA SE AS INFORMAÇÕES DO ELEITOR ESTÃO CORRETAS (CPF, TITULO, CHAVE DE ACESSO E MESÁRIO)
        
    limpar()
    if validacao == True: # SE TUDO ESTIVER CERTO, A ABERTURA É FEITO JUNTO DA ZERÉSIMA
        limpar()
        reset_protocolo()
        print("\t-- ZERÉSIMA -- \n")
        bd.zeresima()
        input( "\n*ATUALIZAÇÃO: Zerésima realizada com sucesso.\n\nAperte ENTER para dar continuidade a votação...")
        arquivoTXT(0,'ABERTURA: Votação iniciada com sucesso. Total de votos zerado.')
        votacao()

    else: # CASO NÃO, NÃO OCORRE A ABERTURA
        limpar()
        validacao
        return
    
def votacao(): # OPÇÃO ABRIR SISTEMA DE VOTAÇÃO
    opcao=0
    
    while opcao != 2:
        limpar()
        print("\n\t-- SISTEMA DE VOTAÇÃO --")
        print("\n1 - Votar")
        print("2 - Encerrar Votação")

        opcao=int(input("\nEscolha uma opção: "))

        match opcao:
            case 1: # OPÇÃO VOTAR
                limpar()
                val.validarEleitor('URNA DE VOTAÇÃO', 1) # VALIDA AS INFORMAÇÕES DO ELEITOR PARA A REALIZAÇÃO DE SEU VOTO

            case 2: # OPÇÃO ENCERRAR VOTAÇÃO
                limpar()
                validacao = val.validarEleitor('FECHANDO URNA DE VOTAÇÃO', 0) # VALIDA AS INFORMAÇÕES DO ELEITOR PARA O FECHAMENTO DA URNA

                if validacao == True: # CASO TUDO ESTEJA VÁLIDO, É ENCERRADO E É REGISTRADO UM LOG DE OCORRÊNCIA SOBRE O FECHAMENTO
                    limpar()
                    print("\n\t-- FECHANDO URNA DE VOTAÇÃO --")
                    input("\n*SUCESSO: O sistema de votação foi fechado com sucesso.\n\nAperte ENTER para continuar...")
                    arquivoTXT(0,'ENCERRAMENTO: Votação finalizada com sucesso.')
                    limpar()
                    pass

                else: # CASO NÃO, VOLTA PARA A ABA DE VOTAÇÃO
                    votacao()

            case _: #OPÇÃO INVÁLIDA
                limpar()
    
def auditoria(): # OPÇÃO AUDITORIA DO SISTEMA DE VOTAÇÃO
    opcao=0
    while opcao != 3:
        limpar()
        print("\n\t-- AUDITORIA DO SISTEMA DE VOTAÇÃO --")
        print("\n1 - Log de Ocorrências")
        print("2 - Protocolos de Votação")
        print("3 - Voltar")

        opcao=int(input("\nEscolha uma opção: "))

        match opcao:
            case 1: # OPÇÃO LOG DE OCORRÊNCIAS
                limpar()
                print("\n\t-- LOG DE OCORRÊNCIAS --")
                conteudo = arquivoTXT(1,'lendo')

                if conteudo: # CASO TENHA CONTEÚDO REGISTRADO, ESTE É MOSTRADO
                    print(conteudo)

                else: # CASO NÃO, UM AVISO É MOSTRADO
                    print("\n*STATUS: Nenhum log foi registrado.")
                input("\nAperte ENTER para retornar...")
            
            case 2: # OPÇÃO PROTOCOLOS DE VOTAÇÃO
                limpar()
                print("\n\t-- PROTOCOLOS DE VOTAÇÃO --\n")

                bd.cursor.execute("SELECT protocolo_votacao, horario_votacao FROM resultado ORDER BY horario_votacao") # SELECIONA OS PROTOCOLOS DE VOTAÇÃO DO BANCO DE DADOS
                protocolos = bd.cursor.fetchall()

                if protocolos: # CASO TENHA PROTOCOLOS REGISTRADOS, ESTES SÃO MOSTRADOS
                    for (protocolo, horario) in protocolos:
                        protocolo = d.descriptografia(2,protocolo) # O PROTOCOLO É DESCRIPTOGRAFADO PARA SER MOSTRADO
                        print(f"({horario}) - {protocolo} - Voto Confirmado")

                else: # CASO NÃO, UM AVISO É MOSTRADO
                    print("*STATUS: Nenhum protocolo registrado.")
                input("\nAperte ENTER para retornar...")
            
            case 3: # OPÇÃO VOLTAR
                limpar()
                return
            
            case _: # OPÇÃO INVÁLIDA
                limpar()

def resultado(): # OPÇÃO RESULTADO DA VOTAÇÃO
    limpar()
    opcao=0
    while opcao != 5:
        print("\n\t-- RESULTADO DA VOTAÇÃO --")
        print("\n1 - Boletim de Urna")
        print("2 - Estatística de Comparecimento")
        print("3 - Votos por Partido")
        print("4 - Validação de Integridade")
        print("5 - Voltar")

        opcao=int(input("\nEscolha uma opção: "))

        match opcao:
            case 1: # OPÇÃO BOLETIM DE URNA
                res.boletimUrna()

            case 2: # OPÇÃO ESTATÍSTICA DE COMPARECIMENTO
                res.estatistica_comparecimento()

            case 3: # OPÇÃO VOTOS POR PARTIDO
                res.votosPartidos()

            case 4: # OPÇÃO VALIDAÇÃO DE INTEGRIDADE
                res.valIntegridade()

            case 5: # OPÇÃO INVÁLIDA
                limpar()
                return
            
            case _: # OPÇÃO INVÁLIDA
                limpar()

def limpar(): # LIMPA O TERMINAL PARA MANTER O SISTEMA ORGANIZADO
    os.system('cls' if os.name == 'nt' else 'clear')

def arquivoTXT(acao, mensagem): # REGISTRA (acao = 0), LÊ (acao = 1) OU APAGA (acao = 2) O LOG DE OCORRÊNCIAS
    momento = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    if acao == 0:
        with open (f"Arquivos_TXT/logOcorrencias.txt", "a", encoding="utf-8") as arq:
            arq.write(f"\n({momento}) - {mensagem}")

    if acao == 1:
        with open (f"Arquivos_TXT/logOcorrencias.txt", "r", encoding="utf-8") as arq:
            conteudo = arq.read()
            return conteudo
            
    if acao == 2:
        with open(f"Arquivos_TXT/logOcorrencias.txt", "w") as arq:
            arq.write("")

def gerador_protocolo(numero_candidato): # GERA O PROTOCOLO DE VOTAÇÃO DE ACORDO COM OS REQUISITOS, OU SEJA, 2 LETRAS ALEATORIAS + 26 + NUM_CANDIDATO + 5 DÍGITOS ALEATÓRIOS
    protocolo = 'V'
    for i in range(2):
        alfabeto = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        letras = r.randint(0,25)
        letras = alfabeto.pop(letras)
        protocolo += str(letras)

    protocolo += '26'

    if numero_candidato < 10:
        protocolo += '0' + str(numero_candidato)

    else:
        protocolo += str(numero_candidato)

    for i in range(5):
        protocolo += str(r.randint(0,9))

    return protocolo

def reset_protocolo(): # LIMPA OS PROTOCOLOS DO BANCO DE DADOS E MUDA O STATUS_VOTO DO ELEITOR PARA 0 A FIM DE RESETAR O SISTEMA DE ELEIÇÃO
    bd.cursor.execute(f"DELETE from resultado")
    bd.conexao.commit()
    bd.cursor.execute(f"UPDATE eleitores SET status_voto = 0")
    bd.conexao.commit()