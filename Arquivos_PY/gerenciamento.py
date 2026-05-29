import Arquivos_PY.bancoDeDados as bd
import Arquivos_PY.criptografia as c
import Arquivos_PY.descriptografia as d
import Arquivos_PY.validacoes as v
import random as r
import os


def opcao_gerenciamento(): #OPÇÃO GERENCIAMENTO
    opcao=0
    limpar()
    while opcao != 7:
        print("\n\t-- GERENCIAMENTO --")
        print("\n1 - Eleitores")
        print("2 - Candidatos")
        print("3 - Voltar para o Menu Principal")

        opcao=int(input("\nEscolha uma opção: "))

        match opcao:
            case 1: #OPÇÃO CADASTRO
                gerenciamento_eleitor()
            case 2: #OPÇÃO EDIÇÃO DE DADOS
                gerenciamento_candidato()
            case 3: #OPÇÃO VOLTAR PARA O MENU PRINCIPAL
                limpar()
                return
            case _: #OPÇÃO INVÁLIDA
                limpar()

def gerenciamento_eleitor():
    opcao=0
    limpar()
    while opcao != 7:
        print("\n\t-- GERENCIAMENTO DO ELEITOR--")
        print("\n1 - Cadastro")
        print("2 - Edição de dados do Eleitor")
        print("3 - Remoção de Eleitor")
        print("4 - Busca por Eleitor")
        print("5 - Listagem de Eleitor")
        print("6 - Voltar")

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
            case 6: #OPÇÃO VOLTAR PARA O MENU PRINCIPAL
                limpar()
                return
            case _: #OPÇÃO INVÁLIDA
                limpar()
            
def gerenciamento_candidato():
    opcao=0
    limpar()
    while opcao != 7:
        print("\n\t-- GERENCIAMENTO DO CANDIDATO --")
        print("\n1 - Adicionar Candidato")
        print("2 - Remoção de Candidatos")
        print("3 - Busca de Candidatos")
        print("4 - Listagem de Candidatos")
        print("5 - Voltar")

        opcao=int(input("\nEscolha uma opção: "))

        match opcao:
            case 1: #OPÇÃO ADICIONAR CANDIDATO
                add_candidato()
            case 2:
                remocao_candidato()
            case 3:
                buscar_candidato()
            case 4:
                list_candidatos()
            case 5: #OPÇÃO VOLTAR PARA O MENU PRINCIPAL
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

    bd.cursor.execute(f"SELECT id_eleitor FROM eleitores WHERE titulo_eleitor = {titulo}")
    resultado = bd.cursor.fetchone()
    if resultado:
        aprovacao = False
    else:
        aprovacao=v.validacaoTituloEleitor(titulo)

    while aprovacao != True:
        limpar()
        print("\n\t-- CADASTRANDO ELEITOR --\n\n*ERRO: O Título de Eleitor informado não é válido, tente novamente.")
        titulo=int(input("\nDigite seu Título de eleitor: "))
        bd.cursor.execute(f"SELECT id_eleitor FROM eleitores WHERE titulo_eleitor = {titulo}")
        resultado = bd.cursor.fetchone()
        if resultado:
            aprovacao = False
        else:
            aprovacao=v.validacaoTituloEleitor(titulo)
    
    limpar()
    print("\n\t-- CADASTRANDO ELEITOR --")
    cpf=int(input("\nDigite seu CPF, sem pontuação: "))

    cpf_crip=c.criptografia(0,cpf)
    bd.cursor.execute(f"SELECT id_eleitor FROM eleitores WHERE cpf = '{cpf_crip}'")
    resultado = bd.cursor.fetchone()
    if resultado:
        aprovacao=False
    else:
        aprovacao=v.validacaoCPF(cpf)

    while aprovacao != True:
        limpar()
        print("\n\t-- CADASTRANDO ELEITOR --\n\n*ERRO: O CPF informado não é válido, tente novamente.")
        cpf=int(input("\nDigite seu CPF, sem pontuação: "))
        bd.cursor.execute(f"SELECT id_eleitor FROM eleitores WHERE cpf = '{cpf}'")
        resultado = bd.cursor.fetchone()
        if resultado:
            aprovacao=False
        else:
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
    print("\n\t-- CADASTRO ELEITOR --")
    chave_acesso = gerar_chave_acesso(nome)
    print("\n*ATUALIZAÇÃO: Cadastro realizado com sucesso.")
    print(f"\nSua chave de acesso é {chave_acesso}.")

    cpf = c.criptografia(0,cpf)
    chave_acesso = c.criptografia(1,chave_acesso)

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

    chave_acesso = c.criptografia(1,chave_acesso)
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
                validacao = False
                while validacao == False:
                    limpar()
                    print("\n\t-- EDIÇÃO DE DADOS DO ELEITOR --")
                    cpf_novo = int(input("\nDigite o novo CPF: "))

                    while len(str(cpf_novo)) != 11:
                        limpar()
                        print("\n\t-- EDIÇÃO DE DADOS DO ELEITOR --")
                        print("\n*ERRO: O CPF precisa conter 11 dígitos.")
                        cpf_novo = int(input("\nDigite o novo CPF: "))

                    cpf_crip = c.criptografia(0, cpf_novo)
                    bd.cursor.execute(f"SELECT id_eleitor FROM eleitores WHERE cpf = '{cpf_crip}'")
                    resultado = bd.cursor.fetchone()

                    if resultado:
                        limpar()
                        print("\n\t-- EDIÇÃO DE DADOS DO ELEITOR --")
                        print("\n*ERRO: Este CPF já está sendo usado.")
                        input("\nPressione Enter para tentar novamente...")
                        continue

                    else:
                        validacao = v.validacaoCPF(cpf_novo)
                        if validacao == False:
                            print("\n*ERRO: Este CPF é inválido.")
                            input("\nPressione Enter para tentar novamente...")
                            continue
                            
                alteracao_mysql(2, cpf_crip, chave_acesso)
                limpar()
                input("\n\t-- EDIÇÃO DE DADOS DO ELEITOR --\n\n*ATUALIZAÇÃO: CPF alterado com sucesso.\n\nAperte ENTER para prosseguir...")
                limpar()

            case 3: # ALTERA O TÍTULO DE ELEITOR
                limpar()
                print("\n\t-- EDIÇÃO DE DADOS DO ELEITOR --")
                alteracao = int(input("\nDigite o novo título de eleitor: "))

                bd.cursor.execute(f"SELECT id_eleitor FROM eleitores WHERE titulo_eleitor = {alteracao}")
                resultado = bd.cursor.fetchone() 
                if resultado:
                    validacao = False
                else:
                    validacao=v.validacaoTituloEleitor(alteracao)

                while validacao == False:
                    limpar()
                    print("\n\t-- EDIÇÃO DE DADOS DO ELEITOR --\n\n*ERRO: Este título de eleitor é inválido ou já está sendo usado, tente novamente.")
                    alteracao = int(input("\nDigite o novo título de eleitor: "))

                    bd.cursor.execute(f"SELECT id_eleitor FROM eleitores WHERE titulo_eleitor = {alteracao}")
                    resultado = bd.cursor.fetchone() 
                    if resultado:
                        validacao = False
                    else:
                        validacao=v.validacaoTituloEleitor(alteracao)

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
    remocao=False
    while remocao == False:
        print(f"\n\t-- REMOÇÃO ELEITOR --\n")
        chave = input(f"Digite a chave de acesso do eleitor: ")
        chave = c.criptografia(1,chave)
        remocao = bd.removerEleitor(chave)
        while remocao <= 0:
            limpar()
            print(f"\n\t-- REMOÇÃO ELEITOR --")
            print("\n*ERRO: Eleitor não encontrado.")
            continuar = input("\nDeseja tentar novamente? (s/n): ")
            continuar=continuar.lower()
            while continuar != "s" and continuar != "n":
                limpar()
                print(f"\n\t-- REMOÇÃO ELEITOR --\n\n*ERRO: Digite 's' para sim e 'n' para não, tente novamente.")
                print("\n*ERRO: Eleitor não encontrado.")
                continuar = input("\nDeseja tentar novamente? (s/n): ")
                continuar = continuar.lower()
                                
            if continuar == "s":
                retirar_eleitor() 
            else:
                remocao=True
    
        if remocao > 0:
            print("\n*ATUALIZAÇÃO: Eleitor removido com sucesso.")
            remocao = True
            
    input("Aperte ENTER para continuar...")
    return

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
    nome=input("Digite o nome do candidato: ")

    limpar()
    print("\n\t-- CADASTRO DE CANDIDATOS --\n")
    num_vot=int(input("Digite o número de votação do candidato: "))
    bd.cursor.execute(f"SELECT id_candidato FROM candidatos WHERE num_votacao = {num_vot}")
    resultado=bd.cursor.fetchone()
    while len(str(num_vot)) != 2 or resultado:
        limpar()
        print("\n\t-- CADASTRO DE CANDIDATOS --")
        print("\n*ERRO: Número de votação inválida, tente novamente.")
        num_vot=int(input("\nDigite o número de votação do candidato: "))
        bd.cursor.execute(f"SELECT id_candidato FROM candidatos WHERE num_votacao = {num_vot}")
        resultado=bd.cursor.fetchone()

    limpar()
    print("\n\t-- CADASTRO DE CANDIDATOS --\n")
    partido=input("Digite o partido do candidato: ")
    bd.inserir_candidato(nome,num_vot,partido)

    limpar()
    print("\n\t-- CADASTRO DE CANDIDATOS --\n")
    input("*ATUALIZAÇÃO: O candidato foi cadastrado com sucesso!\n\nAperte ENTER para retornar...")
    limpar()

def limpar(): #LIMPA O TERMINAL PARA MANTER O SISTEMA ORGANIZADO
    os.system('cls' if os.name == 'nt' else 'clear')

def list_candidatos(): 
    limpar()
    bd.cursor.execute("SELECT id_candidato, nome, partido, num_votacao FROM candidatos")
    resultado=bd.cursor.fetchall()

    print("\n\t-- Lista de Candidatos --\n")

    for candidato in resultado:
        if candidato[1] != 'Voto Nulo':
            print(f"Nome: {candidato [1]} | Partido: {candidato[2]} | Número: {candidato[3]}")
    
    input("\nAperte ENTER para retornar...")
    opcao_gerenciamento()

def buscar_candidato():
    limpar()
    print("\n\t-- BUSCA DE CANDIDATOS --")
    numero=int(input("\nDigite o número da votação: "))

    bd.cursor.execute(f"SELECT nome, partido FROM candidatos WHERE num_votacao = {numero}")

    resultado=bd.cursor.fetchall()

    limpar()
    print("\n\t-- BUSCA DE CANDIDATOS --\n")

    if resultado:
        for nome, partido in resultado:
            print(f"Nome: {nome} | Partido: {partido}")
            
    else:
        print("Candidato não encontrado.")

    input("\nAperte ENTER para retornar...")
    opcao_gerenciamento()

def remocao_candidato():
    limpar()
    print("\n\t-- REMOÇÃO DE CANDIDATOS --")
    num_candidato = input("\nDigite o número do candidato que deseja deletar: ")
    confirmacao = input(f"Tem certeza que deseja deletar o candidato nº {num_candidato}? (s/n): ")
    confirmacao = confirmacao.lower()

    while confirmacao != "s" and confirmacao != "n":
        limpar()
        print("\n\t-- REMOÇÃO DE CANDIDATOS --\n\n*ERRO: Digite 's' para sim e 'n' para não, tente novamente.")
        num_candidato = input("\nDigite o número do candidato que deseja deletar: ")
        confirmacao = input(f"Tem certeza que deseja deletar o candidato nº {num_candidato}? (s/n): ")

    if confirmacao == "s": 
        limpar()
        print("\n\t-- REMOÇÃO DE CANDIDATOS --")
        input("\nCandidato removido com sucesso!\n\nAperte ENTER para retornar...")
        bd.cursor.execute(f"DELETE FROM candidatos WHERE num_votacao = {num_candidato}")
        bd.conexao.commit()
        limpar()
        opcao_gerenciamento()

    if confirmacao == "n":
        limpar()
        print("\n\t-- REMOÇÃO DE CANDIDATOS --")
        input("\nOperação cancelada!\n\nAperte ENTER para retornar...")
        limpar()
        opcao_gerenciamento()

