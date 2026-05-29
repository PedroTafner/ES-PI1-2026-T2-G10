import Arquivos_PY.bancoDeDados as bd
import random as r
import Arquivos_PY.validacoes as val
import os
import datetime
import Arquivos_PY.resultado as res
import Arquivos_PY.criptografia as c
import Arquivos_PY.descriptografia as d
permicao = 0


def opcao_votacao(): #OPÇÃO VOTAÇÃO
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

def abertura(): #OPÇÃO ABERTURA DE SISTEMA DE VOTAÇÃO
    limpar()
    validacao = val.validarEleitor('ABERTURA DE SISTEMA DE VOTAÇÃO', 0)
        
    limpar()
    if validacao == True:
        limpar()
        arquivoTXT(2,'limpando')
        reset_protocolo()
        print("\t-- ZERÉSIMA -- \n")
        bd.zeresima()
        input( "\n*ATUALIZAÇÃO: Zerésima realizada com sucesso\n\nAperte ENTER para dar continuidade a votação...")
        arquivoTXT(0,'ABERTURA: Votação iniciada com sucesso. Total de votos zerado.')
        votacao()

    else:
        limpar()
        validacao
        return
    
def votacao(): #OPÇÃO ABRIR SISTEMA DE VOTAÇÃO
    opcao=0
    
    while opcao != 2:
        limpar()
        print("\n\t-- SISTEMA DE VOTAÇÃO --")
        print("\n1 - Votar")
        print("2 - Encerrar Votação")

        opcao=int(input("\nEscolha uma opção: "))

        match opcao:
            case 1: #OPÇÃO VOTAR
                limpar()
                val.validarEleitor('URNA DE VOTAÇÃO', 1)

            case 2: #OPÇÃO ENCERRAR VOTAÇÃO
                limpar()
                validacao = val.validarEleitor('FECHANDO URNA DE VOTAÇÃO', 0)

                if validacao == True:
                    arquivoTXT(0,'ENCERRAMENTO: Votação finalizada com sucesso.')
                    limpar()
                    pass

                else:
                    votacao()

            case _: #OPÇÃO INVÁLIDA
                limpar()
    
def auditoria(): #OPÇÃO AUDITORIA DO SISTEMA DE VOTAÇÃO
    opcao=0
    while opcao != 3:
        limpar()
        print("\n\t-- AUDITORIA DO SISTEMA DE VOTAÇÃO --")
        print("\n1 - Log de Ocorrências")
        print("2 - Protocolos de Votação")
        print("3 - Voltar")

        opcao=int(input("\nEscolha uma opção: "))

        match opcao:
            case 1: #OPÇÃO LOG DE OCORRÊNCIAS
                limpar()
                print("\n-- Log de Ocorrências --")
                conteudo = arquivoTXT(1,'lendo')
                if conteudo:
                    print(conteudo)
                else:
                    print("\nNenhum log foi registrado.")
                input("\nAperte ENTER para retornar...")
            
            case 2: #OPÇÃO PROTOCOLOS DE VOTAÇÃO
                limpar()
                print("\n-- Protocolos de Votação --\n")
                bd.cursor.execute("SELECT protocolo_votacao, horario_votacao FROM resultado ORDER BY horario_votacao")
                protocolos = bd.cursor.fetchall()
                if protocolos:
                    for (protocolo, horario) in protocolos:
                        protocolo = d.descriptografia(2,protocolo)
                        print(f"({horario}) - {protocolo} - Voto Confirmado")
                else:
                    print("Nenhum protocolo registrado.")
                input("\nAperte ENTER para retornar...")
            
            case 3: #OPÇÃO VOLTAR
                limpar()
                return
            
            case _: #OPÇÃO INVÁLIDA
                limpar()

def resultado(): #OPÇÃO RESULTADO DA VOTAÇÃO
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
            case 1: #OPÇÃO BOLETIM DE URNA
                res.boletimUrna()

            case 2: #OPÇÃO ESTATÍSTICA DE COMPARECIMENTO
                res.estatistica_comparecimento()

            case 3: #OPÇÃO VOTOS POR PARTIDO
                res.votosPartidos()

            case 4: #OPÇÃO VALIDAÇÃO DE INTEGRIDADE
                res.valIntegridade()

            case 5: #OPÇÃO INVÁLIDA
                limpar()
                return
            
            case _: #OPÇÃO INVÁLIDA
                limpar()

def limpar(): #LIMPA O TERMINAL PARA MANTER O SISTEMA ORGANIZADO
    os.system('cls' if os.name == 'nt' else 'clear')

def arquivoTXT(acao, mensagem): #REGISTRA (acao = 0) OU LÊ (acao = 1) UM ARQUIVO TXT
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

def gerador_protocolo(numero_candidato):
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

def reset_protocolo():
    bd.cursor.execute(f"DELETE from resultado")
    bd.conexao.commit()
    bd.cursor.execute(f"UPDATE eleitores SET status_voto = 0")
    bd.conexao.commit()