import bancoDeDados as bd

def validacaoCPF(cpf): #VERIFICA SE O CPF INSERIDO CORRESPONDE AOS REQUISITOS DE VALIDAÇÃO
    stringCPF=str(cpf)
    if len(stringCPF) != 11 or stringCPF == stringCPF[0] * 11:
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

def validacaoTituloEleitor(NUMTIT): #VERIFICA SE O TÍTULO DE ELEITOR INSERIDO CORRESPONDE AOS REQUISITOS DE VALIDAÇÃO
    stringTitEleitor=str(NUMTIT)
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

def validarChaveAcesso(chave): #VERIFICA SE A CHAVE DE ACESSO INSERIDA EXISTE

    if len(chave) != 7:
        return False
    bd.cursor.execute(f"SELECT id_eleitor FROM eleitores WHERE chave_acesso = '{chave}'")
    resultado = bd.cursor.fetchone()

    if resultado:
        return True
    else:
        return False