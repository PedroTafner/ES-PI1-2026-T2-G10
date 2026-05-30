import Arquivos_PY.bancoDeDados as bd
import Arquivos_PY.criptografia as c
import Arquivos_PY.descriptografia as d
import Arquivos_PY.validacoes as v
import random as r
import os


def opcao_gerenciamento(): 

    """
    Exibe o menu base de gerenciamento para gerenciar 
    eleitores ou candidatos.

    Args:
        Não recebe parâmetros.

    Returns:
        Nenhum valor retornado (None).
    """

    opcao=0
    limpar()
    while opcao != 7:
        print("\n\t-- GERENCIAMENTO --")
        print("\n1 - Eleitores")
        print("2 - Candidatos")
        print("3 - Voltar para o Menu Principal")

        opcao=int(input("\nEscolha uma opção: "))

        match opcao:
            case 1: # OPÇÃO PARA GERENCIAR INFORMAÇÕES DOS ELEITORES
                gerenciamento_eleitor()

            case 2: #OPÇÃO PARA GERENCIAR INFORMAÇÕES DOS CANDIDATOS
                gerenciamento_candidato()

            case 3: #OPÇÃO VOLTAR PARA O MENU PRINCIPAL
                limpar()
                return
            
            case _: #OPÇÃO INVÁLIDA
                limpar()

def gerenciamento_eleitor(): 
    
    """
    Menu central para cadastro, edição, remoção, busca e listagem de eleitores.

    Args:
        Não recebe parâmetros.

    Returns:
        Nenhum valor retornado (None).
    """

    opcao=0
    limpar()
    while opcao != 7:
        print("\n\t-- GERENCIAMENTO DO ELEITOR --")
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

            case 2: #OPÇÃO EDIÇÃO DE DADOS DO ELEITOR
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
    
    """
    Menu central para cadastro, remoção, busca e listagem de candidatos.

    Args:
        Não recebe parâmetros.

    Returns:
        Nenhum valor retornado (None).
    """

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
            case 1: # OPÇÃO ADICIONAR CANDIDATO
                add_candidato()

            case 2: # OPÇÃO DE REMOÇÃO DO CANDIDATO
                remocao_candidato()

            case 3: # OPÇÃO DE BUSCA DE CANDIDATOS
                buscar_candidato()

            case 4: # OPÇÃO DE LISTAGEM DE TODOS OS CANDIDATOS REGISTRADOS
                list_candidatos()

            case 5: #OPÇÃO VOLTAR PARA O MENU GERENCIAMENTO
                limpar()
                return
            
            case _: #OPÇÃO INVÁLIDA
                limpar()

def cadastro_eleitor(): 
    
    """
    Cadastra um eleitor, requisitando informações, 
    aplicando as validações de Título e CPF 
    e gerando a chave de acesso criptografada.

    Args:
        Não recebe parâmetros.

    Returns:
        Nenhum valor retornado (None).
    """

    limpar()
    print("\n\t-- CADASTRANDO ELEITOR --")
    nome=str(input("\nDigite seu Nome: "))
    partes_nome = nome.strip().split()

    # 1. NOME
    while len(partes_nome) < 2: # CASO NÃO TENHA 2 NOMES OU NOME E SOBRENOME, QUE É NECESSÁRIO PARA A FORMAÇÃO DA CHAVE DE ACESSO, DA ERRO E PEDE DENOVO
        limpar()
        print("\n\t-- CADASTRANDO ELEITOR --\n\n*ERRO: O nome deve conter pelo menos nome e sobrenome, tente novamente.")
        nome=str(input("\nDigite seu Nome: "))
        partes_nome = nome.strip().split()
    
    # 2. TITULO DE ELEITOR
    limpar()
    print("\n\t-- CADASTRANDO ELEITOR --")
    titulo=int(input("\nDigite seu Título de Eleitor: "))

    bd.cursor.execute(f"SELECT id_eleitor FROM eleitores WHERE titulo_eleitor = {titulo}") # VERIFICA SE O TITULO DE ELEITOR NÃO ESTÁ SENDO USADO POR OUTRA PESSOA
    resultado = bd.cursor.fetchall()
    
    if resultado:
        aprovacao = False
    else:
        aprovacao=v.validacaoTituloEleitor(titulo) # FAZ A VALIDAÇÃO DO TÍTULO DE ELEITOR

    while aprovacao != True: # CASO O TÍTULO NÃO SEJA VÁLIDO É PEDIDO NOVAMENTE
        limpar()
        print("\n\t-- CADASTRANDO ELEITOR --\n\n*ERRO: O Título de Eleitor informado não é válido, tente novamente.")
        titulo=int(input("\nDigite seu Título de eleitor: "))
        bd.cursor.execute(f"SELECT id_eleitor FROM eleitores WHERE titulo_eleitor = {titulo}")
        resultado = bd.cursor.fetchone()
        if resultado:
            aprovacao = False
        else:
            aprovacao=v.validacaoTituloEleitor(titulo)
    
    # 3. CPF
    limpar()
    print("\n\t-- CADASTRANDO ELEITOR --")
    cpf=int(input("\nDigite seu CPF, sem pontuação: "))

    if len(str(cpf)) != 11:
        aprovacao = False
    else:
        cpf_crip=c.criptografia(0,cpf)
        bd.cursor.execute(f"SELECT id_eleitor FROM eleitores WHERE cpf = '{cpf_crip}'") # VERIFICA SE O CPF NÃO ESTÁ SENDO USADO
        resultado = bd.cursor.fetchone()
        if resultado:
            aprovacao=False
        else:
            aprovacao=v.validacaoCPF(cpf) # CASO NÃO, FAZ A SUA VALIDAÇÃO

    while aprovacao != True: # CASO SIM, INFORMA O ERRO E PEDE DENOVO
        limpar()
        print("\n\t-- CADASTRANDO ELEITOR --\n\n*ERRO: O CPF informado não é válido, tente novamente.")
        cpf=int(input("\nDigite seu CPF, sem pontuação: "))
        if len(str(cpf)) != 11:
            aprovacao = False
        else:
            cpf = c.criptografia(0,cpf)
            bd.cursor.execute(f"SELECT id_eleitor FROM eleitores WHERE cpf = '{cpf}'")
            resultado = bd.cursor.fetchone()
            cpf = d.descriptografia(0,cpf)
            if resultado:
                aprovacao=False
            else:
                aprovacao=v.validacaoCPF(cpf)
        
    # 4. Mesário
    limpar()
    print("\n\t-- CADASTRANDO ELEITOR --")
    mesario=str(input("\nVocê atuará como mesário? (s/n): ")) # PERGUNTA SE O ELEITOR QUER SER MESÁRIO OU NÃO
    mesario=mesario.lower()
    
    while mesario != "s" and mesario != "n": # CASO O USUÁRIO NÃO RESPONDA CORRETAMENTE, UM ERRO APARECE E A PERGUNTA É REPETIDA
        limpar()
        print("\n\t-- CADASTRANDO ELEITOR --\n\n*ERRO: Digite 's' para sim e 'n' para não, tente novamente.")
        mesario=str(input("\nVocê atuará como mesário? (s/n): "))

    if mesario == "s":
        mesario=1
    
    else:
        mesario=0
    
    limpar()
    print("\n\t-- CADASTRO ELEITOR --")
    chave_acesso = gerar_chave_acesso(nome) # GERA A CHAVE DE ACESSO
    print(f"\nSua chave de acesso é {chave_acesso}.")
    print("*ATUALIZAÇÃO: Cadastro realizado com sucesso.")

    cpf = c.criptografia(0,cpf) # CRIPTOGRAFA O CPF
    chave_acesso = c.criptografia(1,chave_acesso) # CRIPTOGRAFA A CHAVE DE ACESSO

    input("\nAperte ENTER para prosseguir...")
    bd.inserir_eleitores(nome,titulo,cpf,mesario,chave_acesso) # INSERE TUDO NO BANCO DE DADOS
    limpar()

def gerar_chave_acesso(nome): 

    """
    Gera uma chave de acesso de 7 caracteres para o eleitor.
    Regra: 2 primeiras letras do nome + 1 primeira letra do sobrenome + 4 dígitos aleatórios.

    Args:
        nome (str): O nome completo do eleitor recém-cadastrado.

    Returns:
        str: A chave de acesso estruturada gerada.
    """

    partes_nome = nome.strip().split() # DIVIDE O NOME EM PARTES

    if len(partes_nome) < 2: # CASO NÃO TENHA 2 NOMES OU NOME+SOBRENOME, UM ERRO É GERADO
        raise ValueError("O nome deve conter pelo menos nome e sobrenome.")
    
    primeiro_nome = partes_nome[0] # PRIMEIRO NOME
    segundo_nome = partes_nome[1] # SEGUNDO NOME OU SOBRENOME

    # GERANDO A CHAVE DE ACESSO DE ACORDO COM OS REQUISITOS
    letras = (
        primeiro_nome[:2].upper() +
        segundo_nome[0].upper()
    )

    numeros = ""
    for _ in range(4):
        numeros += str(r.randint(0, 9))

    # FORMAÇÃO DA CHAVE DE ACESSO
    chave_acesso = letras + numeros

    return chave_acesso

def edicao_eleitor(): 

    """
    Acessa o cadastro de um eleitor através de sua chave de acesso, 
    permitindo edições nos dados pessoais e validando novamente qualquer modificação.

    Args:
        Não recebe parâmetros.

    Returns:
        Nenhum valor retornado (None).
    """

    limpar()
    print("\n\t-- EDIÇÃO DE DADOS DO ELEITOR --")

    permicao = verificacao_existencia(0)

    if permicao == True:
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
                            input("\nPressione Enter para retornar...")
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
                    alteracao=alteracao.lower()

                    while alteracao != "s" and alteracao != "n":
                        limpar()
                        print("\n\t-- EDIÇÃO DE DADOS DO ELEITOR--\n\n*ERRO: Digite 's' para sim e 'n' para não, tente novamente.")
                        alteracao=str(input("\nVocê deseja atuar como mesário? (s/n): "))
                        alteracao=alteracao.lower()

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
    else:
        input("\n*ERRO: Não há eleitores cadastrados.\n\nAperte ENTER para retornar...")
        limpar()
        return

def alteracao_mysql(opc, mudanca, chave_acesso): 

    """
    Função de facilitar a atualização de dados no banco 

    Args:
        opc (int): Identificador numérico da coluna que vai ser alterada (1: Nome, 2: CPF, 3: Título, 4: Mesário).
        mudanca (str/int): O novo valor que será inserido na tabela.
        chave_acesso (str): A chave criptografada usada para filtrar o eleitor.

    Returns:
        Nenhum valor retornado (None).
    """

    match opc:
        case 1: #nome
            bd.cursor.execute(f"UPDATE eleitores SET nome = '{mudanca}' WHERE chave_acesso = '{chave_acesso}'")
            bd.conexao.commit()
        case 2: #cpf
            bd.cursor.execute(f"UPDATE eleitores SET cpf = '{mudanca}' WHERE chave_acesso = '{chave_acesso}'")
            bd.conexao.commit()
        case 3: #titulo
            bd.cursor.execute(f"UPDATE eleitores SET titulo_eleitor = {mudanca} WHERE chave_acesso = '{chave_acesso}'")
            bd.conexao.commit()
        case 4: #mesario
            bd.cursor.execute(f"UPDATE eleitores SET mesario = {mudanca} WHERE chave_acesso = '{chave_acesso}'")
            bd.conexao.commit()

def retirar_eleitor(): 

    """
    Remove o cadastro de um eleitor do banco de dados.

    Args:
        Não recebe parâmetros.

    Returns:
        Nenhum valor retornado (None).
    """

    limpar()
    remocao=False
    print(f"\n\t-- REMOÇÃO ELEITOR --\n")

    permicao = verificacao_existencia(0)

    if permicao == True:
        while remocao == False:
            chave = input(f"Digite a chave de acesso do eleitor: ")
            chave = c.criptografia(1,chave)
            remocao = bd.removerEleitor(chave)

            if remocao <= 0:
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
                    limpar()
                    continue
                else:
                    input("\nAperte ENTER para retornar...")
                    limpar()
                    return
        
            else:
                limpar()
                print(f"\n\t-- REMOÇÃO ELEITOR --")
                print("\n*ATUALIZAÇÃO: Eleitor removido com sucesso.\n")
                remocao = True
                
        input("Aperte ENTER para continuar...")
        limpar()
        return
    
    else:
        input("*ERRO: Não há eleitores cadastrados.\n\nAperte ENTER para retornar...")
        limpar()
        return

def busca_eleitores(): 

    """
    Busca por nome os eleitores presentes na base de dados.

    Args:
        Não recebe parâmetros.

    Returns:
        Nenhum valor retornado (None).
    """

    limpar()
    print("\n\t-- BUSCA DE ELEITOR --")

    permicao = verificacao_existencia(0)

    if permicao == True: # CASO SIM, INICIA A BUSCA
        nomeEleitor = input("\nDigite o Nome do eleitor que deseja buscar: ")
        print("")
        resultadoBusca = bd.buscarEleitor(nomeEleitor) # BUSCA NO BANCO DE DADOS TODOS OS ELEITORES COM O NOME DADO

        if resultadoBusca == None: # SE NÃO HOUVER NENHUM 
            print("Mais nenhum eleitor encontrado")

        else:
            print(resultadoBusca) # CASO TENHA
    
    else: # CASO NÃO, AVISA
        print("\n*ERRO: Não há eleitores registrados.")

    input("\nAperte ENTER para continuar...")
    limpar()

def listagem_eleitores(): 
    
    """
    Exibe a listagem de todos os eleitores cadastrados.

    Args:
        Não recebe parâmetros.

    Returns:
        Nenhum valor retornado (None).
    """

    limpar()
    print(f"\n\t-- LISTAGEM DOS ELEITORES --\n")

    permicao = verificacao_existencia(0)

    if permicao == True:
        bd.listar_usuarios() # FUNÇÃO QUE LISTA TODOS OS ELEITORES NO BANCO DE DADOS

    else:
        print("*ERRO: Não há eleitores cadastrados.")
    input("\nAperte ENTER para continuar...")
    limpar()

def add_candidato(): 
    
    """
    Registra um novo candidato eleitoral, incluindo verificação 
    de unicidade do número de votação.

    Args:
        Não recebe parâmetros.

    Returns:
        Nenhum valor retornado (None).
    """

    limpar()
    
    print("\n\t-- CADASTRO DE CANDIDATOS --\n")
    nome=input("Digite o nome do candidato: ")

    limpar()
    print("\n\t-- CADASTRO DE CANDIDATOS --\n")
    num_vot=int(input("Digite o número de votação do candidato: "))
    bd.cursor.execute(f"SELECT id_candidato FROM candidatos WHERE num_votacao = {num_vot}") # VERIFICA SE O NÚMERO DE VOTAÇÃO JÁ ESTÁ SENDO USADO OU NÃO
    resultado=bd.cursor.fetchone()

    while resultado: # SE O NÚMERO DE VOTAÇÃO ESTIVER SENDO USADO APARECE UM ERRO E PEDE NOVAMENTE UM NÚMERO
        limpar()
        print("\n\t-- CADASTRO DE CANDIDATOS --")
        print("\n*ERRO: Número de votação em uso, tente novamente.")
        num_vot=int(input("\nDigite o número de votação do candidato: "))
        bd.cursor.execute(f"SELECT id_candidato FROM candidatos WHERE num_votacao = {num_vot}")
        resultado=bd.cursor.fetchone()

    limpar()
    print("\n\t-- CADASTRO DE CANDIDATOS --\n")
    partido=input("Digite o partido do candidato: ")
    bd.inserir_candidato(nome,num_vot,partido) # CADASTRA NO BANCO DE DADOS O NOME DO CANDIDATO, O SEU NÚMERO E PARTIDO

    limpar()
    print("\n\t-- CADASTRO DE CANDIDATOS --\n")
    input("*ATUALIZAÇÃO: O candidato foi cadastrado com sucesso!\n\nAperte ENTER para retornar...")
    limpar()

def limpar():
    
    """
    Limpa as mensagens do terminal para a organização visual do sistema.

    Args:
        Não recebe parâmetros de entrada.

    Returns:
        Nenhum valor é retornado (None).
    """

    os.system('cls' if os.name == 'nt' else 'clear')

def list_candidatos(): 

    """
    Exibe a listagem de todos os candidatos cadastrados.

    Args:
        Não recebe parâmetros.

    Returns:
        Nenhum valor retornado (None).
    """

    limpar()
    print("\n\t-- LISTAGEM DOS CANDIDATOS --\n")

    permicao = verificacao_existencia(1)

    if permicao == True:
        bd.cursor.execute("SELECT id_candidato, nome, partido, num_votacao FROM candidatos ORDER BY nome")
        resultado=bd.cursor.fetchall()

        for candidato in resultado:
            if candidato[1] != 'Voto Nulo':
                print(f"Nome: {candidato [1]}   Partido: {candidato[2]}   Nº: {candidato[3]}")

    else:
        print("*ERRO: Não há candidatos registrados.")
    
    input("\nAperte ENTER para retornar...")
    limpar()
    return

def buscar_candidato(): # FUNÇÃO PARA BUSCAR UM CANDIDATO PELO SEU NÚMERO DE VOTAÇÃO
    
    """
    Busca por número de votação o candidato presentes na base de dados.

    Args:
        Não recebe parâmetros.

    Returns:
        Nenhum valor retornado (None).
    """

    limpar()
    print("\n\t-- BUSCA DE CANDIDATOS --")

    permicao = verificacao_existencia(1)

    if permicao == True:
        numero=int(input("\nDigite o número da votação: "))

        bd.cursor.execute(f"SELECT nome, partido FROM candidatos WHERE num_votacao = {numero}")

        resultado=bd.cursor.fetchall()

        limpar()
        print("\n\t-- BUSCA DE CANDIDATOS --\n")

        if resultado: # CASO EXISTA CANDIDATO COM TAL NÚMERO, ELE É MOSTRADO
            for nome, partido in resultado:
                print(f"Nome: {nome}\tPartido: {partido}")
                
        else: # CASO NÃO APARECE UMA MENSAGEM DIZENDO QUE NÃO HÁ
            print("*ERRO: Candidato não encontrado.")

        input("\nAperte ENTER para retornar...")
        limpar()
        return
    
    else:
        input("\n*ERRO: Não há candidatos registrados.\n\nAperte ENTER para retornar...")
        limpar()
        return

def remocao_candidato(): # FUNÇÃO PARA REMOVER UM CANDIDATO DO BANCO DE DADOS
    
    """
    Remove o cadastro de um candidato do banco de dados.

    Args:
        Não recebe parâmetros.

    Returns:
        Nenhum valor retornado (None).
    """

    limpar()
    print("\n\t-- REMOÇÃO DE CANDIDATOS --")

    permicao = verificacao_existencia(1)

    if permicao == True:
        num_candidato = input("\nDigite o número do candidato que deseja deletar: ")

        bd.cursor.execute(f"SELECT nome FROM candidatos WHERE num_votacao = {num_candidato}") # VERIFICA SE O CANDIDATO EXISTE
        resultado = bd.cursor.fetchone()

        if resultado: # CASO EXISTA, ELE PEDE UMA CONFIRMAÇÃO DE EXCLUSÃO
            for nome in resultado:
                confirmacao = input(f"Tem certeza que deseja deletar {nome}, nº {num_candidato}? (s/n): ")
                confirmacao = confirmacao.lower()

                while confirmacao != "s" and confirmacao != "n":
                    limpar()
                    print("\n\t-- REMOÇÃO DE CANDIDATOS --\n\n*ERRO: Digite 's' para sim e 'n' para não, tente novamente.")
                    confirmacao = input(f"Tem certeza que deseja deletar o {nome}, nº {num_candidato}? (s/n): ")

                if confirmacao == "s": # CASO SIM, ELE REMOVE E UM AVISO DE EXCLUSÃO É MOSTRADO
                    limpar()
                    print("\n\t-- REMOÇÃO DE CANDIDATOS --")
                    input("\n*SUCESSO: Candidato removido com sucesso!\n\nAperte ENTER para retornar...")
                    bd.cursor.execute(f"DELETE FROM candidatos WHERE num_votacao = {num_candidato}")
                    bd.conexao.commit()
                    limpar()
                    return

                if confirmacao == "n": # CASO NÃO, ELE CANCELA A OPERAÇÃO E VOLTA AO MENU
                    limpar()
                    print("\n\t-- REMOÇÃO DE CANDIDATOS --")
                    input("\nOperação cancelada!\n\nAperte ENTER para retornar...")
                    limpar()
                    return
                
        else: # SE O CANDIDATO NÃO EXISTIR, ELE MOSTRA O ERRO E VOLTA PARA O MENU
            limpar()
            print("\n\t-- REMOÇÃO DE CANDIDATOS --")
            input("\n*ERRO: Candidato não foi encontrado.\n\nAperte ENTER para retornar...")
            limpar()
            return
        
    else:
        input("\n*ERRO: Não há candidatos registrados.\n\nAperte ENTER para retornar...")
        limpar()
        return
    
def verificacao_existencia(opcao): # VERIFICA SE HÁ ELEITORES (opcao = 0) OU CANDIDATOS (opcao = 1) REGISTRADOS NO BANCO DE DADOS
    
    """
    Testa se determinada tabela no banco de dados possui registros.

    Args:
        opcao (int): Especifica a tabela (0 para 'eleitores', 1 para 'candidatos').

    Returns:
        bool: Retorna True se a tabela possuir pelo menos um registro, False se vazia.
    """

    if opcao == 0:
        nome = 'eleitores'
    else:
        nome = 'candidatos'
    
    bd.cursor.execute(f"SELECT nome FROM {nome}")
    resultado = bd.cursor.fetchall()

    if resultado:
        return True
    else:
        return False