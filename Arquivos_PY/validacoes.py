import Arquivos_PY.bancoDeDados as bd
import Arquivos_PY.gerenciamento as ger
import Arquivos_PY.votacao as vot
import Arquivos_PY.criptografia as c
import Arquivos_PY.descriptografia as d


def validacaoCPF(cpf): # VERIFICA SE O CPF INSERIDO CORRESPONDE AOS REQUISITOS DE VALIDAÇÃO
    stringCPF=str(cpf)

    if len(stringCPF) != 11 or stringCPF == stringCPF[0] * 11: # SE O CPF NÃO POSSUIR 11 DIGITOS OU SER REPETIDO, É REPROVADO
        return False
    
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

def validacaoTituloEleitor(titulo): # VERIFICA SE O TÍTULO DE ELEITOR INSERIDO CORRESPONDE AOS REQUISITOS DE VALIDAÇÃO
    stringTitEleitor=str(titulo)

    if len(stringTitEleitor) != 12:
        return False
    
    #DVT 1    
    DVT=0
    digitoT=0

    for multiplicador in range(2,10):
        DVT+=int(stringTitEleitor[digitoT])*multiplicador
        digitoT+=1

    DVT%=11

    if DVT == 10:
        DVT=0
        if stringTitEleitor[8] == '0' and stringTitEleitor[9] == '1' or '2':
            DVT=1

    if int(stringTitEleitor[10]) != DVT:
        return False 

    #DVT 2
    DVT=0
    digitoT=8

    for multiplicador in range(7,10):
        DVT+=int(stringTitEleitor[digitoT])*multiplicador
        digitoT+=1

    DVT%=11

    if DVT == 10:
        DVT=0
        if stringTitEleitor[8] == '0' and stringTitEleitor[9] == '1' or '2':
            DVT=1

    if int(stringTitEleitor[11]) != DVT:
        return False 
    
    return True

def validarChaveAcesso(chave): # VERIFICA SE A CHAVE DE ACESSO INSERIDA EXISTE
    if len(chave) != 7:
        return False
    
    chave = c.criptografia(1,chave)
    bd.cursor.execute(f"SELECT id_eleitor FROM eleitores WHERE chave_acesso = '{chave}'")
    resultado = bd.cursor.fetchone()

    if resultado:
        return True
    else:
        return False
    
def validarEleitor(texto, funcao): # VALIDA SE AS INFORMAÇÕES DO ELEITOR ESTÃO CORRETAS DIANTE DO BANCO DE DADOS
    print(f"\n\t-- {texto} --")

    # 1. VALIDAÇÃO DO TÍTULO DE ELEITOR
    titulo=int(input("\nDigite seu título de eleitor: "))
    validacao=validacaoTituloEleitor(titulo)
    while validacao != True:
        ger.limpar()
        print(f"\n\t-- {texto} --\n\n*ERRO: Título de eleitor inválido, digite novamente.")
        titulo=int(input("\nDigite seu título de eleitor: "))
        validacao= validacaoTituloEleitor(titulo)

    # 2. VALIDAÇÃO DO CPF
    ger.limpar()
    bd.cursor.execute("SELECT cpf FROM eleitores WHERE titulo_eleitor = %s", (titulo,))
    resultado = bd.cursor.fetchone()
    validacao = str(resultado[0])

    validacao = d.descriptografia(0,validacao)
    cpf_4digitos = validacao[:4]

    print(f"\n\t-- {texto} --")
    cpf=int(input("\nDigite os 4 primeiros dígitos do seu CPF: "))
    while len(str(cpf)) != 4 or str(cpf) != cpf_4digitos:
        ger.limpar()
        print(f"\n\t-- {texto} --\n\n*ERRO: Digite os 4 primeiros caracteres do seu CPF, tente novamente.")
        cpf=int(input("\nDigite os 4 primeiros dígitos do seu CPF: "))
    
    cpf = c.criptografia(0,validacao)

    #3. VALIDAÇÃO DA CHAVE DE ACESSO
    ger.limpar()
    bd.cursor.execute(f"SELECT chave_acesso FROM eleitores WHERE cpf LIKE '{cpf}%'")
    resultado=bd.cursor.fetchone()
    validacao = str(resultado[0])

    validacao = d.descriptografia(1,validacao)

    print(f"\n\t-- {texto} --")
    chave=input("\nDigite a sua chave de acesso: ")
    while len(str(chave)) != 7 or str(chave) != validacao:
        ger.limpar()
        print(f"\n\t-- {texto} --\n\n*ERRO: A chave de acesso é inválida, tente novamente.")
        chave=input("\nDigite a sua chave de acesso: ")

    #
    bd.cursor.execute(f"SELECT cpf,mesario,status_voto FROM eleitores WHERE cpf LIKE '{cpf}%'")
    resultado=bd.cursor.fetchall()
    
    for cpfValido,mesario, status_voto in resultado:

        # TEMOS 2 TIPOS DE FUNÇÕES: 1. ABRIR E FECHAR O SISTEMA DE VOTAÇÃO; 2. VERIFICAÇÃO DA REALIZAÇÃO DO VOTO E, CASO NÃO, O SEU REGISTRO

        if funcao == 0:
            if mesario == 0:
                ger.limpar()
                print(f"\n\t-- {texto} --")
                input("\n*ERRO: Somente mesários podem abrir/encerrar o sistema de votação.\n\nAperte ENTER para continuar...")
                vot.arquivoTXT(0,'ALERTA: Tentativa de acesso negado.')
                return False
        
            else:
                return True
        
        if funcao == 1: 
            if status_voto == 1:
                ger.limpar()
                print(f"\n\t-- {texto} --")
                input("\n*ERRO: Você já realizou seu voto.\n\nAperte ENTER para voltar...")
                vot.arquivoTXT(0,'ALERTA: Tentativa de voto duplo.')
                ger.limpar()
                return
            
            else:
                voto_realizado = False
                while voto_realizado == False:
                    ger.limpar()
                    print(f"\n\t-- {texto} --")
                    voto = int(input("\nDigite para quem você vota: "))
                    bd.cursor.execute(f'SELECT nome, partido FROM candidatos WHERE num_votacao = {voto}')
                    resultado = bd.cursor.fetchall()
                    ger.limpar()
                    if resultado:
                        print(f"\n\t-- {texto} --")
                        for (nome, partido) in resultado:
                            print(f"\n Candidato: {nome} | Partido: {partido}")
                            confirmacao=input("\nVocê tem certeza do seu voto? (s/n): ")
                            confirmacao = confirmacao.lower()
                            while confirmacao != "s" and confirmacao != "n":
                                ger.limpar()
                                print(f"\n\t-- {texto} --\n\n*ERRO: Digite 's' para sim e 'n' para não, tente novamente.")
                                print(f"\nCandidato: {nome} | Partido: {partido}")
                                confirmacao=input("\nVocê tem certeza do seu voto? (s/n): ")
                                confirmacao = confirmacao.lower()
                            if confirmacao == 'n':
                                continue
                            else:
                                bd.votoRealizado(voto,cpfValido,texto)
                                voto_realizado=True
                    else:
                        ger.limpar()
                        print(f"\n\t-- {texto} --")
                        print("\n*ERRO: O número de partido inserido é inexistente.")
                        voto_nulo = input("\nDeseja que seu voto seja nulo?(s/n): ")
                        while voto_nulo != "s" and voto_nulo != "n":
                            ger.limpar()
                            print(f"\n\t-- {texto} --\n\n*ERRO: Digite 's' para sim e 'n' para não, tente novamente.")
                            print("\n*ERRO: O número de partido inserido é inexistente.")
                            voto_nulo = input("Deseja que seu voto seja nulo?(s/n): ")
                        if voto_nulo == "s":
                            bd.votoNulo(cpfValido,texto)
                            voto_realizado=True
                        else:
                            continue
                return