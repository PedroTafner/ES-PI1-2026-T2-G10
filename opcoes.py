import bancoDeDados as bd
import random as r
import validacoes as v
import os

def opcao_gerenciamento(): #OPÇÃO GERENCIAMENTO
    opcger=0
    limpar()
    while opcger != 6:
        print("\n\t-- GERENCIAMENTO --")
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
                editarEleitor()
            case 3: #OPÇÃO REMOÇÃO DE ELEITOR
                pass
            case 4: #OPÇÃO BUSCA POR ELEITOR
                buscaEleitores()
            case 5: #OPÇÃO LISTAGEM DE ELEITOR
                pass
            case 6: #OPÇÃO VOLTAR PARA O MENU PRINCIPAL
                limpar()
                return
            case _: #OPÇÃO INVÁLIDA
                limpar()

def opcao_votacao(): #OPÇÃO VOTAÇÃO
    limpar()
    opcvot=0
    while opcvot != 4:
        print("\n\t-- VOTAÇÃO --")
        print("\n1 - Abrir Sistema de Votação")
        print("2 - Auditoria do Sistema de Votação")
        print("3 - Resultado da Votação")
        print("4 - Voltar para o Menu Principal")

        opcvot=int(input("\nEscolha uma opção: "))
        match opcvot:
            case 1: #OPÇÃO ABRIR SISTEMA DE VOTAÇÃO
                abrirSistemaVotacao()
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
        print("\n\t-- SISTEMA DE VOTAÇÃO --")
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
        print("\n\t-- AUDITORIA DO SISTEMA DE VOTAÇÃO --")
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
        print("\n\t-- RESULTADO DA VOTAÇÃO --")
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
                
def opcao_cadastro(): #OPÇÃO CADASTRO
    limpar()
    print("\n\t-- CADASTRANDO ELEITOR --")
    nome=str(input("\nDigite seu Nome: "))
    partes_nome = nome.strip().split()

    while len(partes_nome) < 2:
        print("\n\tErro: O nome deve conter pelo menos nome e sobrenome, tente novamente.")
        nome=str(input("Digite seu Nome: "))
        partes_nome = nome.strip().split()
    

    titulo_eleitor=int(input("Digite seu Título de Eleitor: "))
    aprovacao_titulo=v.validacaoTituloEleitor(titulo_eleitor)

    while aprovacao_titulo != True:
        print("\n\tErro: O Título de Eleitor informado não é válido, tente novamente.")
        titulo_eleitor=int(input("\nDigite seu Título de eleitor: "))
        aprovacao_titulo=v.validacaoTituloEleitor(titulo_eleitor)
    
    cpf=int(input("Digite seu CPF, sem pontuação: "))
    aprovacao_CPF=v.validacaoCPF(cpf)

    while aprovacao_CPF != True:
        print("\n\tErro: O CPF informado não é válido, tente novamente.")
        cpf=int(input("\nDigite seu CPF, sem pontuação: "))
        aprovacao_CPF=v.validacaoCPF(cpf)
        

    mesario=str(input("Você atuará como mesário? (s/n): "))
    mesario=mesario.lower()
    
    while mesario != "s" and mesario != "n":
        print("\n\tErro: Digite 's' para sim e 'n' para não, tente novamente.")
        mesario=str(input("Você atuará como mesário? (s/n): "))

    if mesario == "s":
        mesario=1
    else:
        mesario=0
    print("----------------------------------------------")
    print("\n\tCADASTRO REALIZADO COM SUCESSO!!!")


    chave_acesso = gerar_chave_acesso(nome)
    print(f"\n\tSUA CHAVE DE ACESSO É {chave_acesso} ")
    print("\n-----------------------------------------------")
    bd.inserir_eleitores(nome,titulo_eleitor,cpf,mesario,chave_acesso)

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
        numeros += str(r.randint(0, 9))


    chave_acesso = letras + numeros

    return chave_acesso

def buscaEleitores(): #BUSCA OS ELEITORES CADASTRADOS
    limpar()
    print("\n\t-- BUSCA DE ELEITOR --")
    nomeEleitor = input("Digite o Nome do eleitor que deseja buscar: ")
    resultadoBusca = bd.buscarEleitor(nomeEleitor)
    if resultadoBusca == None:
        print("Mais nenhum eleitor encontrado")
    else:
        print(resultadoBusca)

def abrirSistemaVotacao():
    validacao=False
    while validacao != True:
        titulo_eleitor=int(input("Digite seu título de eleitor: "))
        valTitulo=v.validacaoTituloEleitor(titulo_eleitor)
        while valTitulo != True:
            print("\n\tErro! Título de eleitor inválido, digite novamente.\n")
            titulo_eleitor=int(input("Digite seu título de eleitor: "))
            valTitulo=v.validacaoTituloEleitor(titulo_eleitor)
        cpf=int(input("Digite os 4 primeiros dígitos do seu CPF: "))
        while len(str(cpf))<4 or len(str(cpf))>4:
            print("\n\tErro! Digite os 4 primeiros caracteres do seu CPF, tente novamente.\n")
            cpf=int(input("Digite os 4 primeiros dígitos do seu CPF: "))
        chave=input("Digite a sua chave de acesso: ")
        while len(str(chave))<7 or len(str(chave))>7:
            print("\n\tErro! A chave de acesso precisa ter 7 valores, tente novamente.\n")
            chave=input("Digite a sua chave de acesso: ")
        validacao=bd.validarEleitor(titulo_eleitor,chave,cpf)
        if validacao == True:
            opcao_abrirSistemaVotacao()
        else:
            return
    
def mudandoDados(opc, mudanca, chave_acesso): #FUNÇÃO FEITA PARA FACILITAR A TROCA DE DADOS NO EDITARELEITOR
    match opc:
        case 1: #nome
            bd.cursor.execute(f"UPDATE eleitores SET nome = '{mudanca}' WHERE chave_acesso = '{chave_acesso}'")
            bd.conexao.commit()
        case 2: #cpf
            bd.cursor.execute(f"UPDATE eleitores SET cpf = {mudanca} WHERE chave_acesso = '{chave_acesso}'")
            bd.conexao.commit()
        case 3: #titulo
            bd.cursor.execute(f"UPDATE eleitores SET titulo_eleitor = {mudanca} WHERE chave_acesso = '{chave_acesso}'")
            bd.conexao.commit()
        case 4: #mesario
            bd.cursor.execute(f"UPDATE eleitores SET mesario = {mudanca} WHERE chave_acesso = '{chave_acesso}'")
            bd.conexao.commit()

def editarEleitor(): #OPÇÃO QUE POSSIBILITA A MUDANÇA DE INFORMAÇÕES DO ELEITOR
    limpar()
    print("\n\t-- EDIÇÃO DE DADOS DO ELEITOR --")
    chave_acesso=input("\nDigite a chave de acesso do eleitor: ")
    validacao = v.validarChaveAcesso(chave_acesso)

    while validacao == False:
        print("*ERRO: Chave de acesso inexistente, tente novamente.")
        chave_acesso=input("\nDigite a chave de acesso do eleitor: ")
        validacao = v.validarChaveAcesso(chave_acesso)

    limpar()
    print("\n\t-- EDIÇÃO DE DADOS DO ELEITOR --")

    bd.cursor.execute(f"SELECT nome FROM eleitores WHERE chave_acesso = '{chave_acesso}'")

    for nome in bd.cursor.fetchall():
        print(f"\n\t| Usuário encontrado - {nome[0]} |\nSelecione o que você deseja alterar no seu cadastro:\n\n1 - Nome\n2 - CPF\n3 - Título de Eleitor\n4 - Mesário\n5 - Retornar ao menu Gerenciamento")
        opcao=int(input("\nEscolha uma opção: "))
        
        match opcao:
            case 1:
                limpar()
                print("\n\t-- ALTERANDO NOME --")
                alteracao = str(input("\n\nDigite o novo nome: "))
                mudandoDados(1 , alteracao, chave_acesso)
                input("*ATUALIZAÇÃO: Nome alterado com sucesso.\n\nAperte ENTER para prosseguir...")
                limpar()

            case 2: 
                limpar()
                print("\n\t-- ALTERANDO CPF --")
                alteracao = int(input("\nDigite o novo CPF: "))
                validacao = v.validacaoCPF(alteracao)
                while validacao == False:
                    limpar()
                    print("\n\t-- ALTERANDO CPF --\n\n*ERRO: Este CPF é inválido ou já está sendo usado, tente novamente.")
                    alteracao = int(input("\nDigite o novo CPF: "))
                    validacao = v.validacaoCPF(alteracao)
                mudandoDados(2, alteracao, chave_acesso)
                input("*ATUALIZAÇÃO: CPF alterado com sucesso.\n\nAperte ENTER para prosseguir...")
                limpar()

            case 3:
                limpar()
                print("\n\t-- ALTERANDO TÍTULO DE ELEITOR --")
                alteracao = int(input("\n\nDigite o novo título de eleitor: "))
                validacao = v.validacaoTituloEleitor(alteracao)
                while validacao == False:
                    print("*ERRO: Este título de eleitor é inválido ou já está sendo usado, tente novamente.")
                    alteracao = int(input("\nDigite o novo título de eleitor: "))
                    validacao = v.validacaoTituloEleitor(alteracao)
                mudandoDados(3, alteracao, chave_acesso)
                input("*ATUALIZAÇÃO: Título de eleitor alterado com sucesso.\n\nAperte ENTER para prosseguir...")
                limpar()

            case 4:
                limpar()
                print("\n\t-- ALTERANDO OPÇÃO MESÁRIO --")
                alteracao = str(input("\n\nVocê deseja atuar como mesário? (s/n): "))
                while alteracao != "s" and alteracao != "n":
                    print("*ERRO: Digite 's' para sim e 'n' para não, tente novamente.")
                    alteracao=str(input("\nVocê deseja atuar como mesário? (s/n): "))
                if alteracao == "s":
                    alteracao = 1
                else:
                    alteracao = 0
                mudandoDados(4, alteracao, chave_acesso)
                input("*ATUALIZAÇÃO: Opção Mesário alterado com sucesso.\n\nAperte ENTER para prosseguir...")
                limpar()

            case 5:
                limpar()
                opcao_gerenciamento()
            
            case _:
                limpar()
    
def limpar(): #LIMPA O TERMINAL PARA MANTER O SISTEMA ORGANIZADO
    os.system('cls' if os.name == 'nt' else 'clear')