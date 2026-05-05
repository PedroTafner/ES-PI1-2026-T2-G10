DVTresto3=str(DVTresto)
    if DVTresto >= 10:
        DVTresto4=str(DVTresto)
        DVTresto3=DVTresto4[1]

    if DVTresto3 != stringNUMTIT[10]:
        print("titulo errado")
        return False
        DVTresto3=str(DVTresto)

    DVTresto6=str(DVTresto2)
    if DVTresto2 >= 10:
        DVTresto5=str(DVTresto2)
        DVTresto6=DVTresto5[1]
        
    if str(DVTresto6) != stringNUMTIT[11]:
        print("titulo errado 2")
        return False
    print("Titulo valido")
    
num=(input("Digite Seu Titulo:"))
aprovacao=titulo_eleitor(num)
