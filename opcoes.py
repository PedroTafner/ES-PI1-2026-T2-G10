import bancoDeDados
import random
def opcao_gerenciamento(): #OPÇÃO GERENCIAMENTO
    opcger=0
    while opcger != 6:
        print("\n-- GERENCIAMENTO --")
        print("\n1 - Cadastro")
        print("2 - Edição de dados")
        print("3 - Remoção de Eleitor")
        print("4 - Busca por Eleitor")
        print("5 - Listagem de Eleitor")
        print("6 - Voltar para o Menu Principal")

        opcger=int(input("\nEscolha uma opção: "))

        match opcger:
            case 1: #OPÇÃO CADASTRO
                opcao_cadastro()
            case 2: #OPÇÃO EDIÇÃO DE DADOS
                pass
            case 3: #OPÇÃO REMOÇÃO DE ELEITOR
                pass
            case 4: #OPÇÃO BUSCA POR ELEITOR
                pass
            case 5: #OPÇÃO LISTAGEM DE ELEITOR
                pass
            case 6: #OPÇÃO VOLTAR PARA O MENU PRINCIPAL
                return
            case _: #OPÇÃO INVÁLIDA
                print("Opção Inválida")
def opcao_votacao(): #OPÇÃO VOTAÇÃO
    opcvot=0
    while opcvot != 4:
        print("\n-- VOTAÇÃO --")
        print("\n1 - Abrir Sistema de Votação")
        print("2 - Auditoria do Sistema de Votação")
        print("3 - Resultado da Votação")
        print("4 - Voltar para o Menu Principal")

        opcvot=int(input("\nEscolha uma opção: "))
        match opcvot:
            case 1: #OPÇÃO ABRIR SISTEMA DE VOTAÇÃO
                opcao_abrirSistemaVotacao()
            case 2: #OPÇÃO AUDITORIA DO SISTEMA DE VOTAÇÃO
                opcao_auditoriaSistemaVotacao()
            case 3: #OPÇÃO RESULTADO DA VOTAÇÃO
                opcao_resultadoVotacao()
            case 4: #OPÇÃO SAIR
                return
            case _: #OPÇÃO INVÁLIDA
                print("Opção Inválida")
def opcao_abrirSistemaVotacao(): #OPÇÃO ABRIR SISTEMA DE VOTAÇÃO
    opcasv=0
    while opcasv != 2:
        print("\n-- SISTEMA DE VOTAÇÃO --")
        print("\n1 - Votar")
        print("2 - Encerrar Votação")
        print("3 - Voltar")

        opcasv=int(input("\nEscolha uma opção: "))

        match opcasv:
            case 1: #OPÇÃO VOTAR
                pass
            case 2: #OPÇÃO ENCERRAR VOTAÇÃO
                pass
            case 3: #OPÇÃO VOLTAR
                return
            case _: #OPÇÃO INVÁLIDA
                print("Opção Inválida")

def opcao_auditoriaSistemaVotacao(): #OPÇÃO AUDITORIA DO SISTEMA DE VOTAÇÃO
    opcaud=0
    while opcaud != 3:
        print("\n-- AUDITORIA DO SISTEMA DE VOTAÇÃO --")
        print("\n1 - Log de Ocorrências")
        print("2 - Protocolos de Votação")
        print("3 - Voltar")

        opcaud=int(input("Escolha uma opção: "))

        match opcaud:
            case 1: #OPÇÃO LOG DE OCORRÊNCIAS
                pass
            case 2: #OPÇÃO PROTOCOLOS DE VOTAÇÃO
                pass
            case 3: #OPÇÃO VOLTAR
                return
            case _: #OPÇÃO INVÁLIDA
                print("Opção Inválida")
def opcao_resultadoVotacao(): #OPÇÃO RESULTADO DA VOTAÇÃO
    opcresult=0
    while opcresult != 5:
        print("\n-- RESULTADO DA VOTAÇÃO --")
        print("\n1 - Boletim de Urna")
        print("2 - Estatística de Comparecimento")
        print("3 - Votos por Partido")
        print("4 - Validação de Integridade")
        print("5 - Voltar")

        opcresult=int(input("\nEscolha uma opção: "))

        match opcresult:
            case 1: #OPÇÃO BOLETIM DE URNA
                pass
            case 2: #OPÇÃO ESTATÍSTICA DE COMPARECIMENTO
                pass
            case 3: #OPÇÃO VOTOS POR PARTIDO
                pass 
            case 4: #OPÇÃO VALIDAÇÃO DE INTEGRIDADE
                pass
            case 5: #OPÇÃO INVÁLIDA
                return
            case _: #OPÇÃO INVÁLIDA
                print("Opção Inválida")
                
def validacaoCPF(cpf):
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    stringCPF=str(cpf)
    DV1=0
    digito=0
    for multiplicador in range(10,1,-1):
        DV1+=int(stringCPF[digito])*multiplicador
        digito+=1
    DV1%=11

    if DV1<2:
        if int(stringCPF[9])!= 0:
            return False
    else:
        if int(stringCPF[9]) != 11 - DV1:
            return False
    DV2= 0 
    digito = 0
    for multiplicador in range(11,1,-1):
        DV2+=int(stringCPF[digito])*multiplicador
        digito+=1
    DV2%=11
    if int(stringCPF[10]) != 11 - DV2:
        return False
    
    return True




def opcao_cadastro(): #OPÇÃO CADASTRO
    nome=str(input("Digite seu Nome: "))

    titulo_eleitor=input("Digite seu Título de Eleitor: ")
    
    cpf=int(input("Digite seu CPF, sem : "))
    aprovacao=validacaoCPF(cpf)

    while aprovacao != True:
        print("\n\tErro: O CPF informado não é válido, tente novamente.")
        cpf=int(input("\nDigite seu CPF: "))
        aprovacao=validacaoCPF(cpf)
        

    mesario=str(input("Você atuará como mesário? (sim/nao): "))

    if mesario == "sim":
        mesario=1
        
    else:
        mesario=0

    chave_acesso = gerar_chave_acesso(nome)

    bancoDeDados.inserir_eleitores(nome,titulo_eleitor,cpf,mesario,chave_acesso)


def gerar_chave_acesso(nome): #GERAR CHAVE DE ACESSO

    partes_nome = nome.strip().split()
    if len(partes_nome) < 2:
        raise ValueError("O nome deve conter pelo menos nome e sobrenome.")
    
    primeiro_nome = partes_nome[0]
    segundo_nome = partes_nome[1]

    letras = (
        primeiro_nome[:2].upper() +
        segundo_nome[0].upper()
    )

    numeros = ""
    for _ in range(4):
        numeros += str(random.randint(0, 9))


    chave_acesso = letras + numeros

    return chave_acesso



