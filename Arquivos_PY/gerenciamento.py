import Arquivos_PY.bancoDeDados as bd
import random as r
import Arquivos_PY.validacoes as v
import os


def opcao_gerenciamento(): #OPÇÃO GERENCIAMENTO
    opcao=0
    limpar()
    while opcao != 7:
        print("\n\t-- GERENCIAMENTO --")
        print("\n1 - Cadastro")
        print("2 - Edição de dados")
        print("3 - Remoção de Eleitor")
        print("4 - Busca por Eleitor")
        print("5 - Listagem de Eleitor")
        print("6 - Adicionar Candidato")
        print("7 - Voltar para o Menu Principal")

        opcao=int(input("\nEscolha uma opção: "))

        match opcao:
            case 1: #OPÇÃO CADASTRO
                cadastro_eleitor()
            case 2: #OPÇÃO EDIÇÃO DE DADOS
                edicao_eleitor()
            case 3: #OPÇÃO REMOÇÃO DE ELEITOR
                retirar_eleitor()
            case 4: #OPÇÃO BUSCA POR ELEITOR
                busca_eleitores()
            case 5: #OPÇÃO LISTAGEM DE ELEITOR
                listagem_eleitores()
            case 6: #OPÇÃO ADICIONAR CANDIDATO
                add_candidato()
            case 7: #OPÇÃO VOLTAR PARA O MENU PRINCIPAL
                limpar()
                return
            case _: #OPÇÃO INVÁLIDA
                limpar()

def cadastro_eleitor(): #OPÇÃO CADASTRO
    limpar()
    print("\n\t-- CADASTRANDO ELEITOR --")
    nome=str(input("\nDigite seu Nome: "))
    partes_nome = nome.strip().split()

    while len(partes_nome) < 2:
        limpar()
        print("\n\t-- CADASTRANDO ELEITOR --\n\n*ERRO: O nome deve conter pelo menos nome e sobrenome, tente novamente.")
        nome=str(input("\nDigite seu Nome: "))
        partes_nome = nome.strip().split()
    
    limpar()
    print("\n\t-- CADASTRANDO ELEITOR --")
    titulo=int(input("\nDigite seu Título de Eleitor: "))
    aprovacao=v.validacaoTituloEleitor(titulo)

    while aprovacao != True:
        limpar()
        print("\n\t-- CADASTRANDO ELEITOR --\n\n*ERRO: O Título de Eleitor informado não é válido, tente novamente.")
        titulo=int(input("\nDigite seu Título de eleitor: "))
        aprovacao=v.validacaoTituloEleitor(titulo)
    
    limpar()
    print("\n\t-- CADASTRANDO ELEITOR --")
    cpf=int(input("\nDigite seu CPF, sem pontuação: "))
    aprovacao=v.validacaoCPF(cpf)

    while aprovacao != True:
        limpar()
        print("\n\t-- CADASTRANDO ELEITOR --\n\n*ERRO: O CPF informado não é válido, tente novamente.")
        cpf=int(input("\nDigite seu CPF, sem pontuação: "))
        aprovacao=v.validacaoCPF(cpf)
        
    limpar()
    print("\n\t-- CADASTRANDO ELEITOR --")
    mesario=str(input("\nVocê atuará como mesário? (s/n): "))
    mesario=mesario.lower()
    
    while mesario != "s" and mesario != "n":
        limpar()
        print("\n\t-- CADASTRANDO ELEITOR --\n\n*ERRO: Digite 's' para sim e 'n' para não, tente novamente.")
        mesario=str(input("\nVocê atuará como mesário? (s/n): "))

    if mesario == "s":
        mesario=1
    
    else:
        mesario=0
    
    limpar()
    print("\n\t-- CADASTRO REALIZADO COM SUCESSO!!! --")
    chave_acesso = gerar_chave_acesso(nome)
    print(f"\nSUA CHAVE DE ACESSO É {chave_acesso} ")
    input("\nAperte ENTER para prosseguir...")
    bd.inserir_eleitores(nome,titulo,cpf,mesario,chave_acesso)
    limpar()

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

def edicao_eleitor(): #OPÇÃO QUE POSSIBILITA A MUDANÇA DE INFORMAÇÕES DO ELEITOR
    limpar()
    print("\n\t-- EDIÇÃO DE DADOS DO ELEITOR --")
    chave_acesso=input("\nDigite a chave de acesso do eleitor: ")
    validacao = v.validarChaveAcesso(chave_acesso)

    while validacao == False:
        limpar()
        print("\n\t-- EDIÇÃO DE DADOS DO ELEITOR --\n\n*ERRO: Chave de acesso inexistente, tente novamente.")
        chave_acesso=input("\nDigite a chave de acesso do eleitor: ")
        validacao = v.validarChaveAcesso(chave_acesso)

    limpar()
    print("\n\t-- EDIÇÃO DE DADOS DO ELEITOR --")

    bd.cursor.execute(f"SELECT nome FROM eleitores WHERE chave_acesso = '{chave_acesso}'")

    for nome in bd.cursor.fetchall():
        print(f"\n\t| Usuário encontrado - {nome[0]} |\nSelecione o que você deseja alterar no seu cadastro:\n\n1 - Nome\n2 - CPF\n3 - Título de Eleitor\n4 - Mesário\n5 - Retornar ao menu Gerenciamento")
        opcao=int(input("\nEscolha uma opção: "))
        
        match opcao:
            case 1: #ALTERA O NOME DO ELEITOR
                limpar()
                print("\n\t-- EDIÇÃO DE DADOS DO ELEITOR --")
                alteracao = str(input("\nDigite o novo nome: "))
                
                partes_nome = alteracao.strip().split()
                while len(partes_nome) < 2:
                    limpar()
                    print("\n\t-- EDIÇÃO DE DADOS DO ELEITOR --\n\n*ERRO: O nome deve conter pelo menos nome e sobrenome, tente novamente.")
                    alteracao=str(input("\nDigite seu Nome: "))
                    partes_nome = alteracao.strip().split()

                alteracao_mysql(1 , alteracao, chave_acesso)
                limpar()
                input("\n\t-- EDIÇÃO DE DADOS DO ELEITOR --\n\n*ATUALIZAÇÃO: Nome alterado com sucesso.\n\nAperte ENTER para prosseguir...")
                limpar()

            case 2: # ALTERA O CPF DO ELEITOR 
                limpar()
                print("\n\t-- EDIÇÃO DE DADOS DO ELEITOR --")
                alteracao = int(input("\nDigite o novo CPF: "))
                validacao = v.validacaoCPF(alteracao)
                while validacao == False:
                    limpar()
                    print("\n\t-- EDIÇÃO DE DADOS DO ELEITOR --\n\n*ERRO: Este CPF é inválido ou já está sendo usado, tente novamente.")
                    alteracao = int(input("\nDigite o novo CPF: "))
                    validacao = v.validacaoCPF(alteracao)
                
                alteracao_mysql(2, alteracao, chave_acesso)
                limpar()
                input("\n\t-- EDIÇÃO DE DADOS DO ELEITOR --\n\n*ATUALIZAÇÃO: CPF alterado com sucesso.\n\nAperte ENTER para prosseguir...")
                limpar()

            case 3: # ALTERA O TÍTULO DE ELEITOR
                limpar()
                print("\n\t-- EDIÇÃO DE DADOS DO ELEITOR --")
                alteracao = int(input("\nDigite o novo título de eleitor: "))
                validacao = v.validacaoTituloEleitor(alteracao)
                while validacao == False:
                    limpar()
                    print("\n\t-- EDIÇÃO DE DADOS DO ELEITOR --\n\n*ERRO: Este título de eleitor é inválido ou já está sendo usado, tente novamente.")
                    alteracao = int(input("\nDigite o novo título de eleitor: "))
                    validacao = v.validacaoTituloEleitor(alteracao)
                alteracao_mysql(3, alteracao, chave_acesso)
                limpar()
                input("\n\t-- EDIÇÃO DE DADOS DO ELEITOR --\n\n*ATUALIZAÇÃO: Título de eleitor alterado com sucesso.\n\nAperte ENTER para prosseguir...")
                limpar()

            case 4: #ALTERA A OPÇÃO DE SER MESÁRIO DO ELEITOR
                limpar()
                print("\n\t-- EDIÇÃO DE DADOS DO ELEITOR --")
                alteracao = str(input("\nVocê deseja atuar como mesário? (s/n): "))
                while alteracao != "s" and alteracao != "n":
                    limpar()
                    print("\n\t-- EDIÇÃO DE DADOS DO ELEITOR--\n\n*ERRO: Digite 's' para sim e 'n' para não, tente novamente.")
                    alteracao=str(input("\nVocê deseja atuar como mesário? (s/n): "))
                if alteracao == "s":
                    alteracao = 1
                else:
                    alteracao = 0
                alteracao_mysql(4, alteracao, chave_acesso)
                limpar()
                input("\n\t-- EDIÇÃO DE DADOS DO ELEITOR --\n\n*ATUALIZAÇÃO: Opção Mesário alterado com sucesso.\n\nAperte ENTER para prosseguir...")
                limpar()

            case 5: #VOLTA PARA A ABA GERENCIAMENTO
                limpar()
                opcao_gerenciamento()
            
            case _:
                limpar()

def alteracao_mysql(opc, mudanca, chave_acesso): #FUNÇÃO FEITA PARA FACILITAR A TROCA DE DADOS DO ELEITOR
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

def retirar_eleitor(): # REMOVE CERTO ELEITOR DE UM SISTEMA DE VOTAÇÃO
    limpar()
    print(f"\n\t-- REMOÇÃO ELEITOR --\n")
    chave = input(f"DIGITE A CHAVE DE ACESSO DO ELEITOR: ")
    remocao = bd.removerEleitor(chave)
    while remocao <= 0:
        print("\nELEITOR NÃO ENCONTRADO")
        continuar = input("QUER REALIZAR NOVAMENTE(s/n): ")
        if continuar == "s":
            cpf = input(f"DIGITE O CPF DO ELEITOR: ")
            remocao = bd.remover_eleitor(cpf)
        else:
            input("\nAperte ENTER para continuar...")
            limpar()
            break
    if remocao > 0:
        print("\nELEITOR REMOVIDO COM SUCESSO!")
        input("Aperte ENTER para continuar...")
        limpar()

def busca_eleitores(): #BUSCA OS ELEITORES CADASTRADOS
    limpar()
    print("\n\t-- BUSCA DE ELEITOR --")
    nomeEleitor = input("\nDigite o Nome do eleitor que deseja buscar: ")
    print("")
    resultadoBusca = bd.buscarEleitor(nomeEleitor)
    if resultadoBusca == None:
        print("Mais nenhum eleitor encontrado")
    else:
        print(resultadoBusca)
    input("\nAperte ENTER para continuar...")
    limpar()

def listagem_eleitores(): # FUNÇÃO FEITA PARA LISTAR OS ELEITORES 
    limpar()
    print(f"\n\t-- LISTAGEM DOS ELEITORES --\n")
    bd.listar_usuarios()

    input("\nAperte ENTER para continuar...")
    limpar()

def add_candidato(): # ADICIONA CANDIDATOS AO SISTEMA
    limpar()
    print("\n\t-- CADASTRO DE CANDIDATOS --\n")
    opcao=False
    while opcao==False:
        nomeEleitor=input("Digite seu nome e sobrenome: ")
        opcao=bd.buscar_eleitorCandidato(nomeEleitor)
        if opcao==False:
            print("\n\t*Erro: Você não está cadastrado, faça o cadastro e tente novamente.\n")
        else:
            pass

    limpar()
    print("\n\t-- CADASTRO DE CANDIDATOS --\n")
    nome=input("Digite o nome do candidato: ")
    num_vot=int(input("Digite o número de votação do candidato: "))
    partido=input("Digite o partido do candidato: ")
    bd.inserir_candidato(nome,num_vot,partido)
    limpar()

def limpar(): #LIMPA O TERMINAL PARA MANTER O SISTEMA ORGANIZADO
    os.system('cls' if os.name == 'nt' else 'clear')