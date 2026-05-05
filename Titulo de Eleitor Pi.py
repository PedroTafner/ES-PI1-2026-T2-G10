def titulo_eleitor(NUMTIT):
    if len(NUMTIT) != 12:
        print("Erro, Titulo tem que ter 12 Numeros")
        return False
        
    DVT=0
    digitoT=0
    stringNUMTIT=str(NUMTIT)
    for multiplicador in range(2,10):
        DVT+=int(stringNUMTIT[digitoT])*multiplicador
        digitoT+=1
    DVTint=int(DVT/11) 
    DVTresto=DVT-DVTint*11  

    #DVT 2
    DVT=0
    digitoT=8
    for multiplicador in range(7,10):
        DVT+=int(stringNUMTIT[digitoT])*multiplicador
        digitoT+=1
    DVTint=int(DVT/11) 
    DVTresto2=DVT-DVTint*11 